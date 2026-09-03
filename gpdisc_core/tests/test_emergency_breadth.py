"""Stage 6: the emergency breadth tests — nobody dies of nothing.

The 2026-09-03 global audit fired 55 probes across the gap tiers; 19
returned an EMPTY differential. This suite locks the Tier-1 fixes, class
by class, as Task 6.3-6.7 land. Each test is one of the actual audit
probes — the exact patient who fell through, now caught by behaviour,
not prose.

Class Trauma (Task 6.3): the ladder fall that returned 'COPD', the stab
wound that returned nothing, the crush injury, the baby's scald, the
garden graze with unknown tetanus status.
"""
import pytest
from gpdisc_core.clinical_reasoning.consultation import ConsultationPipeline
from gpdisc_core.clinical_reasoning.safety import SafetyLayer

PIPE = ConsultationPipeline()
SAFETY = SafetyLayer()


def _leader(rec):
    return rec.ranked_differential[0]["name"] if rec.ranked_differential else ""


def _names(rec):
    return {d["name"] for d in rec.ranked_differential} | \
           {d["name"] for d in rec.dangerous_alternatives}


class TestTraumaAndBurns:
    """Audit probes that returned empty or absurd differentials."""

    def test_ladder_fall_tbi_is_emergency_not_copd(self):
        rec = PIPE.run(
            "my husband fell off a ladder and hit his head, he was knocked "
            "out for a minute and has vomited twice since", {})
        assert rec.escalation == "emergency"
        names = _names(rec)
        assert any("brain injury" in n or "head injury" in n for n in names)
        assert "COPD" not in _leader(rec)

    def test_stab_wound_chest_is_emergency_with_trauma_leader(self):
        rec = PIPE.run("my neighbour has been stabbed in the chest", {})
        assert rec.escalation == "emergency"
        # the safety rule short-circuits the engine; the rule name rides
        # in the retained/dangerous slot
        names = _names(rec)
        assert any("penetrating" in n.lower() for n in names)

    def test_crush_injury_with_shock_signs_is_emergency(self):
        rec = PIPE.run(
            "man trapped under rubble for two hours, crushed legs, "
            "pale and cold", {})
        assert rec.escalation == "emergency"
        names = _names(rec)
        assert any(n.startswith("Crush") or "shock" in n.lower()
                   for n in names)

    def test_baby_scald_is_emergency(self):
        rec = PIPE.run(
            "my baby pulled a kettle of boiling water over, scalded her "
            "arm", {})
        assert rec.escalation == "emergency"
        names = _names(rec)
        assert any("burn" in n.lower() for n in names)

    def test_garden_graze_with_unknown_tetanus_is_urgent(self):
        rec = PIPE.run(
            "grazed my elbow in the garden, tetanus injection status "
            "unknown", {})
        assert rec.escalation in ("urgent", "emergency")
        assert "tetanus" in _leader(rec).lower()

    def test_minor_finger_burn_stays_self_care(self):
        """Over-triage guard: a small fingertip burn is not an emergency."""
        rec = PIPE.run("burnt my finger on the iron, small blister", {})
        assert rec.escalation != "emergency"

    def test_mechanical_back_pain_still_routine(self):
        """The spinal rule must not fire on day-to-day back pain."""
        rec = PIPE.run("back pain after lifting boxes, no injury, "
                       "no numbness", {})
        assert rec.escalation != "emergency"

    def test_sciatica_unilateral_numnbess_not_emergency(self):
        """Unilateral leg numbness is sciatica, not cord compression."""
        a = SAFETY.screen("shooting pain down my left leg with numbness "
                          "in the foot for a week", {})
        assert a.level.value != "emergency"


