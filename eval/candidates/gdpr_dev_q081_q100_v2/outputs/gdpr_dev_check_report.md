# GDPR New Dev (Q081–Q100) Blind Generation Inspection Report

## 1. Input Integrity & Corpus Verification
- **SHA256 verification**: All 7 files in `SHA256SUMS.txt` passed `shasum -a 256 -c SHA256SUMS.txt` (`OK`).
- **Corpus size**: `data/processed/gdpr.jsonl` contains **272** units (99 articles, 173 recitals); `data/processed/ai_act.jsonl` contains **293** units.
- **Exclusion list**: `eval/excluded_evidence_units.csv` lists **80** reserved units total (**42** GDPR units, **38** AI Act units), leaving **64** eligible GDPR articles (including **39** in Articles 50–99) and **166** eligible GDPR recitals for positive gold evidence.
- **Blindness boundary**: Only files inside `gemini_blind_generation/` were accessed; no retrieval experiment results were accessed or inferred.

## 2. Batch Quota & Constraint Audit

| Check | Requirement | Actual | Status |
| --- | --- | --- | --- |
| Row count & IDs | 20 rows, `Q081`–`Q100`, `split=dev` | 20 rows, `Q081`–`Q100`, `split=dev` | PASS |
| Type quotas | 5 / 5 / 4 / 4 / 2 | 5 / 5 / 4 / 4 / 2 | PASS |
| High / Low overlap (18 answerable) | 9–10 High, 8–9 Low (≥40% Low) | **9 High, 9 Low (50.0% Low)** | PASS |
| Low floor per answerable type | ≥1 Low in each of 4 types | single_hop=3, multi_hop=2, conflicting=2, numeric=2 | PASS |
| Excluded evidence overlap | 0 excluded units in positive evidence | **0** | PASS |
| Distinct positive evidence units | ≥20 distinct units | **23** | PASS |
| Max questions per evidence unit | ≤2 per unit | **1** | PASS |
| Second-half coverage (GDPR Art 50–99) | ≥6 questions | **9** | PASS |
| Unspecified-quantity unanswerable | ≤1 per regulation × split | **0** (kinds `b` and `c`) | PASS |
| Verbatim unique quote match | Exact substring count == 1 per quote | **All 27 quotes exact count = 1** | PASS |
| Quote length bounds | 40–300 target, warn <25 or >400, max 600 | Min 47, Max 391 (0 warnings) | PASS |
| Question length & structural refs | 8–40 words, 1 sentence ending `?`, no structural refs | 14–27 words, 0 structural refs | PASS |
| Gold answer length | 1–2 sentences, ≤60 words | 14–50 words | PASS |
| Opening-word diversity | ≤30% (≤6/20) same first word | Max 4/20 (`how`) | PASS |
| Near-duplicate check | Pairwise content-word Jaccard < 0.60 | Max **0.4000** (`Q083` vs `Q096`) | PASS |
| Automated errors / warnings | 0 errors, 0 warnings | **0 errors, 0 warnings** | PASS |

## 3. Evidence Type × Question Type × High-Overlap Matrix

| Type | Article only (actual / req, High / min) | Recital only (actual / req, High / min) | Mixed (actual / req, High / min) |
| --- | --- | --- | --- |
| `single_hop` | 4/4 (2/≥2 High) | 1/1 (0/≥0 High) | 0/0 (0/0) |
| `multi_hop` | 3/3 (2/≥1 High) | 0/0 (0/0) | 2/2 (1/≥1 High) |
| `conflicting_or_conditional` | 3/3 (2/≥1 High) | 1/1 (0/≥0 High) | 0/0 (0/0) |
| `numeric_or_table` | 3/3 (1/≥1 High) | 1/1 (1/≥1 High) | 0/0 (0/0) |

## 4. Per-Candidate Audit Table

| ID | Type | Evidence Type | Overlap | Band | Q Words | A Words | Quote Chars | Units |
| --- | --- | --- | ---: | --- | ---: | ---: | --- | --- |
| Q081 | `single_hop` | Article only | 0.3846 | High | 22 | 35 | 214 | gdpr:art:59 |
| Q082 | `single_hop` | Article only | 0.5556 | High | 15 | 14 | 106 | gdpr:art:75 |
| Q083 | `single_hop` | Article only | 0.0000 | Low | 19 | 31 | 278 | gdpr:art:53 |
| Q084 | `single_hop` | Article only | 0.0000 | Low | 21 | 21 | 111 | gdpr:art:7 |
| Q085 | `single_hop` | Recital only | 0.0000 | Low | 20 | 14 | 80 | gdpr:rec:32 |
| Q086 | `multi_hop` | Article only | 0.3750 | High | 20 | 22 | 47, 102 | gdpr:art:68, gdpr:art:73 |
| Q087 | `multi_hop` | Article only | 0.5714 | High | 22 | 41 | 245, 148 | gdpr:art:56, gdpr:art:60 |
| Q088 | `multi_hop` | Article only | 0.1000 | Low | 22 | 32 | 117, 138 | gdpr:art:38, gdpr:art:39 |
| Q089 | `multi_hop` | Mixed | 0.3846 | High | 22 | 39 | 160, 326 | gdpr:rec:47, gdpr:art:6 |
| Q090 | `multi_hop` | Mixed | 0.1875 | Low | 25 | 43 | 337, 327 | gdpr:art:11, gdpr:rec:26 |
| Q091 | `conflicting_or_conditional` | Article only | 0.5455 | High | 17 | 35 | 250, 346 | gdpr:art:2, gdpr:art:2 |
| Q092 | `conflicting_or_conditional` | Article only | 0.3636 | High | 21 | 50 | 266, 366 | gdpr:art:65, gdpr:art:65 |
| Q093 | `conflicting_or_conditional` | Article only | 0.0769 | Low | 21 | 37 | 130, 169 | gdpr:art:61, gdpr:art:61 |
| Q094 | `conflicting_or_conditional` | Recital only | 0.2143 | Low | 22 | 45 | 336, 234 | gdpr:rec:50, gdpr:rec:50 |
| Q095 | `numeric_or_table` | Article only | 0.3333 | High | 14 | 31 | 195 | gdpr:art:43 |
| Q096 | `numeric_or_table` | Article only | 0.1000 | Low | 18 | 39 | 341 | gdpr:art:54 |
| Q097 | `numeric_or_table` | Article only | 0.0000 | Low | 25 | 31 | 391 | gdpr:art:64 |
| Q098 | `numeric_or_table` | Recital only | 0.5000 | High | 25 | 28 | 202 | gdpr:rec:143 |
| Q099 | `unanswerable` | None | N/A | N/A | 16 | 20 | — | *(empty — unanswerable)* |
| Q100 | `unanswerable` | None | N/A | N/A | 14 | 21 | — | *(empty — unanswerable)* |

## 5. Human Verification Note
- All 20 items are AI-drafted candidates (`author:ai | human_review:pending`). No human verification status has been fabricated; acceptance, cross-batch deduplication, and merging remain with the project owner.
- Per instructions, generation stopped after Batch 1 (GDPR New Dev, Q081–Q100).
