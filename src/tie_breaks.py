"""Content-derived order for exact score ties."""
from hashlib import sha256


def content_order(chunks):
    """Map chunk IDs to unique ranks without hashing IDs or using input order."""
    keyed = {}
    for chunk in chunks:
        key = (sha256(chunk.text.encode()).digest(), chunk.unit_digest, chunk.start, chunk.end)
        if key in keyed:
            raise ValueError("Indistinguishable chunk content and provenance in neutral tie order")
        keyed[key] = chunk.chunk_id
    return {keyed[key]: rank for rank, key in enumerate(sorted(keyed))}


def rank_scores(ids, scores, k, tie_order=None, *, reverse_input=False):
    """Keep higher scores first. Without a secondary key, keep input order."""
    indices = range(len(ids))
    if reverse_input:
        indices = reversed(indices)
    if tie_order is None:
        ranked = sorted(indices, key=lambda i: -scores[i])
    else:
        ranked = sorted(indices, key=lambda i: (-scores[i], tie_order[ids[i]]))
    return [ids[i] for i in ranked[:k]]
