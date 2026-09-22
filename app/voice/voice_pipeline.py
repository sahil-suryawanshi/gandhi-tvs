import asyncio

import numpy as np
import sounddevice as sd

from app.audio.playback import AudioPlaybackEngine
from app.voice.llm_provider import LLMProvider
from app.voice.tts_provider import TTSProvider


class VoicePipeline:
    def __init__(
        self,
        llm_provider: LLMProvider,
        tts_provider: TTSProvider,
        playback_engine: AudioPlaybackEngine,
    ):
        self.llm_provider = llm_provider
        self.tts_provider = tts_provider
        self.playback_engine = playback_engine

    def _play_all(self) -> None:
        chunks = []

        while not self.playback_engine.queue.empty():
            chunks.append(
                self.playback_engine.queue.get()
            )

        if not chunks:
            print("No audio chunks to play")
            return

        audio_bytes = b"".join(chunks)

        print(
            "Combined audio:",
            len(audio_bytes),
            "bytes"
        )

        audio = np.frombuffer(
            audio_bytes,
            dtype=np.int16,
        )

        print(
            "Audio samples:",
            len(audio)
        )

        print("Playing combined audio...")

        sd.play(
            audio,
            samplerate=48000,
            device=11,
            blocking=True,
        )

        print("Combined audio playback completed")

    async def process(self, user_text: str) -> str:
        user_text = user_text.strip()

        if not user_text:
            return ""

        print("\n========== VOICE PIPELINE ==========")
        print("User text:", user_text)

        # LLM
        response_text = await self.llm_provider.generate_response(
            user_text
        )

        print("LLM response:", response_text)

        if not response_text:
            return ""

        # TTS
        tts_chunks = 0
        total_bytes = 0

        print("Starting ElevenLabs TTS...")

        async for chunk in self.tts_provider.synthesize(
            response_text
        ):
            tts_chunks += 1
            total_bytes += len(chunk.data)

            print(
                f"TTS chunk {tts_chunks}: "
                f"{len(chunk.data)} bytes, "
                f"{chunk.sample_rate} Hz"
            )

            self.playback_engine.add_tts_chunk(chunk)

        print("TTS finished")
        print("Total TTS chunks:", tts_chunks)
        print("Total TTS bytes:", total_bytes)
        print(
            "Audio queue size:",
            self.playback_engine.queue_size()
        )

        # Playback
        print("Starting playback...")

        await asyncio.to_thread(
            self._play_all
        )

        print("Playback completed")
        print("====================================\n")

        return response_text