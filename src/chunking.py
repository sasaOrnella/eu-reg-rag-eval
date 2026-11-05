"""Split a document into overlapping chunks.

CORE FUNCTION, written by you. See tests/test_chunking.py for the exact behaviour required.
"""


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> list[str]:

  chunks = []
  start = 0

  if text == "":
    return []
  
  if overlap >= chunk_size:
    raise ValueError('Overlap must be smaller than chunk_size!!!')
  
  if len(text) <= chunk_size:
    return [text]

  while start < len(text):
    chunk = text[start:start + chunk_size]
    start = start+ chunk_size - overlap
    chunks.append(chunk)

  return chunks



