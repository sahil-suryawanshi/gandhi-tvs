import os
from typing import AsyncIterator

from dotenv import load_dotenv
from openai import AsyncOpenAI

from app.voice.llm_provider import LLMProvider

load_dotenv()


class OpenAILLMProvider(LLMProvider):
    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
    ):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY is missing")

        self.model = model or os.getenv(
            "OPENAI_MODEL",
            "gpt-5.6-luna",
        )

        self.client = AsyncOpenAI(
            api_key=self.api_key
        )

    async def stream_response(
        self,
        user_text: str,
    ) -> AsyncIterator[str]:

        user_text = user_text.strip()

        if not user_text:
            return

        stream = await self.client.responses.create(
            model=self.model,
            instructions=(
                "You are a voice assistant. "
                "Reply in 5 to 6 words. "
                "Be natural and concise. "
                "No markdown."
            ),
            input=user_text,
            reasoning={"effort": "none"},
            max_output_tokens=16,
            stream=True,
        )

        async for event in stream:
            if event.type == "response.output_text.delta":
                if event.delta:
                    yield event.delta