import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from news_scraper import scrape_and_analyze_headlines

# load secret token from the .env file
load_dotenv()

# set up basic logging so we can see what's going on in the console
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """handles the /start command."""
    user = update.effective_user
    await update.message.reply_text(f"hey {user.first_name}!\n\nsend /help to see what i can do.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """handles the /help command."""
    help_text = (
        "here's how to use me:\n"
        "  - send /news for headlines in english.\n"
        "  - send /news <lang_code> for a translation.\n\n"
        "for example: /news hi (hindi), /news fr (french)."
    )
    await update.message.reply_text(help_text)

async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """handles the /news command and its arguments."""
    # show the "typing..." indicator for better user feedback
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    language_code = 'en'
    # context.args is a list of words sent after the command, e.g., ['hi']
    if context.args:
        language_code = context.args[0].lower()
    
    headlines = scrape_and_analyze_headlines(language_code)
    
    if not headlines:
        await update.message.reply_text("sorry, i couldn't retrieve the headlines right now.")
        return
        
    title = f"latest headlines (translated to {language_code}):" if language_code != 'en' else "latest headlines:"
    response_body = "\n\n".join(headlines)
    full_response = f"{title}\n\n{response_body}"
    
    # telegram has a 4096 character limit per message
    if len(full_response) > 4096:
        full_response = full_response[:4090] + "\n..."

    await update.message.reply_text(full_response)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """a catch-all function to log any unhandled error and tell the user."""
    # log the full error traceback for ourselves to see in the console
    logging.error("exception while handling an update:", exc_info=context.error)
    
    # for the user, just send a simple, friendly message
    if update and update.effective_message:
        await update.effective_message.reply_text("sorry, something went wrong. please try again.")

def main():
    """the main function to set up and run the bot."""
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        logging.error("telegram token not found in .env file.")
        return

    application = ApplicationBuilder().token(token).build()

    # register the error handler first so it can catch issues in other handlers
    application.add_error_handler(error_handler)

    # register all our command handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('news', news))

    # this starts the bot and makes it listen for messages until you press ctrl+c
    application.run_polling()

if __name__ == '__main__':
    main()