import aiohttp
import asyncio
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent
import json
from time import sleep

day_time_in_seconds = 60 * 60 * 24

PAGES_START = 1
PAGES_FINISH = 50
BASE_URL = "https://readli.net/cat/fentezi/uzhasyi-i-mistika/"
HEADERS = {"User-Agent": UserAgent().random}
json_file = "./data.json"
list_books = []

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get(page_url, headers=HEADERS) as responce:
            r = await aiohttp.StreamReader.read(responce.content)
            soup  = BS(r, 'html.parser')

            items = soup.find_all('div', {'class': 'book__cols'})
            for item in items:
                title = item.find('a', {'class': 'book__link'})
                title_text = item.find('a', {'class': 'book__link'}).text.strip()
                book = item.find('a', {'class' : "book__image"})
                book_link = book.get("href")
                book_img = book.find('img').get('src')
                author = item.find('p', {'class': 'book__authors'}).find('a').text.strip()
                
                async with session.get(book_link, headers=HEADERS) as responce:
                    resp = await aiohttp.StreamReader.read(responce.content)
                    soups  = BS(resp, 'html.parser')
                    link_to_download = soups.find('a', {'class':'download__link'}).get('href')
                    
                    if link_to_download == "#":
                        continue
                    
                    description_block = soups.find('article', {'class': 'seo__content'})
                    description = description_block.find('p').text.strip()
                    

                list_books.append({'title': title_text, 'authors': author, 'bookLink': book_link, 'imgLink': book_img, 'downloadLink': f'https://readli.net{link_to_download}', 'description': description})
    
while True:
    if  __name__ == "__main__":
        for i in range(PAGES_START, PAGES_FINISH+1, 1):
            print(i)
            page_url = f"{BASE_URL}page/{i}/"
            loop = asyncio.get_event_loop()
            loop.run_until_complete(main())
    
        with open(f"./pagesJson/pages{PAGES_START}-{PAGES_FINISH}.json", "w+") as fp:
            json.dump(list_books, fp)
            
        
        sleep(day_time_in_seconds)
    