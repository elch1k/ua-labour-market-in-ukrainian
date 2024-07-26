import time
import datetime
from bs4 import BeautifulSoup
import aiohttp
import asyncio
import pandas as pd
import os
import re
import csv

start_time = time.time()
cities = {"kyiv": "Київ", "odesa": "Одеса", "kharkiv": "Харків", "dnipro": "Дніпро", "vinnytsya": "Вінниця", 
          "ivano-frankivsk": "Івано-Франківськ", "cherkasy": "Черкаси", "chernihiv": "Чернігів", "chernivtsi_cv": "Чернівці",
          "poltava": "Полтава", "zaporizhzhya": "Запоріжжя", "lutsk": "Луцьк", "lviv": "Львів", "zhytomyr": "Житомир",
          "uzhhorod": "Ужгород", "rivne": "Рівне", "ternopil": "Тернопіль", "khmelnytskyi": "Хмельницький",
          "mykolaiv_nk": "Миколаїв", "kropyvnytskyi": "Кропивницький", "kherson": "Херсон", "remote": "Дистанційно"}

categories = {"customer-service": "Сфера обслуговування", "production-engineering": "Робочі спеціальності, виробництво", 
                 "sales": "Продаж, закупівля", "retail": "Роздрібна торгівля",
                 "hotel-restaurant-tourism": "Готельно-ресторанний бізнес, туризм",
                 "administration": "Адмiнiстрацiя, керівництво середньої ланки", "logistic-supply-chain": "Логістика, склад, ЗЕД", 
                 "healthcare": "Медицина, фармацевтика", "accounting" : "Бухгалтерія, аудит",
                 "marketing-advertising-pr": "Маркетинг, реклама, PR", "auto-transport": "Транспорт, автобізнес",
                 "it": "IT, комп'ютери, інтернет", "office-secretarial": "Секретаріат, діловодство, АГВ",
                 "banking-finance": "Фінанси, банк", "construction-architecture": "Будівництво, архітектура",
                 "beauty-sports": "Краса, фітнес, спорт", "telecommunications": "Телекомунікації та зв'язок", 
                 "education-scientific": "Освіта, наука", "design-art": "Дизайн, творчість",
                 "security": "Охорона, безпека", "hr-recruitment": "Управління персоналом, HR", "legal": "Юриспруденція",
                 "publishing-media": "ЗМІ, видавництво, поліграфія", "management-executive": "Топменеджмент, керівництво вищої ланки",
                 "agriculture": "Сільське господарство, агробізнес", "culture-music-showbiz": "Культура, музика, шоу-бізнес",
                 "real-estate": "Нерухомість", "insurance": "Страхування"}

study_mark = ["стажер", "учень", "ученик", "intern", "стажерська", "стажування", "практикант", "trainee", "з навчанням", "с обучением"]

big_data = []

