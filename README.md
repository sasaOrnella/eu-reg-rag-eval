# EU Regulation RAG Evaluation

Evaluating retrieval strategies for question answering over public EU regulatory texts
(GDPR, EU AI Act): which strategy gives the best faithfulness per unit of cost and latency?

> This system is a research/engineering exercise. It does not provide legal advice.



## Research question
On the English texts of the GDPR and the EU AI Act, how do retrieval method (BM25, dense, hybrid) and chunk size affect evidence recall under a fixed context-token budget, and does this effect differ by question type (single-hop, multi-hop, conditional, numeric)? Unanswerable questions have no gold evidence, so they are analysed only at the generation stage (does the system correctly abstain?). Answer faithfulness is a secondary outcome with a fixed generation model.

## Hypotheses (write BEFORE running experiments)
- H1: Holding the total retrieved context fixed (about 2,000 tokens, so k = budget / chunk size), evidence recall is an inverted U in chunk size: chunks of roughly 800–1,200 characters outperform both small (≤ 400 characters) and large chunks (≥ 2,000 characters). Sizes stay within the embedding model's input limit, except a whole-article baseline evaluated with BM25 only. A monotonic trend falsifies H1.
  
- H2: (a) On questions with high lexical overlap with their evidence, BM25's recall is at most 0.05 below dense retrieval's (margin fixed in advance). (b) On low-overlap questions and multi-hop questions, dense or hybrid retrieval has higher recall than BM25. (c) Hybrid is not significantly worse than the better single method on any question type (95% bootstrap CI).

- H3 (recall vs. answer quality): On multi-hop questions, gains in recall translate into smaller gains in answer correctness than on single-hop questions (“retrieved does not equal answered correctly”). This hypothesis can be tested only after the generation stage and is stated in advance.

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


<!-- git status
git add .
git commit -m "Rewrite HTML extractor to structured JSONL with validation"
git push -->
