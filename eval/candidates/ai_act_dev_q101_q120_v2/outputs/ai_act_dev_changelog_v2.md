# EU AI Act New Dev (Q101–Q120) Revision Changelog (v1 → v2)

- **Scope**: Targeted revision of **8 items** (`Q103`, `Q105`, `Q108`, `Q109`, `Q110`, `Q112`, `Q114`, `Q119`).
- **Unchanged items (12/20)**: `Q101`, `Q102`, `Q104`, `Q106`, `Q107`, `Q111`, `Q113`, `Q115`, `Q116`, `Q117`, `Q118`, `Q120` — programmatically verified **100% identical** across all 7 CSV columns to `outputs/ai_act_dev_candidates.csv`.
- **Preserved v1 files**: `outputs/ai_act_dev_candidates.csv`, `outputs/ai_act_dev_check_report.md`, `outputs/ai_act_dev_generation_metadata.json`, and all accepted GDPR files remain untouched.

## Item-by-Item Diff

### Q103 (`single_hop`)
- **Reason**: Distinguished notified-body `notification` from `accreditation` and replaced `registration codes` with the exact statutory term `identification numbers`.
- **Lexical Overlap**: `0.1250` → `0.1333`
- **Before (`question`)**: `When an assessment organisation receives accreditation across several European laws, how many registration codes does the Commission issue under the EU AI Act?`
- **After (`question`)**: `If a conformity assessment organisation undergoes notification under multiple European laws, how many identification numbers does it receive under the EU AI Act?`

### Q105 (`single_hop`)
- **Reason**: Replaced `complete software application` with `AI system` to match the exact conceptual distinction discussed in Recital 97 (`ai_act:rec:97`).
- **Lexical Overlap**: `0.0714` → `0.0833`
- **Before (`question`)**: `Why does a standalone machine-learning model fall short of qualifying as a complete software application under the EU AI Act?`
- **After (`question`)**: `Why does a standalone machine-learning model fall short of qualifying as an AI system under the EU AI Act?`

### Q108 (`multi_hop`)
- **Reason**: Replaced `foundation-model rules` with `general-purpose AI model obligations` and added `supervisory and enforcement` to accurately bound the Commission's exclusive Chapter V powers.
- **Lexical Overlap**: `0.1875` → `0.2778`
- **Before (`question`)**: `Who holds sole enforcement authority over foundation-model rules under the EU AI Act, and through what software channels can that enforcer inspect a model?`
- **After (`question`)**: `Who holds sole supervisory and enforcement authority over general-purpose AI model obligations under the EU AI Act, and through what software channels can that enforcer inspect a model?`

### Q109 (`multi_hop`)
- **Reason**: Scoped explicitly to exclude prohibited AI practices (`Without prejudice to the application of Article 5`), large-scale IT components (Art 111(1)), and public-authority systems (Art 111(2) second sentence), and expanded the `ai_act:art:111` quote to include the `Without prejudice to the application of Article 5` clause verbatim (400 chars) so Gold Evidence fully supports the complete answer.
- **Lexical Overlap**: `0.5882` → `0.4615`
- **Before (`question`)**: `When do private-sector high-risk AI systems already launched before 2 August 2026 fall under the EU AI Act, and how is 'significant change' understood?`
- **After (`question`)**: `Aside from prohibited AI practices, when do non-public-authority high-risk AI systems (other than large-scale IT components) already launched before 2 August 2026 become subject to the EU AI Act, and how is 'significant change' understood?`
- **Before (`gold_answer`)**: `Non-public-authority high-risk AI systems (other than large-scale IT components) placed on the market before 2 August 2026 become subject to the EU AI Act only if they undergo significant changes in their designs from that date. The concept of significant change is understood as equivalent in substance to substantial modification.`
- **After (`gold_answer`)**: `Without prejudice to the EU AI Act's prohibited AI practices, operators of covered pre-2 August 2026 high-risk AI systems become subject to the regulation only if those systems undergo significant changes in their designs from that date. The concept of significant change is understood as equivalent in substance to substantial modification.`
- **Before (`gold_evidence`)**: `ai_act:art:111::this Regulation shall apply to operators of high-risk AI systems, other than the systems referred to in paragraph 1 of this Article, that have been placed on the market or put into service before 2 August 2026, only if, as from that date, those systems are subject to significant changes in their designs. || ai_act:rec:177::It is appropriate to clarify that, in this respect, the concept of significant change should be understood as equivalent in substance to the notion of substantial modification, which is used with regard only to high-risk AI systems pursuant to this Regulation.`
- **After (`gold_evidence`)**: `ai_act:art:111::Without prejudice to the application of Article 5 as referred to in Article 113(3), point (a), this Regulation shall apply to operators of high-risk AI systems, other than the systems referred to in paragraph 1 of this Article, that have been placed on the market or put into service before 2 August 2026, only if, as from that date, those systems are subject to significant changes in their designs. || ai_act:rec:177::It is appropriate to clarify that, in this respect, the concept of significant change should be understood as equivalent in substance to the notion of substantial modification, which is used with regard only to high-risk AI systems pursuant to this Regulation.`

