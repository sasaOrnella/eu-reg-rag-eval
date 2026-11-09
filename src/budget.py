"""Fixed context budget. CORE FUNCTION, written by you.

Experimental idea (hypothesis H1):
  Small chunks and large chunks must be compared at the SAME amount of retrieved context,
  otherwise "bigger chunks win" just means "more text was handed to the reader".
  So instead of a fixed top-k, we give each configuration a budget measured in characters
  (rough rule for English: 1 token is about 4 characters, so 8000 characters is about 2000 tokens)
  and keep taking chunks, best first, until the budget is used up.
"""

from src.corpus import Chunk


def select_within_budget(ranked: list[Chunk], budget_chars: int) -> list[Chunk]:
    if budget_chars <= 0:
        raise ValueError("budget_chars must be a positive number!!")
    if len(ranked) == 0:
        return []
    
    selected = []
    total_chars = 0

    for chunk in ranked:
        chunk_length = len(chunk.text)
        if chunk_length <= budget_chars - total_chars or len(selected) == 0:
            selected.append(chunk)
            total_chars += chunk_length
        else:
            break
    
    return selected
