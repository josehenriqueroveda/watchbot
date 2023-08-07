import os
import requests
import logging
from typing import Dict, Tuple

import telebot
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv, find_dotenv

logging.basicConfig(
    format="%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d) [%(filename)s])",
    datefmt="%d-%m-%Y %H:%M:%S",
    level=logging.DEBUG,
)

load_dotenv(find_dotenv())

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_GROUP_ID = os.environ["TELEGRAM_GROUP_ID"]

API_LIST = [
    {"name": os.environ["API_NAME_1"], "url": os.environ["API_URL_1"]},
    {"name": os.environ["API_NAME_2"], "url": os.environ["API_URL_2"]},
]

bot = telebot.TeleBot(TELEGRAM_TOKEN)
last_warnings: Dict[str, int] = {}


def check_api_status(api: Dict[str, str]) -> Tuple[int, str]:
    try:
        response = requests.get(api["url"], timeout=10)
        if response.status_code == requests.codes.ok:
            logging.info(f"{api['name']} is up and running!")
            return (response.status_code, "OK")
        else:
            logging.error(
                f"{api['name']} returned status code {response.status_code}: {response.text}"
            )
            return (response.status_code, response.text)
    except requests.exceptions.Timeout:
        logging.error(f"{api['name']} timed out!")
        return (requests.codes.request_timeout, "Request timed out!")
    except requests.exceptions.RequestException as e:
        logging.error(f"{api['name']} returned an error: {e}")
        return (requests.codes.internal_server_error, str(e))


@bot.message_handler(commands=["start"])
def send_welcome(message: telebot.types.Message) -> None:
    bot.reply_to(
        message, "Welcome to API WatchBot!\n\n Type /status to check APIs status."
    )


@bot.message_handler(commands=["status"])
def send_status(message: telebot.types.Message) -> None:
    response = "*🤖 API Status Monitoring*\n\n"
    for api in API_LIST:
        status_code, status_text = check_api_status(api)
        if status_code == requests.codes.ok:
            response += f"🟢 {api['name']}: _{status_code} - {status_text}_\n\n"
        else:
            response += f"🔴 {api['name']}: _{status_code} - {status_text}_\n\n"
    bot.send_message(TELEGRAM_GROUP_ID, response, parse_mode="Markdown")


def notify_problem() -> None:
    global last_warnings
    for api in API_LIST:
        status_code, status_text = check_api_status(api)
        if status_code != requests.codes.ok:
            if last_warnings.get(api["name"]) != status_code:
                notification = (
                    f"🔴 *{api['name']}* is down! _{status_code} - {status_text}_"
                )
                bot.send_message(TELEGRAM_GROUP_ID, notification, parse_mode="Markdown")
                last_warnings[api["name"]] = status_code


if __name__ == "__main__":
    print(
        """
           ///,        ////
           \  /,      /  >.
            \  /,   _/  /.
             \_  /_/   /.
              \__/_   <
              /<<< \_\_
             /,)^>>_._ \\
             (/   \\ /\\\\\\
                  // ````
                 ((`
           _____ _____  __          __   _       _     _           _   
     /\   |  __ \_   _| \ \        / /  | |     | |   | |         | |  
    /  \  | |__) || |    \ \  /\  / /_ _| |_ ___| |__ | |__   ___ | |_ 
   / /\ \ |  ___/ | |     \ \/  \/ / _` | __/ __| '_ \| '_ \ / _ \| __|
  / ____ \| |    _| |_     \  /\  / (_| | || (__| | | | |_) | (_) | |_ 
 /_/    \_\_|   |_____|     \/  \/ \__,_|\__\___|_| |_|_.__/ \___/ \__|
                                                                       
                                                                                           
"""
    )
    scheduler = BackgroundScheduler()
    scheduler.add_job(notify_problem, "interval", minutes=15)
    scheduler.start()

    bot.infinity_polling()
