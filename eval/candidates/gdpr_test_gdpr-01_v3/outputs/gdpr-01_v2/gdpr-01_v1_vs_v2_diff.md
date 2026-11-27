# `gdpr-01` Revision Diff Report (v1 → v2)

- **Generated At:** `2026-11-27T13:31:21.057594+11:00`
- **v1 CSV (preserved untouched):** `outputs/gdpr-01/gdpr-01_candidates.csv` (`SHA-256: f5195a8123d70a79edc435c81dfa0d798477e584a872b8aacf3fa12288851888`)
- **v2 CSV:** `outputs/gdpr-01_v2/gdpr-01_candidates_v2.csv` (`SHA-256: c8ce60e3e798f5bf93b2b28c824f0288acf2ec41b5502b8c0528b52ca43b81d8`)
- **Modified IDs (8):** `Q128, Q131, Q132, Q133, Q135, Q136, Q137, Q138`
- **Unchanged IDs (10, byte-for-byte verified identical to v1):** `Q121, Q122, Q123, Q124, Q125, Q126, Q127, Q129, Q130, Q134`

## Side-by-Side Comparison of the 8 Revised Questions

### Q128 (`multi_hop` | Overlap: `0.2500` → `0.2500`)

- **Revision Reason:** 补全 Article 26(1) 中 joint controllers 主语定义句及欧盟/成员国法律已确定职责时的例外条款（拆分为两句完整引文以避免单段超 600 字符上限），并使答案与证据完全一致。
- **v1 Question:** When two organizations jointly determine why and how to gather records directly from individuals under the GDPR, how must they divide notice duties and when must they share their identity?
- **v2 Question:** When multiple organizations jointly decide why and how to gather records directly from individuals under the GDPR, how must they divide notice duties and when must they share their identity?
- **v1 Gold Answer:** Joint controllers must transparently allocate their respective information-provision responsibilities through an arrangement between them, and must provide their identity and contact details at the time the personal data are obtained from the individual.
- **v2 Gold Answer:** Joint controllers must transparently allocate their respective notice duties through an arrangement between them, unless and insofar as those responsibilities are determined by Union or Member State law; when collecting personal data directly from individuals, they must provide their identity and contact details at the time the data are obtained.
- **v1 Gold Evidence:** `gdpr:art:26::They shall in a transparent manner determine their respective responsibilities for compliance with the obligations under this Regulation, in particular as regards the exercising of the rights of the data subject and their respective duties to provide the information referred to in Articles 13 and 14, by means of an arrangement between them || gdpr:art:13::Where personal data relating to a data subject are collected from the data subject, the controller shall, at the time when personal data are obtained, provide the data subject with all of the following information: (a) the identity and the contact details of the controller and, where applicable, of the controller's representative;`
- **v2 Gold Evidence:** `gdpr:art:26::Where two or more controllers jointly determine the purposes and means of processing, they shall be joint controllers. || gdpr:art:26::They shall in a transparent manner determine their respective responsibilities for compliance with the obligations under this Regulation, in particular as regards the exercising of the rights of the data subject and their respective duties to provide the information referred to in Articles 13 and 14, by means of an arrangement between them unless, and in so far as, the respective responsibilities of the controllers are determined by Union or Member State law to which the controllers are subject. || gdpr:art:13::Where personal data relating to a data subject are collected from the data subject, the controller shall, at the time when personal data are obtained, provide the data subject with all of the following information: (a) the identity and the contact details of the controller and, where applicable, of the controller's representative;`
- **v1 Notes:** `GDPR | topic:joint_controllers_direct_notice_timing | author:ai | human_review:pending`
- **v2 Notes:** `GDPR | topic:joint_controllers_direct_notice_timing_and_statutory_exception | revision:v2_completed_art26_subject_and_law_exception | author:ai | human_review:pending`

### Q131 (`conflicting_or_conditional` | Overlap: `0.0833` → `0.2941`)

