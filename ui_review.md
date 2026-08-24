# Step 8: Review Results in LangSmith UI

Notes from reviewing the evaluation experiments in the LangSmith web interface.
Endpoint: eu.smith.langchain.com. Project: loan-letter-extraction. Dataset:
loan-rejection-letters and its v2 variant.

## Navigating to the results

Each `client.evaluate` run appears under the dataset's Experiments tab. Opening an
experiment shows the summary view first: one row per example, one column per
evaluator, with the aggregate score for each evaluator across the top. The compare
view (linked from each run) puts experiments side by side on the same 15 examples.

## Aggregate metrics observed

| Experiment | reason_code_exact | manual_review_exact | correctness | deepseek_correctness |
|---|---|---|---|---|
| gpt-4o-mini baseline (v1) | 15/15 | 15/15 | 15/15 | 15/15 |
| gpt-4o-mini (v2) | 14/15 | 15/15 | 14/15 | 14/15 |
| gpt-4o (v2) | 15/15 | 15/15 | 15/15 | 15/15 |

First observation from the summary view: the v1 dataset produced a perfect score
on every evaluator. That is not a strength, it is a signal that the v1 letters
signposted the answer too heavily. It is the reason the v2 dataset exists.

## Examining individual examples

The per example rows are where the UI earns its place. Clicking a row expands the
input letter, the model output json, and each evaluator's score with its comment.

On the v2 gpt-4o-mini run, 14 of 15 rows were green across the board. The one red
row was letter 2 (Ms Brandt). Drilling into it:
- Reference reason_code: credit_score
- Model output: incomplete_application
- Both LLM judges agreed with the deterministic evaluator that this was wrong,
  and their comments pointed at the same thing: v2 reduced the named credit agency
  to an unnamed one, and the model read the withheld detail as missing paperwork.

The manual_review_offered field was correct on all 15 in every run, so in the UI
that column is a flat wall of green. It discriminates nothing on this dataset.

## Patterns and interesting examples

- Clear vs ambiguous: every failure sits on an ambiguous letter. The clear letters
  never failed. The difficulty metadata tracks real difficulty.
- Letter 2 is the example to keep investigating. It is the only one that fails, and
  it is not even stable, it flips between correct and incorrect across runs at
  temperature 0. It is the single most informative row in the dataset.
- Letter 13 (the ombudsman referral) was a designed trap for manual_review_offered.
  The UI shows it passing in every run, so the trap did not catch the model.

## What the UI review fed into

The per example drill down on letter 2 is what the analysis in
`evaluation_summary.md` is built on, and the ambiguous only failure pattern is
what justified the v2 hardening and the gpt-4o comparison in
`optimization_summary.md`.
