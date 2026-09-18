import io
import requests
import sounddevice as sd
from scipy.io.wavfile import write, read
from livekit import rtc
import numpy as np

SAMPLE_RATE = 48000
CHANNELS = 1
DURATION = 10
DEVICE = 1

print("Recording microphone...")

audio = sd.rec(
    int(DURATION * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=CHANNELS,
    dtype="int16",
    device=DEVICE
)

sd.wait()

print("Recording finished.")

# Convert microphone data to bytes
pcm_bytes = audio.tobytes()

# Create LiveKit AudioFrame
frame = rtc.AudioFrame(
    data=pcm_bytes,
    sample_rate=SAMPLE_RATE,
    num_channels=CHANNELS,
    samples_per_channel=len(audio)
)

print("LiveKit AudioFrame created.")
print("Frame sample rate:", frame.sample_rate)
print("Frame channels:", frame.num_channels)

# Convert AudioFrame back to NumPy audio data
frame_audio = np.frombuffer(frame.data, dtype=np.int16)

# Save temporary 48 kHz WAV
wav_48k = io.BytesIO()

write(
    wav_48k,
    SAMPLE_RATE,
    frame_audio
)

wav_48k.seek(0)

# Read the WAV
sample_rate, audio_data = read(wav_48k)

print("Original audio:", sample_rate, "Hz")

# Resample 48 kHz → 16 kHz
from scipy.signal import resample

new_length = int(len(audio_data) * 16000 / sample_rate)

audio_16k = resample(
    audio_data,
    new_length
).astype("int16")

print("Converted audio: 16000 Hz")

# Create final WAV in memory
wav_16k = io.BytesIO()

write(
    wav_16k,
    16000,
    audio_16k
)

wav_16k.seek(0)

print("Sending audio to FastAPI...")

response = requests.post(
    "http://127.0.0.1:8000/audio",
    files={
        "file": (
            "livekit_audio.wav",
            wav_16k,
            "audio/wav"
        )
    }
)

print("Backend status:", response.status_code)
print("Response:", response.json())