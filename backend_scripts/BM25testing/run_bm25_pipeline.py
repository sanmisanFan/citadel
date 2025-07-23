#!/usr/bin/env python
"""
BM25  ➜  Cosine  ➜  Cross‑Encoder  pipeline
-------------------------------------------
Per passage we keep *only raw scores*:

    • bm25        – lexical overlap
    • ce_score    – cross‑encoder logit (if model provided)
    • cos_score   – cosine similarity (if model provided)
    • rank        – position after sorting by ce_score (or fallback)

No min‑max scaling, no blended score.
"""

import argparse, json, re, sys
from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Any

from tqdm import tqdm
from rank_bm25 import BM25Okapi
import pymupdf4llm

# ─── sentence‑transformers ───────────────────────────────────────────
try:
    from sentence_transformers import CrossEncoder, SentenceTransformer, util
except ImportError:
    print("❌  pip install sentence-transformers", file=sys.stderr)
    sys.exit(1)

# ─── Regex helpers ───────────────────────────────────────────────────
BLANK_RE      = re.compile(r"\n\s*\n")
WHITESPACE_RE = re.compile(r"\s+")
MD_CLEAN_RE   = re.compile(r"^(\s{0,3}[-*+] |\s{0,3}\d+\.\s|#+\s)")

# ─── PDF → paragraphs ────────────────────────────────────────────────
def pdf_to_markdown(pdf_path: Path) -> str:
    return pymupdf4llm.to_markdown(str(pdf_path))

def markdown_to_paragraphs(md: str, min_len: int = 40, max_len: int = 1200) -> List[str]:
    paras: List[str] = []
    for raw in BLANK_RE.split(md):
        lines = [MD_CLEAN_RE.sub("", ln).strip() for ln in raw.splitlines()]
        joined = WHITESPACE_RE.sub(" ", " ".join([l for l in lines if l]))
        if min_len <= len(joined) <= max_len:
            paras.append(joined)
    return paras

# ─── BM25 helpers ────────────────────────────────────────────────────
def build_bm25(paragraphs: List[str]) -> BM25Okapi:
    return BM25Okapi([p.split() for p in paragraphs])

def top_k_bm25(bm25, paragraphs, query: str, k: int) -> List[Dict[str, Any]]:
    scores = bm25.get_scores(query.split())
    order  = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
    return [{
        "bm25_rank": r + 1,
        "paragraph_index": i,
        "paragraph": paragraphs[i],
        "bm25": float(scores[i])
    } for r, i in enumerate(order)]

# ─── Add neural scores ───────────────────────────────────────────────
def add_cross_encoder_scores(model: CrossEncoder, context: str, cand_list):
    pairs = [(context, c["paragraph"]) for c in cand_list]
    ce = model.predict(pairs, show_progress_bar=False)
    for c, s in zip(cand_list, ce):
        c["ce_score"] = float(s)

def add_cosine_scores(model: SentenceTransformer, context: str, cand_list):
    emb_q = model.encode(context, convert_to_tensor=True, show_progress_bar=False)
    emb_p = model.encode([c["paragraph"] for c in cand_list],
                         convert_to_tensor=True, show_progress_bar=False)
    cos = util.cos_sim(emb_q, emb_p)[0].tolist()
    for c, s in zip(cand_list, cos):
        c["cos_score"] = float(s)

# ─── Main pipeline ───────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--enriched", required=True)
    ap.add_argument("--pdf_dir", required=True)
    ap.add_argument("--out_dir", default="outputs")
    ap.add_argument("--k", type=int, default=10)
    ap.add_argument("--rerank_model", default="cross-encoder/ms-marco-MiniLM-L-6-v2")
    ap.add_argument("--cosine_model", default="all-MiniLM-L6-v2")
    args = ap.parse_args()

    pdf_dir = Path(args.pdf_dir)
    out_dir = Path(args.out_dir); out_dir.mkdir(parents=True, exist_ok=True)

    ce_model  = CrossEncoder(args.rerank_model)        if args.rerank_model else None
    cos_model = SentenceTransformer(args.cosine_model) if args.cosine_model else None

    # Load enriched JSON → map ref_id to citation contexts
    enriched = json.loads(Path(args.enriched).read_text(encoding="utf-8"))
    contexts_by_ref = defaultdict(list)
    for paper in enriched:
        rid = paper.get("ref_id"); mentions = paper.get("reference_mentions") or []
        if rid is None: continue
        contexts_by_ref[rid].extend(m["text"] if isinstance(m, dict) else m for m in mentions)

    for ref_id, ctxs in tqdm(contexts_by_ref.items(), desc="processing refs"):
        pdf_path = pdf_dir / f"{ref_id}.pdf"
        if not pdf_path.exists():
            continue

        md = pdf_to_markdown(pdf_path)
        Path(out_dir, f"reference_{ref_id}.md").write_text(md, encoding="utf-8")

        paras = markdown_to_paragraphs(md)
        if not paras:
            continue
        bm25 = build_bm25(paras)

        results = []
        for ctx in ctxs:
            cands = top_k_bm25(bm25, paras, ctx, args.k)

            if ce_model:
                add_cross_encoder_scores(ce_model, ctx, cands)
            if cos_model:
                add_cosine_scores(cos_model, ctx, cands)

            # choose sort key: CE > cosine > bm25
            if ce_model:
                cands.sort(key=lambda d: d.get("ce_score", 0.0), reverse=True)
            elif cos_model:
                cands.sort(key=lambda d: d.get("cos_score", 0.0), reverse=True)
            else:
                cands.sort(key=lambda d: d["bm25"], reverse=True)

            for r, c in enumerate(cands, 1):
                c["rank"] = r

            results.append({"citation_context": ctx, "top_k": cands})

        out_json = out_dir / f"results_ref_{ref_id}.json"
        out_json.write_text(
            json.dumps({
                "ref_id": ref_id,
                "cross_encoder": args.rerank_model if ce_model else None,
                "cosine_model": args.cosine_model  if cos_model else None,
                "results": results
            }, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

    print("done.")

if __name__ == "__main__":
    main()
