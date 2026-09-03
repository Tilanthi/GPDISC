#!/usr/bin/env python3
"""Build GPDISC_How_To_Use.md from outputs_howto.json.

Honesty rules honoured here:
- every answer is inserted VERBATIM from outputs_howto.json;
- trimming only at a line/sentence boundary before TRIM_LIMIT, with a
  final line containing just " ...";
- no answer text is ever reworded or reordered.
"""
import json
import re

SRC = "/Users/gjw255/astrodata/SWARM/GPDISC/User_manual/outputs_howto.json"
DST = "/Users/gjw255/astrodata/SWARM/GPDISC/User_manual/GPDISC_How_To_Use.md"
TRIM_LIMIT = 1350

with open(SRC) as fh:
    OUT = {o["label"]: o for o in json.load(fh)}

state = {"trimmed": 0, "examples": 0}
doc = []


def emit(text: str) -> None:
    doc.append(text)


def block(label: str) -> str:
    ans = OUT[label]["answer"]
    assert "```" not in ans, label
    return ans


def example(num: int, label: str) -> None:
    ans = block(label)
    if len(ans) > TRIM_LIMIT:
        cut = ans[:TRIM_LIMIT]
        idx = cut.rfind("\n")
        frag = cut[:idx] if idx != -1 else cut
        if idx == -1:
            ends = [m.end() for m in re.finditer(r"[.!?](?=\s|$)", cut)]
            frag = cut[: ends[-1]] if ends else cut
        lines = frag.split("\n")
        # never end on a dangling empty section header
        while lines and (lines[-1].strip() == "" or lines[-1].rstrip().endswith(":")):
            lines.pop()
        ans = "\n".join(lines) + "\n ..."
        state["trimmed"] += 1
    q = OUT[label]["query"]
    state["examples"] += 1
    emit(f"**{num}. {q}**\n")
    # ```text (not a bare fence): pandoc then emits a fancyvrb Verbatim
    # environment, which the shared preamble's fvset wraps at the margin;
    # a bare fence becomes plain \verbatim and long lines overflow.
    emit(f"```text\n{ans}\n```\n")


# ------------------------------------------------------------------ front
emit("""# How to Use GPDISC --- a practical guide in plain English

**Version 1.1.0 - 3 September 2026 - Private and local.**

GPDISC is a private consultation system that lives entirely on this computer. You type a question in your own words --- exactly as you would say it to your family doctor --- and it replies with a structured consultation record: what it thinks might be going on, what must not be missed, what to answer next, and what should send you back for help.

**Everything stays on this computer.** Nothing you type, and no answer or record GPDISC keeps, is ever sent to any external service or website. There is no account, no cloud, no transmission of any kind.

There is really only one rule for using it: **talk to it as you would talk to a doctor.** No commands, no special words, no jargon. Plain English describing how you feel is exactly what it wants.

**In an emergency, call 999 (or your local emergency number) FIRST.** Chest pain, stroke signs, heavy bleeding, a collapsed or blue child --- telephone for help before you type anything. Software can wait; an emergency cannot. Never wait for software to tell you what you already know is urgent.
""")

# ---------------------------------------------------------- how to ask well
emit("""## How to ask well

The difference between a vague reply and a sharp one is almost always the question. A doctor meeting you for fifteen minutes asks who, how long, how bad. Do the same in your message and GPDISC has something to work with.

**Say who it is about, and their age.** "My 14 year old daughter..." or "I'm 68..." changes what the sensible possibilities are. Age and pregnancy matter enormously to what a symptom can mean.

**Say how long it has been going on.** "Since breakfast", "for three weeks", "for months" --- timescale sorts the worrying from the routine better than almost anything else.

**Say how bad it is, in your own words.** "I can still walk on it", "I had to sit down", "worst pain I've ever had" --- that is exactly the language doctors use with each other.

**Say what makes it better or worse.** Coming on with stairs, easing when you sit forward, starting an hour after a tablet --- these details often crack the case.

**List the medicines, including ones you buy yourself.** "I take warfarin", "my doctor doubled my water tablet", "regular ibuprofen from the chemist" --- medicines cause and colour a remarkable share of symptoms.

**Name the other conditions.** Diabetes, kidney disease, pregnancy, anything long-term. The same symptom in a different body is a different problem.

**Describe tests in everyday words.** You do not need to understand a result to pass it on: "the ECG report says irregularly irregular, no P waves, rate 130". Say what the paper said, plus how the person feels.

**Asking about someone else** is fine and common. Say who they are, their age, and what you saw: "My husband collapsed and now his speech is slurred." For someone who cannot describe it themselves --- a confused parent, a small child, someone dying --- your observation is the consultation.

**Asking about medicines** works best when you say what the medicine is for and who takes it: "My mum takes ibuprofen for her arthritis and has kidney disease --- should she still?" rather than "is ibuprofen safe?"

**Asking to make sense of a test result** --- say the numbers and words exactly as written, who the test was on, and how that person feels. A result without the person is only half a question.

**Asking for a second opinion** --- say what you were told, roughly by whom ("the hospital", "my GP"), and what worries you about it. GPDISC will lay out its own reasoning to compare against what you heard.

**When GPDISC asks you questions back --- answer them in a follow-up message.** Every reply can carry an "Ask next:" line. Those are not a quiz; they are the exact questions a doctor would ask next, and each answer you send sharpens the picture.

**And when a question is asked too bare, GPDISC says so --- it never guesses.** These two replies are real, word for word:
""")

