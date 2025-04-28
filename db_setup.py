import sqlite3
from minio import Minio
import json
import time
import io

# SQLite Bağlantısı
conn = sqlite3.connect('chat_data.db')
cursor = conn.cursor()

# Tablo oluştur
cursor.execute('''
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    username TEXT,
    message TEXT,
    timestamp TEXT,
    minio_file TEXT
)
''')

# MinIO Bağlantısı
minio_client = Minio(
    "localhost:9000",  # MinIO'nun çalıştığı host ve port
    access_key="minioadmin",  # MinIO access key
    secret_key="minioadmin",  # MinIO secret key
    secure=False  # https kullanmıyorsanız False
)

# MinIO Bucket Kontrolü (Yoksa oluştur)
bucket_name = "chat-bot-messages"
if not minio_client.bucket_exists(bucket_name):
    minio_client.make_bucket(bucket_name)

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
    minio_client.put_object(bucket_name, filename, io.BytesIO(message_json.encode()), len(message_json))
    return filename  # MinIO dosya ismini döndürüyoruz

# SQLite'a mesaj kaydetme fonksiyonu
def save_message_to_sqlite(user_id, username, user_message, bot_reply, minio_file):
    cursor.execute('''
    INSERT INTO messages (user_id, username, message, timestamp, minio_file)
    VALUES (?, ?, ?, datetime('now'), ?)
    ''', (user_id, username, user_message, minio_file))
    
    conn.commit()
# db_test.py
import sqlite3

def test_db_connection():
    conn = sqlite3.connect('chat_data.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tablolar:", tables)

    conn.close()

test_db_connection()

# Bağlantıyı kapat
conn.close()

print("Veritabanı ve MinIO bağlantısı hazır! 🎯")
