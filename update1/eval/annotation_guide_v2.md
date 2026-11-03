# Annotation guide (v2, replaces the chunk-id version)

File: `eval/questions.csv` (copy `questions_v2_template.csv`, delete the example row).
Columns: `id, split, type, question, gold_answer, gold_evidence, notes`.

## gold_evidence format
`unit_id::verbatim quote`, several pieces separated by ` || `.

- unit ids: `gdpr:art:33` (Article 33), `gdpr:rec:26` (recital 26), `ai_act:art:5`, `ai_act:rec:12`.
- The quote must be copied from `data/processed/*.jsonl`, exactly (including curly quotes).
- Quote the shortest passage that really answers the question (usually one sentence).
- The quote must occur once inside that unit. If not, make it longer.
- Why quotes and not chunk ids: chunk size is our experimental variable, so chunk ids change between
  experiments. Quotes are resolved to character spans automatically and stay valid.
- Gold evidence comes from the core texts only (GDPR, AI Act). If later you add guidance documents to the
  search index, they act as distractors and are never gold evidence. State this limitation in the report.

## Types and target mix (150-300 questions)
| type | share | evidence rule |
|---|---|---|
| single_hop | 30% | 1 piece |
| multi_hop | 25% | 2+ pieces, from different places |
| unanswerable | 15% | NO evidence; the texts really do not contain the answer |
| conflicting_or_conditional | 15% | include the rule and its exception |
| numeric_or_table | 15% | numbers, deadlines, fines, thresholds |

## Rules
1. Write the question first, then find the evidence. Never answer from memory.
2. Questions must be answerable from the text alone, without knowing the article number. Do not put
   "Article 33" into the question; real users do not know it, and BM25 would match it trivially.
   (Some questions with explicit article numbers can be tagged in `notes` as `explicit_ref`.)
3. Split: `dev` for tuning, `test` for final numbers only. Decide the split when you write the question, e.g. 50/50.
   Do not look at test results while tuning.
4. Re-annotate about 20% a few days later without looking, and report your own agreement.
5. Keep a changelog of every question edited after you have seen system outputs.
6. Run `python -m src.check_questions` after every annotation session.
7. Unanswerable questions are scored separately (do the system's answers say "not stated"?), not with recall.
