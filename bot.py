import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

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
    welcome_message = (
        f"hey {user.first_name}!\n\n"
        "i'm headlinehub, your multilingual news bot.\n\n"
        "send /help to see what i can do."
    )
    await update.message.reply_text(welcome_message)


# --- new part: a dedicated /help command handler ---
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """sends a message when the command /help is issued."""
    help_text = (
        "here's how to use me:\n"
        "  - send /news for headlines in english.\n"
        "  - send /news <lang_code> for a translation.\n\n"
        "for example: /news hi (hindi), /news fr (french), or /news ta (tamil)."
    )
    await update.message.reply_text(help_text)


async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """this function runs when the user sends the /news command."""
    
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    language_code = 'en'
    if context.args:
        language_code = context.args[0].lower()
    
    try:
        # we'll wrap the scraper call in a try block.
        headlines = scrape_and_analyze_headlines(language_code)
        
        if not headlines:
            await update.message.reply_text("sorry, i couldn't retrieve the headlines right now. the news source might be unavailable.")
            return
            
        title = f"here are the latest headlines (translated to {language_code}):" if language_code != 'en' else "here are the latest headlines:"
        response_body = "\n\n".join(headlines)
        full_response = f"{title}\n\n{response_body}"
        
        if len(full_response) > 4096:
            full_response = full_response[:4090] + "\n..."

        await update.message.reply_text(full_response)
        
    # --- new part: catch errors from the scraper ---
    # this will specifically catch errors if the user provides a bad language code.
    except Exception as e:
        logging.error(f"error processing news command: {e}")
        await update.message.reply_text(f"sorry, i couldn't process that. did you use a valid language code? (e.g., 'es', 'hi', 'fr')")


def main():
    """this is where our bot will start running."""

    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        logging.error("telegram token not found in .env file. please add it.")
        return

    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler('start', start))
    # register the new /help handler
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('news', news))

    logging.info("bot is starting up...")
    application.run_polling()
    logging.info("bot has shut down.")


if __name__ == '__main__':
    main()