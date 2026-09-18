from app.audio.buffer import AudioBuffer
from app.audio.config import CHUNK_SIZE, SAMPLE_RATE
from app.audio.packet_tracker import PacketTracker
from app.audio.queue import AudioQueue
from app.audio.resampler import resample_audio


class AudioPipeline:
    def __init__(self):
        self.buffer = AudioBuffer(CHUNK_SIZE)
        self.queue = AudioQueue()
        self.packet_tracker = PacketTracker()

    def add_audio(
        self,
        audio_data: bytes,
        sequence_number: int,
    ) -> list[bytes]:

        self.packet_tracker.add_packet(sequence_number)

        chunks = self.buffer.add(audio_data)

        for chunk in chunks:
            self.queue.put(chunk)

        return chunks

    def get_audio(self) -> bytes:
        return self.queue.get()

    def queue_empty(self) -> bool:
        return self.queue.empty()

    def queue_size(self) -> int:
        return self.queue.size()

    def process_chunk(self, audio_data: bytes) -> bytes:
        return resample_audio(
            audio_data,
            input_rate=SAMPLE_RATE,
            output_rate=16000,
        )

    def flush(self) -> bytes:
        remaining = self.buffer.flush()

        if remaining:
            self.queue.put(remaining)

        return remaining

    def buffered_size(self) -> int:
        return self.buffer.size()

    def dropped_packets(self) -> int:
        return self.packet_tracker.get_dropped_packets()