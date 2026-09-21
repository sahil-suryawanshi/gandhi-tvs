import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

MODEL = "gpt-5.6-luna"


def generate_response(user_text: str) -> str:
    response = client.responses.create(
        model=MODEL,
        instructions=(
            "You are a voice assistant. "
            "Reply in 5 to 6 words. "
            "Be natural and concise. "
            "No markdown."
        ),
        input=user_text,
        reasoning={"effort": "none"},
        max_output_tokens=16,
    )

    return response.output_text.strip()