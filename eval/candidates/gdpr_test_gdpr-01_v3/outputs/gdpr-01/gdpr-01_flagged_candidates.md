# Flagged or Questionable Candidates — Batch `gdpr-01` (Q121–Q138)

## Summary

- **Unmet Quotas / Gaps:** `0` (all 13 active joint quota cells in `gdpr-01` are satisfied without fabricating legal facts).
- **Hard Rule Violations:** `0` (all verbatim quotes occur exactly once in `data/processed/gdpr.jsonl`, zero excluded units used, zero R-Q1/R-Q2/R-Q3/R-E2/R-A2/R-U2 violations).
- **Items Flagged for Targeted Human Legal Review (`human_review:pending`):** `2` borderline review notes below (not rule violations, surfaced transparently for independent legal review).

## Items Flagged for Legal Reviewer Attention

1. **Q128 (`multi_hop` | `article_only` | `low`, overlap `0.2500`) — Pronoun Antecedent in Minimal Quote (`gdpr:art:26`)**
   - **Observation:** The first quote from `gdpr:art:26` begins with `They shall in a transparent manner determine their respective responsibilities...` (336 chars) rather than including the preceding 118-char sentence defining `joint controllers`, in order to stay below the 400-char R-E2 warning threshold (combined length would be 455 chars).
   - **Reviewer Check:** Confirm whether `gdpr:art:26` paragraph 1's second sentence is sufficiently self-contained for R-E1 (it explicitly references `respective responsibilities`, `arrangement between them`, and `Articles 13 and 14`), or whether the reviewer prefers extending the quote to include the opening definition sentence (455 chars, still well under the 600-char hard cap).

2. **Q130 (`conflicting_or_conditional` | `article_only` | `high`) — Scope of `gdpr:art:14(5)` Exceptions**
   - **Observation:** `gdpr:art:14(5)` lists four exceptions `(a)`–`(d)`. The question is deliberately scoped to exception `(a)` (`if the individual already possesses that information`) so that quoting `gdpr:art:14(1)(a)` and `gdpr:art:14(5)(a)` is strictly sufficient and minimal without needing to quote all four subparagraphs.
   - **Reviewer Check:** Confirm that scoping the question to the `already possesses that information` condition preserves a genuine conditional structure (default rule + exception) without feeling overly narrow.