emit(f"```text\n{block('alcohol_metronidazole_bare')}\n```\n")
emit(f"```text\n{block('vague_unwell_bare')}\n```\n")

emit("""That is the honest answer of a system that would rather admit a gap than invent a fact. If you get one, do what it says: describe more --- who, how long, how bad, what else --- and ask again. The thirty examples ahead show how much a fuller question buys you.
""")

# ------------------------------------------------------ how to read the reply
emit("""## How to read the reply

Every GPDISC reply is a consultation record with the same shape every time. Here is a real one, word for word, to a question about a cough:
""")

emit(f"```text\n{block('cough_weight_loss')}\n```\n")

emit("""Part by part:

- **Presenting complaint** --- the question as GPDISC understood it. Check it read you right.
- **Problem representation** --- the features it extracted from your words. When this line says "EMERGENCY pattern matched", the rest of the reply is about speed, not diagnosis.
- **Differential** --- the conditions it is actually considering, most likely first, each with a confidence score. A small score means a weak match, not a small problem.
- **Must-not-miss** --- the dangerous conditions it refuses to forget even though they are unlikely. This list is deliberately cautious: a safety net, not a verdict that you have them.
- **Ask next** --- the questions a doctor would ask you next. Answer them in a follow-up message.
- **Investigations** --- the tests that would settle it, and what each is for.
- **Treatment** --- what could be done now, and on whose advice.
- **Referral** --- who should see you, and how soon. With the safety net, this is where the level of concern lives: "self-care with pharmacy support" is routine; "same-day urgent review" means today; "EMERGENCY ... call 999" means now.
- **Safety net** --- what should change your mind and send you back for help, and how fast. Read this line even if you read nothing else.
- **Ruleset** --- which country's rules the answer ran under: guidelines, emergency number, reporting duties. Say where you are for advice that fits.
- **Uncertainty** --- how sure it is, in plain words. "Competing hypotheses remain close" is an honest invitation to describe more.
- **Validation** --- its own final self-check before showing you the answer. If a line here says an escalation was raised, believe the more urgent version.

One habit ties it together: read the **safety net** and **referral** lines first, then work upwards.
""")

# ------------------------------------------------------------- the examples
emit("""## Thirty examples

Every answer below is a **real, unedited GPDISC reply** to the question shown, exactly as it came back from the live system. Longer replies were cut where the page ran out; the line " ..." marks the cut, and nothing before it was changed. Read the questions as lessons in asking well as much as answers in their own right.
""")

emit("**Describing your own symptoms**\n")
example(1, "cough_weight_loss")
example(2, "weekend_headache")
example(3, "knee_pain")
example(4, "ankle")
example(5, "postural")
example(6, "groin_rash")

emit("**Asking about someone else**\n")
example(7, "stroke_fast")
example(8, "drug_confusion")
example(9, "teen_anorexia")
example(10, "reduced_movements")

emit("**Asking about medicines**\n")
example(11, "paracetamol_warfarin")
example(12, "egfr_metformin")
example(13, "ckd_nsaids")

emit("**Making sense of tests**\n")
example(14, "abg")
example(15, "glomerular_dip")
example(16, "af_ecg")
example(17, "s_aureus_culture")

emit("**Travel and the wider world**\n")
example(18, "trek_nepal")
example(19, "kenya_fever_rash")
example(20, "heat_stroke")
example(21, "offshore_chest_pain")
example(22, "lyme")

emit("**Sensitive questions**\n")
example(23, "ukmec_migraine")
example(24, "emergency_contraception")
example(25, "sti_discharge")
example(26, "testicular")

emit("**Mind, memory and long-term illness**\n")
example(27, "grief_low_mood")
example(28, "memory_loss")
example(29, "terminal_agitation")
example(30, "pd_hallucinations")

# -------------------------------------------------------------- close
emit("""## A last word

Notice how often the replies above end with a safety net --- *what should bring you back, and how fast*. That is GPDISC's most important sentence, every time.

**If in doubt, get a human.** A symptom that frightens you; anything a reply itself calls an emergency: **call 999 in the UK, 112 or 911 elsewhere --- first, and never wait for software.**

GPDISC provides second opinions, education and support for thinking. It is **not a replacement for professional medical care**, not a diagnosis to act on alone, and not a substitute for the emergency services. All medical decisions belong with qualified clinicians, taken together with you.
""")

with open(DST, "w") as fh:
    fh.write("\n".join(doc) + "\n")

print(f"examples: {state['examples']}  trimmed: {state['trimmed']}")
