import telebot
import json
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
OWNER_ID = 123456789  # <-- මෙතනට ඔයාගේ Telegram numeric ID

DATA_FILE = "videos.json"

bot = telebot.TeleBot(BOT_TOKEN)

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(d):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

videos = load_data()

@bot.message_handler(commands=['save'], content_types=['video', 'document'])
def save_video(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "❌ Not allowed")
        return

    text = message.caption or message.text
    if not text or len(text.split()) < 2:
        bot.reply_to(message, "Use caption: /save A001")
        return

    vid = text.split()[1]

    if message.video:
        file_id = message.video.file_id
        ftype = "video"
    else:
        file_id = message.document.file_id
        ftype = "document"

    videos[vid] = {"file_id": file_id, "type": ftype}
    save_data(videos)

    bot.reply_to(message, f"✅ Saved ID: {vid}")

@bot.message_handler(commands=['start'])
def start_cmd(message):
    parts = message.text.split()
    if len(parts) < 2:
        bot.send_message(message.chat.id, "Send /
