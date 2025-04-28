# bot.py
import os
import time
import sqlite3
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from minio import Minio

# Telegram ve OpenWeather API Key
TOKEN = "7356333992:AAGtPt6BSFfVdTD7dM_szu0Vx06-Mr_F_WM"
OPENWEATHER_API_KEY = "c1bab5c2726865b81b6c91ca967583ef"

# MinIO bağlantısı
client = Minio(
    "localhost:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)
bucket_name = "chat-data"
if not client.bucket_exists(bucket_name):
    client.make_bucket(bucket_name)

# Veritabanı fonksiyonları
def save_message_to_db(user_id, username, message_text, timestamp, minio_file):
    conn = sqlite3.connect('chat_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            message TEXT,
            timestamp TEXT,
            minio_file TEXT
        )
    ''')
    cursor.execute('''
        INSERT INTO messages (user_id, username, message, timestamp, minio_file)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, username, message_text, timestamp, minio_file))
    conn.commit()
    conn.close()

def save_message_to_minio(message_text):
    file_name = f"message_{int(time.time())}.txt"
    with open(file_name, "w") as file:
        file.write(message_text)
    client.fput_object(bucket_name, file_name, file_name)
    os.remove(file_name)
    return file_name

# Mesaj handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    message_text = update.message.text
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

    # MinIO'ya ve veritabanına kaydet
    minio_file = save_message_to_minio(message_text)
    save_message_to_db(user_id, username, message_text, timestamp, minio_file)

    await update.message.reply_text("Mesajınız kaydedildi! ✅")

# /start komutu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Merhaba! Hatun 2025 Bot burada! 🎉 Size nasıl yardımcı olabilirim?")

# /info komutu
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ben bir süper bottum! 🚀 Şu an daha da güçleniyorum.")

# /haber komutu (web scraping)
async def haber(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = "https://www.haberturk.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    headlines = soup.find_all("h2", class_="title", limit=3)

    if not headlines:
        await update.message.reply_text("Şu anda haber çekilemedi, lütfen daha sonra deneyin! ❌")
        return

    message = "📰 Son Dakika Haberleri:\n\n"
    for headline in headlines:
        message += f"- {headline.get_text(strip=True)}\n"

    await update.message.reply_text(message)

# /hava komutu (OpenWeather API kullanarak)
async def hava(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Lütfen bir şehir adı girin. Örnek: /hava İstanbul")
        return

    city = " ".join(context.args)
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&lang=tr&units=metric"

    response = requests.get(url)
    data = response.json()

    if data.get("cod") != 200:
        await update.message.reply_text("Şehir bulunamadı. Lütfen doğru yazdığınızdan emin olun.")
        return

    weather = data["weather"][0]["description"]
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]

    message = (
        f"🌤 {city} için hava durumu:\n\n"
        f"🌡 Sıcaklık: {temp}°C\n"
        f"🤔 Hissedilen: {feels_like}°C\n"
        f"📋 Durum: {weather.capitalize()}"
    )
    await update.message.reply_text(message)

# Botu başlat
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("haber", haber))
    app.add_handler(CommandHandler("hava", hava))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot çalışıyor... 🚀")
    app.run_polling()

if __name__ == '__main__':
    main()
