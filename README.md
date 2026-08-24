**Lab:** Micromanage your agents · Module 5, Evaluation & strategy · Week 7, Day 4
**Submission by:** GordanSkopljak

# Custom Dataset Creation and Evaluation with LangSmith

## Domain

The system under evaluation reads a retail bank loan rejection letter and extracts two fields:

- `reason_code`, the primary reason the application was rejected, drawn from a closed set of six values: `credit_score`, `debt_to_income`, `insufficient_income`, `employment_history`, `incomplete_application`, `collateral_value`
- `manual_review_offered`, whether the letter offers the applicant a review of the lending decision itself, `yes` or `no`

Structured extraction against a closed taxonomy was chosen deliberately. Correctness has a defensible answer, which a correctness evaluator needs; a more subjective domain would have produced scores that were noise.

All 15 letters are synthetic and were written for this lab. Real rejection letters are personal data and no lawful basis under GDPR Article 6 exists for processing them here. This is a genuine limitation on the results, not a formality, and is discussed in `evaluation_summary.md`.

## Approach

Four evaluators score every example on the main path:

- `reason_code_exact` and `manual_review_exact`, deterministic string comparison, one per output field
- `correctness`, LLM as judge built with `openevals` and the `CORRECTNESS_PROMPT`, judged by `gpt-4o-mini`
- `deepseek_correctness`, a hand written LLM as judge using DeepSeek

The deterministic evaluators exist because comparing two values from a closed set does not require judgment, and a string comparison cannot be biased. The DeepSeek judge exists to control for self preference bias: an OpenAI judge grading OpenAI output may favour it. It is hand written because DeepSeek's API supports a plain JSON output mode but not the strict schema mode `create_llm_as_judge` requests.

Three experiments were run on the main path:

1. `gpt-4o-mini` on the v1 dataset. Every evaluator scored 15 out of 15, a ceiling effect showing the dataset was too easy to measure anything.
2. `gpt-4o-mini` on the v2 dataset, rewritten with the signposting sentences removed. 14 out of 15 on `reason_code`.
3. `gpt-4o` on the v2 dataset, holding everything else constant. 15 out of 15, at roughly sixteen times the cost.

### Custom evaluator, faithfulness (optional)

A separate evaluator, `faithfulness`, was designed to measure a dimension beyond correctness, then run on the v2 dataset alongside correctness in one experiment. Correctness compares the answer to the reference label. Faithfulness compares the answer to the letter text and never sees the label, so it catches an answer that is not grounded in the source. It was validated with a negative control before use, confirming it returns false on injected wrong codes rather than agreeing with everything. On this dataset it agreed with correctness on all 15 examples, an honest null. Full design, comparison and reflection are in `custom_evaluator.md`.

### Reviewing results in the UI

Notes from the LangSmith interface review, the per example drill down into the one failing letter, and the patterns that drove the v2 hardening are in `ui_review.md`.

## How to run

Requires Python with `langsmith`, `openai`, `openevals` and `python-dotenv`. Create a `.env` file at the repo root containing `LANGSMITH_API_KEY`, `OPENAI_API_KEY` and `DEEPSEEK_API_KEY`. The `.env` file is git ignored and no keys are committed.

```
python check_setup.py                    # verify the LangSmith connection
python upload_dataset.py                 # create the v1 dataset
python upload_dataset_v2.py              # create the v2 dataset
python run_evaluation.py                 # evaluate gpt-4o-mini, four evaluators
python run_comparison.py                 # evaluate gpt-4o on the same dataset
python smoke_test_faithfulness.py        # try the faithfulness judge on 3 letters
python run_custom_evaluator.py           # faithfulness plus correctness on v2
python negative_control_faithfulness.py  # validate the faithfulness judge
```

`run_evaluation.py` is currently pointed at the v2 dataset. To reproduce the v1 run, change `DATASET_NAME` and `experiment_prefix` at the top and bottom of that file.

## LangSmith links

- Dataset v1: https://eu.smith.langchain.com/o/8907f334-2752-4484-a44b-7c59566a0f41/datasets/9ecdf80b-e679-456c-8dd1-0d815bfaa866
- Dataset v2: https://eu.smith.langchain.com/o/8907f334-2752-4484-a44b-7c59566a0f41/datasets/05189410-e578-4cfc-8364-0b253b178996
- Experiment `gpt-4o-mini-baseline-82840908`, v1: https://eu.smith.langchain.com/o/8907f334-2752-4484-a44b-7c59566a0f41/datasets/9ecdf80b-e679-456c-8dd1-0d815bfaa866/compare?selectedSessions=c4e8a5bd-4544-4288-9518-2b4e231301d4
- Experiment `gpt-4o-mini-v2-cce7dff3`: https://eu.smith.langchain.com/o/8907f334-2752-4484-a44b-7c59566a0f41/datasets/05189410-e578-4cfc-8364-0b253b178996/compare?selectedSessions=fe3d7a7e-b629-4173-9b79-b2bc93b0255a
- Experiment `gpt-4o-v2-705cd4da`: https://eu.smith.langchain.com/o/8907f334-2752-4484-a44b-7c59566a0f41/datasets/05189410-e578-4cfc-8364-0b253b178996/compare?selectedSessions=1d38ca39-ef0d-47ea-a6a7-fa970bd2f090
- Experiment `gpt-4o-mini-v2-faithfulness-cd9393f7`, custom evaluator: https://eu.smith.langchain.com/o/8907f334-2752-4484-a44b-7c59566a0f41/datasets/05189410-e578-4cfc-8364-0b253b178996/compare?selectedSessions=b8c1bc88-5b0f-4232-a42f-0ab81febb0af

## Files

| File | Purpose |
|---|---|
| `dataset_documentation.md` | Domain choice, schema, taxonomy and diversity rationale |
| `evaluation_summary.md` | Results, the single failure, and what the results do not support |
| `optimization_summary.md` | The `gpt-4o-mini` against `gpt-4o` comparison |
| `custom_evaluator.md` | The faithfulness evaluator: design, comparison with correctness, reflection |
| `ui_review.md` | Notes from the LangSmith UI review |
| `letters.json` | The 15 v1 letters with ground truth labels |
| `letters_v2.json` | The hardened v2 letters, same labels, signposting removed |
| `check_setup.py` | LangSmith connection check |
| `upload_dataset.py` | Creates the v1 dataset in LangSmith |
| `upload_dataset_v2.py` | Creates the v2 dataset in LangSmith |
| `target_function.py` | The system under evaluation |
| `run_evaluation.py` | The four evaluators and the evaluation run |
| `run_comparison.py` | The A/B run with the model swapped |
| `smoke_test_faithfulness.py` | Tries the faithfulness judge on 3 letters |
| `run_custom_evaluator.py` | Faithfulness plus correctness on the v2 dataset |
| `negative_control_faithfulness.py` | Validates that the faithfulness judge discriminates |
| `instructions.md`, `rubric.md` | Lab brief and grading rubric, provided |
