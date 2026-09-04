# gpdisc_core

**GPDISC: General Practice Discovery and Intelligence System for Consultation**

GPDISC is a private, GP-led medical consultation and second-opinion system.
This package (`gpdisc_core`) holds the whole program: the clinical reasoning
core, the medical specialty domains, the UK practice layer, the MDT
consultation team, and the preserved biology-knowledge foundation.

## Layout

| Path | What it is |
|---|---|
| `clinical_reasoning/` | The GP-led front door: 273-condition corpus, Bayesian test interpretation, safety/escalation screen, differential engine, consultation pipeline, validation layer |
| `domains/` | 44 domain packages — 5 primary UK-framed medical specialties (Cardiology, Epilepsy, General Practice, Orthopedics, Pharmacology), 29 US-framed legacy specialty domains, 10 preserved biology domains |
| `uk_practice/` | NICE/CKS index, 2ww suspected-cancer criteria, DVLA rules, MCA/safeguarding, controlled drugs, antimicrobial stewardship, high-risk drug monitoring, fit notes |
| `mdt/` | Multi-agent consultation team: challenger, six MDT roles + six consultant roles, debate protocol, multimorbidity whole-patient review |
| `consultation_skills/` | ICE questions, SPIKES, safety-net formula, difficult-consultation kinds, consultation models |
| `travel_medicine/`, `preventive_medicine/`, `sexual_health/` | Stage-2 specialist modules (destinations, UK vaccines/screening, UKMEC) |
| `post_exposure/` | Rabies and bloodborne post-exposure prophylaxis, time-boxed |
| `palliative_care/` | End-of-life symptom frames, anticipatory prescribing, cant-swallow route advice |
| `interpretation/` | ECG, ABG, CSF, urine dip, spirometry, synovial fluid, culture logic |
| `resource_settings/`, `jurisdictions/`, `humanitarian_care/` | The same patient in four resource worlds, under stated jurisdiction rules, refugee/asylum consultations |
| `memory/`, `data/` | Local-only persistent memory and storage — patient data never leaves this machine |
| `capabilities/`, `reasoning/`, `causal/`, `self_teaching/`, `physics/`, `simulation/` | Generic BIODISC/ASTRA-era reasoning machinery, preserved as the scientific foundation |
| `dashboard/` | Local web consultation interface (port 8790) |

## Entry point

```python
from gpdisc_core import create_gpdisc_system

system = create_gpdisc_system()
result = system.answer("I'm experiencing chest pain, what should I do?")
print(result['answer'])
```

Every medical query routes through the clinical reasoning front door:
safety screen first, then differential, then consultation record —
emergency patterns are never downgraded by benign reasoning.

## Provenance note

The generic reasoning machinery (`reasoning/`, `causal/`,
`self_teaching/`, `capabilities/`, `simulation/`, `physics/`) was built
in the BIODISC/ASTRA era as general scientific-reasoning architecture
and is retained unchanged as the scientific foundation. The
astronomy-specific modules of the ASTRA lineage (observational strategy,
multiwavelength reconciliation, ISM knowledge, astro databases,
relativistic/quantum/nuclear physics, SPH and stellar simulation) were
removed on 2026-09-04 — this package is medical and biological only.

## Privacy

All patient records are stored locally under `gpdisc_core/data/`.
Nothing is transmitted to external LLMs or services. See the
repository's `CLAUDE.md` for the binding no-push rule.

**GPDISC provides second-opinion consultation and is NOT a replacement
for professional medical care. In an emergency, call 999/911.**
