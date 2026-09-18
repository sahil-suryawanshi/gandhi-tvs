from queue import Queue


class AudioQueue:
    def __init__(self):
        self.queue = Queue()

    def put(self, audio_data: bytes):
        self.queue.put(audio_data)

    def get(self) -> bytes:
        return self.queue.get()

    def empty(self) -> bool:
        return self.queue.empty()

    def size(self) -> int:
        return self.queue.qsize()

    def clear(self):
        while not self.queue.empty():
            self.queue.get()