class TestTraumaSafetyRules:
    """The five Stage 6.3 safety rules, fired directly."""

    def test_head_injury_rule_loc_plus_vomiting(self):
        a = SAFETY.screen("hit his head on the door, knocked out briefly, "
                          "vomiting since", {})
        assert a.emergency_rule == "head_injury_red_flags"

    def test_head_injury_rule_anticoagulated(self):
        a = SAFETY.screen("banged her head this morning, she is on "
                          "warfarin", {})
        assert a.emergency_rule == "head_injury_red_flags"

    def test_penetrating_rule(self):
        a = SAFETY.screen("stepped on a fishing spear, penetrating wound "
                          "to the foot", {})
        assert a.emergency_rule == "penetrating_trauma"

    def test_shock_rule_pale_cold_plus_crush(self):
        a = SAFETY.screen("crushed in a road accident, pale and cold, "
                          "fast pulse", {})
        assert a.emergency_rule == "haemorrhagic_shock"

    def test_burn_rule_scald(self):
        a = SAFETY.screen("toddler pulled a pan of hot oil over", {})
        assert a.emergency_rule == "major_burn"

    def test_spinal_rule_fall_plus_bilateral_numbness(self):
        a = SAFETY.screen("fell from a roof, can't feel his legs, pins "
                          "and needles in both legs", {})
        assert a.emergency_rule == "spinal_injury"

    def test_bare_head_bump_no_loc_no_vomit_not_emergency(self):
        """A trivial head bump with no red flags must stay routine —
        the rule demands TWO of mechanism/LOC/deterioration/anticoag."""
        a = SAFETY.screen("bumped my head on the cupboard door, fine "
                          "otherwise", {})
        assert a.level.value != "emergency"


class TestToxicologyAndWithdrawal:
    """Stage 6 Task 6.4: the poisonings and withdrawals that kill."""

    def test_paracetamol_overdose_emergency_however_well(self):
        rec = PIPE.run("took 20 paracetamol tablets six hours ago, "
                       "feels sick", {})
        assert rec.escalation == "emergency"
        names = _names(rec)
        assert any("paracetamol" in n.lower() or "overdose" in n.lower()
                   for n in names)

    def test_staggered_paracetamol_overdose_emergency(self):
        rec = PIPE.run("been taking a few paracetamol every few hours "
                       "for two days for toothache, more than the packet "
                       "says", {})
        assert rec.escalation == "emergency"

    def test_opioid_overdose_found_unconscious(self):
        rec = PIPE.run(
            "found my son unconscious next to a needle, breathing "
            "slowly, blue lips", {})
        assert rec.escalation == "emergency"
        names = _names(rec)
        assert any("opioid" in n.lower() for n in names)

    def test_carbon_monoxide_family_cluster(self):
        rec = PIPE.run(
            "whole family headache and nausea every evening at home, "
            "gas boiler, better at work", {})
        assert rec.escalation == "emergency"
        names = _names(rec)
        assert any("monoxide" in n.lower() for n in names)

    def test_delirium_tremens_in_custody(self):
        rec = PIPE.run(
            "heavy drinker, in custody since yesterday, seeing things "
            "and confused", {})
        assert rec.escalation == "emergency"

    def test_serotonin_syndrome_named(self):
        rec = PIPE.run(
            "started sertraline last week with tramadol, twitching "
            "legs, sweating, confused", {})
        assert rec.escalation == "emergency"
        assert "serotonin" in _leader(rec).lower() or \
            any("serotonin" in n.lower() for n in _names(rec))

    def test_organophosphate_farmer_emergency(self):
        rec = PIPE.run(
            "farmer sprayed crops yesterday, now drooling, sweating, "
            "pinpoint pupils, weak all over", {})
        assert rec.escalation == "emergency"

    def test_snake_envenomation_emergency(self):
        rec = PIPE.run(
            "bitten by a snake an hour ago while walking, arm swelling "
            "and tender armpit nodes", {})
        assert rec.escalation == "emergency"
        names = _names(rec)
        assert any("snake" in n.lower() or "envenom" in n.lower() or
                   "bite" in n.lower() for n in names)

    def test_opiate_withdrawal_misery_not_emergency(self):
        """Over-triage guard: withdrawal is miserable, not lethal in
        adults — shakes without delirium must not fire the DT rule."""
        rec = PIPE.run(
            "on methadone, pharmacy closed for the holidays, yawning, "
            "aching all over, diarrhoea", {})
        assert rec.escalation != "emergency"
        assert "withdrawal" in _leader(rec).lower()


