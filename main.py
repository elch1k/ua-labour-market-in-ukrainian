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
                    # Зробити власну базу юзер агентів
                    user = fake_useragent.UserAgent().random
                    header = {"user-agent": user}
                    time.sleep(random.randint(5,10))

                res = requests.get(info_url, headers=header)
                soup = BeautifulSoup(res.text, "lxml")

                top_card = soup.find("div", 
                                     class_="card card-hover card-search card-visited wordwrap job-link js-job-link-blank js-hot-block add-top")
                hot_cards = soup.find_all("div", 
                                          class_="card card-hover card-search card-visited wordwrap job-link js-job-link-blank js-hot-block")
                just_cards = soup.find_all("div", 
                                           class_="card card-hover card-search card-visited wordwrap job-link js-job-link-blank")

                cards = []
                if top_card is not None:
                    cards.append(top_card)
                if len(hot_cards) > 0:
                    cards.extend(hot_cards)
                if len(just_cards) > 0:
                    cards.extend(just_cards)

                # Цикл збору відповідної інформації про вакансії
                for card in cards:
                    job_name = card.find("h2", class_="cut-top cut-bottom").text.strip()
                    company_name = card.find("div", class_="add-top-xs").find_next().find_next().text.strip()
                    link = "https://www.work.ua" + str(card.find("h2", class_="cut-top cut-bottom").find_next().get("href"))

                    # Блок знаходження категорії відповідної вакансії
                    for key in categories.keys():
                        if key in info_url:
                            vacancy_category = categories[key]
                            if vacancy_category != None:
                                break

                    # work_education = 1 if "з навчанням" in job_name else 0
                    internship = 1 if any(keyword in job_name.lower() for keyword in study_mark) else 0
                    
                    # Блок коду з виясненням зарплати
                    income = card.find("span", class_="strong-600").text.strip()
                    if company_name == income:
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
                        min_income, max_income = int(singl_inc), int(singl_inc)
                    
                    if len(company_name.split(", ")) > 1:  # Загалом подається 2 значення, проте може бути і 3!
                        add_info = company_name.split(", ")[-1]
                        company_name = company_name.split(", ")[0]
                    else:
                        add_info = None
                    
                    chosen_city = (card.find("div", class_="add-top-xs").find_all("span", class_="")[0]).text.strip().replace(",", "")
                    # іноді не виводить саме місто, яке власне передбачалося, а виводить назву компанії
                    if chosen_city == company_name:
                        for key2 in cities.keys():
                            if key2 in info_url:
                                chosen_city = cities[key2]

                    # Деталі вакансії
                    vacant_text = card.find("p", class_="ellipsis ellipsis-line ellipsis-line-3 text-default-7 cut-bottom").text.strip().lower()
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
                    experience_match = re.search(r"досвід роботи від (\d+)", vacant_text)
                    if experience_match:
                        years_of_experience = int(experience_match.group(1))
                    else:
                        years_of_experience = 0
                    
                    full_info = {"Назва роботи" : job_name,
                                 "Назва компанії": company_name,
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

with open(f"all_labour_market_ua_{date}.csv", mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for row in get_info_of_labour(get_counts_of_page_by_category(get_job_vacancy_category(cities_dict)), categories_ua, keywords, cities_dict):
        writer.writerow(row)

end_time = time.time()
print(f"На роботу скрипта було витрачено {round(end_time-start_time, 2)} секунд.",
      f"Парсинг данних з сайту 'work.ua' по {len(cities_dict)} містам України")

# На роботу скрипта було витрачено 21357.68 секунд (5,93 hours). Парсинг данних з сайту 'work.ua' по 21 містам України (sync method)