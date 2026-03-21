# flor_paper_processor.py  ──  Flor-in / Flor-out
import os, json, requests
from time import sleep

# TODO: make agnostic to LLM chosen
from openai import OpenAI


class PaperProcessor:
    # ─────────────────────────── Init ───────────────────────────
    def __init__(self):
        self.s2_base = "https://api.semanticscholar.org/graph/v1"
        self.max_retries = 3
        self.request_delay = 1
        self.gpt_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.s2_api_key = os.getenv("S2_API_KEY")

        # counters / maps that must persist across refs
        self.author_map, self.author_counter = {}, 1
        self.venue_map, self.venue_counter = {}, 1
        self.citation_counter = 1

        self.fake_author_mapping = {
            "H. Solo": "Han Solo",
            "L. Skywalker": "Luke Skywalker",
            "O.-W. Kenobi": "Obi-Wan Kenobi",
            "D. Smeesters": "Dirk Smeesters",
            "J. Liu": "Jia Liu",
            "J. Hutt": "Jabba Hutt",
            "L. Organa": "Leia Organa",
            "Q.-G. Jinn": "Qui-Gon Jinn",
            "A. Skywalker": "Anakin Skywalker",
            "M. Windu": "Mace Windu",
            "Chewbacca": "Chewbacca",
            "D. Vader": "Darth Vader",
        }

    # ───────────────── Flor INPUT ─────────────────
    def load_refs_from_flor(self):
        df_ref = flor.dataframe("reference")  # bibliography strings
        df_txt = flor.dataframe("reftext")  # body-text mentions

        # *** no suffixes argument because columns don’t collide ***
        merged = df_ref.merge(df_txt, on="refid")

        ref_string_by_id, mentions_by_id = {}, {}
        for refid, grp in merged.groupby("refid"):
            ref_string_by_id[refid] = grp["reference"].iloc[0]
            mentions_by_id[refid] = grp["reftext"].tolist()
        return ref_string_by_id, mentions_by_id

    # ───────────────── GPT parse ─────────────────
    def parse_reference(self, ref_text):
        prompt = f"""
Parse this reference into JSON with keys:
authors (array), title, venue, raw_venue, year, pages, arxiv_id, doi.
Reference: "{ref_text}"
Return JSON only.
"""
        try:
            out = (
                self.gpt_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type": "json_object"},
                    temperature=0.1,
                )
                .choices[0]
                .message.content
            )
            data = json.loads(out)
            if "authors" in data:
                data["authors"] = [
                    self.fake_author_mapping.get(a, a)
                    for a in data["authors"]
                    if "et al" not in a.lower()
                ]
            return data
        except Exception as e:
            print("GPT error:", e)
            return None

    # ────────── Retry helper ──────────
    def retry(self, fn, *a):
        for _ in range(self.max_retries):
            r = fn(*a)
            if r:
                return r
            sleep(self.request_delay)
        return None

    # ────────── External API helpers (Semantic Scholar / OpenAlex) ──────────
    def search_paper(self, title):
        try:
            r = requests.get(
                f"{self.s2_base}/paper/search",
                params={"query": title, "fields": "paperId", "limit": 1},
                headers={"x-api-key": self.s2_api_key},
                timeout=15,
            )
            r.raise_for_status()
            d = r.json()
            return d["data"][0]["paperId"] if d.get("data") else None
        except Exception:
            return None

    def get_s2(self, pid):
        fields = (
            "title,authors.name,authors.authorId,authors.externalIds,"
            "venueimport fitz  # PyMuPDF,year,citationCount,fieldsOfStudy,externalIds,paperId"
        )
        try:
            r = requests.get(
                f"{self.s2_base}/paper/{pid}",
                params={"fields": fields},
                headers={"x-api-key": self.s2_api_key},
                timeout=15,
            )
            r.raise_for_status()
            return r.json()
        except Exception:
            return None

    def get_oa(self, title):
        try:
            r = requests.get(
                "https://api.openalex.org/works",
                params={"filter": f"title.search:{title}", "per-page": 1},
                timeout=15,
            )
            r.raise_for_status()
            d = r.json()
            return d["results"][0] if d.get("results") else None
        except Exception:
            return None

    # ────────── Author merge (re-uses keys) ──────────
    def merge_authors(self, parsed, s2_list, oa_list=None):
        maxlen, out = max(len(parsed), len(s2_list)), []
        for i in range(maxlen):
            raw = parsed[i] if i < len(parsed) else None
            api = s2_list[i] if i < len(s2_list) else {}
            if not api and oa_list and i < len(oa_list):
                api = oa_list[i]

            name = api.get("name")
            s2_id = api.get("authorId")
            orcid = (api.get("externalIds") or {}).get("ORCID")
            if not orcid and oa_list and i < len(oa_list):
                orcid = oa_list[i].get("orcid")

            canon = self.fake_author_mapping.get(raw) if raw and not name else name
            cand = {
                "name": canon or raw,
                "s2_id": s2_id,
                "orcid": orcid,
                "raw_name": raw,
            }

            key = None
            for t, ident in [
                ("orcid", orcid),
                ("s2_id", s2_id),
                ("raw_name", raw),
                ("name", cand["name"]),
            ]:
                if ident and (t, ident) in self.author_map:
                    key = self.author_map[(t, ident)]["key"]
                    break
            if not key:
                key = f"author-{self.author_counter}"
                self.author_counter += 1
                for t, ident in [
                    ("orcid", orcid),
                    ("s2_id", s2_id),
                    ("raw_name", raw),
                    ("name", cand["name"]),
                ]:
                    if ident:
                        self.author_map[(t, ident)] = {"author": cand, "key": key}
            out.append(key)
        return out

    # ────────── Merge helpers ──────────
    def merge_s2(self, gpt, s2, oa_auth=None):
        return {
            "title": s2.get("title", gpt.get("title")),
            "authors": self.merge_authors(
                gpt.get("authors", []), s2.get("authors", []), oa_auth
            ),
            "year": s2.get("year", gpt.get("year")),
            "venue": gpt.get("venue") or s2.get("venue"),
            "raw_venue": gpt.get("raw_venue") or s2.get("venue"),
            "citation_count": s2.get("citationCount", 0),
            "fields_of_study": s2.get("fieldsOfStudy", []),
            "external_ids": s2.get("externalIds", {}),
            "semantic_scholar_id": s2.get("paperId"),
            "arxiv_id": gpt.get("arxiv_id"),
            "doi": s2.get("externalIds", {}).get("DOI", gpt.get("doi")),
            "ref_id": gpt.get("ref_id"),
        }

    def merge_oa(self, gpt, oa):
        oa_auth = [
            {"name": a["author"]["display_name"], "orcid": a["author"]["orcid"]}
            for a in oa.get("authorships", [])
        ]
        return {
            "title": oa.get("display_name", gpt.get("title")),
            "authors": self.merge_authors(gpt.get("authors", []), [], oa_auth),
            "year": oa.get("publication_year", gpt.get("year")),
            "venue": gpt.get("venue") or oa.get("host_venue", {}).get("display_name"),
            "raw_venue": gpt.get("raw_venue")
            or oa.get("host_venue", {}).get("display_name"),
            "citation_count": oa.get("citation_count", 0),
            "fields_of_study": oa.get("concepts", []),
            "external_ids": {"OpenAlex": oa.get("id")},
            "semantic_scholar_id": None,
            "arxiv_id": gpt.get("arxiv_id"),
            "doi": oa.get("doi", gpt.get("doi")),
            "ref_id": gpt.get("ref_id"),
        }

    def gpt_only(self, gpt):
        return {
            "title": gpt.get("title"),
            "authors": self.merge_authors(gpt.get("authors", []), []),
            "year": gpt.get("year"),
            "venue": gpt.get("venue"),
            "raw_venue": gpt.get("raw_venue"),
            "citation_count": 0,
            "fields_of_study": [],
            "external_ids": {},
            "semantic_scholar_id": None,
            "arxiv_id": gpt.get("arxiv_id"),
            "doi": gpt.get("doi"),
            "ref_id": gpt.get("ref_id"),
        }

    # ────────── Add venue / citation keys ──────────
    def add_entity_keys(self, paper):
        paper["citation_key"] = f"citation-{self.citation_counter}"
        self.citation_counter += 1
        v = paper.get("venue")
        if v:
            v_str = v if isinstance(v, str) else str(v)
            if v_str not in self.venue_map:
                self.venue_map[v_str] = f"venue-{self.venue_counter}"
                self.venue_counter += 1
            paper["venue"] = self.venue_map[v_str]
        return paper

    # ────────── MAIN loop ──────────
    def run(self, reference_mentions, raw_references):
        ref_string_by_id, mention_by_id = self.load_refs_from_flor()

        for refid in sorted(ref_string_by_id.keys()):
            gpt = self.parse_reference(ref_string_by_id[refid])
            if not gpt:
                continue
            gpt["ref_id"] = refid

            pid = self.search_paper(gpt.get("title")) if gpt.get("title") else None
            s2 = self.retry(self.get_s2, pid) if pid else None
            need_oa = (
                not s2
                or any(
                    not (a.get("externalIds") or {}).get("ORCID")
                    for a in s2.get("authors", [])
                )
                if s2
                else True
            )
            oa = self.get_oa(gpt["title"]) if need_oa and gpt.get("title") else None

            if s2:
                oa_auth = (
                    [
                        {
                            "name": au["author"]["display_name"],
                            "orcid": au["author"]["orcid"],
                        }
                        for au in oa.get("authorships", [])
                    ]
                    if oa
                    else None
                )
                paper = self.merge_s2(gpt, s2, oa_auth)
            elif oa:
                paper = self.merge_oa(gpt, oa)
            else:
                paper = self.gpt_only(gpt)

            paper["reference_mentions"] = mention_by_id.get(refid, [])
            paper = self.add_entity_keys(paper)

            # ── log out to Flor ──
            flor.log("enriched_citation", paper)
            for (_, _), val in self.author_map.items():
                flor.log("author_entity", {"key": val["key"], **val["author"]})
            for v_str, vk in self.venue_map.items():
                flor.log("venue_entity", {"key": vk, "name": v_str})

            sleep(self.request_delay)
