import uuid
import os
import edge_tts
from faster_whisper import WhisperModel
import tempfile
# from transformers import pipeline
import requests

import asyncio
# model = WhisperModel("base", compute_type="int8")
# model = WhisperModel(
#     "base",
#     device="cpu",
#     compute_type="int8"
# )
model = None

def get_model():
    global model
    if model is None:
        model = WhisperModel("tiny", device="cpu",download_root="/tmp"
)
        # model = WhisperModel("base", device="cpu")
    return model

def transcribe(audio_path):
    model = get_model()
    segments, info = model.transcribe(audio_path)
    return " ".join([s.text for s in segments])
# sentiment = pipeline("sentiment-analysis")

HF_API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"
# HF_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct"
HF_TOKEN = os.getenv("HF_TOKEN",'')


def generate_reply(text, emotion=None):
    url = "https://router.huggingface.co/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "Qwen/Qwen2.5-7B-Instruct",
        "messages": [
            {
                "role": "system",
                "content": "You are Moody, a warm supportive assistant. Reply briefly and naturally."
            },
            {
                "role": "user",
                "content": f"Emotion: {emotion}\nUser said: {text}"
            }
        ],
        "max_tokens": 100,
        "temperature": 0.7
    }

    try:
        res = requests.post(url, headers=headers, json=payload, timeout=30)

        print("STATUS:", res.status_code)
        print("TEXT:", res.text)

        data = res.json()

        if "choices" in data:
            return data["choices"][0]["message"]["content"]

        return f"Unexpected response: {data}"

    except Exception as e:
        print("REAL ERROR:", str(e))
        return "I'm here with you. Tell me more."
def text_to_speech(text, voice="en-US-JennyNeural"):
    file_path = os.path.join(
        tempfile.gettempdir(),
        f"{uuid.uuid4()}.mp3"
    )

    async def _run():
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(file_path)

    asyncio.run(_run())

    return file_path