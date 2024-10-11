import os
from telegram.ext import Updater, CommandHandler
import requests
import time

# Get environment variables
TOKEN = os.environ.get('TOKEN')
GROUP_ID = os.environ.get('GROUP_ID')

def get_crypto_prices():
    url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,dogecoin&vs_currencies=usd'
    response = requests.get(url)
    data = response.json()
    return data

def send_message(context):
    prices = get_crypto_prices()
    message = "Current Crypto Prices:\n"
    message += f"Bitcoin: ${prices['bitcoin']['usd']}\n"
    message += f"Ethereum: ${prices['ethereum']['usd']}\n"
    message += f"Dogecoin: ${prices['dogecoin']['usd']}"
    
    context.bot.send_message(chat_id=GROUP_ID, text=message)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Bot started. It will post crypto prices every hour.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    try:
        while True:
            send_message(updater)
            time.sleep(3600)  # Sleep for 1 hour
    except KeyboardInterrupt:
        updater.stop()

if __name__ == '__main__':
    main()
