from __future__ import annotations

from abc import ABC, abstractmethod
from typing import AsyncIterator

from app.audio.tts_audio import TTSAudioChunk


class TTSProvider(ABC):

    @abstractmethod
    async def synthesize(
        self,
        text: str,
    ) -> AsyncIterator[TTSAudioChunk]:
        raise NotImplementedError(
            "TTS providers must implement synthesize()"
        )