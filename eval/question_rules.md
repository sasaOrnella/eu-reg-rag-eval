# Evaluation question rules (eval/questions.csv)

Version 1. These rules are the single source of truth for writing and auditing evaluation questions.
Every rule has an ID (R-xx). A supervising person or bot must cite those IDs when reporting problems.

中文摘要：本文件规定 80 道评测题（GDPR 与 EU AI Act）的写法与审查方法。核心思想：题目像真实用户的提问，
证据是从原文逐字复制的最短段落，答案只含证据支持的内容，无答案题必须真的在文本里找不到答案，
dev 与 test 不共用任何条款。题目不能根据系统的检索结果修改。

---

## 0. Purpose and how the questions are used

The questions evaluate retrieval strategies (BM25, dense, hybrid; chunk size; context budget) over the English
GDPR (Regulation 2016/679) and the EU AI Act (Regulation 2024/1689). For each answerable question the system is
scored on whether the retrieved context covers the gold evidence. Later, a language model answers from that context
and is judged against `gold_answer`. Therefore:

- the gold evidence must be sufficient and minimal (R-E1, R-E2), otherwise recall is meaningless;
- the question must not leak its evidence through shared wording (R-Q3), otherwise BM25 is rewarded for nothing;
- the dev/test split must be clean (R-S2), otherwise tuning on dev inflates test.

Corpus = `data/processed/gdpr.jsonl` and `data/processed/ai_act.jsonl`: recitals and articles only. Annexes are NOT in the
corpus. Nothing outside the two texts (other laws, case law, guidance, news) may be needed to answer a question.

## 1. File format (R-F)

- **R-F1** File `eval/questions.csv`, UTF-8, header exactly: `id,split,type,question,gold_answer,gold_evidence,notes`.
  Fields containing commas, quotes or newlines are double-quoted. No extra columns, no blank lines inside the file.
- **R-F2** `id`: `Q` + three digits, unique, never reused or renumbered. Q001-Q020 were written by the project owner and
  must never be edited by drafters. Q021-Q050 are GDPR drafts, Q051-Q080 are AI Act drafts.
- **R-F3** `split`: `dev` or `test`. `type`: one of `single_hop`, `multi_hop`, `unanswerable`,
  `conflicting_or_conditional`, `numeric_or_table`.
- **R-F4** `gold_evidence`: one or more pieces `unit_id::verbatim quote`, pieces separated by ` || `.
  Unit ids: `gdpr:art:33`, `gdpr:rec:26`, `ai_act:art:5`, `ai_act:rec:12`. Empty ONLY for `unanswerable`.
- **R-F5** `notes`: starts with the document tag `GDPR | ` or `AI_ACT | ` (for unanswerable questions this is the only
  way to know the document), then free text, then optional tags separated by ` | `:
  - `author:ai` for every question drafted by an AI (mandatory for Q021 and above),
  - `explicit_ref` if the question names a provision (only with justification, see R-Q1),
  - `hard_negative:<unit_id>` the unit that looks relevant but does not answer (mandatory for unanswerable),
  - `alt_evidence:<unit_id>` another unit that also answers the question (see R-E6),
  - `verified:human` is added by the project owner after reading the item (R-P3).

## 2. Quotas and balance (R-B)

Final set: 80 questions = 20 existing + 60 new.

| type | existing | new | total |
|---|---|---|---|
| single_hop | 4 | 18 | 22 |
| multi_hop | 4 | 15 | 19 |
| unanswerable | 4 | 9 | 13 |
| conflicting_or_conditional | 4 | 9 | 13 |
| numeric_or_table | 4 | 9 | 13 |

- **R-B1** Totals per type as above. New GDPR batch (Q021-Q050): single 9, multi 8, unanswerable 4, conditional 4,
  numeric 5. New AI Act batch (Q051-Q080): single 9, multi 7, unanswerable 5, conditional 5, numeric 4.
- **R-B2** Split: 40 dev + 40 test overall. Each new batch has 15 dev + 15 test:
  GDPR dev: single 4, multi 4, unans 2, cond 2, numeric 3; GDPR test: single 5, multi 4, unans 2, cond 2, numeric 2.
  AI Act dev: single 5, multi 3, unans 3, cond 2, numeric 2; AI Act test: single 4, multi 4, unans 2, cond 3, numeric 2.
