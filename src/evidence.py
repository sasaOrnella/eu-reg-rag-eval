"""Gold evidence: verbatim quotes -> character spans, and the overlap rule.

In eval/questions.csv the column `gold_evidence` looks like:

    gdpr:art:33::not later than 72 hours after having become aware of it
    gdpr:art:5::processed lawfully, fairly || gdpr:rec:39::transparent

i.e. `unit_id::verbatim quote`, several pieces separated by ` || `.
Copy quotes from data/processed/*.jsonl (not from the website): the quote must match exactly,
including curly quotes.
"""

from dataclasses import dataclass

from src.corpus import Chunk


@dataclass(frozen=True)
class Span:
    unit_id: str
    start: int
    end: int


def resolve_evidence(field: str, units_by_id: dict[str, dict]) -> list[Span]:
    """Turn the gold_evidence cell into spans. Raises ValueError with a helpful message on any problem."""
    spans = []
    for part in field.split("||"):
        part = part.strip()
        if not part:
            continue
        unit_id, sep, quote = part.partition("::")
        unit_id, quote = unit_id.strip(), quote.strip()
        if not sep or not quote:
            raise ValueError(f"expected 'unit_id::quote', got {part[:60]!r}")
        if unit_id not in units_by_id:
            raise ValueError(f"unknown unit id {unit_id!r}")
        text = units_by_id[unit_id]["text"]
        n = text.count(quote)
        if n == 0:
            raise ValueError(
                f"quote not found in {unit_id}: {quote[:60]!r} (copy it from the jsonl file)"
            )
        if n > 1:
            raise ValueError(
                f"quote appears {n} times in {unit_id}: make it longer/more specific"
            )
        start = text.find(quote)
        spans.append(Span(unit_id, start, start + len(quote)))
    return spans


def chunk_overlaps(chunk: Chunk, span: Span) -> bool:
    """True when the chunk and the evidence span share at least one character of the same unit."""
    return (
        chunk.unit_id == span.unit_id
        and chunk.start < span.end
        and span.start < chunk.end
    )
