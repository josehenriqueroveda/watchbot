import os
import requests

import telebot
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_GROUP_ID = os.environ["TELEGRAM_GROUP_ID"]

API_LIST = [
    {"name": os.environ["API_NAME_1"], "url": os.environ["API_URL_1"]},
    {"name": os.environ["API_NAME_2"], "url": os.environ["API_URL_2"]},
    {"name": os.environ["API_NAME_2"], "url": os.environ["API_URL_3"]},
]

bot = telebot.TeleBot(TELEGRAM_TOKEN)


def check_api_status(api):
    try:
        response = requests.get(api["url"])
        if response.status_code == 200:
            return (200, "OK")
        else:
            return (response.status_code, response.text)
    except requests.exceptions.RequestException as e:
        return (500, str(e))


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(
        message, "Welcome to API WatchBot!\n\n Type /status to check APIs status."
    )


@bot.message_handler(commands=["status"])
def send_status(_):
    response = "*🤖 API Status Monitoring*\n\n"
    for api in API_LIST:
        status_code, status_text = check_api_status(api)
        if status_code == 200:
            response = (
                response + f"{api['name']}: 🟢 _{status_code} - {status_text}_\n\n"
            )
        else:
            response = (
                response + f"{api['name']}: 🔴 _{status_code} - {status_text}_\n\n"
            )
    bot.send_message(TELEGRAM_GROUP_ID, response, parse_mode="Markdown")


if __name__ == "__main__":
    bot.infinity_polling()
