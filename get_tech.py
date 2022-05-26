from get_links import *
from bs4 import BeautifulSoup


products = {}
tech_char = []
x = {'\u2212': '-',
     '\u2265': '&ge;',
     '\u00D8': '&Oslash;',
     '\u00B2': '&sup2;',
     '\u2264': '&leq;',
     '\u00F6': '&ouml;',
     '\u03A3': '&Sigma;',
     '\u03D5': '&straightphi;',
     '\u00E4': '&auml;',
     '\u00FC': '&uuml;',
     '\u00E9': '&eacute;',
     '\u00FB': '&ucirc;',
     '\u03B5': '&epsi;',
     '\u00DC': '&Uuml;',
     '\u00D7': '&times;',
     '\u00B3': '&sup3;',
     '\u00E7': '&ccedil;',
     '\u03A9': '&Omega;',
     '\u22A5': '&UpTee;',
     '\u7443': '&Oslash;', #эти две -- эт жепа
     '\u0301': '&Oacute;',
     '\u2242': '&EqualTilde;',
     '\u03BC': '&mu;',
     '\u2126': '&Omega;',
     '\u00DF': '&szlig;'
     }

# x = {'\u2212': '-',
#      '\u2265': '≥',
#      '\u00D8': 'Ø',
#      '\u00B2': '²',
#      '\u2264': '≤',
#      '\u00F6': 'ö',
#      '\u03A3': 'Σ',
#      '\u03D5': 'φ',
#      '\u00E4': 'ä',
#      '\u00FC': 'ü',
#      '\u00E9': 'é',
#      '\u00FB': 'û',
#      '\u03B5': 'ε',
#      '\u00DC': '&Uuml',
#      '\u00D7': '&times',
#      '\u00B3': '&sup3',
#      '\u00E7': '&ccedil',
#      '\u03A9': '&Omega',
#      '\u22A5': '&UpTee',
#      '\u7443': '&Oslash', #эти две -- эт жепа
#      '\u0301': '&Oacute',
#      '\u2242': '&EqualTilde',
#      '\u03BC': '&mu',
#      '\u2126': '&Omega',
#      '\u00DF': '&szlig'
#      }

def get_html_by_url(src_url):
    webpage = requests.get(src_url, headers=req_headers)
    if webpage.status_code != 200:
        return 'error'
    else:
        return BeautifulSoup(webpage.content, "lxml")

def get_tech(url):
    if 'Child' not in tech_char:
        tech_char.append('Ссылочный номер')
        tech_char.append('Name')
        tech_char.append('Product Name')
        tech_char.append('Url')
        tech_char.append('Описание')
        tech_char.append('Материал')
        tech_char.append('Цвет')
        tech_char.append('стандарты')
        tech_char.append('IMAGE URL')
        tech_char.append('db')
        tech_char.append('Subcategory')
        tech_char.append('Category')
        tech_char.append('Child')
        tech_char.append('Subchild')
        tech_char.append('Исполнение')
        tech_char.append('Размер')
        tech_char.append('Power')
        tech_char.append('Power SBL (self-ballasted lamps)')
        tech_char.append('Количество')
        tech_char.append('Серия')
        tech_char.append('Height above surface')
        tech_char.append('Номинальное напряжение')






    soup = get_html_by_url(url)
    divs = soup.find_all('div', {'class': 'float-box w9'})
    for div in divs:
        if ('Ссылочный номер' not in div.text) and ('Технические характеристики' in div.text):
            techs = div.find_all('td', {'class': 'label'})
            for tech in techs:
                tech = tech.text.replace('\xa0', '').replace(':', '')
                for key in x.keys():
                    tech = tech.replace(key, x[key])
                if len(tech) != 0:
                    while tech[0] == ' ':
                        tech = tech[1:]
                    while tech[len(tech) - 1] == ' ':
                        tech = tech[:1]
                if tech not in tech_char:
                    tech_char.append(tech)
    if 'Разница переключения' not in tech_char:
        tech_char.append('Разница переключения')
    if 'Измерительная толерантность' not in tech_char:
        tech_char.append('Измерительная толерантность')
    if 'Контакт' not in tech_char:
        tech_char.append('Контакт')
    if 'Длина нагрузки кабеля (&ge 1,5 мм2)' not in tech_char:
        tech_char.append('Длина нагрузки кабеля (&ge 1,5 мм2)')
    if 'Диапазон контроля' not in tech_char:
        tech_char.append('Диапазон контроля')
    return tech_char


def get_fieldnames():
    i = 0
    with open('links.json', 'r') as f:
        urls = json.load(f)
    # urls = ['https://www.jung.de/ru/online-catalogue/69799066/']
    for url in urls:
        i += 1
        get_tech(url)
    return tech_char
