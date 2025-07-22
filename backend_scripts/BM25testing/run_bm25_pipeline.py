#!/usr/bin/env python
"""
BM25 + Cross‑Encoder + Cosine (bi‑encoder) pipeline.
"""

import argparse, json, re, sys
from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Any

from tqdm import tqdm
from rank_bm25 import BM25Okapi
import pymupdf4llm

# ─── sentence-transformers imports ───────────────────────────────────
try:
    from sentence_transformers import CrossEncoder, SentenceTransformer, util
except ImportError:
    print("❌  pip install sentence-transformers", file=sys.stderr)
    sys.exit(1)

# ─── Regex helpers ───────────────────────────────────────────────────
BLANK_RE = re.compile(r"\n\s*\n")
WHITESPACE_RE = re.compile(r"\s+")
MD_CLEAN_RE = re.compile(r"^(\s{0,3}[-*+] |\s{0,3}\d+\.\s|#+\s)")

# ─── Extraction helpers ──────────────────────────────────────────────
def pdf_to_markdown(pdf_path: Path) -> str:
    return pymupdf4llm.to_markdown(str(pdf_path))

def markdown_to_paragraphs(md: str, min_len=40, max_len=1200) -> List[str]:
    paras = []
    for raw in BLANK_RE.split(md):
        lines = [MD_CLEAN_RE.sub("", ln).strip() for ln in raw.splitlines()]
        joined = WHITESPACE_RE.sub(" ", " ".join([l for l in lines if l]))
        if min_len <= len(joined) <= max_len:
            paras.append(joined)
    return paras

# ─── BM25 helpers ────────────────────────────────────────────────────
def build_bm25(paragraphs: List[str]) -> BM25Okapi:
    return BM25Okapi([p.split() for p in paragraphs])

def top_k_bm25(bm25, paragraphs, query, k):
    scores = bm25.get_scores(query.split())
    order = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
    return [{
        "bm25_rank": r + 1,
        "paragraph_index": i,
        "paragraph": paragraphs[i],
        "bm25": float(scores[i])
    } for r, i in enumerate(order)]

# ─── Scoring functions ───────────────────────────────────────────────
def add_cross_encoder_scores(model, context, cand_list):
    pairs = [(context, c["paragraph"]) for c in cand_list]
    ce = model.predict(pairs)
    for c, s in zip(cand_list, ce):
        c["ce_score"] = float(s)

def add_cosine_scores(model, context, cand_list):
    emb_q = model.encode(context, convert_to_tensor=True, show_progress_bar=False)
    emb_p = model.encode([c["paragraph"] for c in cand_list],
                         convert_to_tensor=True, show_progress_bar=False)
    cos = util.cos_sim(emb_q, emb_p)[0].tolist()  # list of floats
    for c, s in zip(cand_list, cos):
        c["cos_score"] = float(s)  # already in [-1,1]; often 0–1 for these models

def blend_scores(candidates, w_bm25, w_ce, w_cos):
    # normalise bm25 to 0‑1
    bm = [c["bm25"] for c in candidates]
    bmin, bmax = min(bm), max(bm)
    for c in candidates:
        bm_norm = 0.5 if bmax == bmin else (c["bm25"] - bmin) / (bmax - bmin)
        c["bm25_norm"] = bm_norm
        c["final_score"] = (w_bm25 * bm_norm +
                            w_ce    * c.get("ce_score", 0.0) +
                            w_cos   * c.get("cos_score", 0.0))
        c["final_score_0_10"] = round(c["final_score"] * 10, 2)
    candidates.sort(key=lambda d: d["final_score"], reverse=True)
    for r, c in enumerate(candidates, 1):
        c["final_rank"] = r
    return candidates

# ─── Main ────────────────────────────────────────────────────────────
def main():
    p = argparse.ArgumentParser()
    p.add_argument("--enriched", required=True)
    p.add_argument("--pdf_dir", required=True)
    p.add_argument("--out_dir", default="outputs")
    p.add_argument("--k", type=int, default=10)
    p.add_argument("--rerank_model", default="cross-encoder/ms-marco-MiniLM-L-6-v2")
    p.add_argument("--cosine_model", default="all-MiniLM-L6-v2")  # ### NEW ###
    p.add_argument("--w_bm25", type=float, default=0.5)
    p.add_argument("--w_ce",   type=float, default=0.4)
    p.add_argument("--w_cos",  type=float, default=0.1)           # ### NEW ###
    args = p.parse_args()

    pdf_dir, out_dir = Path(args.pdf_dir), Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    cross_encoder = CrossEncoder(args.rerank_model) if args.rerank_model else None
    bi_encoder    = SentenceTransformer(args.cosine_model) if args.cosine_model else None

    # load enriched
    data = json.loads(Path(args.enriched).read_text(encoding="utf-8"))
    contexts_by_ref = defaultdict(list)
    for ppr in data:
        rid = ppr.get("ref_id"); ment = ppr.get("reference_mentions") or []
        if rid is None: continue
        contexts_by_ref[rid].extend(m["text"] if isinstance(m, dict) else m for m in ment)

    for ref_id, ctxs in tqdm(contexts_by_ref.items(), desc="refs"):
        pdf = pdf_dir / f"{ref_id}.pdf"
        if not pdf.exists(): continue
        md = pdf_to_markdown(pdf)
        Path(out_dir, f"reference_{ref_id}.md").write_text(md, encoding="utf-8")
        paras = markdown_to_paragraphs(md)
        if not paras: continue
        bm25 = build_bm25(paras)

        results = []
        for ctx in ctxs:
            cands = top_k_bm25(bm25, paras, ctx, args.k)
            if cross_encoder:
                add_cross_encoder_scores(cross_encoder, ctx, cands)
            if bi_encoder:
                add_cosine_scores(bi_encoder, ctx, cands)          # ### NEW ###
            blended = blend_scores(cands, args.w_bm25, args.w_ce, args.w_cos)
            results.append({"citation_context": ctx, "top_k": blended})

        out_json = Path(out_dir, f"bm25_results_ref_{ref_id}.json")
        out_json.write_text(json.dumps({
            "ref_id": ref_id,
            "cross_encoder": args.rerank_model,
            "cosine_model": args.cosine_model,
            "results": results
        }, indent=2, ensure_ascii=False))
    print("done.")

if __name__ == "__main__":
    main()
