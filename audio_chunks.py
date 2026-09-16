from scipy.io.wavfile import read, write
import os

INPUT_FILE = "mic_test.wav"
CHUNK_DURATION = 2  # seconds

sample_rate, audio = read(INPUT_FILE)

samples_per_chunk = sample_rate * CHUNK_DURATION

os.makedirs("audio_chunks", exist_ok=True)

chunk_number = 1

for start in range(0, len(audio), samples_per_chunk):
    end = start + samples_per_chunk
    chunk = audio[start:end]

    output_file = f"audio_chunks/chunk_{chunk_number}.wav"
    write(output_file, sample_rate, chunk)

    print(f"Created: {output_file}")

    chunk_number += 1

print("Audio chunking completed.")