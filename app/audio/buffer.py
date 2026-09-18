class AudioBuffer:
    def __init__(self, chunk_size: int):
        self.chunk_size = chunk_size
        self.buffer = bytearray()

    def add(self, audio_data: bytes) -> list[bytes]:
        self.buffer.extend(audio_data)

        chunks = []

        while len(self.buffer) >= self.chunk_size:
            chunk = bytes(self.buffer[:self.chunk_size])
            del self.buffer[:self.chunk_size]
            chunks.append(chunk)

        return chunks

    def flush(self) -> bytes:
        remaining = bytes(self.buffer)
        self.buffer.clear()
        return remaining

    def clear(self):
        self.buffer.clear()

    def size(self) -> int:
        return len(self.buffer)