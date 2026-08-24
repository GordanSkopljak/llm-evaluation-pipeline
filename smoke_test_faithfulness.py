"""
Step 11 smoke test: the custom faithfulness evaluator, tried on 3 letters.

Faithfulness is not correctness. Correctness compares the model answer to the
reference label. Faithfulness never sees the label. It asks only one thing:
does the letter text itself support the reason_code the model picked, or did the
model output a plausible reason that the letter does not actually state?

This file runs the model on 3 v2 letters, then runs the faithfulness judge on
each, and prints the verdict and reasoning. It does not touch LangSmith. Its job
is to confirm the evaluator works before we run the full experiment.
"""

import json
import os
from dotenv import load_dotenv

load_dotenv()

from openai import OpenAI

from target_function import target

# The judge. A different question from correctness, so a hand written prompt.
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

judge_client = OpenAI()


def faithfulness_of(letter: str, reason_code: str) -> dict:
    user_message = (
        "Letter:\n"
        + letter
        + "\n\nThe system selected this reason_code: "
        + reason_code
    )
    response = judge_client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": FAITHFULNESS_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )
    return json.loads(response.choices[0].message.content)


if __name__ == "__main__":
    with open("letters_v2.json", "r", encoding="utf-8") as f:
        letters = {item["id"]: item for item in json.load(f)}

    for letter_id in [1, 3, 2]:
        item = letters[letter_id]
        model_output = target({"letter": item["letter"]})
        picked = model_output.get("reason_code", "")
        verdict = faithfulness_of(item["letter"], picked)

        print("=" * 60)
        print("Letter id:      ", letter_id, "(difficulty:", item["difficulty"] + ")")
        print("Reference label:", item["reason_code"])
        print("Model picked:   ", picked)
        print("Faithful:       ", verdict.get("faithful"))
        print("Judge reason:   ", verdict.get("reason"))
