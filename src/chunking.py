"""Split a document into overlapping chunks.

CORE FUNCTION, written by you. See tests/test_chunking.py for the exact behaviour required.
"""


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> list[str]:
    """Split `text` into chunks of at most `chunk_size` characters.

    Consecutive chunks share `overlap` characters.

    Requirements (checked by the tests):
      - empty text -> []
      - text shorter than chunk_size -> one chunk
      - overlap >= chunk_size -> raise ValueError
      - the last chunk must not be skipped

    Hint: the window start moves forward by (chunk_size - overlap) each step.
    """
    # TODO(you): implement
    raise NotImplementedError
