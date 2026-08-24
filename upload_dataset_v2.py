"""
Upload the hardened v2 dataset to LangSmith as a separate dataset.

The v1 dataset stays untouched so the two iterations can be compared.
"""

import json
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_ENDPOINT"] = "https://eu.api.smith.langchain.com"
os.environ["LANGSMITH_PROJECT"] = "loan-letter-extraction"

from langsmith import Client

DATASET_NAME = "loan-rejection-letters-v2"
DATASET_DESCRIPTION = (
    "Hardened second iteration of the loan rejection letter dataset. "
    "Same 15 scenarios and the same ground truth labels as v1, but the "
    "sentences that signposted which factor was decisive have been removed. "
    "v1 produced a ceiling effect: every evaluator scored 15 out of 15."
)

client = Client()

with open("letters_v2.json", "r", encoding="utf-8") as f:
    letters = json.load(f)

print("Loaded", len(letters), "letters from letters_v2.json")

existing = [d.name for d in client.list_datasets()]

if DATASET_NAME in existing:
    dataset = client.read_dataset(dataset_name=DATASET_NAME)
    print("Dataset already exists, reusing it.")
else:
    dataset = client.create_dataset(DATASET_NAME, description=DATASET_DESCRIPTION)
    print("Created dataset:", DATASET_NAME)

inputs = [{"letter": item["letter"]} for item in letters]

outputs = [
    {
        "reason_code": item["reason_code"],
        "manual_review_offered": item["manual_review_offered"],
    }
    for item in letters
]

metadata = [
    {
        "letter_id": item["id"],
        "reason_code": item["reason_code"],
        "difficulty": item["difficulty"],
        "source": "synthetic",
        "dataset_version": "v2",
    }
    for item in letters
]

client.create_examples(
    inputs=inputs,
    outputs=outputs,
    metadata=metadata,
    dataset_id=dataset.id,
)

count = len(list(client.list_examples(dataset_id=dataset.id)))
print("Examples now in dataset:", count)
print("Dataset id:", dataset.id)
