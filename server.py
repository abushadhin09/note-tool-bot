import telebot
from flask import Flask, jsonify
from threading import Thread

BOT_TOKEN = "8583065012:AAE2FvekNfrNjVsY7o9ppIUnU9rgy55S_k0"
ADMIN_ID = 8397197714  # আপনার Telegram ID

bot = telebot.TeleBot(BOT_TOKEN)

settings = {
    "toolStatus": True,
    "themeColor": "#00ffdd",
    "logo": "",
    "siteName": "NOTE TOOL",
    "notice": "Welcome!"
}

@bot.message_handler(commands=['set_notice','set_theme','set_logo','tool_on','tool_off'])
def admin(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message,"❌ Not Admin")
        return

    t = message.text
    if t.startswith('/set_notice '):
        settings['notice'] = t.replace('/set_notice ','')
        bot.reply_to(message,"✅ Notice Updated")
    elif t.startswith('/set_theme '):
        settings['themeColor'] = t.replace('/set_theme ','')
        bot.reply_to(message,"✅ Theme Updated")
    elif t.startswith('/set_logo '):
        settings['logo'] = t.replace('/set_logo ','')
        bot.reply_to(message,"✅ Logo Updated")
    elif t == '/tool_on':
        settings['toolStatus'] = True
        bot.reply_to(message,"✅ Tool ON")
    elif t == '/tool_off':
        settings['toolStatus'] = False
        bot.reply_to(message,"❌ Tool OFF")

app = Flask(__name__)

@app.route("/settings")
def get_settings():
    return jsonify(settings)

def run_bot():
    bot.infinity_polling()

Thread(target=run_bot).start()
app.run(host="0.0.0.0", port=10000)
