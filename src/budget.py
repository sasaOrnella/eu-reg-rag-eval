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
    """Return the prefix of `ranked` (best first) that fits in `budget_chars` characters.

    Rules (tests/test_budget.py checks every one):
      1. Go through the chunks in rank order and keep adding while the running total of
         len(chunk.text) stays <= budget_chars.
      2. Stop at the FIRST chunk that does not fit. Do not skip ahead to a smaller chunk further
         down the list: that would quietly change the ranking.
      3. Always keep the first chunk, even if it alone is longer than the budget (this happens
         with whole-article chunks). The experiment reports the real context size, so the extra
         cost stays visible instead of silently scoring 0.
      4. Empty input -> empty list.
      5. budget_chars <= 0 -> raise ValueError.
    """
    # TODO(you): implement
    raise NotImplementedError
