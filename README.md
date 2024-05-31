# Аналіз ринку праці у обласних центрах України
**Мета проекту:** загалом за мету проекта було поставлено вивчення особливостей ринку праці та його розподіл стосовно до обласних центрів та категорій вакансій, а також безпосередньо однією з найголовніших цілей було визначення оплати праці відповідно до її розподілу та загалом.

**Використаний датасет:** інформація, яка використовувалася в аналізі, була спарсена з одного з найбільших сайтів пошуки роботи в Україні - [work.ua](https://www.work.ua/). Збір данних відбувався 23 травня 2024 року.

В результаті зібрані дані спочатку пройшли певну передобробку, де було видалено всі вакансії, які хоч якось пов'язані з військовим ремеслом, бо саме такі вакансії зі своїми порівняльно великими зарплатами та розкидом зарплат штучно тягнули оплату ринку праці України догори, а мене власне цікавить саме звичайний цивільний ринок праці. В подальшому редагуванні дані піддалися розвідувальному аналізу та статистичному тестуванню ([EDA](EDA)). У підсумку виявилися певні проблеми, які пов'язані з відсутньою вказаною заробітною платою у вакансіях з боку роботодавців, що становило близько 42% від всіх даних. Це доволі суттєвий мінус для дослідження, проте за мету було поставлено дослідити саме оплату праці та її розподіл як по містах, так і по категоріях. Тож, зробивши декілька порівняльних тестів та прийшовши до певних висновків, відредаговані дані було дослідженно на розподіл зарплат та відправленно до Power BI і вже в подальшому на їх основі були створені показові дашборди.

Дашборд проєкту:
---

Перша сторінка дашборду зображує загальний стан ринку праці по містам України, як бачимо найбільше виділяється саме місто Київ, який має і найбільшу середню зарплату по містам України та найбільше пропозиції на ринку праці. Найгірша ситуація наразі у Херсоні, в цілому й не дивно, бо місто має важке військове становище, що піддає ризику розвиток бізнесів та становить небезпеку для робітників. Роботодавці в більшості випадках орієнтуються на молодих робітників, бо майже 30% вакансій можуть розглядатися студентами. Близько 76% вакансій не вимагають Вищу чи Середньо-спеціальну освіту, що може означати про дешевизну потрібної робочої сили.

![first_page]()

Друга сторінка дашборду показує розподіл ринку праці по категоріям. які доступні на сайті [work.ua](https://www.work.ua/), також було додано відсоток ФОПів від загальної кількості вакансії по категоріям. Як видно найбільша частка ФОПів саме наблюдається в категорії "Дизайн та творчість", найменша в "Юриспруденція". По кількості вакансій зп категоріями ситуація інакша: найбільше вакансій в категорії "Обслуговування", найменше в "Страхування".

![second_page]()

Третя сторінка представляє собою інформацію про середню заробітну плату за доступними категоріями та містами, загальну середню зарплату по Україні (за всіма обласними центрами), та частка вакансій певної категорії до всіх вакансій. Бачимо що найбільше платять в сферах "топменеджменту" та "нерухомості", найменше отримують робітники сфер "освіти, науки" та "роздрібної торгівлі", що доволі показово для ринку праці України.

![third_page]()

Ньюанси та ідеї для покращення проєкту:
---
* Вирішення проблеми автоматичного розкидання вакансій по категоріям за посиланнями [work.ua](https://www.work.ua/), які іноді працювали некоректно, і могли додати охоронника в категорію "ІТ, комп'ютери, інтернет".
* Можна додати до цього проєкту дані з найбільших ІТ спільнот та посумісництву найбільших ІТ сайтів для пошуку роботи: [dou.ua](https://dou.ua/) та [djinni](https://djinni.co/). Проте як на мене це іншого рівня ринки праці, які мають досліджуватися окремо від загально доступних, в цьому випадку краще додати схожий за змістом сайт пошуку роботи [robota.ua](https://robota.ua/) чи щось на кшталт цього.
* Покращити роботу парсера: безпосередньо швидкість збору даних та більш детальний збір інформації (вимагаємий рівень англійської, тощо).
* Створення бота для зручної інтерпретації аналітики по ринку праці України.
* Додати можливість спостерігати динаміку зміни кількості вакансій як загалом так і по категоріям, також це стосується середньої заробітної плати.
* Додавання можливості до інтерактивного користування візуалізацією Power Bi
