import os

from dotenv import load_dotenv
from deepgram import DeepgramClient

load_dotenv()

api_key = os.getenv("DEEPGRAM_API_KEY")

client = DeepgramClient(api_key=api_key)

response = client.listen.v1.media.transcribe_url(
    url="https://archive.phonetics.ucla.edu/Language/MAR/mar_word-list_1973_01.wav",
    model="nova-3",
    smart_format=True
)

transcript = response.results.channels[0].alternatives[0].transcript

print(transcript)