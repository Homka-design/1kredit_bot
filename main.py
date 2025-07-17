# main.py

import os
from flask import Flask, request, abort
from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_webhook
import logging

API_TOKEN = os.getenv("7446181855:AAHESpa1eegvbrE_8qsIpr41iiKqqRtm6jA")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{os.getenv('RENDER_EXTERNAL_URL')}{WEBHOOK_PATH}"
WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.getenv("PORT", 8000))

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
app = Flask(__name__)

@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook_handler():
    data = request.json
    if not data:
        abort(400)
    # Сформировать сообщение
    text = "Новая заявка с Tilda:\n"
    for k, v in data.items():
        text += f"<b>{k}:</b> {v}\n"
    # Отправить сообщение
    chat_id = os.getenv("-1002778652070")
    bot.send_message(chat_id, text, parse_mode="HTML")
    return "OK", 200

async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(dp):
    await bot.delete_webhook()

if __name__ == "__main__":
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
