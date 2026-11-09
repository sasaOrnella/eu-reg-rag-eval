# Week 1 checklist

- [ ] Create a GitHub account and an empty repo named `eu-reg-rag-eval`
- [ ] `git init`, commit this skeleton, push (first commit message: "Initial project skeleton")
- [x] Download GDPR and AI Act texts into `data/raw/` and document their sources in `data/README.md`
- [x] Write the research question and hypotheses in `README.md` (before experiments)
- [x] Implement `chunk_text` in `src/chunking.py` and pass `tests/test_chunking.py`
- [x] Implement `recall_at_k` and `reciprocal_rank` and pass `tests/test_metrics.py`
- [x] Read `src/bm25_baseline.py` and write three sentences explaining it (below)
- [x] Write 20 evaluation questions covering all five question types
- [ ] Commit after each step (small commits, meaningful messages)

> Checklist status reflects the project work discussed so far; confirm GitHub setup and commits locally.

## BM25 reading notes — three sentences

1. `BM25Retriever` tokenizes text into lowercase word-like tokens and uses BM25 to rank corpus passages against a query.
2. BM25 scores lexical relevance using query-term frequency, inverse document frequency, and document-length normalization rather than semantic embeddings.
3. In this project, BM25 serves as the sparse-retrieval baseline against which dense and hybrid methods will be compared on evidence recall.
