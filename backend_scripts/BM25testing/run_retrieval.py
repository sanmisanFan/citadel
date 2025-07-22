#!/usr/bin/env python
"""
run_retrieval_window.py
=======================
• Indexes every non‑empty paragraph in a paper TXT file.  
• Runs BM25 with no section weighting.  
• For each citation context, shows the top‑k hits **with ±window_size
  neighboring paragraphs**, giving you the local region.

Dependencies:  pip install rank_bm25
"""

import argparse, re, textwrap
from pathlib import Path
from rank_bm25 import BM25Okapi


# ---------- helpers ----------

MIN_LEN = 30          # skip very short lines (e.g., "Authors: Li et al.")
BLANK_RE = re.compile(r"\n\s*\n")

def load_paragraphs(path):
    """Return list[str]  (order preserved)."""
    txt = Path(path).read_text(encoding="utf-8")
    paras = [p.strip() for p in BLANK_RE.split(txt) if len(p.strip()) >= MIN_LEN]
    if not paras:
        raise ValueError(f"No usable paragraphs found in {path}")
    return paras

def build_bm25(paragraphs):
    corpus = [p.split() for p in paragraphs]
    return BM25Okapi(corpus)

def print_window(paragraphs, center_idx, score, window):
    lo = max(0, center_idx - window)
    hi = min(len(paragraphs), center_idx + window + 1)
    header = f"[idx {center_idx}]  BM25={score:.2f}"
    print(header)
    print("-" * len(header))
    for i in range(lo, hi):
        prefix = "➤ " if i == center_idx else "  "
        print(prefix + textwrap.fill(paragraphs[i], width=90))
        print()
    print()

# ---------- main ----------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--paper", default="paper_3_li_et_al.txt",
                    help="TXT file of the cited paper")
    ap.add_argument("--contexts", default="citations_contexts.txt",
                    help="File with one citation context per line")
    ap.add_argument("--k", type=int, default=2, help="how many hits to show")
    ap.add_argument("--window", type=int, default=1,
                    help="number of neighboring paragraphs to include on each side")
    args = ap.parse_args()

    paragraphs = load_paragraphs(args.paper)
    bm25 = build_bm25(paragraphs)

    query_lines = [q.strip() for q in Path(args.contexts)
                   .read_text(encoding="utf-8").splitlines()
                   if q.strip() and not q.startswith("#")]

    for q in query_lines:
        print("=" * 120)
        print("Citation context:", q)
        print("=" * 120)
        scores = bm25.get_scores(q.split())
        top_idx = sorted(range(len(scores)), key=lambda i: scores[i],
                         reverse=True)[: args.k]

        for idx in top_idx:
            print_window(paragraphs, idx, scores[idx], args.window)

if __name__ == "__main__":
    main()