### Q110 (`multi_hop`)
- **Reason**: Added Article 54(6) verbatim as a required Gold Evidence piece and updated both question and gold answer to cover the free and open-source GPAI authorised-representative exemption and its systemic-risk carve-out alongside Recital 109's fine-tuning scope.
- **Lexical Overlap**: `0.1579` → `0.2222`
- **Before (`question`)**: `When an overseas developer fine-tunes a foundation model for European release under the EU AI Act, what local representation step is needed, and how far do its provider duties extend?`
- **After (`question`)**: `When an overseas developer fine-tunes a foundation model for European release under the EU AI Act, when is an EU representative required or exempted, and how far do its provider duties extend?`
- **Before (`gold_answer`)**: `Before placing the general-purpose AI model on the Union market, a third-country provider must appoint an authorised representative established in the Union by written mandate. Where a model is modified or fine-tuned, the provider's obligations are limited to that modification or fine-tuning, such as complementing existing technical documentation with modification details and new training data sources.`
- **After (`gold_answer`)**: `Third-country providers must appoint an EU authorised representative by written mandate before market placement, except for qualifying free and open-source models with publicly available parameters, architecture, and usage information—unless they present systemic risks. For a modified or fine-tuned model, provider obligations are limited to that modification or fine-tuning.`
- **Before (`gold_evidence`)**: `ai_act:art:54::1. Prior to placing a general-purpose AI model on the Union market, providers established in third countries shall, by written mandate, appoint an authorised representative which is established in the Union. || ai_act:rec:109::In the case of a modification or fine-tuning of a model, the obligations for providers of general-purpose AI models should be limited to that modification or fine-tuning, for example by complementing the already existing technical documentation with information on the modifications, including new training data sources`
- **After (`gold_evidence`)**: `ai_act:art:54::1. Prior to placing a general-purpose AI model on the Union market, providers established in third countries shall, by written mandate, appoint an authorised representative which is established in the Union. || ai_act:art:54::6. The obligation set out in this Article shall not apply to providers of general-purpose AI models that are released under a free and open-source licence that allows for the access, usage, modification, and distribution of the model, and whose parameters, including the weights, the information on the model architecture, and the information on model usage, are made publicly available, unless the general-purpose AI models present systemic risks. || ai_act:rec:109::In the case of a modification or fine-tuning of a model, the obligations for providers of general-purpose AI models should be limited to that modification or fine-tuning, for example by complementing the already existing technical documentation with information on the modifications, including new training data sources`

### Q112 (`conflicting_or_conditional`)
- **Reason**: Revised question and gold answer to clarify that Article 72(2) does not require collecting records from every deployer (data may be provided by deployers or collected through other sources) while retaining the law-enforcement sensitive operational data exclusion.
- **Lexical Overlap**: `0.4444` → `0.5556`
- **Before (`question`)**: `Must a provider's post-market monitoring system gather operational records from every user organisation deploying its high-risk AI product under the EU AI Act?`
- **After (`question`)**: `Under the EU AI Act, where can a provider's post-market monitoring system obtain operational performance data for a high-risk AI product, and what deployer records are excluded?`
- **Before (`gold_answer`)**: `By default, the post-market monitoring system must actively and systematically collect, document, and analyse relevant performance data provided by deployers or other sources throughout the system's lifetime. However, this obligation does not cover sensitive operational data of deployers that are law-enforcement authorities.`
- **After (`gold_answer`)**: `A post-market monitoring system does not have to collect records from every deployer; it must actively and systematically collect and analyse relevant performance data that may be provided by deployers or collected through other sources. However, this obligation does not cover sensitive operational data of law-enforcement deployers.`

### Q114 (`conflicting_or_conditional`)
- **Reason**: Replaced `connected software` with exact statutory terminology `high-risk AI products with digital elements` and `critical digital goods` to match Recital 78 (`ai_act:rec:78`).
- **Lexical Overlap**: `0.1429` → `0.5000`
- **Before (`question`)**: `Under the EU AI Act, does relying on its compliance check for connected software override stricter safeguards for vital digital goods?`
- **After (`question`)**: `Under the EU AI Act, does applying its compliance assessment to high-risk AI products with digital elements override stricter safeguards for critical digital goods?`

### Q119 (`unanswerable`)
- **Reason**: Replaced the European AI Compensation Tribunal item (too close to existing Q065 on compensation adjudication) with a fresh, natural false-premise unanswerable question on mandatory professional licensing exams for individual AI software engineers (`absence_kind:b`), independently verified across 6 keyword variants in all 293 units of `ai_act.jsonl` with `hard_negative:ai_act:art:4`.
- **Lexical Overlap**: N/A (unanswerable)
- **Before (`question`)**: `How does the EU AI Act structure the appeals procedure before the European AI Compensation Tribunal?`
- **After (`question`)**: `How does the EU AI Act regulate the mandatory professional licensing exams required for individual AI software engineers?`
- **Before (`gold_answer`)**: `Not specified in the EU AI Act; the regulation does not establish a European AI Compensation Tribunal or any appeals procedure before such a body.`
- **After (`gold_answer`)**: `Not specified in the EU AI Act; the regulation promotes AI literacy for staff and other persons dealing with AI systems, but does not establish mandatory professional licensing exams for individual AI software engineers.`
- **Before (`notes`)**: `AI_ACT | author:ai | human_review:pending | absence_kind:b | hard_negative:ai_act:art:85 | search:checked 'Compensation Tribunal'(0), 'tribunal'(0), 'compensation'(1: ai_act:rec:9), 'appeal'(1: ai_act:art:44); inspected ai_act:art:85, ai_act:art:44, ai_act:rec:9 — none establishes a compensation tribunal`
- **After (`notes`)**: `AI_ACT | author:ai | human_review:pending | absence_kind:b | hard_negative:ai_act:art:4 | search:checked 'licensing exam'(0), 'professional licence'(0), 'engineer'(0), 'individual certification'(0), 'AI literacy'(7), 'qualification'(1: ai_act:art:33); inspected ai_act:art:4, ai_act:rec:20, ai_act:art:31 — none establishes professional licensing exams for AI engineers`
