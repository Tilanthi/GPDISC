#!/usr/bin/env python3
"""Verify the GPDISC manual PDFs are honest.

Chain asserted for every example block, in both documents:
  1. PREFIX: the fenced answer shown in the .md is a verbatim prefix
     (full answer, or cut at a line boundary with a trailing '...')
     of a REAL captured answer stored in the matching evidence_*.json
     (those files are written only from live create_gpdisc_system()
     runs - see capture.py and the regeneration step).
  2. PDF CONTAINMENT: the shown answer's letter/digit skeleton appears
     in the PDF's extracted-text skeleton. Skeleton comparison (all
     non-alphanumeric characters dropped on both sides) is immune to
     pdftotext quirks - fvextra wrap arrows, dehyphenation at wrapped
     hyphens, spacing - while still catching any rewording or
     fabrication, which cannot pass a letter-level containment check.
  3. LAYOUT: page count within cap; no glyph beyond the right page
     edge (pdftotext -bbox xMax vs page width).

Run from anywhere:  python3 verify_manuals.py [manual_dir]
Exit 0 = all pass.
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

DOCS = [
    {"md": "GPDISC_User_Manual.md", "pdf": "GPDISC_User_Manual.pdf",
     "evidence": "evidence_manual.json", "cap": 16},
    {"md": "GPDISC_How_To_Use.md", "pdf": "GPDISC_How_To_Use.pdf",
     "evidence": "evidence_howto.json", "cap": 15},
]

HEADER = re.compile(
    r"GPDISC.{0,3}General Practice Discovery and Intelligence System "
    r"for Consultation|^v1\.1\.0$|^\s*\d+\s*$")


def skeleton(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


def pdf_pages_and_overflow(pdf: str):
    info = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout
    pages = int(re.search(r"Pages:\s+(\d+)", info).group(1))
    width = float(re.search(r"Page size:\s+([\d.]+) x", info).group(1))
    bbox = subprocess.run(["pdftotext", "-bbox", pdf, "-"],
                          capture_output=True, text=True).stdout
    over = sum(1 for m in re.finditer(r'xMax="([\d.]+)"', bbox)
               if float(m.group(1)) > width + 1)
    return pages, over


def pdf_skeleton(pdf: str):
    """Skeletons under BOTH pdftotext reading modes. Layout mode and raw
    (content-stream) order transpose fragments differently at wrapped
    lines; the glyphs are identical, so containment in EITHER reading
    proves the text is present and correctly ordered."""
    skels = []
    for flags in ([], ["-raw"]):
        txt = subprocess.run(["pdftotext"] + flags + [pdf, "-"],
                             capture_output=True, text=True).stdout
        kept = [l for l in txt.split("\n") if not HEADER.match(l.strip())]
        skels.append(skeleton("\n".join(kept)))
    return skels


def main(root: str = HERE) -> int:
    os.chdir(root)
    all_ok = True
    for doc in DOCS:
        blocks = re.findall(r"\*\*(\d+)\.\s+(.+?)\*\*\s*\n+```text\n(.*?)\n```",
                            open(doc["md"]).read(), re.S)
        evidence = {e["label"]: e for e in json.load(open(doc["evidence"]))}
        pages, over = pdf_pages_and_overflow(doc["pdf"])
        skels = pdf_skeleton(doc["pdf"])
        fails = []
        for num, _q, body in blocks:
            shown = body.rstrip()
            trimmed = shown.endswith("...")
            shown = shown[:-3].rstrip() if trimmed else shown
            ev = evidence.get(f"ex{num}")
            if trimmed:
                prefix_ok = bool(ev) and ev["answer"].startswith(shown) \
                    and len(ev["answer"]) > len(shown) \
                    and ev["answer"][len(shown):].lstrip(" ").startswith("\n")
            else:
                prefix_ok = bool(ev) and ev["answer"] == shown
            pdf_ok = any(skeleton(shown) in sk for sk in skels)
            if not (prefix_ok and pdf_ok):
                fails.append((num, "prefix" if not prefix_ok else "pdf"))
        ok = not fails and not over and pages <= doc["cap"]
        all_ok &= ok
        print(f"{doc['pdf']}: pages={pages}/{doc['cap']} overflow={over} "
              f"blocks={len(blocks)} fails={len(fails)} {fails} "
              f"-> {'PASS' if ok else 'FAIL'}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else HERE))