- **Revision Reason:** 将提问与答案精确限定为 GDPR 下的 accredited code-of-conduct monitoring mechanism，避免误解为禁止所有外部监督行为，同时保持 Low 词面重叠度（<0.30）。
- **v1 Question:** Can an accredited external entity oversee adherence to an approved industry privacy framework for government agencies under the GDPR?
- **v2 Question:** Does the GDPR's accredited code-of-conduct monitoring mechanism govern state agencies and municipal institutions, or are governmental entities carved out of that oversight scheme?
- **v1 Gold Answer:** No, although an accredited body with appropriate expertise may generally monitor compliance with an approved code of conduct, that monitoring provision does not apply to processing carried out by public authorities and bodies.
- **v2 Gold Answer:** No; while an accredited body with appropriate expertise may monitor compliance with an approved code of conduct under that mechanism, the accredited code-of-conduct monitoring provision does not apply to processing carried out by public authorities and bodies.
- **v1 Gold Evidence:** `gdpr:art:41::the monitoring of compliance with a code of conduct pursuant to Article 40 may be carried out by a body which has an appropriate level of expertise in relation to the subject-matter of the code and is accredited for that purpose by the competent supervisory authority. || gdpr:art:41::This Article shall not apply to processing carried out by public authorities and bodies.`
- **v2 Gold Evidence:** `gdpr:art:41::the monitoring of compliance with a code of conduct pursuant to Article 40 may be carried out by a body which has an appropriate level of expertise in relation to the subject-matter of the code and is accredited for that purpose by the competent supervisory authority. || gdpr:art:41::This Article shall not apply to processing carried out by public authorities and bodies.`
- **v1 Notes:** `GDPR | topic:code_monitoring_public_authority_exception | author:ai | human_review:pending`
- **v2 Notes:** `GDPR | topic:accredited_code_monitoring_public_authority_exception | revision:v2_scoped_to_accredited_code_monitoring_mechanism | author:ai | human_review:pending`

### Q132 (`conflicting_or_conditional` | Overlap: `0.1579` → `0.2381`)

- **Revision Reason:** 明确平行诉讼针对同一控制者/处理者的相同处理事项，并在答案中清晰区分暂停诉讼与拒绝管辖的各自条件。
- **v1 Question:** When parallel lawsuits against the same organization are active in two EU countries under the GDPR, may the second court decline to hear the dispute altogether instead of merely pausing it?
- **v2 Question:** When parallel lawsuits over the same processing dispute involving the same business or vendor are active in two EU countries under the GDPR, may a later court decline the case rather than merely pause it?
- **v1 Gold Answer:** While a court other than the court first seized may generally suspend its proceedings, it may also decline jurisdiction only if the proceedings are pending at first instance, a party applies for it, the first-seized court has jurisdiction, and that court's law permits consolidation.
- **v2 Gold Answer:** When parallel proceedings concern the same processing subject matter by the same controller or processor, a competent court other than the court first seized may suspend proceedings; it may also decline jurisdiction only if proceedings are pending at first instance, a party applies, the first-seized court has jurisdiction, and its law permits consolidation.
- **v1 Gold Evidence:** `gdpr:art:81::Where proceedings concerning the same subject matter as regards processing of the same controller or processor are pending in a court in another Member State, any competent court other than the court first seized may suspend its proceedings. || gdpr:art:81::Where those proceedings are pending at first instance, any court other than the court first seized may also, on the application of one of the parties, decline jurisdiction if the court first seized has jurisdiction over the actions in question and its law permits the consolidation thereof.`
- **v2 Gold Evidence:** `gdpr:art:81::Where proceedings concerning the same subject matter as regards processing of the same controller or processor are pending in a court in another Member State, any competent court other than the court first seized may suspend its proceedings. || gdpr:art:81::Where those proceedings are pending at first instance, any court other than the court first seized may also, on the application of one of the parties, decline jurisdiction if the court first seized has jurisdiction over the actions in question and its law permits the consolidation thereof.`
- **v1 Notes:** `GDPR | topic:parallel_court_proceedings_suspend_or_decline | later_article:yes | author:ai | human_review:pending`
- **v2 Notes:** `GDPR | topic:parallel_court_proceedings_suspend_or_decline | later_article:yes | revision:v2_clarified_same_processing_subject_and_conditions | author:ai | human_review:pending`

### Q133 (`conflicting_or_conditional` | Overlap: `0.1429` → `0.1875`)

