import sounddevice as sd
import numpy as np
import requests
import io
from scipy.io.wavfile import write

SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK_DURATION = 2
DEVICE = 1

print("Starting microphone stream...")
print("Speak into your microphone.")
print("Press CTRL+C to stop.")

try:
    while True:
        print("\nRecording chunk...")

        audio = sd.rec(
            int(CHUNK_DURATION * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype="int16",
            device=DEVICE
        )

        sd.wait()

        # Convert audio chunk to WAV in memory
        audio_buffer = io.BytesIO()

        write(
            audio_buffer,
            SAMPLE_RATE,
            audio
        )

        audio_buffer.seek(0)

        print("Sending chunk to backend...")

        response = requests.post(
            "http://127.0.0.1:8000/audio",
            files={
                "file": (
                    "microphone_chunk.wav",
                    audio_buffer,
                    "audio/wav"
                )
            }
        )

        print("Backend status:", response.status_code)
        print("Response:", response.json())

except KeyboardInterrupt:
    print("\nMicrophone stream stopped.")