async def get_page_info(session, sem, url, page):
    async with sem:
        link = url + "?page=" + str(page)
        async with session.get(link) as response:
            soup = BeautifulSoup(await response.text(), "lxml")

            # перша картка з гарячою пропозицією
            top_hot_card = soup.find("div", 
                                    class_="card card-hover card-search card-visited wordwrap job-link js-job-link-blank js-hot-block mt-lg")
            # перша звичайна картка
            top_card = soup.find("div", class_="card card-hover card-search card-visited wordwrap job-link js-job-link-blank mt-lg")
            # гарячі пропозиції
            hot_cards = soup.find_all("div", 
                                        class_="card card-hover card-search card-visited wordwrap job-link js-job-link-blank js-hot-block")
            # картки з пропозиціями
            just_cards = soup.find_all("div", 
                                        class_="card card-hover card-search card-visited wordwrap job-link js-job-link-blank")

            cards = []
            
            if top_hot_card is not None:
                cards.append(top_hot_card)
            else:
                if top_card is not None:
                    cards.append(top_card)
            if len(hot_cards) > 0:
                cards.extend(hot_cards)
            if len(just_cards) > 0:
                cards.extend(just_cards)
            
            for card in cards: 
                # назва роботи (вакансії)
                try:
                    job_name = card.find("h2", class_="my-0").get_text().strip()
                    # job_name = card.find("h2", class_="my-0").find("a").text.strip()
                except Exception:
                    print("Змінився тег для пошуку job_name")

                # url на дану роботу
                link = "https://www.work.ua" + str(card.find("h2", class_="my-0").find_next().get("href"))
                
                # Бронювання від роботодавця
                reservation = 0
                try:
                    info = card.find("span", class_="label label-green-100 cursor-p").find_all("span")[-1].text.strip()
                    if "Бронювання" in info:
                        reservation = 1
                except Exception:
                    reservation = 0

                # Можливий відгук на вакансію без попереднього резюме
                without_resume = 0
                try:
                    label = card.find("span", class_="label label-blue-mariner-100")
                    if label and "Відгук без резюме" in label.get_text():
                        without_resume = 1
                except Exception:
                    without_resume = 0

                # назва компанії, яка надає вакансію
                raw_company_name = None
                add_info = None

                try:
                    raw_company_name = card.find("div", class_="mt-xs").find("span", class_="mr-xs").find("span", class_="strong-600").text.strip()
                except Exception:
                    try:
                        raw_company_name = card.find("div", class_="mt-xs").find("span", class_="").find("span", class_="strong-600").text.strip()
                    except Exception:
                        print(f"Змінився тег для пошуку. url: {link}")

                if raw_company_name:
                    parts = raw_company_name.split(", ")
                    if len(parts) > 1:
                        add_info = parts[-1]
                        if ")" in add_info and "(" not in add_info:
                            add_info = add_info.replace(")", "")

                # Блок знаходження категорії відповідної вакансії
                for key in categories.keys():
                    if key in url:
                        vacancy_category = categories[key]

                # work_education = 1 if "з навчанням" in job_name else 0
                internship = 1 if any(keyword in job_name.lower() for keyword in study_mark) else 0
                
                # Блок коду з виясненням зарплати
                income_element = card.find("span", class_="strong-600")
                if income_element:
                    income = income_element.text.strip()
                    if raw_company_name == income:
                        income = None
                        min_income, max_income = None, None
                    elif "–" in income or "-" in income:
                        income_cleaned = income.replace("грн", "").strip()
                        min_income, max_income = income_cleaned.split("–") if "–" in income_cleaned else income_cleaned.split("-")
                        min_income = int(re.sub(r"[^0-9-]+", "", min_income))
                        max_income = int(re.sub(r"[^0-9-]+", "", max_income))
                    else:
                        singl_inc = re.sub(r"[^0-9]+", "", income)
                        try:
                            min_income, max_income = int(singl_inc), int(singl_inc)
                        except:
                            min_income, max_income = None, None
                else:
                    min_income, max_income = None, None
                
                # Деталі вакансії
                chosen_city = card.find("div", class_="mt-xs").find("span", class_="").text.strip()
                if chosen_city == raw_company_name:
                    for key in cities.keys():
                        if key in url:
                            chosen_city = cities[key]
                if "," in chosen_city:
                    chosen_city = chosen_city.split(",")[0]
                
                vacant_text = card.find("p", class_="ellipsis ellipsis-line ellipsis-line-3 text-default-7 mb-0").text.strip().lower()
                full_employment = 1 if "повна зайнятість" in vacant_text else 0
                underemployment = 1 if "неповна зайнятість" in vacant_text else 0
                student = 1 if "також готові взяти студента" in vacant_text else 0
                disability = 1 if "людину з інвалідністю" in vacant_text else 0
                veteran = 1 if "ветерана" in vacant_text else 0
                pensioner = 1 if "пенсіонера" in vacant_text else 0 
                
                # Освіта
                if "вища освіта" in vacant_text:
                    necess_education = "Вища освіта"
                elif "середня спеціальна освіта" in vacant_text:
                    necess_education = "Середня спеціальна освіта"
                else:
                    necess_education = None

                # Досвід роботи | іноді досвід в місяцях, тож варто це врахувати
                experience_match = re.search(r"досвід роботи від (\d+)\s*(?:років|рік|року|місяців|місяця|місяць)?", vacant_text)
                if experience_match:
                    experience_amount = int(experience_match.group(1))
                    if 'місяц' in experience_match.group(0):
                        years_of_experience = experience_amount / 12
                    else:
                        years_of_experience = experience_amount
                else:
                    years_of_experience = 0
                
                big_data.append({"Назва роботи" : job_name,
                                "Назва компанії": raw_company_name,
                                "Місто": chosen_city,
                                "Категорія вакансії": vacancy_category,
                                "Стажування / Навчання на роботі": internship, 
                                "Мінімальна ЗП": min_income,
                                "Максимальна ЗП": max_income,
                                "Необхідний досвід": years_of_experience,
                                "Необхідна освіта": necess_education,
                                "Повна зайнятість": full_employment,
                                "Неповна зайнятість": underemployment,
                                "Студент": student,
                                "Інвалідність": disability,
                                "Ветеран": veteran,
                                "Пенсіонер": pensioner,
                                "Бронювання": reservation,
                                "Без резюме": without_resume,
                                "Додаткова інформація": add_info,
                                "Посилання" : link})

