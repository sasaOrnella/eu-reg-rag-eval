# Locked Test Blind Generation Final Verification Report (v3) — Batch `gdpr-02` (Q139–Q156)

- **Generated At:** `2026-11-27T17:19:47.720740+11:00`
- **Protocol Version:** `v3.1-2026-11-27`
- **v3 Output CSV:** `gdpr-02_candidates_v3.csv` (`SHA-256: 2b5f3d3684a3296f67576c5333e04bdb866ad597163aba7f258a8b784c135820`)
- **v2 Preserved CSV:** `outputs/gdpr-02_v2/gdpr-02_candidates_v2.csv` (`SHA-256: 10c6a72fdb18cb066ebe43a4214978c16b523d4c950282a3928a13c2b619b194`)
- **v1 Preserved CSV:** `outputs/gdpr-02/gdpr-02_candidates.csv` (`SHA-256: 3209ae7bd21846879e834aef58b4680f26912cd3b9d7dd2f8294227b57dfce4d`)
- **Unchanged 14 Questions Integrity Check:** `PASS` (byte-for-byte identical to v2)
- **Exact Joint Quota Match:** `PASS` (18/18 questions; High=5, Low=11, N/A=2; all 13 active cells matched)
- **Hard Rule Errors:** `0` | **Soft Warnings:** `1`
- **Excluded Positive Units Violated (out of 146):** `0`
- **Positive Evidence Unit Diversity:** `20` unique units across 16 answerable questions (max reuse per unit = `1`, limit ≤ 2 across all batches)
- **Later Articles Coverage (Art. 70–99):** `8` questions (`Q139, Q140, Q141, Q144, Q145, Q147, Q152, Q153`)
- **Max Pairwise Question Jaccard (R-Q7):** `0.1429` (`Q140` vs `Q151`, warning threshold 0.60)
- **Opening Word Variety (R-Q8):** max count = `4/18` (`22.2%`, limit ≤ 30%)

## 1. Exact Joint Quota Verification (`gdpr-02` v3)

| Type | Evidence Type | Overlap | Target | Actual | Status |
| --- | --- | --- | ---: | ---: | --- |
| `conflicting_or_conditional` | `article_only` | `high` | 1 | 1 | PASS |
| `conflicting_or_conditional` | `article_only` | `low` | 2 | 2 | PASS |
| `conflicting_or_conditional` | `recital_only` | `low` | 1 | 1 | PASS |
| `multi_hop` | `article_only` | `high` | 1 | 1 | PASS |
| `multi_hop` | `article_only` | `low` | 2 | 2 | PASS |
| `multi_hop` | `mixed` | `high` | 1 | 1 | PASS |
| `numeric_or_table` | `article_only` | `low` | 2 | 2 | PASS |
| `numeric_or_table` | `recital_only` | `low` | 1 | 1 | PASS |
| `single_hop` | `article_only` | `high` | 1 | 1 | PASS |
| `single_hop` | `article_only` | `low` | 2 | 2 | PASS |
| `single_hop` | `recital_only` | `high` | 1 | 1 | PASS |
| `single_hop` | `recital_only` | `low` | 1 | 1 | PASS |
| `unanswerable` | `none` | `na` | 2 | 2 | PASS |

## 2. Per-Question Evidence, Unrounded Overlap & Rule Audit (v3)

| ID | Status | Type | Evidence Type | Overlap (Exact) | Bucket | Q Words | A Words | Units | Quote Chars | Verbatim Unique |
| --- | --- | --- | --- | ---: | --- | ---: | ---: | --- | --- | --- |
| Q139 | Unchanged (v2) | `single_hop` | `article_only` | 0.5455 | `high` | 16 | 23 | `gdpr:art:71` | 313 | 1/1 exact |
| Q140 | Unchanged (v2) | `single_hop` | `article_only` | 0.0000 | `low` | 21 | 35 | `gdpr:art:87` | 382 | 1/1 exact |
| Q141 | Unchanged (v2) | `single_hop` | `article_only` | 0.1667 | `low` | 25 | 41 | `gdpr:art:95` | 376 | 1/1 exact |
| Q142 | Unchanged (v2) | `single_hop` | `recital_only` | 0.4615 | `high` | 21 | 40 | `gdpr:rec:33` | 327 | 1/1 exact |
| Q143 | Unchanged (v2) | `single_hop` | `recital_only` | 0.0909 | `low` | 21 | 38 | `gdpr:rec:162` | 260 | 1/1 exact |
| Q144 | Modified (v3) | `multi_hop` | `article_only` | 0.4706 | `high` | 29 | 45 | `gdpr:art:67, gdpr:art:67, gdpr:art:93` | 231, 115, 99 | 1/1 exact |
| Q145 | Unchanged (v2) | `multi_hop` | `article_only` | 0.0667 | `low` | 27 | 41 | `gdpr:art:70, gdpr:art:69` | 129, 240 | 1/1 exact |
| Q146 | Unchanged (v2) | `multi_hop` | `article_only` | 0.1765 | `low` | 27 | 38 | `gdpr:art:47, gdpr:art:63` | 140, 257 | 1/1 exact |
| Q147 | Unchanged (v2) | `multi_hop` | `mixed` | 0.4000 | `high` | 27 | 58 | `gdpr:art:91, gdpr:rec:165` | 324, 202 | 1/1 exact |
| Q148 | Unchanged (v2) | `conflicting_or_conditional` | `article_only` | 0.5000 | `high` | 30 | 52 | `gdpr:art:57, gdpr:art:57` | 159, 353 | 1/1 exact |
| Q149 | Modified (v3) | `conflicting_or_conditional` | `article_only` | 0.1739 | `low` | 34 | 52 | `gdpr:art:49, gdpr:art:49` | 397, 384 | 1/1 exact |
| Q150 | Unchanged (v2) | `conflicting_or_conditional` | `article_only` | 0.2667 | `low` | 26 | 49 | `gdpr:art:25, gdpr:art:25` | 209, 177 | 1/1 exact |
| Q151 | Unchanged (v2) | `conflicting_or_conditional` | `recital_only` | 0.2105 | `low` | 26 | 49 | `gdpr:rec:48, gdpr:rec:48` | 295, 153 | 1/1 exact |
| Q152 | Modified (v3) | `numeric_or_table` | `article_only` | 0.0952 | `low` | 34 | 54 | `gdpr:art:92, gdpr:art:92` | 424, 109 | 1/1 exact |
| Q153 | Unchanged (v2) | `numeric_or_table` | `article_only` | 0.1875 | `low` | 25 | 26 | `gdpr:art:99, gdpr:art:99` | 143, 35 | 1/1 exact |
| Q154 | Unchanged (v2) | `numeric_or_table` | `recital_only` | 0.0000 | `low` | 21 | 13 | `gdpr:rec:172` | 163 | 1/1 exact |
| Q155 | Modified (v3) | `unanswerable` | `none` | N/A | `na` | 24 | 36 | `(none)` | — | N/A |
| Q156 | Unchanged (v2) | `unanswerable` | `none` | N/A | `na` | 23 | 40 | `(none)` | — | N/A |

