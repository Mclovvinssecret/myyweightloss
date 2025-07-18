import os
import json
from datetime import datetime
from flask import Flask, request
import telebot

# === Config ===
BOT_TOKEN = "8097212651:AAE3iv1fERb5on59dWZIfxhqVa3ISWVu3Zg"
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# === Telegram webhook endpoint ===
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def telegram_webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200

# === Homepage (GET request) ===
@app.route("/", methods=["GET"])
def home():
    return "✅ Weight loss bot is running!"

# === Set Webhook on startup (Render only) ===
if os.environ.get("RENDER") == "true":
    bot.remove_webhook()
    bot.set_webhook(url=f"https://myyweightloss.onrender.com/{BOT_TOKEN}")

# === /update command ===
@bot.message_handler(commands=['update'])
def update_data(message):
    try:
        parts = message.text.strip().split()
        if len(parts) != 3:
            bot.reply_to(message, "❌ Usage: /update <weight_kg> <bodyfat_%>")
            return

        weight = float(parts[1])
        bodyfat = float(parts[2])
    except ValueError:
        bot.reply_to(message, "❌ Invalid numbers. Example: /update 50.3 15.2")
        return

    entry = {
        "date": datetime.utcnow().strftime("%Y-%m-%d"),
        "weight": weight,
        "bodyfat": bodyfat
    }

    # Save or append to data.json
    if os.path.exists("data.json"):
        with open("data.json", "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(entry)

    with open("data.json", "w") as f:
        json.dump(data, f, indent=2)

    bot.reply_to(message, f"✅ Updated!\nWeight: {weight} kg\nBody fat: {bodyfat}%")

# === For local testing only ===
if __name__ == "__main__":
    app.run()