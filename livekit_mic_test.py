import sounddevice as sd
from livekit import rtc

SAMPLE_RATE = 48000
CHANNELS = 1
DURATION = 5
DEVICE = 1

print("Recording microphone audio...")

audio = sd.rec(
    int(DURATION * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=CHANNELS,
    dtype="int16",
    device=DEVICE
)

sd.wait()

print("Recording finished.")

pcm_bytes = audio.tobytes()

print("Sample rate:", SAMPLE_RATE)
print("Channels:", CHANNELS)
print("PCM bytes:", len(pcm_bytes))

print("Creating LiveKit AudioFrame...")

frame = rtc.AudioFrame(
    data=pcm_bytes,
    sample_rate=SAMPLE_RATE,
    num_channels=CHANNELS,
    samples_per_channel=len(audio)
)

print("AudioFrame created successfully.")
print("Samples per channel:", frame.samples_per_channel)
print("LiveKit microphone audio test completed.")