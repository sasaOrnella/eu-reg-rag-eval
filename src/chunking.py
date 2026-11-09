"""Split a document into overlapping chunks.

CORE FUNCTION, written by you. See tests/test_chunking.py for the exact behaviour required.
"""


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> list[str]:


  chunks = []
  start = 0
  
  if overlap >= chunk_size:
    raise ValueError('Overlap must be smaller than chunk_size!!!')

  if text == "":
    return []  

  if len(text) <= chunk_size:
    return [text]

  while start < len(text):
    chunk = text[start:start + chunk_size]
    chunks.append(chunk)
    if start + chunk_size >= len(text):
        break
    start = start+ chunk_size - overlap
    

  return chunks




