import os
import logging
from dotenv import load_dotenv
# we need a few more tools from the bot library.
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# load our secret token from the .env file
load_dotenv()

# basic logging to see what the bot is doing
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


# --- new part: defining our first command ---
# command handlers in this library are always 'async' functions.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """this function runs when the user sends the /start command."""
    
    # 'update' contains information about the incoming message, like who sent it.
    user = update.effective_user
    
    # we'll craft a friendly welcome message that uses the user's first name.
    welcome_message = (
        f"hey {user.first_name}!\n\n"
        "i'm headlinehub, your friendly news bot.\n\n"
        "soon, you'll be able to use the /news command to get the latest headlines."
    )
    
    # and here, we send our message back to the user's chat.
    await update.message.reply_text(welcome_message)


def main():
    """this is where our bot will start running."""

    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        logging.error("telegram token not found in .env file. please add it.")
        return

    application = ApplicationBuilder().token(token).build()

    # --- new part: registering the command ---
    # this line creates a link between the text command '/start' and our 'start' function.
    start_handler = CommandHandler('start', start)
    # now, we add this link to our application, so it knows what to do.
    application.add_handler(start_handler)


    # this starts the bot and makes it listen for messages.
    logging.info("bot is starting up...")
    application.run_polling()
    logging.info("bot has shut down.")


# standard python practice to make the script runnable.
if __name__ == '__main__':
    main()