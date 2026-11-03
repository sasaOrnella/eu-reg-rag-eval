# EU Regulation RAG Evaluation

Evaluating retrieval strategies for question answering over public EU regulatory texts
(GDPR, EU AI Act): which strategy gives the best faithfulness per unit of cost and latency?

> This system is a research/engineering exercise. It does not provide legal advice.



## Research question
On the English texts of the GDPR and the EU AI Act, how do retrieval method (BM25, dense, hybrid) and chunk size affect evidence recall under a fixed context-token budget, and does this effect differ by question type (single-hop, multi-hop, unanswerable)? 
Answer faithfulness is evaluated as a secondary outcome with a fixed generation model.

## Hypotheses (write BEFORE running experiments)
- H1 (chunk size): Under a fixed context-token budget, medium-sized chunks (approximately 200–400 words) yield higher evidence recall than both very small chunks (<100 words) and very large chunks (>800 words), producing an inverted-U relationship. Very small chunks split multi-sentence provisions; very large chunks dilute relevant content and waste the budget. A monotonic relationship between chunk size and recall would falsify this hypothesis.
- H2 (retrieval method): Because regulatory text uses fixed terminology and explicit article numbering, BM25 is not weaker than dense retrieval on single-hop questions that contain clear terms. On paraphrased or multi-hop questions, dense or hybrid retrieval performs better. Hybrid retrieval is never worse than the best single method across question types.
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