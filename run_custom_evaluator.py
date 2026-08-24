"""
Steps 11 and 12: run the custom faithfulness evaluator alongside correctness.

Three scorers on the v2 dataset, in one experiment so they can be compared:
  1. reason_code_exact   deterministic, answer vs reference label
  2. correctness         LLM judge, answer vs reference label (openevals)
  3. faithfulness        LLM judge, answer vs the LETTER TEXT, label not seen

The point of Step 12 is the comparison. Correctness asks "does the answer match
the label". Faithfulness asks "does the letter actually support the answer".
They can disagree: a wrong answer can still be grounded in a misreading of the
letter, and a right answer could in principle be an ungrounded lucky guess.
"""

import json
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_ENDPOINT"] = "https://eu.api.smith.langchain.com"
os.environ["LANGSMITH_PROJECT"] = "loan-letter-extraction"

from langsmith import Client
from openai import OpenAI
from openevals.llm import create_llm_as_judge
from openevals.prompts import CORRECTNESS_PROMPT

from target_function import target

DATASET_NAME = "loan-rejection-letters-v2"

client = Client()


def reason_code_exact(outputs: dict, reference_outputs: dict):
    match = outputs.get("reason_code") == reference_outputs.get("reason_code")
    return {"key": "reason_code_exact", "score": bool(match)}


openai_judge = create_llm_as_judge(
    prompt=CORRECTNESS_PROMPT,
    feedback_key="correctness",
    model="openai:gpt-4o-mini",
)


def correctness_evaluator(inputs: dict, outputs: dict, reference_outputs: dict):
    return openai_judge(
        inputs=inputs,
        outputs=outputs,
        reference_outputs=reference_outputs,
    )


# The custom evaluator. Note it ignores reference_outputs by design.
FAITHFULNESS_PROMPT = """You are auditing a structured extraction system for FAITHFULNESS, not correctness.

The system read a retail bank loan rejection letter and selected exactly one
primary rejection reason code from this fixed set:
credit_score, debt_to_income, insufficient_income, employment_history,
incomplete_application, collateral_value.

Your only question: is the selected reason_code supported by the text of the
letter itself?

Score faithful = true if the letter contains wording that states or clearly
implies that this reason is the basis for the rejection.
Score faithful = false if the letter does not support this reason, that is, the
reason is not mentioned, or the letter clearly points to a different reason. Do
not reward a guess that merely happens to be a common rejection reason.

You are NOT given the reference answer and must not assume one. Judge only the
letter text against the selected reason_code.

Reply with json in exactly this shape and nothing else:
{"faithful": true or false, "reason": "one short sentence pointing to the supporting or missing text"}"""

faithfulness_client = OpenAI()


def faithfulness_evaluator(inputs: dict, outputs: dict, reference_outputs: dict):
    user_message = (
        "Letter:\n"
        + inputs.get("letter", "")
        + "\n\nThe system selected this reason_code: "
        + str(outputs.get("reason_code", ""))
    )
    try:
        response = faithfulness_client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": FAITHFULNESS_PROMPT},
                {"role": "user", "content": user_message},
            ],
        )
        verdict = json.loads(response.choices[0].message.content)
        return {
            "key": "faithfulness",
            "score": bool(verdict.get("faithful")),
            "comment": str(verdict.get("reason", "")),
        }
    except Exception as exc:
        return {
            "key": "faithfulness",
            "score": None,
            "comment": "judge call failed: " + str(exc),
        }


if __name__ == "__main__":
    results = client.evaluate(
        target,
        data=DATASET_NAME,
        evaluators=[
            reason_code_exact,
            correctness_evaluator,
            faithfulness_evaluator,
        ],
        experiment_prefix="gpt-4o-mini-v2-faithfulness",
        max_concurrency=2,
    )

    print("Evaluation finished.")
    print("Experiment name:", getattr(results, "experiment_name", "see LangSmith UI"))
