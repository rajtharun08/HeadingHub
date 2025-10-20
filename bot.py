import os
import logging
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder

# load our secret token from the .env file
load_dotenv()

# basic logging to see what the bot is doing
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    """this is where our bot will start running."""

    # first, we get the telegram token from our .env file.
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        # it's crucial to stop if the token isn't found.
        logging.error("telegram token not found in .env file. please add it.")
        return

    # this is the core of the bot, which handles all the updates from telegram.
    application = ApplicationBuilder().token(token).build()

    # we'll register our command handlers here in the next commits.

    # this starts the bot and makes it listen for messages.
    logging.info("bot is starting up...")
    application.run_polling()
    logging.info("bot has shut down.")


# standard python practice to make the script runnable.
if __name__ == '__main__':
    main()