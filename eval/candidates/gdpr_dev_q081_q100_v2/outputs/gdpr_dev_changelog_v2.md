# GDPR New Dev (Q081–Q100) Revision Changelog (v1 → v2)

- **Scope**: Targeted revision of **4 items** (`Q082`, `Q087`, `Q097`, `Q100`) based strictly on independent legal/unanswerability review.
- **Unchanged items (16/20)**: `Q081`, `Q083`, `Q084`, `Q085`, `Q086`, `Q088`, `Q089`, `Q090`, `Q091`, `Q092`, `Q093`, `Q094`, `Q095`, `Q096`, `Q098`, `Q099` — programmatically verified **100% identical** across all 7 CSV columns to `outputs/gdpr_dev_candidates.csv`.
- **Preserved v1 files**: `outputs/gdpr_dev_candidates.csv`, `outputs/generation_metadata.json`, and `outputs/gdpr_dev_check_report.md` remain untouched for side-by-side comparison.

## Item-by-Item Changes

### Q082 (`single_hop`, Article only)
- **Reason**: Replace imprecise term `EU institution` with `EU body` (the European Data Protection Supervisor is an independent EU body/authority, not one of the EU Treaty institutions).
- **Before (`question`)**: `Which EU institution provides the secretariat for the European Data Protection Board under the GDPR?`
- **After (`question`)**: `Which EU body provides the secretariat for the European Data Protection Board under the GDPR?`
- **Other fields**: `gold_answer`, `gold_evidence`, `notes` unchanged. Overlap remains `0.5556` (High).

### Q087 (`multi_hop`, Article only)
- **Reason**: Account for the Article 56(2) local-only derogation by scoping the question to cross-border processing that substantially affects people in multiple EU countries (where the local-only derogation does not apply) and aligning `gold_answer` strictly with Article 56(1) (`is competent to act as lead supervisory authority`) so the two quoted passages (`gdpr:art:56` and `gdpr:art:60`) fully support the entire answer without overstating.
- **Before (`question`)**: `Which supervisory authority leads a cross-border processing case under the GDPR, and what must it share with other concerned authorities before deciding?`
- **After (`question`)**: `For cross-border processing that substantially affects people in multiple EU countries under the GDPR, which supervisory authority is competent to act as lead regulator, and what must it share with other concerned authorities before deciding?`
- **Before (`gold_answer`)**: `The supervisory authority of the controller's or processor's main or single establishment acts as lead supervisory authority. It must submit a draft decision without delay to the other supervisory authorities concerned for their opinion and take due account of their views.`
- **After (`gold_answer`)**: `The supervisory authority of the controller's or processor's main or single establishment is competent to act as lead supervisory authority for that cross-border processing. It must submit a draft decision without delay to the other supervisory authorities concerned for their opinion and take due account of their views.`
- **Other fields**: `gold_evidence`, `notes` unchanged. Overlap changed from `0.5714` to `0.5000` (remains High, ≤0.60).

### Q097 (`numeric_or_table`, Article only)
- **Reason**: Replace ambiguous phrase `EU data protection advisory panel` with explicit statutory name `European Data Protection Board`.
- **Before (`question`)**: `How quickly must the EU data protection advisory panel deliver a consistency review under the GDPR, and what extra time is allowed for complex matters?`
- **After (`question`)**: `How quickly must the European Data Protection Board deliver a consistency review under the GDPR, and what extra time is allowed for complex matters?`
- **Other fields**: `gold_answer`, `gold_evidence`, `notes` unchanged. Overlap changed from `0.0000` to `0.0714` (remains Low, <0.30).

### Q100 (`unanswerable`)
- **Reason**: Previous question about the French CNIL could arguably be partially answered by general GDPR provisions on Member State supervisory authorities. Replaced with a natural legal-compliance question whose topic (corporate tax deductibility of GDPR administrative fines) is completely outside the GDPR (`absence_kind:a`), independently verified across 6 keyword groups in the full `gdpr.jsonl` corpus.
- **Before (`question`)**: `What enforcement responsibilities does the GDPR assign to the French CNIL in cross-border investigations?`
- **After (`question`)**: `How does the GDPR determine whether administrative fines paid by corporate controllers are tax-deductible?`
- **Before (`gold_answer`)**: `Not specified in the GDPR; the regulation sets general rules for Member State supervisory authorities and never names the French CNIL.`
- **After (`gold_answer`)**: `Not specified in the GDPR; the regulation governs the imposition of administrative fines and penalties but does not address their tax deductibility.`
- **Before (`notes`)**: `GDPR | author:ai | human_review:pending | absence_kind:c | hard_negative:gdpr:art:56 | search:checked 'CNIL'(0), 'French'(0), 'France'(0), 'Commission nationale'(0); inspected gdpr:art:56, gdpr:art:60, gdpr:art:62`
- **After (`notes`)**: `GDPR | author:ai | human_review:pending | absence_kind:a | hard_negative:gdpr:art:83 | search:checked 'deduct'(0), 'fiscal'(0), 'accounting'(0), 'corporate tax'(0), 'tax'(3: gdpr:rec:31, gdpr:rec:71, gdpr:rec:112), 'taxation'(1: gdpr:art:23); inspected gdpr:art:83, gdpr:art:84, gdpr:rec:148 and tax mentions — none addresses tax deductibility of fines`
- **Absence verification details**: Searched full `gdpr.jsonl` (all 272 units, including excluded units) for `deduct` (0), `fiscal` (0), `accounting` (0), `corporate tax` (0), `tax` (3: `gdpr:rec:31`, `gdpr:rec:71`, `gdpr:rec:112`), and `taxation` (1: `gdpr:art:23`). Inspected `gdpr:art:83`, `gdpr:art:84`, `gdpr:rec:148` (administrative fines/penalties) and all four tax/taxation mentions (which refer only to tax authorities, tax-evasion monitoring, and public-interest restrictions). None addresses tax deductibility of fines. Recorded `hard_negative:gdpr:art:83`.
