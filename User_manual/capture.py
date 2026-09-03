#!/usr/bin/env python3
"""Capture real GPDISC consultation outputs for the user manuals.

Usage:  python3 capture.py queries.json outputs.json

queries.json:  [{"query": "...", "label": "..."}, ...]
outputs.json:  same records with "answer" = the system's answer, VERBATIM,
               except non-ASCII glyphs mapped to ASCII (repo PDF
               convention: no unicode replacement boxes in print).
               Wording is never edited here; trimming for the page budget
               happens at document-build time, never in this file.
"""
import json
import os
import sys

# Make gpdisc_core importable no matter where this is invoked from:
# repo root is the parent of this script's directory.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

_SANITIZE = {
    "→": "->", "⇒": "=>", "≥": ">=", "≤": "<=",
    "≠": "!=", "±": "+/-", "×": "x", "—": " - ",
    "–": "-", "’": "'", "‘": "'", "“": '"',
    "”": '"', "…": "...", "•": "*", "✓": "[ok]",
    "°C": " C", "µ": "u", "é": "e", "è": "e",
    "ê": "e", "à": "a", " ": " ",
}


def sanitize(text: str) -> str:
    for k, v in _SANITIZE.items():
        text = text.replace(k, v)
    return text


def main(in_path: str, out_path: str) -> None:
    from gpdisc_core import create_gpdisc_system
    system = create_gpdisc_system()
    with open(in_path) as fh:
        queries = json.load(fh)
    out = []
    for item in queries:
        q = item["query"]
        result = system.answer(q)
        answer = sanitize((result.get("answer") or "").strip())
        out.append({"query": q, "label": item.get("label", ""),
                    "answer": answer})
        print(f"captured [{len(answer):5d}] {q[:64]}")
    with open(out_path, "w") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=True)
    print(f"wrote {len(out)} outputs -> {out_path}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
