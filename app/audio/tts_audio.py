from dataclasses import dataclass


@dataclass
class TTSAudioChunk:
    data: bytes
    sample_rate: int
    channels: int
    encoding: str = "pcm_s16le"