# EU AI Act New Dev (Q101–Q120) Blind Generation Inspection Report

## 1. Input Integrity & Corpus Verification
- **Corpus**: `data/processed/ai_act.jsonl` (SHA256: `c4a5b3999f5af5e37f301ceb7f9b1ab2ec311b96583d53044871a9e7089dfa8f`) — **293** units (113 articles, 180 recitals).
- **Exclusion list**: `eval/excluded_evidence_units.csv` (SHA256: `b24684a3549a1eac790c33178199b06c1cd6e1a36a98df99f43a084e393eded8`) — **38** reserved AI Act units excluded, leaving **82** eligible articles (including **45** in Articles 56–113) and **173** eligible recitals.
- **Output CSV**: `outputs/ai_act_dev_candidates.csv` (SHA256: `8aa8e804d7b364f56da4dfbf58dbebc2cde530d567efb300c792ff4f4707f8a4`).
- **ID occupancy check**: Confirmed `Q101`–`Q120` unoccupied prior to generation (`outputs/` contained only `Q081`–`Q100`). Accepted GDPR files remain untouched.
- **Blindness boundary**: Only files inside `gemini_blind_generation/` were accessed; no retrieval experiment results, failure cases, or model rankings were viewed.

## 2. Batch Quota & Constraint Audit

| Check | Requirement | Actual | Status |
| --- | --- | --- | --- |
| Row count & IDs | 20 rows, `Q101`–`Q120`, `split=dev` | 20 rows, `Q101`–`Q120`, `split=dev` | PASS |
| Type quotas | 5 / 5 / 4 / 4 / 2 | 5 / 5 / 4 / 4 / 2 | PASS |
| High / Low overlap (18 answerable) | ≥7 High (9–10 target), ≥40% Low | **9 High, 9 Low (50.0% Low)** | PASS |
| Low floor per answerable type | ≥1 Low in each of 4 types | single_hop=3, multi_hop=2, conflicting=2, numeric=2 | PASS |
| Excluded evidence overlap | 0 excluded units in positive evidence | **0** | PASS |
| Distinct positive evidence units | ≥20 distinct units | **23** | PASS |
| Max questions per evidence unit | ≤2 per unit | **1** | PASS |
| Second-half coverage (AI Act Art 56–113) | ≥6 questions | **10** | PASS |
| Unspecified-quantity unanswerable | ≤1 per regulation × split | **0** (kinds `b` and `a`) | PASS |
| Verbatim unique quote match | Exact substring count == 1 per quote | **All 27 quotes exact count = 1** | PASS |
| Quote length bounds | 40–300 target, warn <25 or >400, max 600 | Min 106, Max 383 (0 warnings) | PASS |
| Question length & structural refs | 8–40 words, 1 sentence ending `?`, no structural refs | 16–30 words, 0 structural refs | PASS |
| Gold answer length | 1–2 sentences, ≤60 words | 16–58 words | PASS |
| Opening-word diversity | ≤30% (≤6/20) same first word | Max 5/20 (`when`) | PASS |
| Near-duplicate check | Pairwise content-word Jaccard < 0.60 | Max **0.3529** (`Q115` vs `Q120`) | PASS |
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
| Q101 | `single_hop` | Article only | 0.5833 | High | 19 | 16 | 106 | ai_act:art:64 |
| Q102 | `single_hop` | Article only | 0.3846 | High | 20 | 24 | 243 | ai_act:art:84 |
| Q103 | `single_hop` | Article only | 0.1250 | Low | 23 | 23 | 145 | ai_act:art:35 |
| Q104 | `single_hop` | Article only | 0.0000 | Low | 21 | 23 | 137 | ai_act:art:61 |
| Q105 | `single_hop` | Recital only | 0.0714 | Low | 20 | 31 | 220 | ai_act:rec:97 |
| Q106 | `multi_hop` | Article only | 0.5385 | High | 28 | 58 | 262, 269 | ai_act:art:68, ai_act:art:90 |
| Q107 | `multi_hop` | Article only | 0.3750 | High | 29 | 55 | 166, 251 | ai_act:art:11, ai_act:art:18 |
| Q108 | `multi_hop` | Article only | 0.1875 | Low | 24 | 41 | 383, 197 | ai_act:art:88, ai_act:art:92 |
| Q109 | `multi_hop` | Mixed | 0.5882 | High | 24 | 50 | 305, 260 | ai_act:art:111, ai_act:rec:177 |
| Q110 | `multi_hop` | Mixed | 0.1579 | Low | 30 | 56 | 207, 319 | ai_act:art:54, ai_act:rec:109 |
| Q111 | `conflicting_or_conditional` | Article only | 0.4667 | High | 22 | 44 | 171, 224 | ai_act:art:57, ai_act:art:57 |
| Q112 | `conflicting_or_conditional` | Article only | 0.4444 | High | 23 | 42 | 263, 110 | ai_act:art:72, ai_act:art:72 |
| Q113 | `conflicting_or_conditional` | Article only | 0.2000 | Low | 26 | 39 | 322, 338 | ai_act:art:83, ai_act:art:83 |
| Q114 | `conflicting_or_conditional` | Recital only | 0.1429 | Low | 21 | 41 | 376, 272 | ai_act:rec:78, ai_act:rec:78 |
| Q115 | `numeric_or_table` | Article only | 0.3636 | High | 18 | 29 | 181 | ai_act:art:44 |
| Q116 | `numeric_or_table` | Article only | 0.1250 | Low | 25 | 30 | 300 | ai_act:art:33 |
| Q117 | `numeric_or_table` | Article only | 0.1875 | Low | 22 | 22 | 313 | ai_act:art:81 |
| Q118 | `numeric_or_table` | Recital only | 0.4286 | High | 25 | 19 | 214 | ai_act:rec:180 |
| Q119 | `unanswerable` | None | N/A | N/A | 16 | 25 | — | *(empty — unanswerable)* |
| Q120 | `unanswerable` | None | N/A | N/A | 17 | 29 | — | *(empty — unanswerable)* |

## 5. Legal-Semantic Self-Check Highlights
- **Statutory terminology**: Verified exact statutory body names (`Commission`, `AI Office`, `Union AI testing support structures`, `scientific panel`, `European Data Protection Supervisor`, `European Data Protection Board`) with no loose or ambiguous labels.
- **Exception & scope precision**: `Q109` explicitly scopes to private-sector high-risk AI systems (excluding the 2 August 2030 public-authority deadline in Art 111(2) and large-scale IT systems in Art 111(1)); `Q111`, `Q112`, `Q113`, and `Q114` quote both default rule and statutory exception/condition verbatim.
- **Recital exclusivity**: Confirmed `ai_act:rec:97`, `ai_act:rec:177`, `ai_act:rec:109`, `ai_act:rec:78`, and `ai_act:rec:180` supply facts/interpretations not duplicated in any EU AI Act article.
- **Multi-hop necessity**: Each of `Q106`–`Q110` links two distinct units where neither unit alone answers both linked parts of the question.
- **Unanswerable absence verification**: Both `Q119` (false premise: European AI Compensation Tribunal, kind `b`) and `Q120` (outside scope: patent ownership for AI-generated inventions, kind `a`) were verified across all 293 units in `ai_act.jsonl` with ≥4 keyword variants and manual inspection of the closest units; neither can be partially answered by general EU AI Act provisions.

## 6. Human Verification Note
- All 20 items are AI-drafted candidates (`author:ai | human_review:pending`). No human verification status has been fabricated.
- Stopped after Batch 2 (EU AI Act Dev, Q101–Q120) as instructed.
