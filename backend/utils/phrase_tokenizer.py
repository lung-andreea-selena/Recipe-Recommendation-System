from __future__ import annotations
import re
from pathlib import Path
from typing import List, Set

__all__ = ["tokenizer", "PHRASES"]

PHRASES_PATH: Path = Path(__file__).with_name("phrase_file.txt")

if not PHRASES_PATH.exists():
    raise FileNotFoundError(
        f"Required phrase list not found: {PHRASES_PATH}. "
        "Create the file or adjust PHRASES_PATH."
    )

with open(PHRASES_PATH, "r", encoding="utf-8") as f:
    PHRASES: Set[str] = {ln.strip().lower() for ln in f if " " in ln.strip()}

if not PHRASES:
    raise ValueError(
        "phrases.txt is empty or contains no multi‑word entries — cannot build tokenizer"
    )

JOIN_RE: re.Pattern[str] = re.compile(
    r"\b(?:" + "|".join(re.escape(p) for p in sorted(PHRASES, key=len, reverse=True)) + r")\b",
    flags=re.IGNORECASE,
)


def tokenizer(doc: str) -> List[str]:
    if not doc:
        return []
    lowered = doc.lower()
    joined = JOIN_RE.sub(lambda m: m.group(0).replace(" ", "_"), lowered)
    tokens = re.findall(r"[a-z_]+", joined)
    return tokens