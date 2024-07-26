# Аналіз ринку праці у обласних центрах України
**Мета проекту:** загалом за мету проекта було поставлено вивчення особливостей ринку праці та його розподіл стосовно до обласних центрів й дистанційного формату та категорій вакансій, а також безпосередньо однією з найголовніших цілей було визначення оплати праці відповідно до її розподілу.

**Використаний датасет:** інформація, яка використовувалася в аналізі, була спарсена з одного з найбільших сайтів пошуки роботи в Україні - [work.ua](https://www.work.ua/). Збір данних відбувався 22 липня 2024 року.

В подальшій роботі дані піддалися розвідувальному аналізу та статистичному тестуванню ([EDA](https://github.com/elch1k/ua-labour-market-in-ukrainian/blob/main/labour_market_preprocessing.ipynb)). У підсумку виявилися певні проблеми, які пов'язані з відсутньою вказаною заробітною платою у вакансіях з боку роботодавців, що становило близько 42% від всіх даних. Це доволі суттєвий мінус для дослідження, проте за мету було поставлено дослідити саме оплату праці та її розподіл як по містах, так і по категоріях. Тож, зробивши декілька порівняльних тестів та прийшовши до певних висновків, відредаговані дані було дослідженно на розподіл зарплат та відправленно до Power BI і вже в подальшому на їх основі були створені показові дашборди.

Дашборд проєкту:
---

Перша сторінка дашборду зображує загальний стан ринку праці по містам України, як бачимо найбільше виділяється саме місто Київ, який має найбільше пропозиції на ринку праці. Найгірша ситуація наразі у Херсоні. Роботодавці в більшості випадках орієнтуються на молодих робітників, бо майже 30% вакансій можуть розглядатися студентами. Близько 76% вакансій не вимагають Вищу чи Середньо-спеціальну освіту, що може означати про дешевизну потрібної робочої сили розміщених вакансій.

![first_page](https://github.com/elch1k/ua-labour-market-in-ukrainian/blob/main/dashboard_imgs/page1.png)

Друга сторінка дашборду показує розподіл ринку праці по категоріям, які доступні на сайті [work.ua](https://www.work.ua/), також було додано частку ФОПів від загальної кількості вакансії по категоріям. Як видно найбільша частка ФОПів саме наблюдається в категорії "Краса, фітнес, спорт", найменша в "Юриспруденція" та "Охорона, безпека". По кількості вакансій загалом за категоріями ситуація наступна: найбільше вакансій в категорії "Обслуговування", найменше в "Страхування".

![second_page](https://github.com/elch1k/ua-labour-market-in-ukrainian/blob/main/dashboard_imgs/page2.png)

Третя сторінка зображує розподіл заробітної плати по містам та дистаційної форми, а також зображено частку вакансій у яких зарплата більша за середню. Також варто відмітити невеликий необхідний досвід (43% просять нульовий досвід) для праці та високий рівень заробітку без певной указаної освіти. 

![third_page](https://github.com/elch1k/ua-labour-market-in-ukrainian/blob/main/dashboard_imgs/page3.png)

Четверта сторінка представляє собою інформацію про середню заробітну плату за доступними категоріями та можливістю глянути ситуацію конкретно в місті, загальну середню зарплату по Україні (за всіма обласними центрами), та частка вакансій певної категорії до всіх вакансій. Бачимо що найбільше платять в сферах "Топменеджменту" та "Нерухомості", найменше отримують робітники сфер "Охорона, безпека" та "Роздрібної торгівлі", що доволі показово для ринку праці України.

![fourth_page](https://github.com/elch1k/ua-labour-market-in-ukrainian/blob/main/dashboard_imgs/page4.png)

Ньюанси та ідеї для покращення проєкту:
---
* Вирішення проблеми автоматичного розкидання вакансій по категоріям за посиланнями [work.ua](https://www.work.ua/), які іноді працювали некоректно, і могли додати охоронника в категорію "ІТ, комп'ютери, інтернет".
* Можна додати до цього проєкту дані з найбільших ІТ спільнот та посумісництву найбільших ІТ сайтів для пошуку роботи: [dou.ua](https://dou.ua/) та [djinni](https://djinni.co/). Проте як на мене це іншого рівня ринки праці, які мають досліджуватися окремо від загально доступних, в цьому випадку краще додати схожий за змістом сайт пошуку роботи [robota.ua](https://robota.ua/) чи щось на кшталт цього.
* Покращити роботу парсера: більш детальний збір інформації (вимагаємий рівень англійської, тощо).
* Створення бота для зручної інтерпретації аналітики по ринку праці України.
* Додати можливість спостерігати динаміку зміни кількості вакансій як загалом так і по категоріям, також це стосується середньої заробітної плати.
* Додавання можливості до інтерактивного користування візуалізацією Power Bi
