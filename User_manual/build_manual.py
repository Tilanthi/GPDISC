#!/usr/bin/env python3
"""Assemble GPDISC_User_Manual.md from the template + verbatim captures.

The four front-door failures (bare "I don't have enough knowledge" fallbacks
with no consultation content) are replaced in position by the four backup
captures. Answers longer than TRIM_LIMIT are cut at the last sentence or
line boundary BEFORE the limit and a line containing just " ..." is appended.
No other editing of any kind.
"""
import json
import re

HERE = "/Users/gjw255/astrodata/SWARM/GPDISC/User_manual"
TRIM_LIMIT = 1650

# Ordered slots: (label to use, swapped_in bool)
ORDER = [
    ("acs", False),
    ("sah", False),
    ("paediatric_meningitis", False),
    ("routine_self_care", False),
    ("drug_interaction", False),
    ("palliative_pain", False),
    ("stable_angina", False),
    ("burn", True),               # replaced pre_travel (fallback, non-consultation)
    ("fever_after_travel", False),
    ("dysphagia_2ww", False),
    ("rabies_pep", False),
    ("paracetamol_od", True),     # replaced hot_joint (fallback)
    ("reduced_movements", True),  # replaced inferior_stemi (fallback)
    ("first_seizure_dvla", False),
    ("multimorbidity", False),
    ("tiredness", False),
    ("postural_dizziness", True), # replaced non_mobile_bruise (fallback)
    ("bloodborne_pep", False),
    ("heart_failure", False),
    ("kawasaki", False),
]


def trim(answer: str):
    """Cut at the last sentence- or line-boundary before TRIM_LIMIT."""
    if len(answer) <= TRIM_LIMIT:
        return answer, False
    head = answer[:TRIM_LIMIT]
    candidates = []
    nl = head.rfind("\n")
    if nl != -1:
        candidates.append(nl)                 # keep everything before the newline
    m = None
    for m in re.finditer(r"\.(?=\s|$)", head):
        pass
    if m is not None:
        candidates.append(m.end())            # keep up to and including the full stop
    cut = max(candidates)
    return answer[:cut].rstrip() + "\n ...", True


def main():
    with open(f"{HERE}/outputs_manual.json") as fh:
        main_by_label = {r["label"]: r for r in json.load(fh)}
    with open(f"{HERE}/outputs_backups.json") as fh:
        backup_by_label = {r["label"]: r for r in json.load(fh)}

    blocks = []
    trimmed = 0
    swapped = 0
    total_chars = 0
    for n, (label, is_swap) in enumerate(ORDER, start=1):
        src = backup_by_label if is_swap else main_by_label
        rec = src[label]
        answer, was_trimmed = trim(rec["answer"])
        trimmed += int(was_trimmed)
        swapped += int(is_swap)
        total_chars += len(answer)
        blocks.append(f'**{n}. "{rec["query"]}"**\n\n```\n{answer}\n```\n')

    with open(f"{HERE}/manual_template.md") as fh:
        template = fh.read()
    assert "{{EXAMPLES}}" in template
    doc = template.replace("{{EXAMPLES}}", "\n".join(blocks))
    with open(f"{HERE}/GPDISC_User_Manual.md", "w") as fh:
        fh.write(doc)

    print(f"examples: {len(ORDER)}  trimmed: {trimmed}  swapped: {swapped}")
    print(f"total answer characters in document: {total_chars}")


if __name__ == "__main__":
    main()
