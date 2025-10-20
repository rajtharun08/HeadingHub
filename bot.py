import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- new part: import our own scraper function ---
# this makes the functions in news_scraper.py available here.
from news_scraper import scrape_and_analyze_headlines

# load our secret token from the .env file
load_dotenv()

# basic logging to see what the bot is doing
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """this function runs when the user sends the /start command."""
    user = update.effective_user
    # let's update the welcome message to mention the new command.
    welcome_message = (
        f"hey {user.first_name}!\n\n"
        "i'm headlinehub, your friendly news bot.\n\n"
        "use the /news command to get the latest headlines with sentiment."
    )
    await update.message.reply_text(welcome_message)


# --- new part: defining the /news command handler ---
async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """this function runs when the user sends the /news command."""
    
    # let the user know we've received the command and are working on it.
    await update.message.reply_text("fetching the latest headlines, please wait...")
    
    # call our scraper function. by default, this gets english headlines.
    headlines = scrape_and_analyze_headlines() 
    
    # it's important to handle the case where the scraping fails.
    if not headlines:
        await update.message.reply_text("sorry, i couldn't retrieve the headlines right now. please try again later.")
        return
        
    # if we got headlines, we'll join them together into one big message.
    # we use two newlines '\n\n' to create a blank line between each headline for readability.
    response_text = "\n\n".join(headlines)
    
    await update.message.reply_text(response_text)


def main():
    """this is where our bot will start running."""

    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        logging.error("telegram token not found in .env file. please add it.")
        return

    application = ApplicationBuilder().token(token).build()

    # register the /start handler.
    application.add_handler(CommandHandler('start', start))
    
    # --- new part: register the /news handler ---
    # now we link the '/news' command to our new 'news' function.
    application.add_handler(CommandHandler('news', news))

    logging.info("bot is starting up...")
    application.run_polling()
    logging.info("bot has shut down.")


if __name__ == '__main__':
    main()