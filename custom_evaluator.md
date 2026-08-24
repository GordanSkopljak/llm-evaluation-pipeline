# Custom Evaluator: Faithfulness

This document covers the optional custom evaluator work: the design of an
evaluator beyond correctness (Step 11), running it alongside correctness and
comparing (Step 12), and the findings and reflection (Step 13).

Code: `run_custom_evaluator.py`, with validation in `smoke_test_faithfulness.py`
and `negative_control_faithfulness.py`.

## Step 11: Design of the custom evaluator

### What it measures

The dimension is **faithfulness**, also called grounding. It is different from
correctness. Correctness compares the model answer to the reference label in the
dataset. Faithfulness never sees the label. It asks a separate question: does the
text of the letter itself support the `reason_code` the model chose, or did the
model output a plausible reason the letter does not actually state?

This matters for an extraction task in a regulated domain. A model can return an
answer that happens to match a label by guessing, and a model can return a wrong
answer that is still a reasonable reading of the letter. Correctness alone does
not separate a grounded answer from a lucky one. Faithfulness does.

### Evaluator prompt and scoring

The evaluator is an LLM as judge using `gpt-4o-mini` at temperature 0, with a
hand written prompt. The judge is given the letter and the reason_code the model
selected, and explicitly is not given the reference answer. It returns a binary
score and a one sentence justification.

Scoring:
- `faithful = true` when the letter contains wording that states or clearly
  implies the selected reason is the basis for the rejection.
- `faithful = false` when the letter does not support the selected reason, that
  is, the reason is absent or the letter points to a different reason.

Output shape from the judge:

```
{"faithful": true or false, "reason": "one short sentence pointing to the supporting or missing text"}
```

The full prompt is in `run_custom_evaluator.py` as `FAITHFULNESS_PROMPT`.

### Testing the evaluator

Two validation passes were run before trusting the judge.

Smoke test (`smoke_test_faithfulness.py`), 3 real cases, model output judged:

| Letter | Model picked | Faithful | Judge reasoning |
|---|---|---|---|
| 1 (clear) | credit_score | true | rating recorded does not reach the level required |
| 3 (clear) | debt_to_income | true | obligations would absorb a greater share of net income than permitted |
| 2 (ambiguous) | credit_score | true | information returned did not meet the profile required |

All three faithful, which is correct since each pick is grounded. But a judge
that only ever returns true would produce the same output, so a negative control
was added.

Negative control (`negative_control_faithfulness.py`): real letters paired with a
reason_code injected by us that is wrong for that letter, plus one correct pair.

| Letter | Injected code | Expected | Judge said | Result |
|---|---|---|---|---|
| 1 (credit_score) | collateral_value | false | false | pass |
| 3 (debt_to_income) | employment_history | false | false | pass |
| 5 (insufficient_income) | incomplete_application | false | false | pass |
| 1 (credit_score) | credit_score | true | true | pass |

4 of 4 as expected. The judge moves in both directions and its reasoning cites
the actual letter text. This is evaluator validation, not model output. The wrong
codes were injected on purpose to test the judge.

## Step 12: Run with correctness and compare

The evaluator was run on the v2 dataset (`loan-rejection-letters-v2`) together
with two correctness scorers, in a single experiment so the columns line up.

- Experiment: `gpt-4o-mini-v2-faithfulness-cd9393f7`
- Link: https://eu.smith.langchain.com/o/8907f334-2752-4484-a44b-7c59566a0f41/datasets/05189410-e578-4cfc-8364-0b253b178996/compare?selectedSessions=b8c1bc88-5b0f-4232-a42f-0ab81febb0af
- Export: `gpt-4o-mini-v2-faithfulness-cd9393f7.csv`

| Scorer | What it compares | Score |
|---|---|---|
| reason_code_exact | answer vs label, deterministic | 15 / 15 |
| correctness | answer vs label, LLM judge | 15 / 15 |
| faithfulness | answer vs letter text, LLM judge | 15 / 15 |

Divergences between correctness and faithfulness: **0 of 15**.

### Where the two could have diverged

The one letter capable of splitting the two scorers is letter 2. In an earlier v2
run the model read a withheld credit agency as missing paperwork and answered
`incomplete_application`, which is wrong against the label but arguably still
grounded in the letter's mention of withheld information. That is the profile of a
correctness fail with a faithfulness pass. In this run letter 2 answered
`credit_score` and passed both, so the split did not occur. The model output on
letter 2 is not stable at temperature 0, it flips between runs.

## Step 13: Findings and reflection

What the custom evaluator revealed on this dataset: nothing that correctness did
not already show. Faithfulness agreed with correctness on all 15 examples. On a
dataset where the model answers correctly and never invents an ungrounded reason,
a faithfulness judge adds no separating signal.

That is an honest null, and it is worth stating rather than dressing up. The value
of a faithfulness evaluator appears on a different failure mode than this dataset
produces. It catches hallucinated reasons, answers with no support in the source.
This dataset's one real failure, letter 2, is the opposite kind of error: a
misreading that stays grounded in the text. Faithfulness would pass that failure,
not catch it. So on this specific task, faithfulness is a weaker safety net than
correctness, not a stronger one.

Where faithfulness would earn its place: a production setting with no reference
labels, where correctness cannot be computed at all because there is no ground
truth to compare against. There, a grounding check is one of the few automated
signals available, and the negative control shows it is a real signal rather than
a judge that always agrees.
