"""
Steps 6 and 7: evaluators and the evaluation run.

Four evaluators:
  1. reason_code_exact        deterministic string comparison
  2. manual_review_exact      deterministic string comparison
  3. correctness              LLM as judge via openevals, OpenAI judge
  4. deepseek_correctness     hand written LLM as judge, DeepSeek judge

The two judges score the same outputs. Comparing them, and comparing both
against the deterministic evaluators, is the point: an OpenAI judge marking
OpenAI output is exposed to self preference bias, a DeepSeek judge is not.

Note on DeepSeek: its API supports a plain JSON output mode but not the strict
schema mode that openevals requests, which is why judge 4 is written by hand.
Its API also requires the word "json" to appear in the prompt.
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


def manual_review_exact(outputs: dict, reference_outputs: dict):
    match = outputs.get("manual_review_offered") == reference_outputs.get(
        "manual_review_offered"
    )
    return {"key": "manual_review_exact", "score": bool(match)}


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


deepseek_client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com",
)

DEEPSEEK_JUDGE_PROMPT = """You are grading a structured extraction system.

The system read a loan rejection letter and returned two fields: the primary
rejection reason code, and whether the letter offers a manual review of the
lending decision.

Compare the system output against the reference answer. The output is correct
only if both fields match the reference in meaning.

Reply with json in exactly this shape and nothing else:
{"correct": true or false, "reason": "one short sentence"}"""


def deepseek_correctness(inputs: dict, outputs: dict, reference_outputs: dict):
    user_message = (
        "Letter:\n"
        + inputs.get("letter", "")
        + "\n\nSystem output (json):\n"
        + json.dumps(outputs)
        + "\n\nReference answer (json):\n"
        + json.dumps(reference_outputs)
    )

    try:
        response = deepseek_client.chat.completions.create(
            model="deepseek-chat",
            temperature=0,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": DEEPSEEK_JUDGE_PROMPT},
                {"role": "user", "content": user_message},
            ],
        )
        verdict = json.loads(response.choices[0].message.content)
        return {
            "key": "deepseek_correctness",
            "score": bool(verdict.get("correct")),
            "comment": str(verdict.get("reason", "")),
        }
    except Exception as exc:
        return {
            "key": "deepseek_correctness",
            "score": None,
            "comment": "judge call failed: " + str(exc),
        }


if __name__ == "__main__":
    results = client.evaluate(
        target,
        data=DATASET_NAME,
        evaluators=[
            reason_code_exact,
            manual_review_exact,
            correctness_evaluator,
            deepseek_correctness,
        ],
        experiment_prefix="gpt-4o-mini-v2",
        max_concurrency=2,
    )

    print("Evaluation finished.")
    print("Experiment name:", getattr(results, "experiment_name", "see LangSmith UI"))
