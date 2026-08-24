# Evaluation Summary

A `gpt-4o-mini` extraction system was evaluated on 15 synthetic loan rejection letters, scored by two deterministic exact match evaluators (one per output field) and two LLM as judge correctness evaluators (one OpenAI, one DeepSeek). The first dataset produced a ceiling effect: every evaluator scored 15 out of 15, which meant the dataset had not been shown to measure anything. A second version was written with the signposting removed, meaning the sentences in which each letter named the factor that had been decisive. On that harder dataset the system scored 14 out of 15 on `reason_code` and 15 out of 15 on `manual_review_offered`, with both judges agreeing with exact match on every example.

## Scores

| Evaluator | v1 | v2 |
|---|---|---|
| reason_code_exact | 15/15 | 14/15 |
| manual_review_exact | 15/15 | 15/15 |
| correctness (OpenAI judge) | 15/15 | 14/15 |
| deepseek_correctness (DeepSeek judge) | 15/15 | 14/15 |

Run cost, 15 examples: v1 0.00075 USD, v2 0.00069 USD. Mean latency under 1 second in both runs.

## The single failure

Letter 2, v2. Ground truth `credit_score`, system answered `incomplete_application`. The v1 wording named the credit reference agency explicitly; the v2 wording reduced this to an unnamed agency returning information that did not meet the required profile. The system appears to have read the withheld detail as missing paperwork. Both judges marked it incorrect, agreeing with exact match.

## What the results do not support

One failure out of fifteen is thin evidence. No claim about where the system breaks down should be built on a single example, and no per category accuracy is reported here because with two or three examples per reason code such figures would be noise.

Two designed hypotheses were not confirmed. Letter 13 was written to test whether the system could distinguish a complaints or ombudsman route from a review of the lending decision itself; it was answered correctly in both versions, including after the clarifying sentence was removed. More broadly, `manual_review_offered` was answered correctly on all 30 examples across both runs, so the field discriminates nothing at this difficulty and the dataset provides no evidence about it either way.

The two judges never disagreed, with each other or with exact match, across 30 examples. The DeepSeek judge was introduced specifically to control for self preference bias, an OpenAI judge grading OpenAI output being liable to favour it. With no disagreements, no bias was observed, but neither was any evidence gathered that would have detected it. The control is sound and the result is null.

## Limitations

The letters are synthetic and were written by the same process that defined the label taxonomy, so the ground truth may be easier to recover than it would be in real correspondence. Real rejection letters were not used because they are personal data and no lawful basis under GDPR Article 6 exists for processing them here.

Two labels are contestable and were fixed by judgment rather than derived: letter 6 names both low income and short tenure with no tiebreaker, and letter 13 turns on whether a complaints procedure counts as a manual review. Both are recorded as `ambiguous`.

The DeepSeek judge is hand written rather than built with `openevals`, because DeepSeek's API supports a plain JSON output mode but not the strict schema mode that `create_llm_as_judge` requests. The two judges therefore differ in prompt as well as in model, and are not a clean controlled comparison.
