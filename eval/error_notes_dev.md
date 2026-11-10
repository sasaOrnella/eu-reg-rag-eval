# Dev 召回问题笔记

条件：块大小 800、预算 8000 字符。召回小于 1 的都算有问题，召回为 0 的是其中一部分。下面 7 道全部记下。Q017 两种方法都是 1.0，没有问题，不记。

查看命令：

```
python -m src.inspect_question <qid> --method bm25 --chunk-size 800
python -m src.inspect_question <qid> --method dense --chunk-size 800
```

`*` 表示这块进了预算，`HIT` 表示它盖住一条金标准证据。类别：词汇差距、序言排在条款前面、混进另一部法规、其他。

| 题 | BM25 | 稠密 | 是不是 0 |
|---|---|---|---|
| Q001 | 0 | 0 | 两种都是 0 |
| Q003 | 0 | 1.0 | 只有 BM25 是 0 |
| Q005 | 0 | 0 | 两种都是 0 |
| Q007 | 0.5 | 0.5 | 都不是 0，但是没找全 |
| Q013 | 0 | 0.75 | 只有 BM25 是 0 |
| Q016 | 0 | 0 | 两种都是 0 |
| Q019 | 0 | 0 | 两种都是 0 |

## Q001 知情与访问（single_hop）

问句：我问机构它是否持有我的信息，它必须告诉我什么。金标准是 GDPR 第 15 条。词面重叠 0.25。

- BM25：前 50 名里没有第 15 条。第 1 名是序言 58。类别：词汇差距；序言排在条款前面；混进另一部法规。
- 稠密：第 15 条排在第 35，进不了预算。类别：词汇差距。

```
bm25: first hit None, context 11

  1*     gdpr:rec:58      [0:800] The principle of transparency requires that any information addressed to the public or to
  2*     ai_act:art:99    [3600:4400] or committing the infringement; (e) any other aggravating or mitigating factor applicable
  3*     gdpr:art:83      [1440:2240] (g) the categories of personal data affected by the infringement; (h) the manner in which
  4*     gdpr:art:79      [0:800] 1. Without prejudice to any available administrative or non-judicial remedy, including the
  5*     ai_act:art:36    [5760:6473] me immediate responsibility for those AI systems and completes its assessment within 12 mo
  6*     gdpr:rec:32      [720:1052] ried out for the same purpose or purposes. When the processing has multiple purposes, cons
  7*     ai_act:rec:134   [1440:1741] lated text to the extent it is published with the purpose of informing the public on matte
  8*     ai_act:art:78    [2160:2960]  the activities of law enforcement, border control, immigration or asylum authorities. Whe

dense: first hit 35, context 11, hit ranks [(35, 'gdpr:art:15')]

  1*     gdpr:art:61      [720:1520]  information on the conduct of an investigation. 3. Requests for assistance shall contain
  2*     ai_act:art:91    [720:1520] fic panel under Article 68(2). 4. The request for information shall state the legal basis
  3*     gdpr:rec:26      [0:800] The principles of data protection should apply to any information concerning an identified
  4*     gdpr:art:38      [720:1385] his tasks. The data protection officer shall directly report to the highest management lev
  5*     gdpr:rec:142     [0:800] Where a data subject considers that his or her rights under this Regulation are infringed,
  6*     gdpr:art:13      [0:800] 1. Where personal data relating to a data subject are collected from the data subject, the
  7*     gdpr:art:39      [0:800] 1. The data protection officer shall have at least the following tasks: (a) to inform and
  8*     ai_act:art:31    [0:800] 1. A notified body shall be established under the national law of a Member State and shall
```

## Q003 推断能力（single_hop）

问句：AI 系统和只执行固定人工指令的软件，差在什么能力。金标准是 AI 法序言 12（infer）。词面重叠 0.09。

- BM25：召回 0。第 1、2 名是序言 53，序言 12 排在第 31。类别：词汇差距。
- 稠密：召回 1.0。含金标准的那一块排在第 5，已经在预算里。

