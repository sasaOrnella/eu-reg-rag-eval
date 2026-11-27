# Locked Test Blind Generation Verification Report (v3) — Batch `gdpr-01` (Q121–Q138)

- **Generated At:** `2026-11-27T14:21:46.066713+11:00`
- **Protocol Version:** `v3.1-2026-11-27`
- **v3 Output CSV:** `gdpr-01_candidates_v3.csv` (`SHA-256: 62fe32585eccc92a6666cb9a7682b6e2113d87aba1d9f19d0d45bd95a0639952`)
- **v2 Preserved CSV:** `outputs/gdpr-01_v2/gdpr-01_candidates_v2.csv` (`SHA-256: c8ce60e3e798f5bf93b2b28c824f0288acf2ec41b5502b8c0528b52ca43b81d8`)
- **v1 Preserved CSV:** `outputs/gdpr-01/gdpr-01_candidates.csv` (`SHA-256: f5195a8123d70a79edc435c81dfa0d798477e584a872b8aacf3fa12288851888`)
- **Unchanged 17 Questions (Q121–Q137) Integrity Check:** `PASS` (byte-for-byte identical to v2)
- **Exact Joint Quota Match:** `PASS` (18/18 questions; High=6, Low=10, N/A=2; all 13 active cells matched)
- **Hard Rule Errors:** `0` | **Soft Warnings:** `1`
- **Excluded Positive Units Violated:** `0`
- **Positive Evidence Unit Diversity:** `20` unique units across 16 answerable questions (max reuse per unit = `1`, limit ≤ 2 across all batches)
- **Later Articles Coverage (Art. 70–99):** `8` questions (`Q121, Q122, Q123, Q124, Q126, Q129, Q132, Q134`)
- **Max Pairwise Question Jaccard (R-Q7):** `0.3333` (`Q121` vs `Q134`, warning threshold 0.60)
- **Opening Word Variety (R-Q8):** max count = `4/18` (`22.2%`, limit ≤ 30%)

## 1. Exact Joint Quota Verification (`gdpr-01` v3)

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

## 2. Per-Question Evidence, Unrounded Overlap & Rule Audit (v3)

| ID | Status | Type | Evidence Type | Overlap (Exact) | Bucket | Q Words | A Words | Units | Quote Chars | Verbatim Unique |
| --- | --- | --- | --- | ---: | --- | ---: | ---: | --- | --- | --- |
| Q121 | Unchanged (v2) | `single_hop` | `article_only` | 0.5833 | `high` | 19 | 31 | `gdpr:art:76` | 201 | 1/1 exact |
| Q122 | Unchanged (v2) | `single_hop` | `article_only` | 0.3846 | `high` | 21 | 23 | `gdpr:art:74` | 115 | 1/1 exact |
| Q123 | Unchanged (v2) | `single_hop` | `article_only` | 0.0909 | `low` | 18 | 25 | `gdpr:art:98` | 248 | 1/1 exact |
| Q124 | Unchanged (v2) | `single_hop` | `article_only` | 0.0714 | `low` | 18 | 20 | `gdpr:art:94` | 262 | 1/1 exact |
| Q125 | Unchanged (v2) | `single_hop` | `recital_only` | 0.1000 | `low` | 14 | 22 | `gdpr:rec:160` | 159 | 1/1 exact |
| Q126 | Unchanged (v2) | `multi_hop` | `article_only` | 0.5000 | `high` | 26 | 37 | `gdpr:art:5, gdpr:art:89` | 260, 272 | 1/1 exact |
| Q127 | Unchanged (v2) | `multi_hop` | `article_only` | 0.0667 | `low` | 26 | 34 | `gdpr:art:40, gdpr:art:24` | 208, 234 | 1/1 exact |
| Q128 | Unchanged (v2) | `multi_hop` | `article_only` | 0.2500 | `low` | 30 | 50 | `gdpr:art:26, gdpr:art:26, gdpr:art:13` | 118, 500, 332 | 1/1 exact |
| Q129 | Unchanged (v2) | `multi_hop` | `mixed` | 0.4000 | `high` | 23 | 44 | `gdpr:art:85, gdpr:rec:153` | 276, 154 | 1/1 exact |
| Q130 | Unchanged (v2) | `conflicting_or_conditional` | `article_only` | 0.4375 | `high` | 27 | 38 | `gdpr:art:14, gdpr:art:14` | 261, 105 | 1/1 exact |
| Q131 | Unchanged (v2) | `conflicting_or_conditional` | `article_only` | 0.2941 | `low` | 23 | 37 | `gdpr:art:41, gdpr:art:41` | 268, 88 | 1/1 exact |
| Q132 | Unchanged (v2) | `conflicting_or_conditional` | `article_only` | 0.2381 | `low` | 35 | 53 | `gdpr:art:81, gdpr:art:81` | 241, 290 | 1/1 exact |
| Q133 | Unchanged (v2) | `conflicting_or_conditional` | `recital_only` | 0.1875 | `low` | 24 | 39 | `gdpr:rec:63, gdpr:rec:63` | 178, 115 | 1/1 exact |
| Q134 | Unchanged (v2) | `numeric_or_table` | `article_only` | 0.5000 | `high` | 24 | 18 | `gdpr:art:72` | 135 | 1/1 exact |
| Q135 | Unchanged (v2) | `numeric_or_table` | `article_only` | 0.2105 | `low` | 27 | 39 | `gdpr:art:62, gdpr:art:62` | 274, 317 | 1/1 exact |
| Q136 | Unchanged (v2) | `numeric_or_table` | `recital_only` | 0.2500 | `low` | 22 | 24 | `gdpr:rec:171` | 207 | 1/1 exact |
| Q137 | Unchanged (v2) | `unanswerable` | `none` | N/A | `na` | 16 | 28 | `(none)` | — | N/A |
| Q138 | Replaced (v3) | `unanswerable` | `none` | N/A | `na` | 23 | 36 | `(none)` | — | N/A |

## 3. Soft Warnings & Notes

- **Soft Warning:** `Q128: Quote len 500 in gdpr:art:26 outside [25, 400] (hard cap 600)` — Retained unchanged from v2 to preserve the complete verbatim sentence of `gdpr:art:26(1)` without mid-sentence truncation.

## 4. Input & Output SHA-256 Hashes

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
| `outputs/gdpr-01/gdpr-01_candidates.csv` | `f5195a8123d70a79edc435c81dfa0d798477e584a872b8aacf3fa12288851888` |
| `outputs/gdpr-01_v2/gdpr-01_candidates_v2.csv` | `c8ce60e3e798f5bf93b2b28c824f0288acf2ec41b5502b8c0528b52ca43b81d8` |
| `outputs/gdpr-01_v3/gdpr-01_candidates_v3.csv` | `62fe32585eccc92a6666cb9a7682b6e2113d87aba1d9f19d0d45bd95a0639952` |
| `outputs/gdpr-01_v3/gdpr-01_q138_v2_vs_v3_diff.md` | `677614e4d95d9b8797719f25aae24f5aa724665750fca14a7ce1087bb7f9a646` |