class TestObstetricEmergencies:
    """Stage 6 Task 6.5: birth is the commonest reason a healthy young
    woman dies. The audit's PPH probe returned 'I don't have enough
    knowledge'."""

    def test_eclampsia_seizure_in_pregnancy(self):
        rec = PIPE.run("34 weeks pregnant, just had a seizure at home", {})
        assert rec.escalation == "emergency"
        names = _names(rec)
        assert any("eclamps" in n.lower() for n in names)

    def test_postpartum_haemorrhage_emergency(self):
        rec = PIPE.run("gave birth this morning, bleeding heavily, "
                       "soaking pads every hour, pale and dizzy", {})
        assert rec.escalation == "emergency"
        names = _names(rec)
        assert any("haemorrhage" in n.lower() or "bleed" in n.lower()
                   for n in names)

    def test_imminent_birth_crowning(self):
        rec = PIPE.run("the baby is coming now, contractions every two "
                       "minutes, need to push", {})
        assert rec.escalation == "emergency"

    def test_shoulder_dystocia_head_out_body_stuck(self):
        rec = PIPE.run("head is out but the shoulders are stuck", {})
        assert rec.escalation == "emergency"

    def test_cord_prolapse(self):
        rec = PIPE.run("waters broke and i can feel the cord coming out", {})
        assert rec.escalation == "emergency"

    def test_puerperal_sepsis_after_home_birth(self):
        rec = PIPE.run("six days after giving birth, fever 39, smelly "
                       "bleeding, womb tender", {})
        assert rec.escalation == "emergency"
        assert "sepsis" in _leader(rec).lower() or \
            any("sepsis" in n.lower() for n in _names(rec))

    def test_early_miscarriage_urgent_not_emergency(self):
        """Over-triage guard: light bleeding at 8 weeks is EPU-same-day,
        not 999 — and eclampsia matched on 'pregnant' alone must not
        floor it (the single-token contender lesson)."""
        rec = PIPE.run("8 weeks pregnant, light bleeding, mild cramps", {})
        assert rec.escalation == "urgent"
        assert "miscarriage" in _leader(rec).lower()

    def test_obstructed_labour_named(self):
        rec = PIPE.run("been in labour since last night, exhausted, "
                       "no progress for hours", {})
        names = _names(rec)
        assert rec.escalation in ("urgent", "emergency")
        assert any("labour" in n.lower() or "labor" in n.lower()
                   for n in names)


class TestOncologySupportiveAndDermEmergencies:
    """Stage 6 Task 6.6: the emergencies of people who already have
    cancer, and the skin conditions that kill."""

    def test_neutropenic_sepsis_on_chemo(self):
        rec = PIPE.run("on chemotherapy for lung cancer, fever 38.5 at "
                       "home tonight", {})
        assert rec.escalation == "emergency"
        names = _names(rec)
        assert any("neutropenic" in n.lower() for n in names)

    def test_cord_compression_in_known_cancer(self):
        rec = PIPE.run("breast cancer spread to bones, back pain worse "
                       "at night, legs feel weak", {})
        assert rec.escalation == "emergency"

    def test_svco_named(self):
        rec = PIPE.run("face and neck swollen, neck veins bulging, "
                       "worse lying flat, breathless", {})
        assert rec.escalation == "emergency"
        assert any("vena cava" in n.lower() or "svco" in n.lower()
                   for n in _names(rec))

    def test_sjs_ten_painful_rash_mucosal(self):
        rec = PIPE.run("started lamotrigine two weeks ago, now a rash "
                       "with sore blistered lips and eyes, skin hurts", {})
        assert rec.escalation == "emergency"
        assert any("stevens" in n.lower() or "necrolysis" in n.lower()
                   for n in _names(rec))

    def test_eczema_herpeticum(self):
        rec = PIPE.run("his eczema flared with clusters of little holes, "
                       "fever, not drinking", {})
        assert rec.escalation == "emergency"
        assert any("herpeticum" in n.lower() for n in _names(rec))

    def test_necrotising_fasciitis_pain_beyond_look(self):
        rec = PIPE.run("calf pain far more painful than it looks after "
                       "a small graze, spreading fast, fever", {})
        assert rec.escalation == "emergency"

    def test_erythroderma_skin_failure(self):
        rec = PIPE.run("skin red all over and shedding, shivering, "
                       "can't get warm", {})
        assert rec.escalation == "emergency"
        assert any("erythroderma" in n.lower() or "skin failure" in n.lower()
                   for n in _names(rec))

    def test_plain_cellulitis_stays_urgent_not_necrotising(self):
        """Over-triage guard: red painful leg with a low-grade temperature
        is cellulitis — the necrotising rule needs pain-disproportion
        plus rapid spread/dark change."""
        a = SAFETY.screen("red hot painful shin, mild temperature, "
                          "no rapid spread", {})
        assert a.emergency_rule != "necrotising_infection"


