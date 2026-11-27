# Open Issues & Independent Q155 Backup Candidates — Batch `gdpr-02` (v2)

## 1. Open Issues / Reviewer Notes

- **Unmet Quotas / Hard Rule Violations:** `0` (all 13 joint quota cells, 146 excluded-unit checks, verbatim uniqueness, High/Low cutoffs including Q144 High and Q151 Low, and 7-row byte-identity checks pass).
- **Remaining Soft Warning (1):** `Q152` retains the complete 424-character first sentence of `gdpr:art:92(5)` (strictly below the 600-character hard cap) as explicitly requested to preserve the full objection and early non-objection conditions without truncation.

## 2. Q155 (`unanswerable` | `absence_kind:c`) — Three Independent Candidates Summary

All three candidates below test completely independent absent named entities (none referencing Ireland or any EU national supervisory authority) and were verified against all 272 units of `data/processed/gdpr.jsonl`. **Candidate 1 (Amazon Web Services)** is selected for `gdpr-02_candidates_v2.csv`; **Candidates 2 and 3** are provided below as ready-to-swap backups if cross-split screening flags any overlap.

### Candidate 1 (Selected for `gdpr-02_candidates_v2.csv`): Amazon Web Services (Cloud Vendor)
- **Question:** `Does the GDPR grant Amazon Web Services an exemption from cross-border data transfer safeguards for its European cloud regions?`
- **Gold Answer:** `Not specified in the GDPR, which sets general rules and safeguard mechanisms for transfers to third countries and international organisations without naming Amazon Web Services or granting any vendor-specific cloud exemption.`
- **Notes:** `GDPR | absence_kind:c | hard_negative:gdpr:art:46 | search:variants=Amazon, Web Services, cloud, appropriate safeguards; inspected=gdpr:art:46, gdpr:art:44, gdpr:art:45, gdpr:rec:108; missing=any mention of Amazon Web Services or any vendor-specific cloud exemption from cross-border transfer safeguards (gdpr:art:44 states the general transfer principle, gdpr:art:45 covers adequacy decisions, and gdpr:art:46 and gdpr:rec:108 govern appropriate safeguards generically without naming cloud providers) | revision:v2_replaced_irish_dpc_with_independent_named_vendor_kind_c | author:ai | human_review:pending`

### Candidate 2 (Backup A): United States Federal Trade Commission (Non-EU Regulator)
- **Question:** `What joint enforcement powers does the GDPR confer on the United States Federal Trade Commission for cross-border investigations?`
- **Gold Answer:** `Not specified in the GDPR, which directs the Commission and supervisory authorities to develop international cooperation and mutual assistance with third countries generally without naming the United States Federal Trade Commission or conferring powers on it.`
- **Full-Corpus Verification (272 units):** `Federal Trade Commission`: 0 hits; `United States`: 0 hits; `FTC` (whole word): 0 hits; `international cooperation`: 3 hits (`gdpr:rec:101`, `gdpr:rec:116`, `gdpr:art:50`).
- **Notes:** `GDPR | absence_kind:c | hard_negative:gdpr:art:50 | search:variants=Federal Trade Commission, United States, FTC, international cooperation; inspected=gdpr:art:50, gdpr:rec:116, gdpr:art:62, gdpr:rec:101; missing=any mention of the United States Federal Trade Commission or enforcement powers conferred on a named non-EU regulator (gdpr:art:50 and gdpr:rec:116 address international cooperation with third countries generally, while gdpr:art:62 governs joint operations among EU Member State supervisory authorities only) | author:ai | human_review:pending`

### Candidate 3 (Backup B): ISO/IEC 27001 (Named External Security Standard)
- **Question:** `Does the GDPR recognize ISO/IEC 27001 certification as automatically satisfying a controller's data security obligations?`
- **Gold Answer:** `Not specified in the GDPR, which allows adherence to approved GDPR certification mechanisms as an element to demonstrate security compliance without naming ISO/IEC 27001 or treating it as automatic compliance.`
- **Full-Corpus Verification (272 units):** `27001`: 0 hits; `International Organization for Standardization`: 0 hits; `ISO` (whole word): 1 hit (`gdpr:art:43`, citing `EN-ISO/IEC 17065/2012` for certification body accreditation, not `ISO/IEC 27001`); `certification mechanism`: 13 hits (`gdpr:art:32`, `gdpr:art:42`, etc.).
- **Notes:** `GDPR | absence_kind:c | hard_negative:gdpr:art:32 | search:variants=ISO, 27001, International Organization for Standardization, certification mechanism; inspected=gdpr:art:32, gdpr:art:42, gdpr:art:43, gdpr:rec:100; missing=any mention of ISO/IEC 27001 or automatic satisfaction of security obligations through it (gdpr:art:32(3) and gdpr:art:42 only allow approved GDPR certification mechanisms as an element to demonstrate compliance, and gdpr:art:43 cites EN-ISO/IEC 17065/2012 solely for accrediting certification bodies) | author:ai | human_review:pending`
