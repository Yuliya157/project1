from selenium import webdriver
import json
import time

driver = webdriver.Firefox()
driver.get('https://paperity.org/journal/43313/journal-of-big-data')

N = 11 #количество страниц
name_author = []
date = []
title = []
short_description = []
url = []
keywords = []
pages = []

for i in range(2, N+2):
    author = driver.find_elements_by_class_name('bib-authors')
    short = driver.find_elements_by_class_name('bib-abstract')
    date1 = driver.find_elements_by_class_name('bib-date')
    art_title = driver.find_elements_by_class_name('paper-list-title')

    for author1 in author:
        name_author.append(author1.text)

    for short1 in short:
        short_description.append(short1.text)

    for element in art_title:
        url.append(element.find_element_by_tag_name('a').get_attribute('href'))

    for datee in date1:
        date.append(datee.text)

    for titlee in art_title:
        title.append(titlee.text)

    link = 'https://paperity.org/journal/43313/journal-of-big-data' + '/' + str(i)
    driver.get(link)

url.remove('https://paperity.org/p/73244106/sentiment-analysis-using-product-review-data')#данная статья не в pdf

for elem in url:
    driver.get(elem)
    button_option_for_tools = driver.find_element_by_class_name('endnote').find_element_by_tag_name('a').get_attribute('href')
    driver.get(button_option_for_tools)
    time.sleep(1)
    bott = driver.find_element_by_xpath('//button[@id="secondaryToolbarToggle"]').click()
    botton1 = driver.find_element_by_xpath('//button[@id="documentProperties"]').click()
    keywords.append((driver.find_element_by_xpath('//p[@id="keywordsField"]')).text)
    pages.append((driver.find_element_by_xpath('//p[@id="pageCountField"]')).text)

name_author = [x for x in name_author if x != ''] #пустые элементы в списке
date = [y for y in date if y != '']

url.insert(258, 'https://paperity.org/p/73244106/sentiment-analysis-using-product-review-data')
keywords.insert(258, '-')
pages.insert(258, '-')
print(len(url))
print(len(title))
print(len(name_author))
print(len(date))
print(len(short_description))
print(len(keywords))
print(len(pages))
d = [{'url': url[x], 'title':title[x], 'authors':name_author[x], 'date_article':date[x], 'short_description': short_description[x], 'keywords':keywords[x], 'number_of_pages':pages[x]} for x in range(len(title))]
with open('data.json', 'w', encoding="utf-8") as f:
    json.dump(d, f, indent = 4, ensure_ascii = False)

driver.close()