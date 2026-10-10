"""
Mechanical-prose checks for outreach text: stock LLM vocabulary, signpost transitions, editorialising
participle endings, false antithesis, hedges and cover-letter cliches, plus a rhythm check for longer prose.

Used by llm_tailor.validate_pitch (a violation triggers the retry) and by the template tests, so the fixed
letter/email wording stays clean too.
"""
import re

# Stems, so inflections are caught too ("fostered", "landscapes", "seamlessly")
BANNED_STEMS = [
    "delve", "foster", "garner", "underscor", "illuminat", "harness", "pique", "cultivat", "travers", "navigat",
    "tapestr", "realm", "testament", "beacon", "paradigm", "landscape", "nuance", "interplay", "symphon",
    "multifaceted", "pivotal", "intricate", "profound", "vibrant", "indispensable", "bespoke", "holistic",
    "seamless", "inextricabl", "unequivocal", "undeniabl",
]

TRANSITION_OPENERS = ["moreover", "furthermore", "in addition", "additionally", "consequently", "ultimately"]

# Participles that comment on the sentence instead of adding a fact ("..., highlighting my commitment to X").
# Result participles that state a fact ("..., reducing MTTR") are fine and appear in the fact bank.
EDITORIAL_PARTICIPLES = ["highlighting", "underscoring", "showcasing", "demonstrating", "reflecting",
                         "emphasizing", "emphasising", "illustrating", "signaling", "signalling", "shaping",
                         "paving", "cementing", "reinforcing", "positioning"]

HEDGES = ["it is important to", "it's important to", "it is worth noting", "it's worth noting", "needless to say",
          "a balanced perspective", "in today's", "in the ever-", "as we move"]

CLICHES = ["i hope this email finds you well", "i hope this message finds you well", "i am writing to express",
           "strong interest", "thank you for your time and consideration", "i would welcome the opportunity",
           "passionate about", "team player", "fast-paced environment", "go-getter", "think outside the box"]

FALSE_ANTITHESIS = re.compile(r"\b(?:is|isn't|is not|it's|it is)\s+not\s+(?:just|merely|only|simply)\b|"
                              r"\bnot\s+(?:just|merely|simply)\s+about\b[^.]*?[;,]\s*(?:it'?s|it is|but)\b",
                              re.IGNORECASE)


def sentences(text):
    flat = re.sub(r"\s+", " ", text or "").strip()
    return [s for s in re.split(r"(?<=[.!?:])\s+(?=[A-Z\"'(])", flat) if s]


def lint(text, allowed=""):
    """
    Returns a list of problems in `text`. Words that also appear in `allowed` (e.g. the source fact a bullet
    rephrases) are not flagged, so a faithful rephrase is never penalised for the fact's own wording.
    """
    problems = []
    if not text:
        return problems
    low = text.lower()
    allowed_low = (allowed or "").lower()

    for stem in BANNED_STEMS:
        for m in re.finditer(rf"\b{stem}\w*", low):
            if m.group(0) not in allowed_low:
                problems.append(f"stock AI word '{m.group(0)}'")
                break

    words = len(text.split())
    em_dashes = text.count("—") + text.count(" -- ")
    if em_dashes > max(1, -(-words // 800)):
        problems.append(f"{em_dashes} em dashes (limit one per 800 words)")

    for s in sentences(text):
        s_low = s.lower()
        for t in TRANSITION_OPENERS:
            if s_low.startswith(t + ",") or s_low.startswith(t + " "):
                problems.append(f"signpost transition '{t.capitalize()}'")
        m = re.search(r",\s+(" + "|".join(EDITORIAL_PARTICIPLES) + r")\b[^,.;]*[.!?]?$", s_low)
        if m:
            problems.append(f"editorialising ending ', {m.group(1)} ...'")

    if FALSE_ANTITHESIS.search(text):
        problems.append("false antithesis ('not just X ... it's Y')")
    for phrase in HEDGES:
        if phrase in low:
            problems.append(f"hedge '{phrase}'")
    for phrase in CLICHES:
        if phrase in low and phrase not in allowed_low:
            problems.append(f"cliche '{phrase}'")
    return problems


def rhythm_problems(text, min_sentences=4):
    """
    For multi-sentence prose: flag a flat cadence (no short sentence, narrow length spread) and runs of three
    sentences opening with the same word ("I ... I ... I ...").
    """
    sents = [s for s in sentences(text) if len(s.split()) > 1]
    if len(sents) < min_sentences:
        return []
    problems = []
    lengths = [len(s.split()) for s in sents]
    if min(lengths) > 10:
        problems.append(f"no short sentence (shortest is {min(lengths)} words)")
    if max(lengths) - min(lengths) < 12:
        problems.append(f"flat cadence (sentence lengths {min(lengths)}-{max(lengths)} words)")
    openers = [re.sub(r"[^a-z']", "", s.split()[0].lower()) for s in sents]
    for i in range(len(openers) - 2):
        if openers[i] == openers[i + 1] == openers[i + 2]:
            problems.append(f"three sentences in a row open with '{sents[i].split()[0]}'")
            break
    return problems
