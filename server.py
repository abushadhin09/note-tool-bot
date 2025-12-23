import telebot
from flask import Flask, jsonify, request
from threading import Thread

BOT_TOKEN = "8583065012:AAE2FvekNfrNjVsY7o9ppIUnU9rgy55S_k0"
ADMIN_ID = 8397197714
ADMIN_SECRET = "ADMIN_SECRET_123"

bot = telebot.TeleBot(BOT_TOKEN)

# 🔹 Global settings (shared by all users)
settings = {
    "toolStatus": True,
    "themeColor": "#00ffdd",
    "logo": "",
    "siteName": "NOTE TOOL",
    "notice": "Welcome!"
}

# 🔹 Telegram admin (optional, still works)
@bot.message_handler(commands=['tool_on','tool_off'])
def admin_bot(message):
    if message.from_user.id != ADMIN_ID:
        return
    if message.text == "/tool_on":
        settings["toolStatus"] = True
        bot.reply_to(message,"✅ Tool ON")
    if message.text == "/tool_off":
        settings["toolStatus"] = False
        bot.reply_to(message,"❌ Tool OFF")

app = Flask(__name__)

# 🔹 User tool fetches this
@app.route("/settings")
def get_settings():
    return jsonify(settings)

# 🔹 Admin panel updates this
@app.route("/update", methods=["POST"])
def update_settings():
    data = request.json

    if data.get("key") != ADMIN_SECRET:
        return {"error": "unauthorized"}, 403

    for k in settings:
        if k in data:
            settings[k] = data[k]

    return {"success": True, "settings": settings}

def run_bot():
    bot.infinity_polling()

Thread(target=run_bot).start()
app.run(host="0.0.0.0", port=10000)