```
bm25: first hit 31, context 10, hit ranks [(31, 'ai_act:rec:12')]

  1*     ai_act:rec:53    [1440:2240]  result of a previously completed human activity that may be relevant for the purposes of
  2*     ai_act:rec:53    [2160:2960] e the use of the AI system follows a previously completed human assessment which it is not
  3*     ai_act:art:3     [6480:7280] g data set, either as a fixed or variable split; (32) ‘testing data’ means data used for p
  4*     ai_act:rec:103   [0:800] Free and open-source AI components covers the software and data, including models and gene
  5*     ai_act:art:3     [16560:17079] tion’ means any mathematical operation or assignment involving floating-point numbers, whi
  6*     ai_act:art:3     [2880:3680] with its intended purpose, but which may result from reasonably foreseeable human behaviou
  7*     ai_act:rec:88    [0:800] Along the AI value chain multiple parties often supply AI systems, tools and services but
  8*     ai_act:art:17    [0:800] 1. Providers of high-risk AI systems shall put a quality management system in place that e

dense: first hit 5, context 10, hit ranks [(5, 'ai_act:rec:12'), (10, 'ai_act:rec:12')]

  1*     ai_act:rec:12    [2160:2640] an involvement and of capabilities to operate without human intervention. The adaptiveness
  2*     ai_act:rec:133   [1440:2026]  generally acknowledged state of the art. Such techniques and methods can be implemented a
  3*     ai_act:rec:53    [1440:2240]  result of a previously completed human activity that may be relevant for the purposes of
  4*     ai_act:rec:53    [2160:2960] e the use of the AI system follows a previously completed human assessment which it is not
  5* HIT ai_act:rec:12    [0:800] The notion of ‘AI system’ in this Regulation should be clearly defined and should be close
  6*     ai_act:rec:97    [720:1520] tuned into new models. Although AI models are essential components of AI systems, they do
  7*     ai_act:rec:97    [0:800] The notion of general-purpose AI models should be clearly defined and set apart from the n
  8*     ai_act:rec:53    [720:1520] ations in which one or more of the following conditions are fulfilled. The first such cond
```

## Q005 合同与角色（multi_hop）

问句：公司雇供应商处理客户记录时，角色怎么分，需要什么法律安排。金标准是 GDPR 第 4 条的 controller / processor，以及第 28 条的合同。词面重叠 0.09。两种召回都是 0。

- BM25：第 1、2 名是第 26 条（联合控制者）。第 28 条排在第 16。问句里的 company / vendor 对不上条文用词，又被 controller 这个高频词带走。前 10 里还有 AI 法。类别：词汇差距；混进另一部法规。
- 稠密：第 28 条排在第 39。前面是第 27、6、30 条和序言 40。类别：其他。

```
bm25: first hit 16, context 10, hit ranks [(16, 'gdpr:art:28')]

  1*     gdpr:art:26      [0:800] 1. Where two or more controllers jointly determine the purposes and means of processing, t
  2*     gdpr:art:26      [720:1118] n paragraph 1 shall duly reflect the respective roles and relationships of the joint contr
  3*     ai_act:rec:71    [0:800] Having comprehensible information on how high-risk AI systems have been developed and how
  4*     gdpr:rec:39      [720:1520] ed and their right to obtain confirmation and communication of personal data concerning th
  5*     gdpr:rec:127     [720:1520] the case pursuant to the provision on cooperation between the lead supervisory authority a
  6*     ai_act:art:91    [720:1520] fic panel under Article 68(2). 4. The request for information shall state the legal basis
  7*     gdpr:rec:158     [0:800] Where personal data are processed for archiving purposes, this Regulation should also appl
  8*     ai_act:art:74    [5760:6560] 12. Without prejudice to the powers provided for under Regulation (EU) 2019/1020, and wher

dense: first hit 39, context 12, hit ranks [(39, 'gdpr:art:28'), (48, 'gdpr:art:4')]

  1*     gdpr:art:27      [720:1370] e the data subjects, whose personal data are processed in relation to the offering of good
  2*     gdpr:art:6       [0:800] 1. Processing shall be lawful only if and to the extent that at least one of the following
  3*     gdpr:art:30      [0:800] 1. Each controller and, where applicable, the controller's representative, shall maintain
  4*     gdpr:rec:40      [0:560] In order for processing to be lawful, personal data should be processed on the basis of th
  5*     gdpr:art:39      [0:800] 1. The data protection officer shall have at least the following tasks: (a) to inform and
  6*     ai_act:rec:79    [0:291] It is appropriate that a specific natural or legal person, defined as the provider, takes
  7*     gdpr:rec:47      [1440:1656] ses of preventing fraud also constitutes a legitimate interest of the data controller conc
  8*     gdpr:art:37      [0:800] 1. The controller and the processor shall designate a data protection officer in any case
```

## Q007 高风险分类与权利评估（multi_hop）

问句：公共部门部署高风险类别的 AI 时，分类由什么决定，事先要做什么权利评估。金标准是 AI 法第 6 条和第 27 条。词面重叠 0.32。两种召回都是 0.5，不是 0，但没找全。

- BM25：第 27 条排在第 3。第 6 条没进前 50。第 1 名是 GDPR 序言 77。类别：序言排在条款前面；混进另一部法规。
- 稠密：第 27 条排在第 4，第 6 条排在第 34。前 3 名是序言 96 和 93。类别：序言排在条款前面。

