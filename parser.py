import math
import time

import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

FILE = 'items.xlsx'
CHROME_OPTIONS = webdriver.ChromeOptions()
DRIVER = webdriver.Chrome(options=CHROME_OPTIONS)
TITLE_HTML = 'a2g0'
PRICE_HTML = 'b5v6'


def correct_url(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url
    return url


def page_scroll(driver):
    body = driver.find_element_by_tag_name('body')
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.2)


def get_items_on_page(driver):
    page_scroll(driver)
    length = driver.find_elements_by_class_name('a0t8')
    return(len(length))


def get_pages_count(driver, url):
    driver.get(url)
    all_items_number = driver.find_elements_by_class_name('b6r4')
    all_items_number_text = [item.text for item in all_items_number]
    items_number = all_items_number_text[0].replace(
        '\u2009', '').split(' ')
    pages_count = math.ceil(int(items_number[0]) / get_items_on_page(driver))
    return pages_count


def get_content(url, driver, page, html, items_on_page):
    correct_url(url)
    page_scroll(driver)
    items = driver.find_elements_by_class_name(html)
    items_text = [item.text for item in items[:get_items_on_page(driver)]]
    return items_text


def save_file(titles, prices, file):
    df = pd.DataFrame([titles, prices],
                      index=['Название', 'Цена']).transpose()
    df.index += 1
    df.to_excel(file)


def driver_quit(driver):
    driver.quit()


def parse():
    URL = input('Введите URL: ')
    all_titles = []
    all_prices = []
    pages_count = get_pages_count(DRIVER, URL)
    items_on_page = get_items_on_page(DRIVER)
    for page in range(1, pages_count+1):
        print(f'Парсинг страницы {page} из {pages_count}...')
        DRIVER.get(f'{URL}?page={page}')
        titles = get_content(URL, DRIVER, page, TITLE_HTML, items_on_page)
        prices = get_content(URL, DRIVER, page, PRICE_HTML, items_on_page)
        all_titles.extend(titles)
        all_prices.extend(prices)
    save_file(all_titles, all_prices, FILE)
    print(f'Получено {len(all_titles)} товаров')
    driver_quit(DRIVER)


if __name__ == '__main__':
    parse()
