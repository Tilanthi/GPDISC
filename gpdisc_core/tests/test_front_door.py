"""The front door: what the person asking actually sees.

The 2026-09-03 global audit found the consultation was computed and
attached as a side-channel while the primary answer text still showed a
system-init banner. On '3 year old, fever, stiff neck' the visible answer
was 'STAN system initialized...'. These tests lock the fix: the validated
consultation summary IS the answer.

Class 2 locks honesty: when the corpus has nothing to say, the system says
so instead of force-fitting a leader (the palliative->quinsy failure).
"""
import pytest
from gpdisc_core.core.unified_enhanced import EnhancedUnifiedGPDISCSystem
from gpdisc_core.clinical_reasoning.consultation import ConsultationPipeline

SYSTEM = EnhancedUnifiedGPDISCSystem()
PIPE = ConsultationPipeline()


class TestAnswerDisplaysTheConsultation:
    def test_emergency_query_answer_is_the_consultation(self):
        r = SYSTEM.answer("I think my 3 year old has a fever and a stiff neck")
        text = str(r.get("answer", ""))
        assert "STAN system initialized" not in text
        assert "Meningitis" in text or "meningococcal" in text
        assert "999" in text or "Emergency" in text or "emergency" in text

    def test_routine_query_answer_is_the_consultation(self):
        r = SYSTEM.answer("sore throat and runny nose for three days")
        text = str(r.get("answer", ""))
        assert "STAN system initialized" not in text
        assert "Safety net" in text   # consultation summary signature

    def test_legacy_text_preserved_as_metadata(self):
        r = SYSTEM.answer("sore throat and runny nose for three days")
        # nothing is lost: the legacy domain text moves aside, not away
        assert "consultation" in r
        assert r.get("escalation") in ("self_care", "routine", "urgent", "emergency")

    def test_consultation_summary_carries_validation(self):
        r = SYSTEM.answer("sore throat and runny nose for three days")
        text = str(r.get("answer", ""))
        assert "Validation" in text


class TestHonestUncertainty:
    def test_dying_probe_answered_by_palliative_module(self):
        # History: this probe was the original palliative->quinsy
        # force-fit failure, then locked as an 'outside what I know'
        # honesty placeholder. Since 7.4 the palliative module answers
        # it for real — the lock now pins that the answer is useful
        # AND still never force-fits an airway leader.
        rec = PIPE.run("my father is dying at home, how do we keep him "
                       "comfortable", {})
        summary = rec.summary().lower()
        assert "outside what i know" not in summary
        assert "don't have enough" not in summary
        assert "anticipatory" in summary or "comfort" in summary
        # and it must NOT force-fit an airway leader
        assert "quinsy" not in summary
        assert "epiglottitis" not in summary

    def test_noise_leader_flagged_not_presented(self):
        # 7.3: this probe was originally 'leaking urine when I cough or
        # sneeze' — stress_incontinence now claims that story with a
        # genuine leader, so it is no longer noise. Replaced with a
        # presentation no corpus entry can honestly score.
        rec = PIPE.run("just not felt right since the party, can't put "
                       "my finger on it", {})
        # a noise-scored leader (single generic word) must not be presented
        # as the diagnosis; the record must admit low confidence
        assert rec.uncertainty, "low-confidence differential must be honest"
        assert "describe more" in rec.uncertainty.lower() or \
               "low confidence" in rec.uncertainty.lower()

    def test_every_benign_bank_row_still_gets_a_real_leader(self):
        import sys
        sys.path.insert(0, "gpdisc_core/tests")
        from regression_bank import BANK
        for row in BANK:
            if row["escalation"] not in ("routine", "self_care", None):
                continue
            rec = PIPE.run(row["case"], {})
            assert rec.ranked_differential, row["case"]
            assert not (rec.uncertainty and "low confidence" in
                        rec.uncertainty.lower()), \
                f"honesty floor swallowed a benign row: {row['case']}"
