"""MDT debate protocol — pipeline, challenge, respond, synthesise.

Stage 4, Task 3. One deterministic pass: the consultation pipeline builds
the differential and safety position; the challenger attacks it; each role
responds; the chair synthesises. Disagreement is recorded, never smoothed
away — "the MDT was split" is clinical information.
"""
from dataclasses import dataclass, field
from types import SimpleNamespace
from typing import List, Optional

from gpdisc_core.clinical_reasoning.consultation import ConsultationPipeline
from gpdisc_core.mdt.challenger import Challenge, challenge_differential
from gpdisc_core.mdt.roles import MDT_ROLES, contribute


@dataclass
class MDTResult:
    presentation: str
    escalation: str = ""
    syndrome: str = ""
    differential_ids: List[str] = field(default_factory=list)
    challenges: List[Challenge] = field(default_factory=list)
    role_notes: dict = field(default_factory=dict)
    synthesis: str = ""
    disagreements: List[str] = field(default_factory=list)
    actions: List[str] = field(default_factory=list)


class _DifferentialView(SimpleNamespace):
    """Attribute-style view over the pipeline's dict-shaped differential."""

    def __init__(self, ranked: List[dict], retained: List[dict]):
        super().__init__(
            ranked=[SimpleNamespace(condition_id=d["condition_id"],
                                    score=d.get("score", 0.0))
                    for d in ranked],
            retained_dangerous=[SimpleNamespace(condition_id=d["condition_id"])
                                for d in retained],
        )


def run_mdt(presentation: str, context: Optional[dict] = None) -> MDTResult:
    """Run the full MDT debate on a presentation.

    Emergency → escalation first. Otherwise: differential → challenges →
    role notes → chair's synthesis, with uncertainty stated aloud and the
    challenger's case against the leader recorded as disagreement.
    """
    ctx = context or {}
    rec = ConsultationPipeline().run(presentation, ctx)

    result = MDTResult(
        presentation=presentation,
        escalation=rec.escalation,
        syndrome=rec.syndrome,
    )
    # On emergency the pipeline short-circuits ranking and files the matched
    # rule under dangerous_alternatives — that rule IS the working diagnosis.
    if rec.ranked_differential:
        result.differential_ids = [d["condition_id"]
                                   for d in rec.ranked_differential]
    elif rec.escalation == "emergency" and rec.dangerous_alternatives:
        result.differential_ids = [d["condition_id"]
                                   for d in rec.dangerous_alternatives]

    view = _DifferentialView(rec.ranked_differential,
                             rec.dangerous_alternatives or [])
    result.challenges = challenge_differential(view)

    for role in MDT_ROLES:
        # consultants draw on the differential's corpus profiles (9.1);
        # the core six have always computed from presentation + context
        notes = contribute(role.key, presentation, ctx, differential=view)
        if notes:
            result.role_notes[role.key] = notes

    # The chair's synthesis — uncertainty is stated, never hidden.
    leader = result.differential_ids[0] if result.differential_ids else ""
    if rec.ranked_differential:
        leader_name = rec.ranked_differential[0]["name"]
    elif rec.dangerous_alternatives:
        leader_name = rec.dangerous_alternatives[0]["name"]
    else:
        leader_name = "undetermined"
    if rec.escalation == "emergency":
        result.synthesis = (f"Emergency presentation: treat as {leader_name} "
                            "and escalate now.")
        result.actions.append("Escalate immediately (999/emergency pathway)")
    elif len(result.differential_ids) >= 3:
        runner_names = [d["name"] for d in rec.ranked_differential[1:3]]
        result.synthesis = (f"Working diagnosis: {leader_name}, actively held "
                            f"against {', '.join(runner_names)}. Not settled — "
                            + ("investigate to discriminate"
                               if rec.investigation_strategy
                               else "I don't know yet"))
    else:
        result.synthesis = (f"Working diagnosis: {leader_name}. "
                            "I don't know yet — the presentation does not fit "
                            "a single pattern.")

    # Disagreement: the challenger's case against the leader, recorded.
    for c in result.challenges:
        if leader and c.target_condition == leader:
            result.disagreements.append(f"Challenger vs leader: {c.argument}")
            break

    # Actions: safety first, then challenges, then discriminating questions.
    if rec.safety_net:
        result.actions.append("Safety-net: " + rec.safety_net)
    for c in result.challenges:
        result.actions.append(c.action)
    for q in rec.discriminating_questions:
        result.actions.append("Ask: " + q)

    seen = set()
    result.actions = [a for a in result.actions
                      if not (a in seen or seen.add(a))]
    return result
