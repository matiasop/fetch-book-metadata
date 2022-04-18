import json

def read_quotes(file_name, book_title):
    with open(file_name, "r", encoding="utf-8") as file:
        quotes_dict = json.load(file)
        book_quotes = quotes_dict[book_title]
        for q in book_quotes:
            print(f"{q['date']} {q['time']}")
            print(f"{q['quote']}")
            print(64*"-")

if __name__ == "__main__":
    file_name = "./data/quotes.json"
    book_title = "La meta (Eliyahu M. Goldratt)"
    read_quotes(file_name, book_title)
