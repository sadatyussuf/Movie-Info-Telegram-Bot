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
        text_genre_title = (
            "Please add a genre name attached to the command e.g.  /genre *comedy*"
        )
    if len(context.args) > 1:
        text_genre_title = "Please add only one genre name attached to the command e.g.  /genre *comedy*"

    if len(context.args) == 1:
        text_genre_title = f" **_🎥 Top 10 Popular {context.args[0].upper()} Movies and TV Shows on IMDb_** \n\n"
        text = context.args[0].lower()
        get_genre_info = search_genre(text)

        if len(get_genre_info) > 0:
            for line in get_genre_info:
                text_genre_title += f"*{line['film_position']}*  {line['film_name']} - 🌟*{line['film_rating']}* \n\n"

        # if results is empty
        if len(get_genre_info) == 0:
            text_genre_title = "No result Found"

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text_genre_title,
        parse_mode=ParseMode.MARKDOWN,
    )


async def movie(update: Update, context: ContextTypes):

    text_genre_title = (
        "Please add a genre name attached to the command e.g.  /genre *Men In Black*"
    )
    # print(context.args)
    if len(context.args) > 0:
        text = " ".join(context.args)
        get_movie_info = search_movie(text)

        text_genre_title = (
            f"**_ No Result Found for Movie with title_** *{text.upper()}* "
        )
        if len(get_movie_info) > 0:
            text_genre_title = f" {get_movie_info[0]['film_name']} - 🌟 *{get_movie_info[0]['film_rating']}* 🌟  **_{get_movie_info[0]['film_genre']}_** \n\n"

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text_genre_title,
        parse_mode=ParseMode.MARKDOWN,
    )


def main():
    application = ApplicationBuilder().token(ACCESS_TOKEN).build()

    start_handler = CommandHandler("start", start)
    genre_handler = CommandHandler("genre", genre)
    movie_handler = CommandHandler("movie", movie)

    application.add_handler(start_handler)
    application.add_handler(genre_handler)
    application.add_handler(movie_handler)

    application.run_polling()


if __name__ == "__main__":
    # asyncio.run(main())
    main()
