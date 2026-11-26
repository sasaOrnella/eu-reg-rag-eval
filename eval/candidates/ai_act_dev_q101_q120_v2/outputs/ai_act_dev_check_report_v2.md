# EU AI Act New Dev (Q101–Q120) Recalculated Quota & Inspection Report (v2)

## 1. Revision & Integrity Summary
- **Revised CSV**: `outputs/ai_act_dev_candidates_v2.csv` (SHA256: `24629721006055e26873cc308c6179449d654c93122307dfcf5315530be2b14d`)
- **Preserved v1 CSV**: `outputs/ai_act_dev_candidates.csv` (SHA256: `8aa8e804d7b364f56da4dfbf58dbebc2cde530d567efb300c792ff4f4707f8a4` — untouched)
- **Modified rows**: `Q103`, `Q105`, `Q108`, `Q109`, `Q110`, `Q112`, `Q114`, `Q119` (8 rows). **Unchanged rows**: 12 rows verified byte-for-byte identical to v1.
- **Blindness boundary**: No retrieval scores or locked Test results accessed.

## 2. Recalculated Batch Quota & Constraint Audit (v2)

| Check | Requirement | Actual (v2) | Status |
| --- | --- | --- | --- |
| Row count & IDs | 20 rows, `Q101`–`Q120`, `split=dev` | 20 rows, `Q101`–`Q120`, `split=dev` | PASS |
| Type quotas | 5 / 5 / 4 / 4 / 2 | 5 / 5 / 4 / 4 / 2 | PASS |
| High / Low overlap (18 answerable) | ≥7 High (9–10 target), ≥40% Low | **10 High, 8 Low (44.4% Low)** | PASS |
| Low floor per answerable type | ≥1 Low in each of 4 types | single_hop=3, multi_hop=2, conflicting=1, numeric=2 | PASS |
| Excluded evidence overlap | 0 excluded units in positive evidence | **0** | PASS |
| Distinct positive evidence units | ≥20 distinct units | **23** | PASS |
| Max questions per evidence unit | ≤2 per unit | **1** | PASS |
| Second-half coverage (AI Act Art 56–113) | ≥6 questions | **10** | PASS |
| Unspecified-quantity unanswerable | ≤1 per regulation × split | **0** (kinds `b` and `a`) | PASS |
| Verbatim unique quote match | Exact substring count == 1 per quote | **All 28 quotes exact count = 1** | PASS |
| Quote length bounds | Target 40–300, soft warn >400, hard max 600 | Min 106, Max 448 (1 soft >400 warn: `Q110` Art 54(6) indivisible statutory sentence, ≤600) | PASS |
| Question length & structural refs | 8–40 words, 1 sentence ending `?`, no structural refs | 16–35 words, 0 structural refs | PASS |
| Gold answer length | 1–2 sentences, ≤60 words | 16–58 words | PASS |
| Opening-word diversity | ≤30% (≤6/20) same first word | Max 3/20 (`under`) | PASS |
| Near-duplicate check | Pairwise content-word Jaccard < 0.60 | Max **0.3529** (`Q115` vs `Q120`) | PASS |
| Automated errors / overlap warnings | 0 errors, 0 overlap warnings (>0.60) | **0 errors, 0 overlap warnings** | PASS |

## 3. Evidence Type × Question Type × High-Overlap Matrix (v2)

| Type | Article only (actual / req, High / min) | Recital only (actual / req, High / min) | Mixed (actual / req, High / min) |
| --- | --- | --- | --- |
| `single_hop` | 4/4 (2/≥2 High) | 1/1 (0/≥0 High) | 0/0 (0/0) |
| `multi_hop` | 3/3 (2/≥1 High) | 0/0 (0/0) | 2/2 (1/≥1 High) |
| `conflicting_or_conditional` | 3/3 (2/≥1 High) | 1/1 (1/≥0 High) | 0/0 (0/0) |
| `numeric_or_table` | 3/3 (1/≥1 High) | 1/1 (1/≥1 High) | 0/0 (0/0) |

## 4. Per-Candidate Audit Table (v2)

| ID | Revised? | Type | Evidence Type | Overlap | Band | Q Words | A Words | Quote Chars | Units |
| --- | --- | --- | --- | ---: | --- | ---: | ---: | --- | --- |
| Q101 | No | `single_hop` | Article only | 0.5833 | High | 19 | 16 | 106 | ai_act:art:64 |
| Q102 | No | `single_hop` | Article only | 0.3846 | High | 20 | 24 | 243 | ai_act:art:84 |
| Q103 | Yes | `single_hop` | Article only | 0.1333 | Low | 23 | 23 | 145 | ai_act:art:35 |
| Q104 | No | `single_hop` | Article only | 0.0000 | Low | 21 | 23 | 137 | ai_act:art:61 |
| Q105 | Yes | `single_hop` | Recital only | 0.0833 | Low | 19 | 31 | 220 | ai_act:rec:97 |
| Q106 | No | `multi_hop` | Article only | 0.5385 | High | 28 | 58 | 262, 269 | ai_act:art:68, ai_act:art:90 |
| Q107 | No | `multi_hop` | Article only | 0.3750 | High | 29 | 55 | 166, 251 | ai_act:art:11, ai_act:art:18 |
| Q108 | Yes | `multi_hop` | Article only | 0.2778 | Low | 28 | 41 | 383, 197 | ai_act:art:88, ai_act:art:92 |
| Q109 | Yes | `multi_hop` | Mixed | 0.4615 | High | 35 | 51 | 400, 260 | ai_act:art:111, ai_act:rec:177 |
| Q110 | Yes | `multi_hop` | Mixed | 0.2222 | Low | 32 | 48 | 207, 448, 319 | ai_act:art:54, ai_act:art:54, ai_act:rec:109 |
| Q111 | No | `conflicting_or_conditional` | Article only | 0.4667 | High | 22 | 44 | 171, 224 | ai_act:art:57, ai_act:art:57 |
| Q112 | Yes | `conflicting_or_conditional` | Article only | 0.5556 | High | 27 | 47 | 263, 110 | ai_act:art:72, ai_act:art:72 |
| Q113 | No | `conflicting_or_conditional` | Article only | 0.2000 | Low | 26 | 39 | 322, 338 | ai_act:art:83, ai_act:art:83 |
| Q114 | Yes | `conflicting_or_conditional` | Recital only | 0.5000 | High | 24 | 41 | 376, 272 | ai_act:rec:78, ai_act:rec:78 |
| Q115 | No | `numeric_or_table` | Article only | 0.3636 | High | 18 | 29 | 181 | ai_act:art:44 |
| Q116 | No | `numeric_or_table` | Article only | 0.1250 | Low | 25 | 30 | 300 | ai_act:art:33 |
| Q117 | No | `numeric_or_table` | Article only | 0.1875 | Low | 22 | 22 | 313 | ai_act:art:81 |
| Q118 | No | `numeric_or_table` | Recital only | 0.4286 | High | 25 | 19 | 214 | ai_act:rec:180 |
| Q119 | Yes | `unanswerable` | None | N/A | N/A | 18 | 34 | — | *(empty — unanswerable)* |
| Q120 | No | `unanswerable` | None | N/A | N/A | 17 | 29 | — | *(empty — unanswerable)* |

## 5. Human Verification Note
- All 20 items remain AI-drafted candidates (`author:ai | human_review:pending`).
- Stopped after Batch 2 v2 revision as instructed.
