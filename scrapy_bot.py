from bs4 import BeautifulSoup
import requests


GENRE_URL = "https://www.imdb.com/search/title/"


def search_genre(genre):
    page = requests.get(f"{GENRE_URL}?genres={genre}")
    soup = BeautifulSoup(page.content, "html.parser")
    results = []

    count = 1
    for res in soup.find_all("div", {"class": "lister-item mode-advanced"}):
        film_rating = (
            res.find("div", {"class": "inline-block ratings-imdb-rating"})
            .find("strong")
            .get_text()
        )

        film_name = res.find("h3", {"class": "lister-item-header"}).find("a").get_text()

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

    # print(soup.prettify())


search_genre("action")