```
bm25: first hit 3, context 11, hit ranks [(3, 'ai_act:art:27')]

  1*     gdpr:rec:77      [0:773] Guidance on the implementation of appropriate measures and on the demonstration of complia
  2*     ai_act:rec:51    [0:513] The classification of an AI system as high-risk pursuant to this Regulation should not nec
  3* HIT ai_act:art:27    [0:800] 1. Prior to deploying a high-risk AI system referred to in Article 6(2), with the exceptio
  4*     ai_act:rec:54    [0:800] As biometric data constitutes a special category of personal data, it is appropriate to cl
  5*     gdpr:rec:154     [0:800] This Regulation allows the principle of public access to official documents to be taken in
  6*     gdpr:art:35      [0:800] 1. Where a type of processing in particular using new technologies, and taking into accoun
  7*     ai_act:art:31    [720:1520] ied bodies shall also be independent of any other operator having an economic interest in
  8*     ai_act:art:27    [2160:2837] he notification. In the case referred to in Article 46(1), deployers may be exempt from th

dense: first hit 4, context 10, hit ranks [(4, 'ai_act:art:27'), (34, 'ai_act:art:6')]

  1*     ai_act:rec:96    [0:800] In order to efficiently ensure that fundamental rights are protected, deployers of high-ri
  2*     ai_act:rec:93    [0:800] Whilst risks related to AI systems can result from the way such systems are designed, risk
  3*     ai_act:rec:96    [720:1520]  rights impact assessment is for the deployer to identify the specific risks to the rights
  4* HIT ai_act:art:27    [0:800] 1. Prior to deploying a high-risk AI system referred to in Article 6(2), with the exceptio
  5*     ai_act:rec:52    [0:800] As regards stand-alone AI systems, namely high-risk AI systems other than those that are s
  6*     ai_act:rec:56    [720:1448] and training that individuals will receive or will be able to access or for monitoring and
  7*     ai_act:art:43    [1440:2240] . However, where the high-risk AI system is intended to be put into service by law enforce
  8*     ai_act:rec:93    [720:1375] nnex to this Regulation also play a critical role in informing natural persons and should,
```

## Q013 删除请求是否必须答应（conflicting_or_conditional）

问句：我要求网站删除我的个人信息，它是否必须照做。金标准是 GDPR 第 17 条的删除义务和例外。词面重叠 0.14。

- BM25：召回 0。前 50 名里没有第 17 条。第 3 名是序言 65。前 10 里还有 AI 法。类别：序言排在条款前面；混进另一部法规。
- 稠密：召回 0.75。第 17 条排在第 3，还差一条金标准没盖住。类别：其他。

```
bm25: first hit None, context 11

  1*     gdpr:rec:32      [720:1052] ried out for the same purpose or purposes. When the processing has multiple purposes, cons
  2*     gdpr:rec:143     [2160:2960] reliminary ruling on the interpretation of Union law, including this Regulation. Furthermo
  3*     gdpr:rec:65      [720:1520] ght is relevant in particular where the data subject has given his or her consent as a chi
  4*     ai_act:art:75    [720:1520]  laid down in this Regulation, they shall cooperate with the AI Office to carry out compli
  5*     ai_act:art:22    [1440:2240] nd, if applicable, the certificate issued by the notified body; (c) provide a competent au
  6*     gdpr:rec:58      [0:800] The principle of transparency requires that any information addressed to the public or to
  7*     ai_act:art:16    [720:1520] ssessment procedure as referred to in Article 43, prior to its being placed on the market
  8*     gdpr:art:61      [720:1520]  information on the conduct of an investigation. 3. Requests for assistance shall contain

dense: first hit 3, context 11, hit ranks [(3, 'gdpr:art:17'), (10, 'gdpr:art:17')]

  1*     gdpr:rec:64      [0:295] The controller should use all reasonable measures to verify the identity of a data subject
  2*     gdpr:rec:39      [1440:2097]  strict minimum. Personal data should be processed only if the purpose of the processing c
  3* HIT gdpr:art:17      [0:800] 1. The data subject shall have the right to obtain from the controller the erasure of pers
  4*     gdpr:rec:66      [0:607] To strengthen the right to be forgotten in the online environment, the right to erasure sh
  5*     gdpr:rec:28      [0:317] The application of pseudonymisation to personal data can reduce the risks to the data subj
  6*     gdpr:rec:65      [0:800] A data subject should have the right to have personal data concerning him or her rectified
  7*     gdpr:art:18      [0:800] 1. The data subject shall have the right to obtain from the controller restriction of proc
  8*     gdpr:art:11      [0:786] 1. If the purposes for which a controller processes personal data do not or do no longer r
```

## Q016 敏感用途是否一律高风险（conflicting_or_conditional）

问句：落入敏感用途的 AI 产品，是不是在任何情况下都自动算高风险。金标准是 AI 法第 6 条里的附件 III 规则、例外，以及画像仍然算高风险。词面重叠 0.21。两种召回都是 0。

