import time
import datetime
from bs4 import BeautifulSoup
import aiohttp
import asyncio
import pandas as pd
import os

start_time = time.time()

cities_dict = {"kyiv": "Київ", "odesa": "Одеса", "kharkiv": "Харків", "dnipro": "Дніпро", "vinnytsya": "Вінниця", 
               "ivano-frankivsk": "Івано-Франківськ", "cherkasy": "Черкаси", "chernihiv": "Чернігів", "chernivtsi_cv": "Чернівці",
               "poltava": "Полтава", "zaporizhzhya": "Запоріжжя", "lutsk": "Луцьк", "lviv": "Львів", "zhytomyr": "Житомир",
               "uzhhorod": "Ужгород", "rivne": "Рівне", "ternopil": "Тернопіль", "khmelnytskyi": "Хмельницький",
               "mykolaiv_nk": "Миколаїв", "kropyvnytskyi": "Кропивницький", "kherson": "Херсон", "remote": "Дистанційно"}

async def get_category_links(city, session):  # отримуємо посилання за кожною категорією по кожному місту
    url = f"https://www.work.ua/jobs-{city}/"
    async with session.get(url) as response:
        response.raise_for_status()
        soup = BeautifulSoup(await response.text(), "lxml")
        block_of_vacancies = soup.find("ul", id="category_selection")  # збирання блоку "Категорія вакансії"
        vacancies = block_of_vacancies.find_all("a", class_="filter-link checkbox-link-js text-default no-decoration")  # збір кожної вакансії 

        category_links = []
        for vacancy in vacancies:
            category_links.append("https://www.work.ua/" + str(vacancy.get("href")))
        return category_links

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        tasks = [asyncio.create_task(get_category_links(city, session)) for city in cities_dict]     
        all_links = await asyncio.gather(*tasks)
        
        flat_links = [link for links in all_links for link in links]
        df = pd.DataFrame(flat_links, columns=["category_urls"])
        curr_direct = os.path.dirname(os.path.abspath(__file__))
        cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H")
        df.to_csv(os.path.join(curr_direct, f"links_{cur_time}.csv"), index=False)

        finish_time = time.time() - start_time
        print(f"Було витрачено часу на збір посилань та кількості сторінок: {finish_time}")

if __name__=='__main__':
    asyncio.run(main())

# Було витрачено часу на збір посилань та кількості сторінок: 3.68 seconds