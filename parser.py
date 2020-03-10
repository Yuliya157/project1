from selenium import webdriver
import json
import time

driver = webdriver.Firefox()
driver.get('https://paperity.org/journal/43313/journal-of-big-data')

N = 11 #количество страниц
name_author = []
date_article = []
name_article = []
short_description = []
url = []
for i in range(2, N+2):
    author = driver.find_elements_by_class_name('bib-authors')
    date = driver.find_elements_by_class_name('bib-date')
    name = driver.find_elements_by_class_name('paper-list-title')
    short = driver.find_elements_by_class_name('bib-abstract')

    for a in author:
        name_author.append(a.text)

    for b in date:
        date_article.append(b.text)

    for c in name:
         name_article.append(c.text)

    for d in short:
        short_description.append(d.text)

    for e in name:
        url.append(e.find_element_by_tag_name('a').get_attribute('href'))

    link = 'https://paperity.org/journal/43313/journal-of-big-data' + '/' + str(i)
    driver.get(link)

    time.sleep(5)

name_author = [x for x in name_author if x != ''] #в списке появляются пустые элементы
date_article = [y for y in date_article if y != '']

d = {x + 1: (url[x], name_article[x], name_author[x], date_article[x], short_description[x]) for x in range(len(name_article))}
with open('data.json', 'w', encoding="utf-8") as f:
    json.dump(d, f, indent=4, ensure_ascii=False)

driver.close()