"""
Step 5: the target function under evaluation.

Takes one loan rejection letter and returns the primary rejection reason code
and whether a manual review of the lending decision is offered.

Run this file directly to smoke test it on a single letter before evaluating.
"""

import json
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_ENDPOINT"] = "https://eu.api.smith.langchain.com"
os.environ["LANGSMITH_PROJECT"] = "loan-letter-extraction"

from langsmith import traceable
from langsmith.wrappers import wrap_openai
from openai import OpenAI

openai_client = wrap_openai(OpenAI())

MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = """You extract structured data from retail bank loan rejection letters.

Return the primary reason the application was rejected, using exactly one of
these codes:

credit_score, debt_to_income, insufficient_income, employment_history,
incomplete_application, collateral_value

Also return whether the letter offers the applicant a manual review or
reconsideration of the lending decision itself. Answer "yes" or "no".

Respond with JSON only, no other text, in this exact shape:
{"reason_code": "...", "manual_review_offered": "..."}"""


@traceable
def extract_fields(letter: str) -> dict:
    response = openai_client.chat.completions.create(
        model=MODEL,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": letter},
        ],
    )
    return json.loads(response.choices[0].message.content)


def target(inputs: dict) -> dict:
    return extract_fields(inputs["letter"])


if __name__ == "__main__":
    with open("letters.json", "r", encoding="utf-8") as f:
        letters = json.load(f)

    test_letter = letters[0]

    result = target({"letter": test_letter["letter"]})

    print("Letter id:", test_letter["id"])
    print("Model returned:", result)
    print("Ground truth:  ", {
        "reason_code": test_letter["reason_code"],
        "manual_review_offered": test_letter["manual_review_offered"],
    })
