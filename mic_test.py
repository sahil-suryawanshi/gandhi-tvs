import sounddevice as sd
from scipy.io.wavfile import write

SAMPLE_RATE = 16000
DURATION = 10
CHANNELS = 1
DEVICE = 1

print("Recording started...")
audio = sd.rec(
    int(DURATION * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=CHANNELS,
    dtype="int16",
    device=DEVICE
)

sd.wait()

write("mic_test.wav", SAMPLE_RATE, audio)

print("Recording finished.")
print("Saved as mic_test.wav")