class TestPaediatricProtection:
    """Stage 6 Task 6.7: the child-protection and paediatric-syndrome
    probes. A bruise on a baby who cannot yet crawl is a safeguarding
    presentation, never 'just a bruise'."""

    def test_bruised_non_mobile_baby_is_safeguarding_urgent(self):
        rec = PIPE.run("my 5 month old baby has bruises on his back and "
                       "i don't know how he got them", {})
        assert rec.escalation in ("urgent", "emergency")
        names = _names(rec)
        assert any("non-accidental" in n.lower() or
                   "nonaccidental" in n.lower() or "abuse" in n.lower()
                   for n in names)
        assert "safeguard" in (rec.safety_net + rec.summary()).lower()

    def test_patterned_inflicted_injury_is_emergency(self):
        rec = PIPE.run("baby has a bite mark on his arm and a belt welt "
                       "across his back", {})
        assert rec.escalation == "emergency"

    def test_shaken_baby_is_emergency(self):
        rec = PIPE.run("she admitted shaking the baby last night, now he "
                       "is very sleepy and won't feed", {})
        assert rec.escalation == "emergency"
        assert "inflicted injury" in _names(rec) or \
            "inflicted_injury" in rec.problem_representation

    def test_kawasaki_six_day_fever_red_eyes(self):
        rec = PIPE.run("my 2 year old has had fever for six days, both "
                       "eyes red, cracked lips, so irritable", {})
        assert rec.escalation == "emergency"
        names = _names(rec)
        assert any("kawasaki" in n.lower() for n in names)

    def test_kawasaki_rule_direct(self):
        a = SAFETY.screen("fever for five days, red eyes, no other "
                          "cause found", {})
        assert a.emergency_rule == "kawasaki_fever_days"

    def test_kawasaki_rule_not_short_fever(self):
        """Over-triage guard: three days of fever with red eyes is a
        virus, not yet Kawasaki — the rule needs >=5 days."""
        a = SAFETY.screen("fever for three days, red eyes, snotty nose", {})
        assert a.emergency_rule != "kawasaki_fever_days"

    def test_iga_vasculitis_hsp_named(self):
        rec = PIPE.run("7 year old, purple spots you can feel on his "
                       "legs and bottom, ankles swollen, tummy pain", {})
        names = _names(rec)
        assert any("vasculitis" in n.lower() or "henoch" in n.lower() or
                   "hsp" in n.lower() for n in names)
        assert rec.escalation in ("urgent", "emergency")

    def test_febrile_convulsion_short_recovered_not_emergency(self):
        """Over-triage guard: a 2-minute fit with fever in a 3 year old
        who is back to normal is a febrile convulsion — same-day review,
        not 999 (status wording keeps the emergency rule for >5 min)."""
        rec = PIPE.run("my 3 year old had a fit with a fever, lasted two "
                       "minutes, back to himself now", {})
        assert rec.escalation != "emergency"
        names = _names(rec)
        assert any("febrile convulsion" in n.lower() for n in names)

    def test_neonatal_illness_is_emergency(self):
        rec = PIPE.run("four week old baby, not feeding, grunting, "
                       "temperature 38.2", {})
        assert rec.escalation == "emergency"
        assert "neonatal illness" in _names(rec) or \
            "neonatal_illness" in rec.problem_representation

    def test_neonatal_pale_stools_flags_biliary_atresia(self):
        """Pale stools + dark urine in a jaundiced newborn is biliary
        atresia until proven otherwise — the Kasai window closes by
        ~8 weeks, so the safety net must say so."""
        rec = PIPE.run("three week old baby still yellow, poo pale and "
                       "wee like tea", {})
        assert rec.escalation in ("urgent", "emergency")
        assert any("jaundice" in n.lower() or "biliary" in n.lower()
                   for n in _names(rec))
        assert "pale" in rec.safety_net.lower() or \
            "biliary" in rec.safety_net.lower()

    def test_slapped_cheek_warns_pregnant_contacts(self):
        """Parvovirus B19: harmless to the child, dangerous to pregnant
        contacts and sickle-cell patients — the safety net must say."""
        rec = PIPE.run("my daughter has bright red cheeks and a lacy "
                       "rash on her arms, sister is 20 weeks pregnant", {})
        assert any("slapped" in n.lower() or "parvovirus" in n.lower()
                   or "fifth" in n.lower() for n in _names(rec))
        assert "pregnan" in rec.safety_net.lower()

    def test_mobile_toddler_shin_bruises_not_escalated(self):
        """Over-triage guard: bruises on the shins of a climbing 4 year
        old are normal childhood. The non-mobile rule must not fire."""
        rec = PIPE.run("my 4 year old is always climbing, bruises on his "
                       "shins, otherwise fine", {})
        assert rec.escalation in ("routine", "self_care")
