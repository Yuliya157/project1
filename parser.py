from selenium import webdriver
import json
import time
from datetime import datetime
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from tkinter import *

driver = webdriver.Firefox()
driver.get('https://paperity.org/journal/43313/journal-of-big-data')

N = 11 #количество страниц
name_author = []
date_try = []
date = []
title = []
short_description = []
url = []
keywords = []
pages = []
url_pdf = []
abstract = []

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
        date_try.append(datee.text)

    for titlee in art_title:
        title.append(titlee.text)

    link = 'https://paperity.org/journal/43313/journal-of-big-data' + '/' + str(i)
    driver.get(link)

url.remove('https://paperity.org/p/73244106/sentiment-analysis-using-product-review-data')#данная статья не в pdf

for elem in url:
    driver.get(elem)
    button_option_for_tools = driver.find_element_by_class_name('endnote').find_element_by_tag_name('a').get_attribute('href')
    url_pdf.append(button_option_for_tools)
    driver.get(button_option_for_tools)
    time.sleep(1)
    bott = driver.find_element_by_xpath('//button[@id="secondaryToolbarToggle"]').click()
    botton1 = driver.find_element_by_xpath('//button[@id="documentProperties"]').click()
    keywords.append((driver.find_element_by_xpath('//p[@id="keywordsField"]')).text)
    pages.append((driver.find_element_by_xpath('//p[@id="pageCountField"]')).text)

    ActionChains(driver).key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).perform() #Ctrl + A
    time.sleep(2)
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('c').key_up(Keys.CONTROL).perform() #Ctrl + C
    time.sleep(2)
    root = Tk()
    paste = Tk().clipboard_get() #текст из буфера
    abstract1 = paste.find('Abstract') + 8  # +8, чтобы убрать слово abstract
    keywords1 = paste.find('Keywords')
    string = paste[abstract1:keywords1]
    abstract.append(string)
    root.destroy()

name_author = [x for x in name_author if x != ''] #пустые элементы в списке
date_try = [y for y in date_try if y != '']
for element in date_try:
    date.append(datetime.strptime(element, "%b %Y").strftime('%m-%Y')) #перевод в формат datetime

url.insert(258, 'https://paperity.org/p/73244106/sentiment-analysis-using-product-review-data')
keywords.insert(258, '-')
pages.insert(258, '-')
abstract.insert(258, '-')
url_pdf.insert(258, 'https://link.springer.com/content/pdf/10.1186%2Fs40537-015-0015-2.pdf')

d = [{'url': url[x], 'title':title[x], 'authors':name_author[x], 'date_article':date[x], 'short_description': short_description[x], 'keywords':keywords[x], 'number_of_pages':pages[x], 'url_pdf': url_pdf[x], 'abstract': abstract[x]}
     for x in range(len(title))]
with open('data.json', 'w', encoding="utf-8") as f:
    json.dump(d, f, indent = 4, ensure_ascii=False)

driver.close()