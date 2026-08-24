"""
Step 4: create the LangSmith dataset and upload the 15 loan rejection letters.
Run once. Safe to re-run: it skips creation if the dataset already exists.
"""

import json
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_ENDPOINT"] = "https://eu.api.smith.langchain.com"
os.environ["LANGSMITH_PROJECT"] = "loan-letter-extraction"

from langsmith import Client

DATASET_NAME = "loan-rejection-letters"
DATASET_DESCRIPTION = (
    "15 synthetic German retail bank loan rejection letters. "
    "Task: extract the primary rejection reason code and whether a manual "
    "review of the lending decision is offered."
)

client = Client()

with open("letters.json", "r", encoding="utf-8") as f:
    letters = json.load(f)

print("Loaded", len(letters), "letters from letters.json")

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
