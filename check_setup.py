import os
from dotenv import load_dotenv

load_dotenv()

os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_ENDPOINT"] = "https://eu.api.smith.langchain.com"
os.environ["LANGSMITH_PROJECT"] = "loan-letter-extraction"

from langsmith import Client

client = Client()
print("Datasets visible:", len(list(client.list_datasets())))
print("connection ok")