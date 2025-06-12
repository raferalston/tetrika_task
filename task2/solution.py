'''С тестами парсинга я еще не сталкивался, но с интересом изучу и данную тему. 
Сам парсинг давно не применял, все через апи делать получается'''

import csv
import logging
import requests
import time

from collections import defaultdict
from bs4 import BeautifulSoup


logging.basicConfig(
    filename='wiki_animals_parser.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

BASE_URL = "https://ru.wikipedia.org"
CATEGORY_URL = f"{BASE_URL}/wiki/Категория:Животные_по_алфавиту"

def get_animals_by_letter():
    counts = defaultdict(int)
    next_page = CATEGORY_URL
    counter = 1

    logging.info("Starting animal parsing process")
    
    while next_page:
        try:
            logging.info(f"Fetching page {counter}: {next_page}")
            response = requests.get(next_page)
            response.raise_for_status() 
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for li in soup.select('#mw-pages .mw-category li'):
                name = li.text.strip()
                first_letter = name[0].upper()
                if 'А' <= first_letter <= 'Я':
                    counts[first_letter] += 1
                    
            next_link = soup.select_one('a:-soup-contains("Следующая страница")')
            if not next_link:
                for a in soup.select('#mw-pages a'):
                    if 'Следующая страница' in a.text:
                        next_page = BASE_URL + a['href']
                        break
                else:
                    logging.info("Next page not found")
                    next_page = None
            else:
                next_page = BASE_URL + next_link['href']
            
            time.sleep(0.1)
            logging.info(f"Successfully processed page {counter}")
            counter += 1
            
        except requests.RequestException as e:
            logging.error(f"Error fetching page {counter}: {str(e)}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error processing page {counter}: {str(e)}")
            raise
            
    logging.info(f"Parsing completed. Processed {counter-1} pages")
    return counts
        

def save_to_csv(data, filename='beasts.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for letter in sorted(data.keys()):
            writer.writerow([letter, data[letter]])
    logging.info(f"Results can be found in a beasts.csv")

animals_count = get_animals_by_letter()
save_to_csv(animals_count)
