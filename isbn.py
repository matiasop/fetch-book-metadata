import requests
import time
import os


def correct_title(title):
    correct = {
        "El hombre unidimensional (Herbert Marcuse)": "One-Dimensional Man",
        "Richard Taylor (Restoring Pride The Lost Virtue of Our Age (1995, Prometheus Books))": "Restoring Pride The Lost Virtue of Our Age",
        "Rudiger Safranski (Nietzsche A Philosophical Biography (2003, W. W. Norton;Company))": "Nietzsche A Philosophical Biography (Rudiger Safranski)",
        "La cultura (Dietrich Schwanitz)": "culture (Dietrich Schwanitz)",
        "En defensa de la Ilustración (Steven Pinker)": "enlightenment now (steven pinker)",
        "La tabla rasa (Steven Pinker)": "The Blank Slate (steven pinker)",
        "Conjuración de Catilina y otros textos (Salustio;Pseudo Salustio;Pseudo Cicerón)": "Conjuración de Catilina",
        "How to DeFi (CoinGecko;Lau, Darren;Lau, Daryl;Teh, Sze Jin;Kho, Kristian;Azmi, Erina;Lee, TM;Ong, Bobby)": "How To Defi",
        "Que_es_el_hombre_martin_buber (Martin Buber)": "Que es el hombre (Martin Buber)",
        "Guerra y paz (Lev Nikoláievich Tolstoi)": "War and Peace",
        "The Bitcoin Standard (Saifedean Ammous)": "Bitcoin Standard",
        "Madame Bovary (trad. Juan Bravo Castillo) (Gustave Flaubert)": "Madame Bovary",
        "Meditaciones (Gredos) (Marco Aurelio Antonino Augusto)": "Meditaciones (Marco Aurelio)",
        "Copia-o-Muerte-Book (Desconocido)": "Copia o Muerte",
        "El Imperio Final (Ed. ilustrada) (Brandon Sanderson)": "The Final Empire (Brandom Sanderson)",
        "Early Retirement Extreme: A philosophical and practical guide to financial independence (Fisker, Jacob Lund;Averbach, Zev;Beaver, Ann)": "Early Retirement Extreme: A philosophical and practical guide to financial independence",
        "El camino de los reyes (Brandon Sanderson)": "The way of kings",
        "LA FE EXPLICADA Leo J 1.doc (Unknown)": "La fe explicada (Leo J. Trese)",
    }

    if title not in correct:
        return title
    return correct[title]


def get_book_info(title):
    print(f"Getting data for:\n{title}")
    initial_time = time.time()
    search_query = correct_title(title)
    api_key = os.getenv('API_KEY')
    url = f"https://www.googleapis.com/books/v1/volumes?q={search_query}&key={api_key}"
    print('URL', url)

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()

    if data["totalItems"] == 0:
        print(f"total Items for {title} is equal to 0")
        raise Exception
        return ("", "", "", "", "", "", "", "", "")

    book_info = data["items"][0]
    book_title = book_info["volumeInfo"]["title"]
    author = book_info["volumeInfo"]["authors"][0]
    published_date = book_info["volumeInfo"]["publishedDate"]
    page_count = ""
    if "pageCount" in book_info["volumeInfo"]:
        page_count = book_info["volumeInfo"]["pageCount"]
    language = book_info["volumeInfo"]["language"]
    isbn_10 = ""
    isbn_13 = ""
    for id in book_info["volumeInfo"]["industryIdentifiers"]:
        if id["type"] == "ISBN_10":
            isbn_10 = id["identifier"]
        elif id["type"] == "ISBN_13":
            isbn_10 = id["identifier"]

    # Get book thumbnail
    small_thumbnail = ""
    thumbnail = ""
    if "imageLinks" in book_info["volumeInfo"]:
        small_thumbnail = book_info["volumeInfo"]["imageLinks"]["smallThumbnail"]
        thumbnail = book_info["volumeInfo"]["imageLinks"]["thumbnail"]
    print(f"Time elapsed: {time.time() - initial_time}\n")
    return (
        book_title,
        author,
        published_date,
        page_count,
        language,
        small_thumbnail,
        thumbnail,
        isbn_10,
        isbn_13,
    )


if __name__ == "__main__":
    title = "Anna Karénina (Lev Nikoláievich Tolstói)"
    title = "Augustus (Williams, John)"
    title = "Elogio de la Ociosidad y otros ensayos (Bertrand Russell)"
    get_book_info(title)
