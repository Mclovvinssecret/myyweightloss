import telebot
import json
import os
from datetime import datetime
from flask import Flask, request

# === Bot token and setup ===
BOT_TOKEN = "8097212651:AAE3iv1fERb5on59dWZIfxhqVa3ISWVu3Zg"
bot = telebot.TeleBot(BOT_TOKEN)

# === Flask for Render hosting ===
app = Flask(__name__)

@app.route(f"/{BOT_TOKEN}", methods=['POST'])
def telegram_webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "!", 200

@app.route("/", methods=['GET'])
def home():
    return "Weight loss bot is running!"

# === Set webhook on startup ===
with app.app_context():
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

    new_entry = {
        "date": datetime.utcnow().strftime("%Y-%m-%d"),
        "weight": weight,
        "bodyfat": bodyfat
    }

    if os.path.exists("data.json"):
        with open("data.json", "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(new_entry)

    with open("data.json", "w") as f:
        json.dump(data, f, indent=2)

    bot.reply_to(message, f"✅ Updated!\nWeight: {weight} kg\nBody fat: {bodyfat}%")

# === needed ===
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)