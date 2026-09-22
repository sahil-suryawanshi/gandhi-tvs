import numpy as np
import sounddevice as sd

from app.audio.queue import AudioQueue


class AudioPlayback:
    def __init__(
        self,
        sample_rate: int = 48000,
        channels: int = 1,
        device=None,
    ):
        self.sample_rate = sample_rate
        self.channels = channels
        self.device = device

    def start(self):
        # Playback is started by sd.play() when audio is provided.
        pass

    def play(self, audio_data: bytes):
        audio = np.frombuffer(
            audio_data,
            dtype=np.int16,
        )

        if self.channels > 1:
            audio = audio.reshape(-1, self.channels)

        sd.play(
            audio,
            samplerate=self.sample_rate,
            device=self.device,
            blocking=True,
        )

    def stop(self):
        sd.stop()


class AudioPlaybackEngine:
    def __init__(
        self,
        sample_rate: int = 16000,
        channels: int = 1,
        device=None,
    ):
        self.queue = AudioQueue()

        self.playback = AudioPlayback(
            sample_rate=sample_rate,
            channels=channels,
            device=device,
        )

    def start(self):
        self.playback.start()

    def add_audio(self, audio_data: bytes):
        self.queue.put(audio_data)

    def add_tts_chunk(self, chunk):
        audio_data = chunk.data

        if chunk.sample_rate != self.playback.sample_rate:
            from app.audio.resampler import resample_audio

            audio_data = resample_audio(
                audio_data,
                input_rate=chunk.sample_rate,
                output_rate=self.playback.sample_rate,
            )

        self.add_audio(audio_data)

    def play_next(self):
        if self.queue.empty():
            return False

        audio_data = self.queue.get()
        self.playback.play(audio_data)

        return True

    def queue_size(self):
        return self.queue.size()

    def stop(self):
        self.playback.stop()