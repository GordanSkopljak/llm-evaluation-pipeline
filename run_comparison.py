"""
A/B comparison: the same v2 dataset and the same four evaluators, but the
system under test runs on gpt-4o instead of gpt-4o-mini.

Everything else is held constant, so any score difference is attributable to
the model swap.
"""

import target_function

target_function.MODEL = "gpt-4o"

from target_function import target

import run_evaluation
from run_evaluation import (
    client,
    reason_code_exact,
    manual_review_exact,
    correctness_evaluator,
    deepseek_correctness,
)

DATASET_NAME = "loan-rejection-letters-v2"

if __name__ == "__main__":
    print("System under test is running on:", target_function.MODEL)

    results = client.evaluate(
        target,
        data=DATASET_NAME,
        evaluators=[
            reason_code_exact,
            manual_review_exact,
            correctness_evaluator,
            deepseek_correctness,
        ],
        experiment_prefix="gpt-4o-v2",
        max_concurrency=2,
    )

    print("Evaluation finished.")
    print("Experiment name:", getattr(results, "experiment_name", "see LangSmith UI"))