- BM25：第 6 条开头排在第 4，但那一段不是金标准。序言 51 排在第 2。类别：序言排在条款前面；其他。
- 稠密：第 6 条开头排在第 2，序言 51 排在第 1。金标准那几句都不在前 50。类别：序言排在条款前面；其他。

```
bm25: first hit None, context 10

  1*     ai_act:rec:87    [0:532] In addition, where a high-risk AI system that is a safety component of a product which fal
  2*     ai_act:rec:51    [0:513] The classification of an AI system as high-risk pursuant to this Regulation should not nec
  3*     ai_act:rec:84    [0:800] To ensure legal certainty, it is necessary to clarify that, under certain specific conditi
  4*     ai_act:art:6     [0:800] 1. Irrespective of whether an AI system is placed on the market or put into service indepe
  5*     ai_act:art:46    [720:1520]  a duly justified situation of urgency for exceptional reasons of public security or in th
  6*     ai_act:art:25    [2160:2960] s under Article 16 under either of the following circumstances: (a) the high-risk AI syste
  7*     ai_act:rec:54    [0:800] As biometric data constitutes a special category of personal data, it is appropriate to cl
  8*     ai_act:art:43    [2880:3680] ection A of Annex I enables the product manufacturer to opt out from a third-party conform

dense: first hit None, context 10

  1*     ai_act:rec:51    [0:513] The classification of an AI system as high-risk pursuant to this Regulation should not nec
  2*     ai_act:art:6     [0:800] 1. Irrespective of whether an AI system is placed on the market or put into service indepe
  3*     ai_act:rec:166   [0:407] It is important that AI systems related to products that are not high-risk in accordance w
  4*     ai_act:rec:53    [2880:3680] follow. That condition covers, inter alia, smart solutions for file handling, which includ
  5*     ai_act:art:20    [0:800] 1. Providers of high-risk AI systems which consider or have reason to consider that a high
  6*     ai_act:rec:52    [0:800] As regards stand-alone AI systems, namely high-risk AI systems other than those that are s
  7*     ai_act:art:25    [2160:2960] s under Article 16 under either of the following circumstances: (a) the high-risk AI syste
  8*     ai_act:rec:125   [0:800] Given the complexity of high-risk AI systems and the risks that are associated with them,
```

## Q019 禁止性 AI 做法的罚款档（numeric_or_table）

问句：公司从事被禁止的 AI 做法，最高罚款档是多少。金标准是 AI 法第 99 条。词面重叠 0.12。两种召回都是 0。

- BM25：前 50 名里没有第 99 条。靠前的是序言 33 和 GDPR 序言 151。类别：词汇差距；混进另一部法规。
- 稠密：第 1 名是第 5 条，第 3 名是第 101 条。第 99 条不在前 50。类别：其他。

```
bm25: first hit None, context 10

  1*     ai_act:rec:33    [720:1520] for a maximum period of at least four years and as they are defined in the law of that Mem
  2*     ai_act:rec:33    [0:800] The use of those systems for the purpose of law enforcement should therefore be prohibited
  3*     gdpr:rec:151     [0:744] The legal systems of Denmark and Estonia do not allow for administrative fines as set out
  4*     gdpr:rec:58      [0:800] The principle of transparency requires that any information addressed to the public or to
  5*     ai_act:art:5     [4320:5120] tion or executing a criminal penalty for offences referred to in Annex II and punishable i
  6*     ai_act:rec:54    [720:1520] sed for biometric verification, including authentication, the sole purpose of which is to
  7*     ai_act:art:56    [0:800] 1. The AI Office shall encourage and facilitate the drawing up of codes of practice at Uni
  8*     ai_act:art:56    [2880:3680] ove a code of practice and give it a general validity within the Union. That implementing

dense: first hit None, context 11

  1*     ai_act:art:5     [0:800] 1. The following AI practices shall be prohibited: (a) the placing on the market, the putt
  2*     ai_act:art:25    [0:800] 1. Any distributor, importer, deployer or other third-party shall be considered to be a pr
  3*     ai_act:art:101   [0:800] 1. The Commission may impose on providers of general-purpose AI models fines not exceeding
  4*     ai_act:rec:26    [0:511] In order to introduce a proportionate and effective set of binding rules for AI systems, a
  5*     ai_act:rec:169   [0:740] Compliance with the obligations on providers of general-purpose AI models imposed under th
  6*     ai_act:rec:66    [0:528] Requirements should apply to high-risk AI systems as regards risk management, the quality
  7*     ai_act:rec:166   [0:407] It is important that AI systems related to products that are not high-risk in accordance w
  8*     ai_act:rec:124   [0:627] It is appropriate that, in order to minimise the burden on operators and avoid any possibl
```
