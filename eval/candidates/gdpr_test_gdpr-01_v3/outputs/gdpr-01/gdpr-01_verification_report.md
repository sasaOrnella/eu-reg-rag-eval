# Locked Test Blind Generation Verification Report — Batch `gdpr-01` (Q121–Q138)

- **Generated At:** `2026-11-27T12:48:01.976881+11:00`
- **Protocol Version:** `v3.1-2026-11-27`
- **Output CSV:** `gdpr-01_candidates.csv` (`SHA-256: f5195a8123d70a79edc435c81dfa0d798477e584a872b8aacf3fa12288851888`)
- **Exact Joint Quota Match:** `PASS` (18/18 questions; High=6, Low=10, N/A=2)
- **Hard Rule Errors:** `0` | **Soft Warnings:** `0`
- **Excluded Positive Units Violated:** `0`
- **Positive Evidence Unit Diversity:** `20` unique units across 16 answerable questions (max reuse per unit = `1`, limit ≤ 2 across all batches)
- **Later Articles Coverage (Art. 70–99):** `8` questions (`Q121, Q122, Q123, Q124, Q126, Q129, Q132, Q134`)
- **Max Pairwise Question Jaccard (R-Q7):** `0.3333` (`Q121` vs `Q134`, warning threshold 0.60)
- **Opening Word Variety (R-Q8):** max count = `4/18` (`22.2%`, limit ≤ 30%)

## 1. Exact Joint Quota Verification (`gdpr-01`)

| Type | Evidence Type | Overlap | Target | Actual | Status |
| --- | --- | --- | ---: | ---: | --- |
| `conflicting_or_conditional` | `article_only` | `high` | 1 | 1 | PASS |
| `conflicting_or_conditional` | `article_only` | `low` | 2 | 2 | PASS |
| `conflicting_or_conditional` | `recital_only` | `low` | 1 | 1 | PASS |
| `multi_hop` | `article_only` | `high` | 1 | 1 | PASS |
| `multi_hop` | `article_only` | `low` | 2 | 2 | PASS |
| `multi_hop` | `mixed` | `high` | 1 | 1 | PASS |
| `numeric_or_table` | `article_only` | `high` | 1 | 1 | PASS |
| `numeric_or_table` | `article_only` | `low` | 1 | 1 | PASS |
| `numeric_or_table` | `recital_only` | `low` | 1 | 1 | PASS |
| `single_hop` | `article_only` | `high` | 2 | 2 | PASS |
| `single_hop` | `article_only` | `low` | 2 | 2 | PASS |
| `single_hop` | `recital_only` | `low` | 1 | 1 | PASS |
| `unanswerable` | `none` | `na` | 2 | 2 | PASS |

## 2. Per-Question Evidence, Overlap & Rule Audit

| ID | Type | Evidence Type | Overlap (Exact) | Bucket | Q Words | A Words | Units | Quote Chars | Verbatim Unique |
| --- | --- | --- | ---: | --- | ---: | ---: | --- | --- | --- |
| Q121 | `single_hop` | `article_only` | 0.5833 | `high` | 19 | 31 | `gdpr:art:76` | 201 | 1/1 exact |
| Q122 | `single_hop` | `article_only` | 0.3846 | `high` | 21 | 23 | `gdpr:art:74` | 115 | 1/1 exact |
| Q123 | `single_hop` | `article_only` | 0.0909 | `low` | 18 | 25 | `gdpr:art:98` | 248 | 1/1 exact |
| Q124 | `single_hop` | `article_only` | 0.0714 | `low` | 18 | 20 | `gdpr:art:94` | 262 | 1/1 exact |
| Q125 | `single_hop` | `recital_only` | 0.1000 | `low` | 14 | 22 | `gdpr:rec:160` | 159 | 1/1 exact |
| Q126 | `multi_hop` | `article_only` | 0.5000 | `high` | 26 | 37 | `gdpr:art:5, gdpr:art:89` | 260, 272 | 1/1 exact |
| Q127 | `multi_hop` | `article_only` | 0.0667 | `low` | 26 | 34 | `gdpr:art:40, gdpr:art:24` | 208, 234 | 1/1 exact |
| Q128 | `multi_hop` | `article_only` | 0.2500 | `low` | 30 | 33 | `gdpr:art:26, gdpr:art:13` | 341, 332 | 1/1 exact |
| Q129 | `multi_hop` | `mixed` | 0.4000 | `high` | 23 | 44 | `gdpr:art:85, gdpr:rec:153` | 276, 154 | 1/1 exact |
| Q130 | `conflicting_or_conditional` | `article_only` | 0.4375 | `high` | 27 | 38 | `gdpr:art:14, gdpr:art:14` | 261, 105 | 1/1 exact |
| Q131 | `conflicting_or_conditional` | `article_only` | 0.0833 | `low` | 19 | 33 | `gdpr:art:41, gdpr:art:41` | 268, 88 | 1/1 exact |
| Q132 | `conflicting_or_conditional` | `article_only` | 0.1579 | `low` | 31 | 44 | `gdpr:art:81, gdpr:art:81` | 241, 290 | 1/1 exact |
| Q133 | `conflicting_or_conditional` | `recital_only` | 0.1429 | `low` | 24 | 34 | `gdpr:rec:63, gdpr:rec:63` | 178, 115 | 1/1 exact |
| Q134 | `numeric_or_table` | `article_only` | 0.5000 | `high` | 24 | 18 | `gdpr:art:72` | 135 | 1/1 exact |
| Q135 | `numeric_or_table` | `article_only` | 0.0556 | `low` | 27 | 26 | `gdpr:art:62` | 317 | 1/1 exact |
| Q136 | `numeric_or_table` | `recital_only` | 0.1333 | `low` | 22 | 24 | `gdpr:rec:171` | 207 | 1/1 exact |
| Q137 | `unanswerable` | `none` | N/A | `na` | 16 | 26 | `(none)` | — | N/A |
| Q138 | `unanswerable` | `none` | N/A | `na` | 23 | 37 | `(none)` | — | N/A |

## 3. Input & Output SHA-256 Hashes

### Inputs (Verified against `SHA256SUMS.txt`)

| File | SHA-256 |
| --- | --- |
| `blind_generation_spec.md` | `0026a2fdeb96f9b9446c3252f6f70d9afb24464e6744cc99b7c9a41a8f083026` |
| `question_rules.md` | `7381a76b2bc6957d8b74f374f178a81d61b00a3e6f2fd44e3d30c0515b77b606` |
| `locked_test_batch_schedule_v3_1.csv` | `e698303c4fbe3621c599cc1b5c936ce3a3918e43456d52f62ddc0f1c87490ad5` |
| `locked_test_quotas_v3.json` | `e8f2fde72b36298e030c416bc090e86d95db1afbdde7fcf6616b1f9ba0c2cc4c` |
| `excluded_evidence_units.csv` | `3fcf07f78552030cf4c30775ea6b97cd6100dda1e6d879a51051143bce059d26` |
| `data/processed/gdpr.jsonl` | `e8bbb70c2be3890d8f8307ad26cf583c9b41b17b291094851913806ac3de0df6` |
| `data/raw/gdpr.html` | `fde27ea4627c51465d51a45268c18f05ed772ab0163382ca34ed3e83d9f98126` |
| `SHA256SUMS.txt` | `5040c043365b7eb38ce9cc242e8596d097f5be66fef8f2c99ac1a47c45ceba9c` |

### Output

- `gdpr-01_candidates.csv`: `f5195a8123d70a79edc435c81dfa0d798477e584a872b8aacf3fa12288851888`
