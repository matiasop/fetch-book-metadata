from typing import Iterator, DefaultDict, Tuple, List
from collections import defaultdict
from datetime import datetime
from isbn import get_book_info
from operator import itemgetter
import json

TO_BE_IGNORED: set = {"Mis recortes  ", "Unknown (Usuario de Microsoft Office)",
                  "Pina Polo, Ciceron_triunfo_y_frustracion_de_un_homo  ",
                  "How to DeFi (CoinGecko;Lau, Darren;Lau, Daryl;Teh, Sze Jin;Kho, Kristian;Azmi, Erina;Lee, TM;Ong, Bobby)",
                  }

def read_quote(filename: str) -> Iterator[list]:
    with open(filename, 'r', encoding='utf-8') as file:
        quote = []
        for line in file:
            if '=========' in line:
                yield quote
                quote = []
            else:
                fixed_line = line.replace('\n', '')
                quote.append(fixed_line)

def parse_position(data: str):
    return data.split()[-1].split("-")

def rreplace(s: str, old: str, new: str) -> str:
    return (s[::-1].replace(old[::-1],new[::-1], 1))[::-1]

def parse_datetime(data: str):
    month_dict = {
        "enero": "01",
        "febrero": "02",
        "marzo": "03",
        "abril": "04",
        "mayo": "05",
        "junio": "06",
        "julio": "07",
        "agosto": "08",
        "septiembre": "09",
        "octubre": "10",
        "noviembre": "11",
        "diciembre": "12"
    }


    if "Añadido el" in data:
        # Spanish data
        day, month_name, year, timestring = data.replace("de", "").split(",")[-1].split()
        month = month_dict[month_name]
        date = f"{year}-{month}-{day}"
    elif "Added on" in data:
        # English data
        data = rreplace(data, ",", "")
        english_month_name, day, year, timestring, midday = data.split(",")[1:][0].strip().split()
        date_string = f"{english_month_name} {day} {year} {timestring} {midday}"
        parsed_time = datetime.strptime(date_string, "%B %d %Y %I:%M:%S %p")
        date, timestring = parsed_time.isoformat().split("T")
    else:
        raise ValueError
    return date, timestring


def parse_quotes(quote_iterator: Iterator[list], to_be_ignored: set) -> DefaultDict:
    quote_dict = defaultdict(list)
    for title, metadata, _, quote in quote_iterator:
        if title in to_be_ignored:
            continue
        
        position_data, date_data  = metadata.split('|')
        initial_pos, final_pos = parse_position(position_data)
        date, timestring = parse_datetime(date_data)

        quote_dict[title].append({'title': title, 'metadata': metadata, 'quote': quote,
                                 'initial_pos': initial_pos, 'final_pos': final_pos,
                                  'date': date, 'time': timestring})

    return quote_dict


def read_books_metadata_file(filename: str):
    with open(filename, "r") as json_file:
        books_metadata = json.load(json_file)
    return books_metadata

def write_json(filename: str, json_dict: dict):
    json_string = json.dumps(json_dict, ensure_ascii=False, indent=4, sort_keys=True)
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(json_string)


def get_quote_metadata(quote_dict: DefaultDict, books_metadata: dict) -> Tuple[DefaultDict, List]:
    quote_complete_dict = defaultdict(list)
    quote_list = []
    for title in quote_dict:
        if title in books_metadata:
            print(f"Found book: '{title}' in books_metadata file")
            book_title, author, published_date, page_count, language, small_thumbnail, thumbnail, isbn_10, isbn_13 = itemgetter('book_title', 'author', 'published_date', 'page_count', 'language', 'small_thumbnail', 'thumbnail', 'isbn_10', 'isbn_13')(books_metadata[title])
        else:
            print(f"Fetching data for book: '{title}'")
            book_title, author, published_date, page_count, language, small_thumbnail, thumbnail, isbn_10, isbn_13 = get_book_info(title)
            books_metadata[title] = {'book_title': book_title, 'author': author, 'published_date': published_date, 'page_count': page_count, 'language': language, 'small_thumbnail': small_thumbnail, 'thumbnail': thumbnail, 'isbn_10': isbn_10, 'isbn_13': isbn_13}
        for q in quote_dict[title]:
            data = {'title': q['title'], 'metadata': q['metadata'], 'quote': q['quote'],
                    'initial_pos': q['initial_pos'], 'final_pos': q['final_pos'],
                    'date': q['date'], 'time': q['time'], 'book_title': book_title,
                    'author': author, 'published_date': published_date,
                    'page_count': page_count, 'language': language,
                    'small_thumbnail': small_thumbnail, 'thumbnail': thumbnail,
                    'isbn_10': isbn_10, 'isbn_13': isbn_13}
            quote_complete_dict[title].append(data)
            quote_list.append(data)
    
    return quote_complete_dict, quote_list, books_metadata


def main():
    quote_iterator = read_quote('data/My Clippings.txt')
    quote_dict: DefaultDict = parse_quotes(quote_iterator, TO_BE_IGNORED)
    books_metadata = read_books_metadata_file('data/books_metadata.json')
    quote_complete_dict, quote_list, books_metadata = get_quote_metadata(quote_dict, books_metadata)

    # Create json file with json metadata
    write_json('data/books_metadata.json', books_metadata)

    # Create json file with titles as keys (OPTIONAL)
    write_json('data/quotes.json', quote_dict)

    # Create json file with additional info
    write_json('data/quotes_complete.json', quote_complete_dict)

if __name__ == "__main__":
    main()