- **R-B3** Document balance: 40 GDPR + 40 AI Act overall.
- **R-B4** Coverage, not popularity. Do not cluster on famous provisions. Across a batch: use at least 20 distinct
  evidence units; no unit is the evidence of more than 2 questions; at least 20% of answerable questions use a recital as
  evidence (only where R-E5 allows); at least 6 questions use a unit from the second half of the document (articles 50-99
  for GDPR, 56-113 for the AI Act). Spread topics: GDPR (scope and definitions, principles, lawfulness and consent,
  data subject rights, controller/processor duties, security and breaches, DPIA and DPO, transfers, supervisory
  authorities and cooperation, remedies and penalties, specific situations); AI Act (scope and definitions, prohibited
  practices, high-risk classification and requirements, provider/deployer/importer duties, transparency, general-purpose
  models, governance and authorities, conformity and standards, sandboxes and testing, penalties, timelines).
- **R-B5** Do not reuse any unit that is the evidence of Q001-Q020 (list below). Existing evidence units:
  gdpr:art:4, 8, 15, 17, 20, 28, 33, 34, 37, 83; ai_act:rec:12, ai_act:art:5, 6, 27, 50, 53, 55, 73, 99.

## 3. Question text (R-Q)

- **R-Q1 No structural references.** The question must not contain article, recital, annex, chapter, section, paragraph
  or point numbers ("Article 8", "recital 26", "Annex III", "paragraph 2"). Real users do not know them and BM25 would
  match them trivially. Naming the regulation ("the GDPR", "the AI Act") is allowed. Exception: a deliberate
  `explicit_ref` question, at most 3 in the whole set, each justified in notes.
- **R-Q2 One real question.** One sentence ending with `?`, 8 to 40 words, a single information need (no "and also"
  questions with two unrelated asks; a multi_hop question may ask for two linked facts). English only.