async def gather_data():
    curr_direct = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_csv(os.path.join(curr_direct, "links_22_07_2024_15.csv"))
    sem = asyncio.Semaphore(15)
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(len(df)):
            url = df.iloc[i].iloc[-1]
            async with session.get(url) as response:
                soup = BeautifulSoup(await response.text(), "lxml")
                try:
                    counts_of_page = int(soup.find_all("a", class_="ga-pagination-default pointer-none-in-all")[-1].text.strip())
                except (IndexError, ValueError):
                    counts_of_page = 1

                for page in range(1, counts_of_page + 1):
                    task = asyncio.create_task(get_page_info(session, sem, url, page))
                    tasks.append(task)
        
        await asyncio.gather(*tasks)

def main():
    asyncio.run(gather_data())
    cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H")

    with open(f"async_all_labour_market_ua_{cur_time}_1.csv", mode="w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                "Назва роботи",
                "Назва компанії",
                "Місто",
                "Категорія вакансії",
                "Стажування / Навчання на роботі", 
                "Мінімальна ЗП",
                "Максимальна ЗП",
                "Необхідний досвід",
                "Необхідна освіта",
                "Повна зайнятість",
                "Неповна зайнятість",
                "Студент",
                "Інвалідність",
                "Ветеран",
                "Пенсіонер",
                "Бронювання",
                "Без резюме",
                "Додаткова інформація",
                "Посилання"
            )
        )

    for data in big_data:
        with open(f"async_all_labour_market_ua_{cur_time}_1.csv", mode="a", newline='', encoding="utf-8") as file:
            writer = csv.writer(file)

            writer.writerow(
                (
                    data["Назва роботи"],
                    data["Назва компанії"],
                    data["Місто"],
                    data["Категорія вакансії"],
                    data["Стажування / Навчання на роботі"], 
                    data["Мінімальна ЗП"],
                    data["Максимальна ЗП"],
                    data["Необхідний досвід"],
                    data["Необхідна освіта"],
                    data["Повна зайнятість"],
                    data["Неповна зайнятість"],
                    data["Студент"],
                    data["Інвалідність"],
                    data["Ветеран"],
                    data["Пенсіонер"],
                    data["Бронювання"],
                    data["Без резюме"],
                    data["Додаткова інформація"],
                    data["Посилання"]
                )
            )
    finish_time = time.time() - start_time
    print(f"Витрачений час на роботу скрипту: {finish_time}")

if __name__=="__main__":
    main()

# в минулий раз щоб спарсити всю інфу по всім містам потрібно було 21357.68 секунд (5,93 годин)
# для асинхронного парсера з додатковим місцем роботи (remote work) потрібно було 2031.72 секунд (близько 34 хвилин)
# в результаті швидкість покращена в 10.5 разів