# Locked Test Blind Generation Verification Report (v2) — Batch `gdpr-01` (Q121–Q138)

- **Generated At:** `2026-11-27T13:31:21.057594+11:00`
- **Protocol Version:** `v3.1-2026-11-27`
- **v2 Output CSV:** `gdpr-01_candidates_v2.csv` (`SHA-256: c8ce60e3e798f5bf93b2b28c824f0288acf2ec41b5502b8c0528b52ca43b81d8`)
- **v1 Preserved CSV:** `outputs/gdpr-01/gdpr-01_candidates.csv` (`SHA-256: f5195a8123d70a79edc435c81dfa0d798477e584a872b8aacf3fa12288851888`)
- **Unchanged 10 Questions Integrity Check:** `PASS` (byte-for-byte identical to v1)
- **Exact Joint Quota Match:** `PASS` (18/18 questions; High=6, Low=10, N/A=2; all 13 active cells matched)
- **Hard Rule Errors:** `0` | **Soft Warnings:** `1`
- **Excluded Positive Units Violated:** `0`
- **Positive Evidence Unit Diversity:** `20` unique units across 16 answerable questions (max reuse per unit = `1`, limit ≤ 2 across all batches)
- **Later Articles Coverage (Art. 70–99):** `8` questions (`Q121, Q122, Q123, Q124, Q126, Q129, Q132, Q134`)
- **Max Pairwise Question Jaccard (R-Q7):** `0.3333` (`Q121` vs `Q134`, warning threshold 0.60)
- **Opening Word Variety (R-Q8):** max count = `4/18` (`22.2%`, limit ≤ 30%)

## 1. Exact Joint Quota Verification (`gdpr-01` v2)

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

## 2. Per-Question Evidence, Unrounded Overlap & Rule Audit (v2)

| ID | Status | Type | Evidence Type | Overlap (Exact) | Bucket | Q Words | A Words | Units | Quote Chars | Verbatim Unique |
| --- | --- | --- | --- | ---: | --- | ---: | ---: | --- | --- | --- |
| Q121 | Unchanged (v1) | `single_hop` | `article_only` | 0.5833 | `high` | 19 | 31 | `gdpr:art:76` | 201 | 1/1 exact |
| Q122 | Unchanged (v1) | `single_hop` | `article_only` | 0.3846 | `high` | 21 | 23 | `gdpr:art:74` | 115 | 1/1 exact |
| Q123 | Unchanged (v1) | `single_hop` | `article_only` | 0.0909 | `low` | 18 | 25 | `gdpr:art:98` | 248 | 1/1 exact |
| Q124 | Unchanged (v1) | `single_hop` | `article_only` | 0.0714 | `low` | 18 | 20 | `gdpr:art:94` | 262 | 1/1 exact |
| Q125 | Unchanged (v1) | `single_hop` | `recital_only` | 0.1000 | `low` | 14 | 22 | `gdpr:rec:160` | 159 | 1/1 exact |
| Q126 | Unchanged (v1) | `multi_hop` | `article_only` | 0.5000 | `high` | 26 | 37 | `gdpr:art:5, gdpr:art:89` | 260, 272 | 1/1 exact |
| Q127 | Unchanged (v1) | `multi_hop` | `article_only` | 0.0667 | `low` | 26 | 34 | `gdpr:art:40, gdpr:art:24` | 208, 234 | 1/1 exact |
| Q128 | Modified (v2) | `multi_hop` | `article_only` | 0.2500 | `low` | 30 | 50 | `gdpr:art:26, gdpr:art:26, gdpr:art:13` | 118, 500, 332 | 1/1 exact |
| Q129 | Unchanged (v1) | `multi_hop` | `mixed` | 0.4000 | `high` | 23 | 44 | `gdpr:art:85, gdpr:rec:153` | 276, 154 | 1/1 exact |
| Q130 | Unchanged (v1) | `conflicting_or_conditional` | `article_only` | 0.4375 | `high` | 27 | 38 | `gdpr:art:14, gdpr:art:14` | 261, 105 | 1/1 exact |
| Q131 | Modified (v2) | `conflicting_or_conditional` | `article_only` | 0.2941 | `low` | 23 | 37 | `gdpr:art:41, gdpr:art:41` | 268, 88 | 1/1 exact |
| Q132 | Modified (v2) | `conflicting_or_conditional` | `article_only` | 0.2381 | `low` | 35 | 53 | `gdpr:art:81, gdpr:art:81` | 241, 290 | 1/1 exact |
| Q133 | Modified (v2) | `conflicting_or_conditional` | `recital_only` | 0.1875 | `low` | 24 | 39 | `gdpr:rec:63, gdpr:rec:63` | 178, 115 | 1/1 exact |
| Q134 | Unchanged (v1) | `numeric_or_table` | `article_only` | 0.5000 | `high` | 24 | 18 | `gdpr:art:72` | 135 | 1/1 exact |
| Q135 | Modified (v2) | `numeric_or_table` | `article_only` | 0.2105 | `low` | 27 | 39 | `gdpr:art:62, gdpr:art:62` | 274, 317 | 1/1 exact |
| Q136 | Modified (v2) | `numeric_or_table` | `recital_only` | 0.2500 | `low` | 22 | 24 | `gdpr:rec:171` | 207 | 1/1 exact |
| Q137 | Modified (v2) | `unanswerable` | `none` | N/A | `na` | 16 | 28 | `(none)` | — | N/A |
| Q138 | Modified (v2) | `unanswerable` | `none` | N/A | `na` | 21 | 36 | `(none)` | — | N/A |

## 3. Soft Warnings & Notes

- **Soft Warning:** `Q128: Quote len 500 in gdpr:art:26 outside [25, 400] (hard cap 600)` — Necessary to retain the complete verbatim sentence of `gdpr:art:26(1)` containing both the allocation-by-arrangement rule and the Union/Member State law exception without mid-sentence truncation (strictly under the 600-character hard cap).

## 4. Unanswerable Items Freshness & Corpus Verification (Q137, Q138)

- **Q137 (`absence_kind:a` — Data-center energy-efficiency / carbon-emission standards):** Completely replaces the v1 cyber-insurance topic. Searched all 272 units in `data/processed/gdpr.jsonl` across 5 variants (`energy`: 0 hits, `carbon`: 0 hits, `emission`: 0 hits, `data center`: 0 hits, `environment`: 2 hits in non-environmental contexts `gdpr:rec:66` and `gdpr:rec:92`). Inspected `gdpr:art:32` (hard negative), `gdpr:art:25`, `gdpr:rec:66`, and `gdpr:rec:92`. Natural real-world compliance question with zero giveaway words.
- **Q138 (`absence_kind:b` — Annual data-processing license renewal with national supervisory authority):** Completely replaces the v1 fictional tribunal topic. Searched all 272 units in `data/processed/gdpr.jsonl` across 5 variants (`license`/`licence`: 0 hits, `renew`: 3 hits in `gdpr:art:42`, `gdpr:art:43`, `gdpr:art:73`, `general notification`: 1 hit in `gdpr:rec:89`, `prior consultation`: 3 hits). Inspected `gdpr:art:42` (hard negative), `gdpr:rec:89`, `gdpr:art:36`, and `gdpr:art:43`. Grounded in a realistic misconception (pre-GDPR national DPA registrations vs. GDPR abolition of general notification obligations).

## 5. Input & Output SHA-256 Hashes

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
| `outputs/gdpr-01_v2/gdpr-01_v1_vs_v2_diff.md` | `93d383177b4d3860ca6a621a726fb5e18a0d00052ff28d92ed2730835fd8c17d` |
