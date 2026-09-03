"""Adversarial Diagnostic Challenger — the MDT's designated dissenter.

Stage 4, Task 1. Deliberately over-inclusive: it attacks every leading
diagnosis with the questions a careful physician asks before committing —
especially "which dangerous mimic am I assuming away?". Attacks cite the
corpus's dangerous_mimic_of links so they stay evidence-anchored.
"""
from dataclasses import dataclass
from typing import List

from gpdisc_core.clinical_reasoning.knowledge import find_condition

ATTACK_TYPES = ("dangerous_mimic", "anchor_bias", "missing_discriminator",
                "prevalence_challenge")


@dataclass(frozen=True)
class Challenge:
    attack_type: str
    target_condition: str
    argument: str
    action: str


def challenge_differential(differential) -> List[Challenge]:
    """Attack a differential result: dangerous mimics first, then anchor
    bias, missing discriminators, and prevalence challenges.

    Never silent: any differential with a leader draws at least the
    missing-discriminator or prevalence question.
    """
    challenges: List[Challenge] = []
    if not differential.ranked:
        return challenges

    leader = differential.ranked[0]
    leader_profile = find_condition(leader.condition_id)
    ranked_ids = [d.condition_id for d in differential.ranked]

    # 1. Dangerous mimics of the leader that were NOT ranked or retained.
    mimic_challenges: List[Challenge] = []
    if leader_profile:
        for mimic_id in leader_profile.dangerous_mimic_of:
            if mimic_id in ranked_ids:
                continue
            if any(d.condition_id == mimic_id
                   for d in differential.retained_dangerous):
                continue
            mimic_profile = find_condition(mimic_id)
            mimic_name = mimic_profile.name if mimic_profile else mimic_id
            mimic_challenges.append(Challenge(
                attack_type="dangerous_mimic",
                target_condition=leader.condition_id,
                argument=(f"'{leader_profile.name}' is the leader, but its "
                          f"dangerous mimic '{mimic_name}' is neither ranked "
                          "nor on the retained-dangerous list."),
                action=(f"Ask explicitly what would distinguish {mimic_name} "
                        "and document why it is excluded."),
            ))
        if not mimic_challenges and differential.retained_dangerous:
            # Retention without exclusion is silent anchoring: the engine is
            # holding dangerous alternatives, but nobody has said why each
            # can be safely set aside.
            names = []
            for d in differential.retained_dangerous[:3]:
                prof = find_condition(d.condition_id)
                names.append(prof.name if prof else d.condition_id)
            challenges.append(Challenge(
                attack_type="dangerous_mimic",
                target_condition=leader.condition_id,
                argument=("The engine retains dangerous alternatives — "
                          + ", ".join(names)
                          + " — but none has a documented exclusion."),
                action=("For each retained danger, ask the one finding that "
                        "would confirm or exclude it, and record the "
                        "exclusion reason."),
            ))
    challenges.extend(mimic_challenges)

    # 2. Anchor bias: leader dominates but the runner-up is close.
    if len(differential.ranked) >= 2 and leader.score > 0:
        runner = differential.ranked[1]
        if runner.score / max(leader.score, 1e-9) > 0.6:
            second = find_condition(runner.condition_id)
            second_name = second.name if second else runner.condition_id
            challenges.append(Challenge(
                attack_type="anchor_bias",
                target_condition=leader.condition_id,
                argument=(f"The runner-up '{second_name}' scores "
                          f"{runner.score / leader.score:.0%} of the leader — "
                          "close enough that anchoring on the leader would be "
                          "premature."),
                action=("Name one feature that would move you off the leader; "
                        "if none exists, the two are not yet distinguished."),
            ))

    # 3. Missing discriminator: the leader has discriminating features
    #    nobody has elicited yet.
    if leader_profile and leader_profile.discriminators:
        challenges.append(Challenge(
            attack_type="missing_discriminator",
            target_condition=leader.condition_id,
            argument=(f"The leader '{leader_profile.name}' has discriminating "
                      "features that have not been elicited: "
                      + "; ".join(leader_profile.discriminators[:3]) + "."),
            action="Ask the discriminating questions before treating.",
        ))

    # 4. Prevalence challenge: a rare leader needs an explicit reason.
    if leader_profile and leader_profile.prevalence_per_consult < 0.005:
        challenges.append(Challenge(
            attack_type="prevalence_challenge",
            target_condition=leader.condition_id,
            argument=(f"'{leader_profile.name}' is rare in consultation "
                      f"(~{leader_profile.prevalence_per_consult:.1%}) — an "
                      "uncommon leader needs an explicit reason."),
            action=("Justify the leader with a specific finding, or re-rank "
                    "with the common conditions first."),
        ))

    return challenges
