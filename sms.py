import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import sqlite3
from minio import Minio
import time
import json
import io

# MinIO Bağlantısı
minio_client = Minio(
    "localhost:9000",  # MinIO'nun çalıştığı host ve port
    access_key="minioadmin",  # MinIO access key
    secret_key="minioadmin",  # MinIO secret key
    secure=False  # https kullanmıyorsanız False
)

# SQLite Bağlantısı
def get_db_connection():
    conn = sqlite3.connect('chat_data.db')
    return conn

# Mesajları MinIO'ya kaydetme fonksiyonu
def save_message_to_minio(user_id, user_message, bot_reply):
    # Mesaj verisini JSON formatında kaydediyoruz
    message_data = {
        "user_id": user_id,
        "user_message": user_message,
        "bot_reply": bot_reply,
        "timestamp": int(time.time())
    }

    message_json = json.dumps(message_data)
    filename = f"chat_{int(time.time())}.json"  # Dosya ismi timestamp ile
    minio_client.put_object('chat-bot-messages', filename, io.BytesIO(message_json.encode()), len(message_json))
    return filename  # MinIO dosya ismini döndürüyoruz

# SQLite'a mesaj kaydetme fonksiyonu
def save_message_to_sqlite(user_id, username, user_message, bot_reply, minio_file):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO messages (user_id, username, message, timestamp, minio_file)
                      VALUES (?, ?, ?, datetime('now'), ?)''',
                   (user_id, username, user_message, minio_file))
    conn.commit()
    conn.close()

# API URL'nizi yazın
API_URL = "http://localhost:8002/chat"

# 📩 Mesaj geldiğinde çalışacak handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.lower()
    user_id = update.message.from_user.id
    username = update.message.from_user.username

    # API'ye mesajı gönder
    response = requests.post(API_URL, json={"message": user_message})
    
    if response.status_code == 200:
        bot_response = response.json().get('response', 'Üzgünüm, bir hata oluştu.')
    else:
        bot_response = "API ile bağlantı kurulamadı."

    # Mesajı MinIO'ya kaydet
    minio_file = save_message_to_minio(user_id, user_message, bot_response)

    # Mesajı SQLite'a kaydet
    save_message_to_sqlite(user_id, username, user_message, bot_response, minio_file)

    # API'den gelen yanıtı kullanıcıya gönder
    await update.message.reply_text(bot_response)

# 🚀 /start komutu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Merhaba! Ben Hatun Bot. Sana gününü güzelleştirmeye geldim! 🌸")

# Bot başlatma
def main():
    TOKEN = "7356333992:AAGtPt6BSFfVdTD7dM_szu0Vx06-Mr_F_WM"
    app = ApplicationBuilder().token(TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot çalışıyor... 🚀")
    app.run_polling()

if __name__ == '__main__':
    main()
