# Flagged Candidates for Independent Legal Review — Batch `gdpr-02` (Q139–Q156)

## Summary

- **Unmet Quotas / Gaps:** `0` (all 13 active joint quota cells in `gdpr-02` are satisfied without fabricating legal facts).
- **Hard Rule Violations:** `0` (all verbatim quotes occur exactly once in `data/processed/gdpr.jsonl`, zero excluded units out of 146 used, zero R-Q1/R-Q2/R-Q3/R-A2/R-U2 violations).
- **Items Surfaced for Targeted Independent Legal Review (`human_review:pending`):** `3` transparent review notes below.

## Items for Reviewer Attention

1. **Q154 (`numeric_or_table` | `recital_only` | `low`, `gdpr:rec:172`) — Calendar Date as `numeric_or_table` in Recital-Only Slot**
   - **Observation:** After excluding all 146 reserved units (including `gdpr:rec:171` used in `gdpr-01`), the remaining non-excluded recitals containing numeric durations/thresholds (`gdpr:rec:13` 250 employees, `gdpr:rec:85` 72 hours, `gdpr:rec:136` two-thirds majority, `gdpr:rec:137` three months) all duplicate operative Articles (R-E5 preference). `gdpr:rec:172` (`7 March 2012`) is strictly recital-only with zero article duplication.
   - **Reviewer Check:** Confirm that the exact calendar date `7 March 2012` satisfies `numeric_or_table` for this recital-only slot, or advise if a recital with a duration/threshold that echoes an excluded article is preferred.

2. **Q152 (`numeric_or_table` | `article_only` | `low`, `gdpr:art:92`) — Quote Length Soft Warning (424 chars)**
   - **Observation:** The first sentence of `gdpr:art:92(5)` is 424 characters (24 characters above the 400-char R-E2 soft warning threshold, well below the 600-char hard cap), retained unbroken to preserve the full legal condition for delegated-act entry into force alongside the `three months` objection period.
   - **Reviewer Check:** Confirm keeping the complete sentence (424 chars) is preferable to mid-sentence truncation.

3. **Q149 (`conflicting_or_conditional` | `article_only` | `low`, `gdpr:art:49`) — Context of Article 49(1) Intro Clause**
   - **Observation:** Quote 1 begins at `(g) the transfer is made from a register...` (397 chars) and Quote 2 cites `gdpr:art:49(2)` (384 chars) so both stay under 400 characters. The question explicitly scopes to `the GDPR's register derogation` for transfers outside Europe.
   - **Reviewer Check:** Confirm whether quoting `(g)` + paragraph 2 is sufficiently self-contained for R-E1, or if adding the 308-char opening clause of `gdpr:art:49(1)` (`In the absence of an adequacy decision...`) as a third quote is preferred.