- **Revision Reason:** 区分因保护商业秘密/软件著作权而适当限制部分披露与绝对拒绝提供全部信息，避免绝对化表述。
- **v1 Question:** May a company refuse to disclose any requested records to an individual under the GDPR in order to protect proprietary software or business secrets?
- **v2 Question:** How does safeguarding proprietary software or business secrets affect an individual's access request under the GDPR—can a firm refuse everything or only limit disclosure?
- **v1 Gold Answer:** No; although the right of access should not adversely affect others' rights such as trade secrets or software copyright, those considerations should not result in refusing to provide all information to the data subject.
- **v2 Gold Answer:** While an individual's access right should not adversely affect others' rights such as trade secrets, intellectual property, or software copyright—allowing appropriate limits on disclosure—those considerations should not result in a refusal to provide all information to the data subject.
- **v1 Gold Evidence:** `gdpr:rec:63::That right should not adversely affect the rights or freedoms of others, including trade secrets or intellectual property and in particular the copyright protecting the software. || gdpr:rec:63::However, the result of those considerations should not be a refusal to provide all information to the data subject.`
- **v2 Gold Evidence:** `gdpr:rec:63::That right should not adversely affect the rights or freedoms of others, including trade secrets or intellectual property and in particular the copyright protecting the software. || gdpr:rec:63::However, the result of those considerations should not be a refusal to provide all information to the data subject.`
- **v1 Notes:** `GDPR | topic:access_right_trade_secrets_limit | recital_justification:trade_secrets_and_no_total_refusal_only_in_recital | author:ai | human_review:pending`
- **v2 Notes:** `GDPR | topic:access_right_trade_secrets_partial_limit_vs_total_refusal | recital_justification:trade_secrets_and_no_total_refusal_only_in_recital | revision:v2_distinguished_partial_restriction_from_total_refusal | author:ai | human_review:pending`

### Q135 (`numeric_or_table` | Overlap: `0.0556` → `0.2105`)

- **Revision Reason:** 补充 Article 62(2) 第二句原文引文，使 Gold Evidence 本身完整自足地解释联合行动邀请与回应义务及一个月期限，并精简题目。
- **v1 Question:** How long must partner privacy regulators wait for a silent lead authority to act on a collaborative enforcement invitation before adopting domestic interim steps under the GDPR?
- **v2 Question:** How long must partner privacy regulators wait for a competent authority to fulfill its joint-operation invitation and response duty before taking interim domestic steps under the GDPR?
- **v1 Gold Answer:** Other supervisory authorities may adopt a provisional domestic measure if the competent supervisory authority fails to comply with its invitation and response obligation within one month.
- **v2 Gold Answer:** If a competent supervisory authority fails within one month to invite concerned Member State authorities to take part in joint operations or respond without delay to a participation request, the other supervisory authorities may adopt a provisional domestic measure.
- **v1 Gold Evidence:** `gdpr:art:62::Where a joint operation is intended and a supervisory authority does not, within one month, comply with the obligation laid down in the second sentence of paragraph 2 of this Article, the other supervisory authorities may adopt a provisional measure on the territory of its Member State in accordance with Article 55.`
- **v2 Gold Evidence:** `gdpr:art:62::The supervisory authority which is competent pursuant to Article 56(1) or (4) shall invite the supervisory authority of each of those Member States to take part in the joint operations and shall respond without delay to the request of a supervisory authority to participate. || gdpr:art:62::Where a joint operation is intended and a supervisory authority does not, within one month, comply with the obligation laid down in the second sentence of paragraph 2 of this Article, the other supervisory authorities may adopt a provisional measure on the territory of its Member State in accordance with Article 55.`
- **v1 Notes:** `GDPR | topic:joint_operations_one_month_timeout | author:ai | human_review:pending`
- **v2 Notes:** `GDPR | topic:joint_operations_one_month_timeout | revision:v2_added_art62_para2_invitation_response_quote | author:ai | human_review:pending`

### Q136 (`numeric_or_table` | Overlap: `0.1333` → `0.2500`)

- **Revision Reason:** 严格区分 GDPR 的 entry into force（生效）与 date of application（适用日期），修正过渡期限的提问与答案表述。
- **v1 Question:** How much time does the GDPR grant after it takes effect to bring ongoing legacy operations into alignment with the new framework?
- **v2 Question:** How much time after the GDPR's formal entry into force is allowed to align ongoing activities already active when it begins applying?
- **v1 Gold Answer:** Processing already under way on the GDPR's date of application should be brought into conformity within two years after the regulation enters into force.
- **v2 Gold Answer:** Processing already under way on the GDPR's date of application should be brought into conformity within two years after the regulation's entry into force.
- **v1 Gold Evidence:** `gdpr:rec:171::Processing already under way on the date of application of this Regulation should be brought into conformity with this Regulation within the period of two years after which this Regulation enters into force.`
- **v2 Gold Evidence:** `gdpr:rec:171::Processing already under way on the date of application of this Regulation should be brought into conformity with this Regulation within the period of two years after which this Regulation enters into force.`
- **v1 Notes:** `GDPR | topic:ongoing_processing_two_year_transition | recital_justification:two_year_conformity_period_only_in_recital | author:ai | human_review:pending`
- **v2 Notes:** `GDPR | topic:ongoing_processing_two_year_transition | recital_justification:two_year_conformity_period_only_in_recital | revision:v2_distinguished_entry_into_force_vs_date_of_application | author:ai | human_review:pending`

