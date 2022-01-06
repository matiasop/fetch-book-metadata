from typing import Iterator, DefaultDict
from collections import defaultdict
from datetime import datetime

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

def parse_quotes(quote_iterator: Iterator[list], to_be_ignored: set):
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

def main():
    quote_iterator = read_quote('My Clippings.txt')
    quote_dict: DefaultDict = parse_quotes(quote_iterator, TO_BE_IGNORED)
    print(quote_dict)

if __name__ == "__main__":
    main()
