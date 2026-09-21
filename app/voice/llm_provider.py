from __future__ import annotations

from abc import ABC, abstractmethod
from typing import AsyncIterator


class LLMProvider(ABC):

    @abstractmethod
    async def stream_response(
        self,
        user_text: str,
    ) -> AsyncIterator[str]:
        raise NotImplementedError

    async def generate_response(
        self,
        user_text: str,
    ) -> str:

        chunks = []

        async for chunk in self.stream_response(user_text):
            chunks.append(chunk)

        return "".join(chunks).strip()