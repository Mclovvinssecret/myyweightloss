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
        bot.reply_to(message, "❌ Invalid numbers. Usage: /update 50.3 15.2")
        return

    # Continue updating the data.json...