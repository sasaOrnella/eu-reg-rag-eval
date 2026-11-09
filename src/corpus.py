"""Load the extracted units and turn them into chunks that remember where they came from.

Design decision (important for the experiment):
  * Gold evidence is stored as verbatim quotes inside a stable unit (an article or a recital).
  * A chunk records (unit_id, start, end) = its character range inside that unit's text.
  * So the same gold evidence stays valid when chunk size changes, and a retrieved chunk counts as a
    hit when its character range overlaps the gold range (see src/evidence.py).
  * Chunks never cross unit boundaries.
"""

import json
from dataclasses import dataclass
from pathlib import Path

from src.chunking import chunk_text


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    unit_id: str
    start: int
    end: int
    text: str


def make_unit_id(unit: dict) -> str:
    """'gdpr:art:33' for Article 33, 'gdpr:rec:26' for recital 26."""
    if unit["kind"] == "article":
        return f"{unit['doc']}:art:{unit['article']}"
    return f"{unit['doc']}:rec:{unit['number']}"


def load_units(*paths: str | Path) -> list[dict]:
    """Read one or more JSONL files and add a 'unit_id' field to every unit."""
    units = []
    for path in paths:
        with open(path, encoding="utf-8") as f:
            for line in f:
                u = json.loads(line)
                u["unit_id"] = make_unit_id(u)
                units.append(u)
    ids = [u["unit_id"] for u in units]
    assert len(ids) == len(set(ids)), "duplicate unit ids"
    return units


def build_chunks(
    units: list[dict], chunk_size: int | None, overlap: int = 0, chunker=chunk_text
) -> list[Chunk]:
    """Chunk every unit. chunk_size=None means 'one chunk per whole unit' (structural baseline).

    `chunker` is injectable so this function can be tested without your chunk_text.
    It relies on the stepping rule: chunk i starts at i * (chunk_size - overlap).
    """
    chunks = []
    for u in units:
        text = u["text"]
        if chunk_size is None:
            pieces, step = [text], 0
        else:
            pieces, step = chunker(text, chunk_size, overlap), chunk_size - overlap
        for i, piece in enumerate(pieces):
            start = i * step
            assert text[start : start + len(piece)] == piece, (
                f"chunk {i} of {u['unit_id']} is not text[{start}:{start + len(piece)}]. "
                "chunk_text must not strip or alter characters and must advance by chunk_size - overlap."
            )
            chunks.append(
                Chunk(
                    f"{u['unit_id']}#{i}",
                    u["unit_id"],
                    start,
                    start + len(piece),
                    piece,
                )
            )
    return chunks
