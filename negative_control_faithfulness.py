"""
Step 11 evaluator validation: negative control for the faithfulness judge.

The full experiment returned faithful = true on all 15 real outputs. That alone
does not prove the judge can say false. This script feeds the judge real letters
paired with a reason_code we know is WRONG for that letter, and checks that it
returns faithful = false. One correct pairing is included as a positive sanity
check, so we see the judge move in both directions.

This is evaluator validation, not model output. The wrong codes are injected by
us on purpose to test the judge.
"""

import json
import os
from dotenv import load_dotenv

load_dotenv()

from openai import OpenAI

# Same prompt the real evaluator uses.
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
        "Letter:\n" + letter + "\n\nThe system selected this reason_code: " + reason_code
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


# (letter_id, injected_reason_code, what we expect the judge to say)
CASES = [
    (1, "collateral_value", False),      # a credit_score letter, wrong code injected
    (3, "employment_history", False),    # a debt_to_income letter, wrong code injected
    (5, "incomplete_application", False),# an insufficient_income letter, wrong code injected
    (1, "credit_score", True),           # positive sanity: correct code, should stay true
]


if __name__ == "__main__":
    with open("letters_v2.json", "r", encoding="utf-8") as f:
        letters = {item["id"]: item for item in json.load(f)}

    passed = 0
    for letter_id, injected_code, expected in CASES:
        item = letters[letter_id]
        verdict = faithfulness_of(item["letter"], injected_code)
        actual = bool(verdict.get("faithful"))
        ok = actual == expected
        passed += ok

        print("=" * 60)
        print("Letter id:      ", letter_id, "(true reason:", item["reason_code"] + ")")
        print("Injected code:  ", injected_code)
        print("Expected faithful:", expected, " | Judge said:", actual, " |", "PASS" if ok else "FAIL")
        print("Judge reason:   ", verdict.get("reason"))

    print("=" * 60)
    print(f"Negative control result: {passed} / {len(CASES)} as expected")
