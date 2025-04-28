from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline

# FastAPI uygulaması başlat
app = FastAPI()

# Huggingface modelini yükle
chatbot = pipeline("text2text-generation", model="facebook/blenderbot-400M-distill")

class Message(BaseModel):
    message: str

# Hafıza listesi (önceki mesajları hatırlamak için)
memory = []

@app.post("/chat")
async def chat(message: Message):
    user_message = message.message

    # Hafızaya kullanıcı mesajını ekle
    memory.append(user_message)

    # Modelden cevap al
    response = chatbot(user_message)[0]['generated_text']

    # Hafızayı sınırlamak için en fazla 5 mesaj tutuyoruz
    if len(memory) > 5:
        memory.pop(0)

    return {"response": response}