## 3. Targeted Legal & Necessity Audit of the 4 Revised Questions

- **Q144 (`multi_hop` × `article_only` × `high`):** Trimmed `gdpr:art:67` quote 1 to 230 chars (removing the standardised-format example); `gdpr:art:67` supplies the implementing-act instrument and cross-reference to the examination procedure, while `gdpr:art:93(2)` supplies `Article 5 of Regulation (EU) No 182/2011`. Removing either unit makes a complete answer impossible.
- **Q149 (`conflicting_or_conditional` × `article_only` × `low`):** Question asks both (1) statutory open-consultation and particular-case consultation conditions (strictly requiring `gdpr:art:49(1)(g)`) and (2) restrictions on transferring entire datasets/categories and legitimate-interest recipient conditions (strictly requiring `gdpr:art:49(2)`). Neither quote can be dropped.
- **Q152 (`numeric_or_table` × `article_only` × `low`):** Accurately frames `shall enter into force only if` as a necessary condition (not an automatic guarantee), scoped to GDPR delegated acts under `Article 12(8)` and `Article 43(8)` (with zero article numbers in the question text), preserving the complete 424-char and 109-char verbatim sentences of `gdpr:art:92(5)`.
- **Q155 (`unanswerable` | `absence_kind:c`):** Eliminates any EU-internal transfer ambiguity by specifying transfers to Amazon Web Services facilities located in a **third country** and asking whether the GDPR establishes a dedicated vendor exemption or special arrangement. Re-verified `gdpr:art:44`, `gdpr:art:45`, `gdpr:art:46`, and `gdpr:art:49` in full: all govern general third-country transfer rules/safeguards/derogations without naming AWS.

## 4. Input & Output SHA-256 Hashes

| File | SHA-256 |
| --- | --- |
| `blind_generation_spec.md` | `5845463bd36637c4ecdbf35a8bca3feab422fdde6878f5ef8a736cd32b56c869` |
| `question_rules.md` | `7381a76b2bc6957d8b74f374f178a81d61b00a3e6f2fd44e3d30c0515b77b606` |
| `locked_test_batch_schedule_v3_1.csv` | `e698303c4fbe3621c599cc1b5c936ce3a3918e43456d52f62ddc0f1c87490ad5` |
| `locked_test_quotas_v3.json` | `e8f2fde72b36298e030c416bc090e86d95db1afbdde7fcf6616b1f9ba0c2cc4c` |
| `excluded_evidence_units.csv` | `eeb00d51afc4b964da144714f9fee84cb2fe724e28805fb045f3da983cc2523b` |
| `data/processed/gdpr.jsonl` | `e8bbb70c2be3890d8f8307ad26cf583c9b41b17b291094851913806ac3de0df6` |
| `data/raw/gdpr.html` | `fde27ea4627c51465d51a45268c18f05ed772ab0163382ca34ed3e83d9f98126` |
| `SHA256SUMS.txt` | `3533ac99d18595bfd5cf7877cba040d369a68b1c5b9ad35aa40417648d75e93e` |
| `outputs/gdpr-02/gdpr-02_candidates.csv` | `3209ae7bd21846879e834aef58b4680f26912cd3b9d7dd2f8294227b57dfce4d` |
| `outputs/gdpr-02_v2/gdpr-02_candidates_v2.csv` | `10c6a72fdb18cb066ebe43a4214978c16b523d4c950282a3928a13c2b619b194` |
| `outputs/gdpr-02_v3/gdpr-02_candidates_v3.csv` | `2b5f3d3684a3296f67576c5333e04bdb866ad597163aba7f258a8b784c135820` |
| `outputs/gdpr-02_v3/gdpr-02_v2_vs_v3_diff.md` | `5c27f391cb8537accbe96173e063cd01b814b221125dad78f81129703bba4467` |
