import sounddevice as sd
import requests
import io
import os

from scipy.io.wavfile import write, read

SAMPLE_RATE = 16000
CHANNELS = 1
DEVICE = 1

# Change this value for different tests:
# 30 = 30 seconds
# 60 = 1 minute
# 120 = 2 minutes
RECORDING_DURATION = 30

CHUNK_DURATION = 2

OUTPUT_FILE = "long_recording.wav"


print(f"Recording for {RECORDING_DURATION} seconds...")
print("Speak clearly into the microphone.")
print("Recording started...")

audio = sd.rec(
    int(RECORDING_DURATION * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=CHANNELS,
    dtype="int16",
    device=DEVICE
)

sd.wait()

print("Recording finished.")

write(
    OUTPUT_FILE,
    SAMPLE_RATE,
    audio
)

print(f"Saved recording as {OUTPUT_FILE}")


# Read the recorded audio
sample_rate, audio = read(OUTPUT_FILE)

samples_per_chunk = sample_rate * CHUNK_DURATION

total_chunks = (len(audio) + samples_per_chunk - 1) // samples_per_chunk

print(f"\nTotal chunks: {total_chunks}")
print(f"Chunk duration: {CHUNK_DURATION} seconds")

transcripts = []


# Process each chunk
for chunk_number, start in enumerate(
    range(0, len(audio), samples_per_chunk),
    start=1
):
    end = start + samples_per_chunk

    chunk = audio[start:end]

    audio_buffer = io.BytesIO()

    write(
        audio_buffer,
        sample_rate,
        chunk
    )

    audio_buffer.seek(0)

    print(f"\nProcessing chunk {chunk_number}/{total_chunks}...")

    response = requests.post(
        "http://127.0.0.1:8000/audio",
        files={
            "file": (
                f"chunk_{chunk_number}.wav",
                audio_buffer,
                "audio/wav"
            )
        }
    )

    print("Backend status:", response.status_code)

    if response.status_code == 200:
        result = response.json()

        transcript = result.get("transcript", "")

        print("Transcript:", transcript)

        transcripts.append(transcript)

    else:
        print("Error:", response.text)


# Combine all transcripts
full_transcript = " ".join(
    transcript for transcript in transcripts if transcript
)

print("\n" + "=" * 60)
print("FINAL COMBINED TRANSCRIPT")
print("=" * 60)

print(full_transcript)

print("\nTest completed.")