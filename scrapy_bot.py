from bs4 import BeautifulSoup
import requests


URL = "https://www.imdb.com/search/title/"


def search_genre(genre):
    try:
        page = requests.get(f"{URL}?genres={genre}")
        soup = BeautifulSoup(page.content, "html.parser")
        results = []

        count = 1
        for res in soup.find_all("div", {"class": "lister-item mode-advanced"}):

            film_rating = (
                res.find("div", {"class": "ratings-imdb-rating"})
                # .find("strong")
                # .get_text()
            )
            if film_rating is not None:
                film_rating = film_rating.find("strong").get_text()
            if film_rating is None:
                film_rating = 0.0

            film_name = (
                res.find("h3", {"class": "lister-item-header"}).find("a").get_text()
            )

            film_position = (
                res.find("h3", {"class": "lister-item-header"})
                .find("span", {"class": "lister-item-index unbold text-primary"})
                .get_text()
            )

            print(film_position, film_name, film_rating)
            results.append(
                {
                    "film_position": film_position,
                    "film_name": film_name,
                    "film_rating": film_rating,
                }
            )

            if count >= 10:
                break
            count += 1
        print("--------------------------------")
        print(results)
        print("--------------------------------")
        return results
    except AttributeError as e:
        print(e)


def search_movie(movie_title):
    pass
    page = requests.get(f"{URL}?title={movie_title}")
    soup = BeautifulSoup(page.content, "html.parser")

    result = []

    movie_card = soup.find("div", {"class": "lister-item mode-advanced"})
    film_rating = (
        movie_card.find("div", {"class": "ratings-imdb-rating"})
        # .find("strong")
        # .get_text()
    )
    if film_rating is not None:
        film_rating = film_rating.find("strong").get_text()
    if film_rating is None:
        film_rating = 0.0

    film_name = (
        movie_card.find("h3", {"class": "lister-item-header"}).find("a").get_text()
    )

    print(film_name, film_rating)
    result.append(
        {
            "film_name": film_name,
            "film_rating": film_rating,
        }
    )


# search_genre("comedy")
# search_genre("action")

search_movie("men in black")