- **R-Q3 Paraphrase, do not copy.** Write as an ordinary person or professional would ask, in your own words. Do not
  lift phrases from the evidence. Target lexical overlap (share of the question's content words found in the evidence)
  of 0.0 to 0.6; 0.6 to 0.8 is a warning, above 0.8 is not acceptable. At least 40% of questions must have overlap
  below 0.3. Defined terms may appear (for example "personal data", "high-risk") but the surrounding wording must differ.
- **R-Q4 Self-contained and unambiguous.** Understandable without the document; no "this article", "the above". If both
  regulations could plausibly answer, name the regulation. A competent reader of the evidence must arrive at one
  answer, not several.
- **R-Q5 Natural register.** No test-writer language ("According to the text...", "Which of the following..."). No
  trick questions, double negatives, or loaded premises, EXCEPT deliberate false-premise unanswerable questions (R-U).
- **R-Q6 Answerable from the two texts alone.** No external knowledge (other EU laws, national laws, the Charter,
  court rulings, current events, fines actually imposed).
- **R-Q7 No near-duplicates.** No two questions may ask the same thing in different words, nor use the same fact as
  their answer (token Jaccard similarity of content words below 0.6 is the automatic warning level).
- **R-Q8 Variety of form.** Mix who/what/when/how many/under what conditions/is it allowed/what happens if.
  No more than 30% of questions may start with the same word.

## 4. Gold evidence (R-E)

- **R-E1 Sufficient.** Reading only the quote(s) must be enough to derive the entire gold answer. Test: hide everything
  else; can you still answer? If not, the evidence is incomplete (typical mistake: quoting a sentence that ends with
  a colon but not the list item that completes it).
- **R-E2 Minimal and necessary.** Quote the shortest passage that is still sufficient, normally one sentence or one
  list item: target 40 to 300 characters, warning below 25 or above 400, never above 600. Every quoted piece must be
  needed; no padding with "context".
- **R-E3 Verbatim and unique.** Copy-paste from the `.jsonl` file, including curly quotes `‘ ’`. The quote must occur
  exactly once inside its unit (the checker enforces this). Never retype from memory or from a website.
- **R-E4 multi_hop needs distinct pieces.** At least two quotes, and they must come from different units or from clearly
  separate passages of one unit (gap of 400+ characters). Each piece is necessary and none alone answers the question.
  Both pieces come from the same regulation.
- **R-E5 Prefer operative text.** If an article states the point, cite the article, not a recital that explains it.
  Cite a recital only when no article states the point, or when the question is about the explanatory content that only the
  recital gives. Recitals are still allowed as evidence (R-B4) in those cases.
- **R-E6 Alternative evidence.** The evidence model supports one set of pieces that are ALL required. If another unit
  also answers the question, keep one as gold and record the other as `alt_evidence:<unit_id>` in notes. Better: rewrite
  the question so only one location answers it.
- **R-E7 Conditional questions quote both sides.** For `conflicting_or_conditional` the evidence must contain the rule
  and the exception/condition that changes the answer, each as its own quote.
- **R-E8 Numeric questions quote the number.** For `numeric_or_table` the quote contains the figure, unit or threshold
  exactly as in the text (for example `20 000 000 EUR`, `72 hours`, `six months`).

## 5. Gold answer (R-A)

- **R-A1 Supported.** Every statement in `gold_answer` must be supported by the quoted evidence. No extra facts, no
  hedges ("subject to exceptions") unless an exception is in the evidence. This is checked by deleting the evidence from
  view and asking whether any sentence of the answer would still be justified (it must not be).
- **R-A2 Short and plain.** One or two sentences, at most 60 words, in your own words, no quotation of whole articles.
- **R-A3 Exact numbers.** Numbers, units and thresholds are written as in the text (digits as the text writes them).
- **R-A4 Conditional answers name the condition.** State both the default and what changes it.
- **R-A5 Unanswerable answers.** Start with `Not specified` followed by one short reason, for example
  `Not specified: the text only states the storage-limitation principle without a number of days.`

## 6. Type rules (R-T, R-U)

- **R-T1 single_hop.** One quote, one unit, answer found in one place.
- **R-T2 multi_hop.** See R-E4. Typical patterns: definition + obligation, rule + procedure, requirement + deadline from
  another unit, two obligations that apply together. Not multi_hop: two sentences of the same list item.
- **R-T3 conflicting_or_conditional.** The correct answer is "it depends" or "yes, but": a general rule with an
  exception, or alternative cases with different outcomes. See R-E7 and R-A4.
- **R-T4 numeric_or_table.** The answer is a number, period, percentage, threshold or a small enumerated list of
  figures. See R-E8.
- **R-U1 Truly absent.** The answer must not be in the corpus. Verification is mandatory and must be recorded: search
  the `.jsonl` files for at least three keyword variants of the key concept (for example for retention: `retention`,
  `retain`, `kept for`, `storage period`, `days`), read the three most related units, and confirm none answers. Record
  the nearest misleading unit as `hard_negative:<unit_id>` in notes.
- **R-U2 Natural looking.** An unanswerable question must read exactly like an answerable one. Forbidden tell-tale words:
  `exact`, `exactly`, `specific`, `specifically`, `precise`, `single`, `universal`, `every single`, `maximum number
  of days` and similar. A system must not be able to detect "no answer" from phrasing.
- **R-U3 Variety of absence.** Across the set, unanswerable questions are mixed from these four kinds, and at most one
  third are of the "quantity not specified" kind: (a) topic not covered at all, (b) false premise (asks about a body,
  procedure or right the text does not create), (c) named entity not in the text (a specific country's authority, a
  company, a product), (d) quantity or detail not specified although the topic is covered.
- **R-U4 No evidence.** `gold_evidence` is empty; the answer follows R-A5; notes carry the doc tag, the kind (a-d) and
  `hard_negative`.

## 7. Split rules (R-S)

- **R-S1** Quotas per R-B2. Every question has exactly one split.
- **R-S2 Unit-level exclusivity.** A unit used as evidence in a dev question must never be used as evidence in a test
  question, and the reverse. The checker `python -m src.check_questions` enforces this on the whole file. Unanswerable
  questions have no evidence, so choose their hard negatives freely.
- **R-S3** Dev is for tuning. Test numbers are produced once, at the end, with `--final`. Nobody looks at test results
  while tuning.

## 8. Process rules (R-P)

- **R-P1 Write first, test never.** Questions must be written from the texts alone. It is forbidden to run any retrieval
  experiment (the runner, the inspector, BM25, embeddings) in order to select, reword, drop or relabel questions. A
  question may be changed after seeing system output only through a logged changelog entry (R-P4).
- **R-P2 Check tools.** Run `python -m src.check_questions` (format, quotes, types, split leakage) and
  `python -m src.audit_questions --existing <old file>` (this file's heuristics) after every writing session. ERROR lines must
  be fixed. WARN lines must be fixed or justified in notes.
- **R-P3 Human verification.** AI-drafted questions are drafts. The project owner reads every question, its evidence and
  its answer against the source text, then adds `verified:human` to notes, or edits/rejects the item. The report must state
  that 60 of 80 questions were AI-drafted and human-verified, and that 20 were human-written.
- **R-P4 Changelog.** Any edit of a question after it was first committed is recorded in `eval/CHANGELOG.md`
  (date, id, what, why, whether system output had been seen).
- **R-P5 Stable ids.** Never delete and renumber. A rejected question is replaced by a new id.

## 9. Supervisor procedure (for the person or bot auditing the set)

Automated tools do not replace reading. For every one of the 60 new questions, report one line per rule with
PASS / FAIL / UNSURE and a one-sentence reason. Run these five tests, which no script can do:

1. **Answerability test (R-E1, R-A1).** Read only the quotes. Can you write the gold answer, and is every statement of the
   gold answer justified by them? Report unsupported statements.
2. **Necessity test (R-E2, R-E4).** Remove each quote in turn. Does the answer break? A quote whose removal changes nothing is
   padding. For multi_hop, confirm no single quote suffices.
3. **Paraphrase test (R-Q3).** Is the question phrased differently from the evidence, or has wording been copied?
4. **Ambiguity test (R-Q4, R-E6).** Could a careful reader find a different location or answer in the two texts? Search for
   key terms in the `.jsonl` files and name any competing unit.
5. **Absence test (R-U1).** For each unanswerable question, search independently (do not trust the notes), name the nearest
   unit, and state whether it answers. Any doubt is FAIL.

Then report: counts per type / split / document against R-B1 to R-B3, the number of distinct evidence units and the share of
recital evidence (R-B4), any structural reference (R-Q1), any tell-tale word in unanswerable questions (R-U2), the starting-word
distribution (R-Q8), and the list of FAIL items with a suggested fix. Do not rewrite questions silently: propose changes.

## 10. What the scripts check

| Rule | `check_questions` | `audit_questions` | needs a reader |
|---|---|---|---|
| R-F1 to R-F4, R-S2, R-T (evidence counts), R-E3 quote exists and is unique | yes | | |
| R-F5 tags | | yes | |
| R-B1 to R-B5 | | yes (`--check-quotas`) | partly |
| R-Q1, R-Q2, R-Q3, R-Q7, R-Q8 | | yes | R-Q4, R-Q5, R-Q6 |
| R-E2 length, R-E4 distinct pieces, R-E8 numbers | | yes | R-E1, R-E5, R-E6, R-E7 |
| R-A2, R-A3, R-A5 | | yes | R-A1, R-A4 |
| R-U2 tell-tale words, R-U1 first-pass screen | | yes | R-U1 final decision, R-U3 |
| R-P3, R-P4 | | | yes |

## 11. Known limitations (accepted, to be stated in the report)

- Gold evidence is one set of pieces; alternative locations are only noted (R-E6).
- A retrieved chunk counts as a hit when it overlaps the evidence by at least one character; the report adds a
  coverage-based check.
- 80 questions give wide confidence intervals; differences between methods must be read with the intervals.
- 60 questions were drafted by an AI model and verified by the project owner; the 20 human-written questions can be
  analysed separately to check that the drafting source does not change the conclusions.
