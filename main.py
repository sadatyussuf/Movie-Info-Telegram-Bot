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

# from telegram.parsemode import ParseMode
from telegram.constants import ParseMode

from scrapy_bot import search_genre, search_movie

load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

logging.basicConfig(
    format=" %(asctime)s - %(name)s - %(levelname)s: %(message)s", level=logging.INFO
)


async def start(update: Update, context: ContextTypes):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=" Hi! IMDb Info Dumper at your service. \n\n With me you can get Info about your favorite movies and series on IMDb. \n\n /genre *GENRE_NAME* : Fetches list of top 10 movies and tv shows belonging to that genre  \n\n /movie *MOVIE_NAME* : Fetches movie name with genre and rating of the movie",
        parse_mode=ParseMode.MARKDOWN,
    )


async def genre(update: Update, context: ContextTypes):
    if len(context.args) == 0:
        text_genre_title = "Please add a genre name e.g.  /genre *comedy*"
    if len(context.args) > 1:
        text_genre_title = "Please add only one genre name e.g.  /genre *comedy*"

    if len(context.args) == 1:
        text_genre_title = ""
        text = context.args[0].lower()
        get_genre_info = search_genre(text)

        if len(get_genre_info) > 0:
            for line in get_genre_info:
                text_genre_title += f"*{line['film_position']}* 🎥 {line['film_name']} - 🌟*{line['film_rating']}* \n\n"

        # if results is empty
        if len(get_genre_info) == 0:
            text_genre_title = "No result Found"

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text_genre_title,
        parse_mode=ParseMode.MARKDOWN,
    )


def main():
    application = ApplicationBuilder().token(ACCESS_TOKEN).build()

    start_handler = CommandHandler("start", start)
    genre_handler = CommandHandler("genre", genre)

    application.add_handler(start_handler)
    application.add_handler(genre_handler)

    application.run_polling()


if __name__ == "__main__":
    # asyncio.run(main())
    main()
