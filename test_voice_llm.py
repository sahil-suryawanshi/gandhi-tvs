import requests

AUDIO_URL = "http://127.0.0.1:8000/audio"
CHAT_URL = "http://127.0.0.1:8000/chat"


def transcribe_audio(audio_file: str) -> str:
    with open(audio_file, "rb") as file:
        response = requests.post(
            AUDIO_URL,
            files={
                "file": (
                    audio_file,
                    file,
                    "audio/wav",
                )
            },
        )

    response.raise_for_status()

    return response.json()["transcript"]


def generate_llm_response(transcript: str) -> str:
    response = requests.post(
        CHAT_URL,
        json={"message": transcript},
    )

    response.raise_for_status()

    return response.json()["response"]


transcript = transcribe_audio("llm_voice_test.wav")

print("Transcript:", transcript)

if transcript.strip():
    answer = generate_llm_response(transcript)
    print("LLM:", answer)
else:
    print("No speech detected.")