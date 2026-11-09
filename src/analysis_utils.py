"""Small analysis helpers (provided for you).

lexical_overlap gives every question an objective 'how much does it repeat the words of its evidence' score.
H2 compares BM25 and dense retrieval on high-overlap versus low-overlap questions; computing the score
automatically avoids subjective, after-the-fact labelling of which questions count as 'paraphrased'.
"""

from src.bm25_baseline import tokenize

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "can", "do", "does", "for", "from", "has", "have",
    "how", "i", "if", "in", "is", "it", "its", "may", "me", "my", "must", "no", "not", "of", "on", "or",
    "shall", "should", "so", "than", "that", "the", "their", "them", "there", "these", "this", "to",
    "under", "what", "when", "where", "which", "who", "whom", "will", "with", "would", "you",
}  # fmt: skip


def content_tokens(text: str) -> set[str]:
    return {t for t in tokenize(text) if t not in STOPWORDS and len(t) > 1}


def lexical_overlap(question: str, evidence_text: str) -> float:
    """Fraction of the question's content words that also occur in the evidence text (0.0 to 1.0)."""
    q = content_tokens(question)
    if not q:
        return 0.0
    return len(q & content_tokens(evidence_text)) / len(q)
