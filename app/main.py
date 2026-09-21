import os

from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from deepgram import DeepgramClient

from app.voice.openai_llm_provider import OpenAILLMProvider
from app.audio.playback import AudioPlaybackEngine
from app.voice.elevenlabs_tts_provider import ElevenLabsTTSProvider
from app.voice.openai_llm_provider import OpenAILLMProvider
from app.voice.voice_pipeline import VoicePipeline

load_dotenv()

app = FastAPI()

llm_provider = OpenAILLMProvider()
tts_provider = ElevenLabsTTSProvider()
playback_engine = AudioPlaybackEngine(
    sample_rate=48000,
    channels=1,
    device=11,
)

voice_pipeline = VoicePipeline(
    llm_provider=llm_provider,
    tts_provider=tts_provider,
    playback_engine=playback_engine,
)

llm_provider = OpenAILLMProvider()

class ChatRequest(BaseModel):
    message: str

deepgram = DeepgramClient(
    api_key=os.getenv("DEEPGRAM_API_KEY")
)


@app.get("/")
def home():
    return {"message": "Gandhi TVS API is working"}


@app.post("/audio")
async def receive_audio(file: UploadFile = File(...)):   #POST /audio endpoint. It accepts the WAV file.

    audio_data = await file.read()                       #"Here I read the uploaded audio into bytes."

    print(f"Received audio: {file.filename}")
    print(f"Audio size: {len(audio_data)} bytes")

    response = deepgram.listen.v1.media.transcribe_file(
        request=audio_data,
        model="nova-3",
        smart_format=True
    )
    # "The backend returns the transcript as JSON."

    transcript = response.results.channels[0].alternatives[0].transcript

    print(f"Transcript: {transcript}")

    return {
        "message": "Audio processed successfully",
        "filename": file.filename,
        "transcript": transcript
    }
@app.post("/chat")
async def chat(request: ChatRequest):
    response = await llm_provider.generate_response(request.message)

    return {
        "response": response
    }

class VoiceRequest(BaseModel):
    message: str


@app.post("/voice")
async def voice(request: VoiceRequest):
    response_text = await voice_pipeline.process(
        request.message
    )

    return {
        "user_text": request.message,
        "response": response_text,
    }