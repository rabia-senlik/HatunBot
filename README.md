
# 🤖 HatunBot — Telegram Chatbot with FastAPI, MinIO and SQLite

HatunBot is a Telegram chatbot that communicates with users and stores their messages securely using a backend powered by FastAPI, MinIO (for object storage), and SQLite (for structured data).

## 🧠 Features

- Responds to user messages with AI-generated replies (via FastAPI backend).
- Saves chat messages in both:
  - 📦 **MinIO** (as JSON objects)
  - 🗃️ **SQLite** (for fast querying and indexing)
- Lightweight and modular Python codebase.
- Designed for extensibility and customization.

## 🗂️ Project Structure

```
HatunBot/
├── chat_api.py         # FastAPI backend to handle chat requests
├── sms.py              # Telegram bot logic and message handling
├── db_setup.py         # SQLite database setup
├── .env                # (Ignored) Stores credentials for MinIO and others
├── chat_data.db        # SQLite database file
├── minio/              # MinIO server (not included in repo)
├── README.md           # Project documentation
└── .gitignore          # Ignored files and folders
```

## ⚙️ Technologies Used

- **Python** 3.10+
- **FastAPI** – for the backend API
- **MinIO** – for object storage (message JSONs)
- **SQLite** – lightweight relational database
- **python-telegram-bot** – for Telegram bot interaction

## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/rabia-senlik/HatunBot.git
cd HatunBot
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Set up Environment Variables

Create a `.env` file with your MinIO and API details:

```ini
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
TELEGRAM_TOKEN=your_telegram_bot_token
```

> **Note:** This file is ignored from GitHub using `.gitignore`.

### 5. Run MinIO and FastAPI

Run MinIO locally, then start your FastAPI server:

```bash
python chat_api.py
```

### 6. Start the Bot

```bash
python sms.py
```

## 💾 Message Storage Example

When a user sends a message, this happens:

1. The message is forwarded to the FastAPI backend.
2. The bot receives a response and sends it back to the user.
3. The user message and response are:
   - Stored in **MinIO** as a `.json` file.
   - Saved in **SQLite** with a timestamp and MinIO filename.

## 🧪 Example Response

```json
{
  "user_id": 12345678,
  "user_message": "hello",
  "bot_reply": "Hi there! How can I help you today?",
  "timestamp": 1714370000
}
```

## 🔒 Security Notes

- Store credentials in a `.env` file and never commit it.
- Avoid pushing heavy files (like MinIO binary) to GitHub.

## 💡 Development Plans

Here are some ideas for future improvements:

- 🧠 Integrate a more advanced language model (e.g., GPT-4).
- 🌐 Deploy the backend API and bot on a cloud platform (e.g., Heroku, AWS).
- 🖼️ Add a web-based chat UI using Streamlit or Gradio.
- 🧾 Implement chat history retrieval and export features.
- 🛡️ Add user authentication and message moderation.
- 📊 Build an analytics dashboard to track usage.
- 🗣️ Support for multiple languages.

## 📬 Contact

Developed by **Rabia Şenlik**  
📧 [LinkedIn Profile](https://www.linkedin.com/in/rabia-şenlik)
