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

    async def process(self, user_text: str) -> str:
        user_text = user_text.strip()

        if not user_text:
            return ""

        response_text = await self.llm_provider.generate_response(
            user_text
        )

        if not response_text:
            return ""

        async for chunk in self.tts_provider.synthesize(
            response_text
        ):
            self.playback_engine.add_tts_chunk(chunk)

        while self.playback_engine.play_next():
            pass

        return response_text