import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

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
    # let's update the welcome message to explain the new feature.
    welcome_message = (
        f"hey {user.first_name}!\n\n"
        "i'm headlinehub, your multilingual news bot.\n\n"
        "here's how to use me:\n"
        "  - send /news for headlines in english.\n"
        "  - send /news <lang_code> for a translation.\n\n"
        "for example: /news hi (hindi), /news fr (french), or /news ta (tamil)."
    )
    await update.message.reply_text(welcome_message)


async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """this function runs when the user sends the /news command."""
    
    # by default, we'll get english news.
    language_code = 'en'
    
    # 'context.args' is a list of words sent after the command.
    if context.args:
        # we take the first word after the command as our language code.
        language_code = context.args[0].lower()
        await update.message.reply_text(f"fetching headlines and translating to '{language_code}', please wait...")
    else:
        await update.message.reply_text("fetching the latest english headlines, please wait...")
    
    # now, we pass the chosen language code to our scraper function.
    headlines = scrape_and_analyze_headlines(language_code) 
    
    if not headlines:
        await update.message.reply_text("sorry, i couldn't retrieve the headlines right now. please try again later.")
        return
        
    title = f"here are the latest headlines (translated to {language_code}):" if language_code != 'en' else "here are the latest headlines:"
    
    # we'll add extra newlines for spacing between each translated block.
    response_body = "\n\n".join(headlines)
    
    # combine the title and the body for the final message.
    full_response = f"{title}\n\n{response_body}"
    
    # telegram has a message length limit of 4096 characters.
    # this is the corrected, complete line.
    if len(full_response) > 4096:
        full_response = full_response[:4090] + "\n..."

    await update.message.reply_text(full_response)


def main():
    """this is where our bot will start running."""

    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        logging.error("telegram token not found in .env file. please add it.")
        return

    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('news', news))

    logging.info("bot is starting up...")
    application.run_polling()
    logging.info("bot has shut down.")


if __name__ == '__main__':
    main()