# Annotation guide

Target: 150-300 questions. Aim for roughly this mix:

| type | share | description |
|---|---|---|
| single_hop | 30% | answer is in one passage |
| multi_hop | 25% | needs two or more passages (e.g. a definition + an obligation) |
| unanswerable | 15% | the texts do not contain the answer; correct behaviour is to say so |
| conflicting_or_conditional | 15% | answer depends on conditions/exceptions in the text |
| numeric_or_table | 15% | numbers, thresholds, deadlines, fines |

Rules
1. Write the question first, then locate evidence in the source text. Record evidence chunk ids.
2. Gold answers must be checkable against the source. Never rely on memory.
3. Split into `dev` (tune things) and `test` (final numbers only). Do not look at test while tuning.
4. Re-annotate 20% of questions a few days later without looking; report your own agreement.
5. Keep a changelog of any question you edit after seeing system outputs.
