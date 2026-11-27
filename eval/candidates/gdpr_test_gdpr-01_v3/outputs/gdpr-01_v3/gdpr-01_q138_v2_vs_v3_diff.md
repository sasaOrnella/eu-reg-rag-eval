# `gdpr-01` Revision Diff Report — Q138 (v2 → v3)

- **Generated At:** `2026-11-27T14:21:46.066713+11:00`
- **v1 CSV (preserved untouched):** `outputs/gdpr-01/gdpr-01_candidates.csv` (`SHA-256: f5195a8123d70a79edc435c81dfa0d798477e584a872b8aacf3fa12288851888`)
- **v2 CSV (preserved untouched):** `outputs/gdpr-01_v2/gdpr-01_candidates_v2.csv` (`SHA-256: c8ce60e3e798f5bf93b2b28c824f0288acf2ec41b5502b8c0528b52ca43b81d8`)
- **v3 CSV:** `outputs/gdpr-01_v3/gdpr-01_candidates_v3.csv` (`SHA-256: 62fe32585eccc92a6666cb9a7682b6e2113d87aba1d9f19d0d45bd95a0639952`)
- **Modified ID (1):** `Q138`
- **Unchanged IDs (17, byte-for-byte verified identical to v2):** `Q121–Q137`

## Q138 Replacement Details (`unanswerable` | `absence_kind:b`)

- **Reason for Replacement:** Avoid cross-split semantic overlap with legacy question Q048 (mandatory operating/data-broker license & `gdpr:art:42` hard negative). Replaced with an entirely independent, realistic false premise: applying for a statutory whistleblower reward under the GDPR after reporting an employer's violation to a supervisory authority.
- **v2 Question:** What procedure must a private company follow under the GDPR to renew its annual data-processing license with its national supervisory authority?
- **v3 Question:** How does an employee apply under the GDPR for a statutory whistleblower reward after reporting an employer's data-handling violation to a supervisory authority?
- **v2 Gold Answer:** Not specified in the GDPR, which does not create a mandatory annual data-processing license or renewal procedure with supervisory authorities; instead, it abolishes general notification obligations and provides only for voluntary certification and high-risk prior consultation.
- **v3 Gold Answer:** Not specified in the GDPR, which grants data subjects the right to lodge a complaint with a supervisory authority and provides for administrative fines, but creates no statutory whistleblower reward or application procedure for reporting violations.
- **v2 Hard Negative:** `gdpr:art:42`
- **v3 Hard Negative:** `gdpr:art:77`
- **v2 Notes:** `GDPR | absence_kind:b | hard_negative:gdpr:art:42 | search:variants=license, licence, renew, general notification, prior consultation; inspected=gdpr:art:42, gdpr:rec:89, gdpr:art:36, gdpr:art:43; missing=any mandatory annual data-processing license or license-renewal procedure with a national supervisory authority (gdpr:rec:89 explicitly abolishes indiscriminate general notification obligations, gdpr:art:42 and gdpr:art:43 govern voluntary certification and accreditation rather than mandatory operating licenses, and gdpr:art:36 applies only to prior consultation for high-risk processing) | revision:v2_replaced_tribunal_with_fresh_kind_b | author:ai | human_review:pending`
- **v3 Notes:** `GDPR | absence_kind:b | hard_negative:gdpr:art:77 | search:variants=whistleblower, reward, bounty, informant, lodge a complaint; inspected=gdpr:art:77, gdpr:rec:141, gdpr:art:83, gdpr:art:88; missing=any statutory whistleblower reward, financial bounty, or application procedure for employees who report infringements to a supervisory authority (gdpr:art:77 and gdpr:rec:141 cover lodging complaints and judicial remedies, gdpr:art:83 covers administrative fines without informant payouts, and gdpr:art:88 covers employment-context data processing rules) | revision:v3_replaced_license_renewal_with_whistleblower_reward_kind_b | author:ai | human_review:pending`

## Full-Corpus Verification Log for Q138 (v3)

- Searched all 272 units in `data/processed/gdpr.jsonl` across 5 distinct keyword variants:
  - `whistleblow`: 0 hits
  - `reward`: 0 hits
  - `bounty`: 0 hits
  - `informant`: 0 hits
  - `lodge a complaint`: 8 hits (`gdpr:rec:141`, `gdpr:rec:142`, `gdpr:art:13`, `gdpr:art:14`, `gdpr:art:15`, `gdpr:art:47`, `gdpr:art:77`, `gdpr:art:79`)
- Inspected 4 valid GDPR units including the hard negative: `gdpr:art:77` (hard negative — data subject's right to lodge a complaint), `gdpr:rec:141` (complaint handling and judicial remedy), `gdpr:art:83` (administrative fines imposed by supervisory authorities, with no informant payout), and `gdpr:art:88` (processing in the employment context).
- Confirmed genuine absence of any statutory whistleblower reward or application procedure, with natural phrasing and zero giveaway terms.
