# EU Regulation RAG Evaluation

Evaluating retrieval strategies for question answering over public EU regulatory texts
(GDPR, EU AI Act): which strategy gives the best faithfulness per unit of cost and latency?

> This system is a research/engineering exercise. It does not provide legal advice.

## Research question
TODO(you): one sentence. Example: "Does hybrid retrieval (BM25 + dense) with a reranker improve
answer faithfulness over dense-only retrieval, and at what cost and latency?"

## Hypotheses (write BEFORE running experiments)
- H1: TODO
- H2: TODO

## Repository layout
```
data/raw/          source texts (download yourself, see data/README.md)
data/processed/    chunked corpus
eval/              evaluation set template and annotation guide
src/               chunking, retrieval, metrics, cost tracking
tests/             unit tests (run with: pytest)
WEEK1.md           task checklist for week 1
```

## Quick start
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest                                               # core tests fail until you implement TODOs
```

## Results
TODO: add tables with 95% bootstrap confidence intervals after experiments.

## Limitations
TODO: be honest. (Evaluation set size, single domain, judge bias, etc.)
