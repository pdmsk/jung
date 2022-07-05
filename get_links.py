import json
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import os

req_headers = {"Accept": "*/*", "Accept-Encoding": "gzip, deflate, br",
               "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/71.0.3578.98 Safari/537.36 ', "Connection": "keep-alive"}

WORKING_DIR = os.getcwd()
filename = datetime.now()
json_filename = filename.strftime("%m_%d_%Y__%H_%M_%S")
DOMAIN = 'https://www.jung.de'
END = '?view=list'
links = []
url_data = []
products = []


def get_html_by_url(url):
    webpage = requests.get(url, headers=req_headers)
    if webpage.status_code != 200:
        return 'error'
    else:
        return BeautifulSoup(webpage.content, "lxml")


def get_links(product_id):
    if 'ыыыы' not in product_id:
        url = DOMAIN + product_id + END
        soup = get_html_by_url(url)
        if soup.find('div', {'class': 'float-box w9 clean catalogue'}):
            soup = soup.find('div', {'class': 'float-box w9 clean catalogue'})
            if 'Ссылочный номер' not in soup.text:
                soup = soup.find_all('a', href=True)
                link = []
                for a in soup:
                    a = a['href']
                    if '/ru/online-catalogue' in a:
                        link.append(a)
                return link

    return product_id + 'ыыыы'


def get_url():
    i = 0
    product_id = '/ru/online-catalogue/'
    # product_id = '/ru/online-catalogue/3996973179/'
    product_ids = get_links(product_id)
    while len(product_ids) != 1:
        print(len(product_ids))
        links = []
        products = []
        for product_id in product_ids:
            if 'ыыыы' in product_id:
                product_id = DOMAIN + product_id.replace('ы', '')
                url_data.append(product_id)
            else:
                products.append(product_id)
        for product in products:
            links.append(get_links(product))
            links = str(links).replace('[', '').replace(']', '').replace("'", '').split(', ')
        product_ids = [links]
        product_ids = str(product_ids)[2:-2].replace("'", '').split(', ')
        i += 1

    new_file = open(f'{WORKING_DIR}/links.json', 'w')
    new_file.write(json.dumps(url_data))
    new_file.close()
    return url_data