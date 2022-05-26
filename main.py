import csv
import html
import time
from datetime import datetime
from bs4 import BeautifulSoup
import requests
from columns import *
import os
import json
import random
from csv_saver import csv_sav
from get_links import *
from html.parser import HTMLParser

req_headers = {"Accept": "*/*", "Accept-Encoding": "gzip, deflate, br",
               "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/71.0.3578.98 Safari/537.36 ', "Connection": "keep-alive"}

WORKING_DIR = os.getcwd()
filename = datetime.now()
json_filename = filename.strftime("%m_%d_%Y__%H_%M_%S")
DOMAIN = 'https://www.jung.de'
END = '?view=list'
links = []
data = []
products = {}
h = HTMLParser()
x = {'\u2212': '&minus',
     '\u2265': '&ge',
     '\u00D8': '&Oslash',
     '\u00B2': '&sup2',
     '\u2264': '&leq',
     '\u00F6': '&ouml',
     '\u03A3': '&Sigma',
     '\u03D5': '&straightphi',
     '\u00E4': '&auml',
     '\u00FC': '&uuml',
     '\u00E9': '&eacute',
     '\u00FB': '&ucirc',
     '\u03B5': '&epsi',
     '\u00DC': '&Uuml',
     '\u00D7': '&times',
     '\u00B3': '&sup3',
     '\u00E7': '&ccedil',
     '\u03A9': '&Omega',
     '\u22A5': '&UpTee',
     '\u7443': '&Oslash', #эти две -- эт жепа
     '\u0301': '&Oacute',
     '\u2242': '&EqualTilde',
     '\u03BC': '&mu',
     '\u2126': '&Omega',
     '\u00DF': '&szlig'
     }

def get_html_by_url(src_url):
    webpage = requests.get(src_url, headers=req_headers)
    if webpage.status_code != 200:
        return 'error'
    else:
        return BeautifulSoup(webpage.content, "lxml")



def get_location(soup):
    if soup.find('div', {'class': 'breadcrumb'}):
        div = soup.find('div', {'class': 'breadcrumb'})
        div = div.find_all('a')
        names = []
        for a in div:
            aa = str(a)
            if 'title' in aa:
                a = a.text
            if '\n' in a:
                a = a[:-1]
            names.append(a)
    products[DB] = names[0]
    products[CATEGORY] = names[1]
    if len(names) >= 4:
        products[SUBCATEGORY] = names[2]
        if len(names) >= 5:
            products[CHILD] = names[3]
            if len(names) >= 6:
                products[SUBCHILD] = names[4]


def get_info(soup):
    div = soup.find('div', {'class': 'wrapper product-description'})
    name = div.find('h2').text
    name = name.replace('  ', '').replace('\n', ' ')
    if name[0] == ' ':
        name = name[1:]
    if name[len(name) - 1] == ' ':
        name = name[:-1]
    products[NAME] = name
    products[INFO] = div.find('div', {'class': 'product-description-text'})
    if div.find('a'):
        products[STANDARDS] = div.find('a')['href']


def get_image(soup):
    div = soup.find('div', {'class': 'catalogue-product-image'})
    if div.find('div', {'class': 'clean image-scroller'}):
        div = div.find('div', {'class': 'clean image-scroller'})
        div = div.find('div', {'class': 'main-listing-container'})
        divs = div.find_all('a', {'class': 'main-listing-image'})
        for img in divs:
            img = img.find('div', {'class': 'main-listing-image-wrap'})
            a = 0


def get_material(soup):
    divs = soup.find_all('div', {'class': 'float-box w9'})
    for div in divs:
        if ('Ссылочный номер' in div.text) and ('Технические характеристики' not in div.text):
            name = div.find('div', {'class': 'float-box'}).text
            if (' ' in name) or (len(name) >= 5):
                name = name.replace('\n', '').replace('  ', '')
                if name[0] == ' ':
                    name = name[1:]
                if name[len(name) - 1] == ' ':
                    name = name[:-1]
                products[MATERIAL] = name


def get_data(url):
    soup = get_html_by_url(url)
    d = []
    hed = []
    if 'Ссылочный номер' in soup.text:
        divs = soup.find_all('tr')
        he = divs[0].find_all('th')
        for h in he:
            h = h.text.replace('\xa0', '').replace('\n', '').replace(':', '')
            if h not in hed and len(h) > 0 and h != 'ИНФОРМАЦИЯ':
                hed.append(h)
        for di in divs:
            if ('ИНФО' in di.text) and ('ИНФОРМАЦИЯ' not in di.text):
                d.append(di)
        for div in d:
            div = div.find_all('td')
            products[URL] = url
            for i in range(len(hed)):
                products[hed[i]] = div[i].text
            get_location(soup)
            get_name(soup)
            get_info(soup)
            get_material(soup)
            get_tech(soup)
            get_image()
            data.append(products.copy())
            products.clear()
    else:
        products[URL] = url
        get_location(soup)
        get_name(soup)
        get_info(soup)
        get_material(soup)
        get_tech(soup)
        get_image()
        data.append(products.copy())
        products.clear()


def get_name(soup):
    if soup.find('div', {'class': 'wrapper product-description'}):
        soup = soup.find('div', {'class': 'wrapper product-description'})
        soup = soup.find('h2').text
        soup = soup.replace("\n", " ").replace("  ", "")
        if soup.find(" ") == 0:
            soup = soup[1:]
        products[PRODUCT_NAME] = soup


def get_tech(soup):
    divs = soup.find_all('div', {'class': 'float-box w9'})
    for div in divs:
        if ('Ссылочный номер' not in div.text) and ('Технические характеристики' in div.text):
            techs = div.find_all('td')
            i = 0
            for tech in techs:
                if tech.attrs['class'][0] == 'label' and i != 0:
                    name = tech.text.replace('\xa0', '').replace('\u2265','≥').replace(':', '')
                    # name = html.escape(name)
                    for key in x.keys():
                        name = name.replace(key, x[key])
                    if len(name) != 0:
                        while name[0] == ' ':
                            name = name[1:]
                if tech.attrs['class'][0] == 'data' and i != 0:
                    tech = tech.text.replace('\u2212', '&minus')
                    for key in x.keys():
                        tech = tech.replace(key, x[key])
                    # if '+45' in tech:
                    #     print(tech)
                        # tech = tech.replace('\u2212', '-')
                        # print(tech.replace('\u2212', '-').encode('cp1251'))
                    products[name] = tech
                i += 1


def get_image():
    link = products['Ссылочный номер'].replace(' ', '')
    image_link = f'https://downloads.jung.de/catalogue/images/800x800_png/JUNG_{link}.png'
    products[IMAGE_URL] = image_link


if __name__ == "__main__":
    i = 0
    # urls = get_url()
    with open('links.json', 'r') as f:
        urls = json.load(f)
    i = 0
    for url in urls:
        get_data(url)
        print(len(urls)-i)
        i = i+1
    csv_sav(data)

