"""Offline prototype. See README.md for scope and limitations."""
import re
from dataclasses import dataclass

PARTS = {
    "bumper": ["bumper"],
    "bonnet": ["bonnet", "hood"],
    "door": ["door", "darwaza"],
    "front door": ["front door", "aage ka darwaza", "aage wala darwaza"],
    "rear door": ["rear door", "peeche ka darwaza", "pichla darwaza"],
    "windshield": ["windshield", "front glass", "sheesha", "aage ka glass"],
    "tyre": ["tyre", "tire", "pahiya", "wheel"],
    "headlight": ["headlight", "headlamp", "light"],
    "brake": ["brake"],
    "engine": ["engine", "motor"],
    "interior": ["interior", "seat", "dashboard", "cabin"],
    "roof": ["roof", "chhat"],
    "fender": ["fender", "mudguard"],
}

CONDITIONS = {
    "scratch": ["scratch", "scratches", "kharonch"],
    "dent": ["dent", "dent hai", "gadha", "dabb gaya"],
    "crack": ["crack", "cracked", "darar", "toota"],
    "rust": ["rust", "rusted", "jung", "zang"],
    "paint fade": ["fade", "faded", "paint utar", "rang uda"],
    "wear": ["worn", "wear", "ghis", "ghisa"],
    "leak": ["leak", "leaking", "leakage", "tapak"],
    "noise": ["noise", "awaz", "awaaz", "rattle", "khadkhad"],
    "ok": ["theek", "ok", "fine", "sahi hai", "good condition", "saaf"],
}

SEVERITY_MAJOR = ["zyada", "major", "bada", "heavy", "deep", "poor", "bahut"]
SEVERITY_MINOR = ["halka", "minor", "chhota", "slight", "thoda"]


@dataclass
class Finding:
    part: str
    condition: str
    severity: str        # major | minor | info
    quote: str


def parse_notes(transcript: str) -> list[Finding]:
    findings = []
    sentences = re.split(r"[.\n,;]+", transcript)
    for sent in sentences:
        low = sent.lower().strip()
        if not low:
            continue
        if re.search(r"\b(no|not|nahi|nahin|without)\b", low):
            # Ambiguous clause-level negation must be reviewed, not turned into damage.
            continue
        parts = [p for p, kws in PARTS.items() if any(k in low for k in kws)]
        if ("front door" in parts or "rear door" in parts) and "door" in parts:
            parts.remove("door")  # specific beats generic
        conds = [c for c, kws in CONDITIONS.items() if any(k in low for k in kws)]
        if not parts or not conds:
            continue
        sev = "info"
        if any(w in low for w in SEVERITY_MAJOR):
            sev = "major"
        elif any(w in low for w in SEVERITY_MINOR):
            sev = "minor"
        for p in parts:
            for c in conds:
                if c == "ok" and len(conds) > 1:
                    continue
                findings.append(Finding(p, c,
                                        "info" if c == "ok" else (sev if sev != "info" else "minor"),
                                        sent.strip()))
    # dedupe same part+condition, keeping the worst severity
    best = {}
    rank = {"major": 2, "minor": 1, "info": 0}
    for f in findings:
        k = (f.part, f.condition)
        if k not in best or rank[f.severity] > rank[best[k].severity]:
            best[k] = f
    return list(best.values())
