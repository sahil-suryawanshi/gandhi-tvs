import asyncio

from app.audio.playback import AudioPlaybackEngine
from app.voice.elevenlabs_tts_provider import ElevenLabsTTSProvider


async def main():
    text = "I'm fine, thanks!"

    tts = ElevenLabsTTSProvider()

    playback = AudioPlaybackEngine(
        sample_rate=48000,
        channels=1,
        device=11,
    )

    print("Generating TTS...")
    
    async for chunk in tts.synthesize(text):
        playback.add_tts_chunk(chunk)

    print("Playing response...")

    while playback.play_next():
        pass

    playback.stop()

    print("TTS playback completed.")


asyncio.run(main())