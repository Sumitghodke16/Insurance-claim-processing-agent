import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


# Load variables from .env
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError(
        "OPENAI_API_KEY was not found. "
        "Check your .env file."
    )


model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


response = model.invoke(
    "Explain in one sentence what an insurance claim is."
)


print("\nLLM CONNECTION SUCCESSFUL")
print("=" * 40)
print(response.content)