import csv

from get_tech import get_fieldnames


def csv_sav(data):
    csv.register_dialect('my_dialect', delimiter='|', lineterminator='\n')
    with open('mainfile.csv', 'w', encoding='cp1251', errors='xmlcharrefreplace') as csvfile:
        fieldnames = get_fieldnames()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='my_dialect')

        writer.writeheader()
        for product in data:
            writer.writerow(product)
        print("Writing completed")