import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, Application, ContextTypes


load_dotenv()
telegram_bot_token = os.getenv("bot_token").strip()
scrape_url = os.getenv("scrape_url").strip()
subscribed_users = set()


def scrape_swedish_data():
    response = requests.get(scrape_url)
    soup = BeautifulSoup(response.text, features="html.parser")
    swedish_input_field = soup.find('span', class_="text-success")
    return swedish_input_field.text


async def send_announcement(context: ContextTypes.DEFAULT_TYPE):
    print("Sending annoucement")
    exchange_rate = scrape_swedish_data()
    text = f"1 SGD equals to {exchange_rate} SEK"
    for chat_id in subscribed_users:
        url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage?chat_id={chat_id}&text={text}"
        requests.get(url)


async def subscribe(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    print(f"{update.message.chat_id} subscribe")
    if chat_id not in subscribed_users:
        subscribed_users.add(chat_id)
        rate = scrape_swedish_data()
        await update.message.reply_text("You have subscribed to receive announcements.")
        await update.message.reply_text(f"1 SGD equals to {rate} SEK")
    else:
        await update.message.reply_text("You are already subscribed to receive annoucements.")


async def unsubscribe(update: Update, context: CallbackContext):
    print(f"{update.message.chat_id} unsubscribe")
    chat_id = update.message.chat_id
    if chat_id in subscribed_users:
        subscribed_users.remove(chat_id)
        
        await update.message.reply_text("You have unsubscribed successfully.")
    else:
        await update.message.reply_text("You are not subscribed to receive annoucements.")


async def start(update: Update, context: CallbackContext):
    print(f"{update.message.chat_id} start")
    await update.message.reply_text("Welcome! Use /subscribe to receive announcements.")


def main():
    print('Starting bot...')
    app = Application.builder().token(telegram_bot_token).build()

    # Commands
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('subscribe', subscribe))
    app.add_handler(CommandHandler('unsubscribe', unsubscribe))

    # Schedule the announcement every 6 hours
    app.job_queue.run_repeating(send_announcement, interval=6*3600, first=0)

    # Start polling
    app.run_polling(poll_interval=3)


if __name__ == '__main__':
    main()