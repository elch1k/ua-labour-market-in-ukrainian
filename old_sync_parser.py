import time
import datetime
import requests
from bs4 import BeautifulSoup
import re
import csv
import fake_useragent
import random

cities_dict = {"kyiv": "Київ", "odesa": "Одеса", "kharkiv": "Харків", "dnipro": "Дніпро", "vinnytsya": "Вінниця", 
               "ivano-frankivsk": "Івано-Франківськ", "cherkasy": "Черкаси", "chernihiv": "Чернігів", "chernivtsi_cv": "Чернівці",
               "poltava": "Полтава", "zaporizhzhya": "Запоріжжя", "lutsk": "Луцьк", "lviv": "Львів", "zhytomyr": "Житомир",
               "uzhhorod": "Ужгород", "rivne": "Рівне", "ternopil": "Тернопіль", "khmelnytskyi": "Хмельницький",
               "mykolaiv_nk": "Миколаїв", "kropyvnytskyi": "Кропивницький", "kherson": "Херсон"} 

categories_ua = {"customer-service": "Сфера обслуговування", "production-engineering": "Робочі спеціальності, виробництво", 
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

keywords = ["стажер", "учень", "ученик", "intern", "стажерська", "стажування", "практикант", "trainee", "з навчанням", "с обучением"]

start_time = time.time()
date = datetime.datetime.now().strftime("%Y-%m-%d")
def get_job_vacancy_category(cities):
    for city in cities:
        url = f"https://www.work.ua/jobs-{city}/"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "lxml")
            vacancies = soup.find("div", id="category_selection").find_all("div", class_="checkbox")
        for vacancy in vacancies:
            category_link = vacancy.find("a", class_="filter-link checkbox-link-js text-default no-decoration")
            if category_link:
                category_link = "https://www.work.ua/" + str(category_link.get("href"))
            yield category_link

def get_counts_of_page_by_category(link):  # збираю кількість сторінок по яких потрібно пройтись
    for url in link:
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, "lxml")
        try:
            counts_of_page = (soup.find_all("a", class_="ga-pagination-default pointer-none-in-all")[-1]).text.strip()  # може бути тільки одна сторінка
        except Exception:
            counts_of_page = 1
        finally:
            cat_dict = {url : int(counts_of_page)}       
        yield cat_dict

def get_info_of_labour(parameter, categories, study_mark, cities):
    for dict_link in parameter:
        for linkk, pages in dict_link.items():
            print(pages)
            # pages = 1  # TEST
            for page in range(1, pages + 1):
                info_url = linkk + "?page=" + str(page)

                if (page % 25 == 0):
                    time.sleep(random.randint(15,18))

                if (page-1) % 45 == 0:
                    user = fake_useragent.UserAgent().random
                    header = {"user-agent": user}
                    time.sleep(random.randint(5,10))

                res = requests.get(info_url, headers=header)
                soup = BeautifulSoup(res.text, "lxml")

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
                        job_name = card.find("h2", class_="my-0").text.strip()
                    except Exception:
                        print("Змінився тег для пошуку job_name")
                    
                    # url на дану роботу
                    link = "https://www.work.ua" + str(card.find("h2", class_="my-0").find_next().get("href"))
                    
                    # назва компанії, яка надає вакансію
                    raw_company_name = None
                    add_info = None

                    try:
                        raw_company_name = card.find("span", class_="add-right-xs").find("span", class_="strong-600").text.strip()
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
                        if key in info_url:
                            vacancy_category = categories[key]

                    # work_education = 1 if "з навчанням" in job_name else 0
                    internship = 1 if any(keyword in job_name.lower() for keyword in study_mark) else 0
                    
                    # Блок коду з виясненням зарплати
                    income = card.find("span", class_="strong-600").text.strip()
                    if raw_company_name == income:
                        income = None
                        min_income, max_income = None, None
                    elif " – " in income:
                        income_cleaned = income.replace("грн", "").strip()
                        min_income = income_cleaned.split("–")[0]
                        min_income = int(re.sub(r"[^0-9-]+", "", min_income))
                        max_income = income_cleaned.split("–")[-1]
                        max_income = int(re.sub(r"[^0-9-]+", "", max_income))
                    else:
                        singl_inc = re.sub(r"[^0-9]+", "", income)
                        try:
                            min_income, max_income = int(singl_inc), int(singl_inc)
                        except:
                            min_income, max_income = None, None 
                    
                    # Деталі вакансії
                    chosen_city = card.find("div", class_="mt-xs").find("span", class_="").text.strip()
                    chosen_city = card.find("div", class_="mt-xs").find("span", class_="").text.strip()
                    if chosen_city == raw_company_name:  # навіть спрацює у разі remote work
                        for key in cities.keys():
                            if key in info_url:
                                chosen_city = cities[key]

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
                    
                    full_info = {"Назва роботи" : job_name,
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
                                 "Додаткова інформація": add_info,
                                 "Посилання" : link,}
                                        
                    yield full_info

fieldnames = ["Назва роботи", "Назва компанії", "Місто", "Категорія вакансії", "Стажування / Навчання на роботі",  "Мінімальна ЗП",
              "Максимальна ЗП", "Необхідний досвід", "Необхідна освіта", "Повна зайнятість", "Неповна зайнятість", "Студент", 
              "Інвалідність", "Ветеран", "Пенсіонер", "Додаткова інформація", "Посилання",]

with open(f"sync_all_labour_market_ua_{date}.csv", mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for row in get_info_of_labour(get_counts_of_page_by_category(get_job_vacancy_category(cities_dict)), categories_ua, keywords, cities_dict):
        writer.writerow(row)

end_time = time.time()
print(f"На роботу скрипта було витрачено {round(end_time-start_time, 2)} секунд.",
      f"Парсинг данних з сайту 'work.ua' по {len(cities_dict)} містам України")

# На роботу скрипта було витрачено 21357.68 секунд (5,93 hours). Парсинг данних з сайту 'work.ua' по 21 містам України (sync method)