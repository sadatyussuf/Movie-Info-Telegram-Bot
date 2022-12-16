from dotenv import load_dotenv

# import telegram
# import asyncio
import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

logging.basicConfig(
    format=" %(asctime)s - %(name)s - %(levelname)s: %(message)s", level=logging.INFO
)

# print(ACCESS_TOKEN)
async def start(update: Update, context: ContextTypes):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot,Please talk to me"
    )


async def echo(update: Update, context: ContextTypes):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=update.message.text
    )


async def caps(update: Update, context: ContextTypes):
    text_caps = " ".join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)
    # print("=====================================")
    # print(context.args)


async def unknown(update: Update, context: ContextTypes):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command"
    )


if __name__ == "__main__":
    # asyncio.run(main())
    application = ApplicationBuilder().token(ACCESS_TOKEN).build()

    start_handler = CommandHandler("start", start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    caps_handler = CommandHandler("caps", caps)

    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(caps_handler)
    application.add_handler(unknown_handler)

    # application.run_polling(stop_signals=None)
    application.run_polling()