### Q137 (`unanswerable` | Overlap: `N/A` → `N/A`)

- **Revision Reason:** 完全更换与已有题重复的强制责任保险主题，替换为全新自然的 absence_kind:a 不可回答题（数据中心能效/碳排标准），并附完整语料核查记录。
- **v1 Question:** Does the GDPR require organizations handling large volumes of personal data to maintain cyber liability insurance?
- **v2 Question:** Does the GDPR establish energy-efficiency or carbon-emission standards for data centers that host European personal data?
- **v1 Gold Answer:** Not specified in the GDPR, which establishes liability for damages and security obligations but contains no requirement for controllers or processors to carry cyber liability insurance.
- **v2 Gold Answer:** Not specified in the GDPR, which sets technical and organisational security and design obligations for processing systems but contains no energy-efficiency, carbon-emission, or environmental standards for data centers.
- **v1 Gold Evidence:** `(empty)`
- **v2 Gold Evidence:** `(empty)`
- **v1 Notes:** `GDPR | absence_kind:a | hard_negative:gdpr:art:82 | search:variants=insurance, insurer, cyber, liability; inspected=gdpr:art:82, gdpr:rec:146, gdpr:art:32, gdpr:rec:52; missing=any obligation or rule requiring controllers or processors to purchase or maintain cyber liability or data-breach insurance (gdpr:art:82 and gdpr:rec:146 cover civil compensation liability, gdpr:art:32 covers technical and organisational security measures, and gdpr:rec:52 only mentions health insurance claims) | author:ai | human_review:pending`
- **v2 Notes:** `GDPR | absence_kind:a | hard_negative:gdpr:art:32 | search:variants=energy, carbon, emission, data center, environment; inspected=gdpr:art:32, gdpr:art:25, gdpr:rec:66, gdpr:rec:92; missing=any energy-efficiency, carbon-emission, or environmental sustainability standards for data centers (gdpr:art:32 covers technical and organisational security of processing, gdpr:art:25 covers data protection by design and by default, and gdpr:rec:66 and gdpr:rec:92 only use 'environment' in non-environmental contexts) | revision:v2_replaced_insurance_topic_with_fresh_kind_a | author:ai | human_review:pending`

### Q138 (`unanswerable` | Overlap: `N/A` → `N/A`)

- **Revision Reason:** 完全更换重复的虚构 European Data Protection Tribunal，替换为全新自然的 absence_kind:b 虚假前提题（向国家监管机构续期年度数据处理许可证），并附完整语料核查记录。
- **v1 Question:** How does a controller appeal a binding decision of the European Data Protection Board to the European Data Protection Tribunal under the GDPR?
- **v2 Question:** What procedure must a private company follow under the GDPR to renew its annual data-processing license with its national supervisory authority?
- **v1 Gold Answer:** Not specified in the GDPR, which does not establish a European Data Protection Tribunal or an appeal procedure before such a body; challenges to Board decisions are instead brought as annulment actions before the Court of Justice.
- **v2 Gold Answer:** Not specified in the GDPR, which does not create a mandatory annual data-processing license or renewal procedure with supervisory authorities; instead, it abolishes general notification obligations and provides only for voluntary certification and high-risk prior consultation.
- **v1 Gold Evidence:** `(empty)`
- **v2 Gold Evidence:** `(empty)`
- **v1 Notes:** `GDPR | absence_kind:b | hard_negative:gdpr:rec:143 | search:variants=tribunal, appeal, Court of Justice, binding decision; inspected=gdpr:rec:143, gdpr:art:78, gdpr:art:48, gdpr:art:65; missing=any European Data Protection Tribunal or appeal procedure to it (gdpr:rec:143 directs annulment actions against Board decisions to the Court of Justice under Article 263 TFEU, gdpr:art:78 covers national judicial remedies against supervisory authorities, gdpr:art:65 covers Board dispute resolution, and gdpr:art:48 only refers to third-country tribunals) | author:ai | human_review:pending`
- **v2 Notes:** `GDPR | absence_kind:b | hard_negative:gdpr:art:42 | search:variants=license, licence, renew, general notification, prior consultation; inspected=gdpr:art:42, gdpr:rec:89, gdpr:art:36, gdpr:art:43; missing=any mandatory annual data-processing license or license-renewal procedure with a national supervisory authority (gdpr:rec:89 explicitly abolishes indiscriminate general notification obligations, gdpr:art:42 and gdpr:art:43 govern voluntary certification and accreditation rather than mandatory operating licenses, and gdpr:art:36 applies only to prior consultation for high-risk processing) | revision:v2_replaced_tribunal_with_fresh_kind_b | author:ai | human_review:pending`
