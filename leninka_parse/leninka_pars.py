import requests
# from bs4 import BeautifulSoup

import json
from pandas import DataFrame, Series

spheres = ['аппаратура', 'программное обеспечение', 'тестирование', 'дизайн', 'администрирование', 'разработка']

ids = []
names = []
annotations = []
authors = []
years = []
links = []
journals = []
journal_links = []
catalogs = []
article_spheres = []

for sphere_IT in spheres:
    raw = requests.post('https://cyberleninka.ru/api/search',
    json = {"terms":[8],
    "mode":"articles",
    "q":sphere_IT,
    "size":10000,
    "from":0})
    fs = raw.json()
# print(fs["articles"][0]['annotation'].replace('<b>', '').replace('</b>', ''))
# print(fs["articles"][0].keys())
# print(fs["articles"][0]['catalogs'])

    articles = fs["articles"]
    print(fs.keys())
    print(sphere_IT)

    for one_article in articles:
        names.append(one_article['name'])
        annotations.append(one_article['annotation'].replace('<b>', '').replace('</b>', ''))
        authors.append(one_article['authors'])
        years.append(one_article['year'])
        link = one_article['link']
        links.append(link)
        ids.append(link.replace('/article/n/', ''))
        journals.append(one_article['journal'])
        journal_links.append(one_article['journal_link'])
        catalogs.append(one_article['catalogs'])
        article_spheres.append(sphere_IT)

table = DataFrame({'ID': ids,
                    'Name':names,
                    'Annotations': annotations,
                    'Authors':authors,
                    'Years':years,
                    'Links':links,
                    'Journals':journals,
                    'Journal_links':journal_links,
                    'Catalogs':catalogs, 
                    'Сфера ИТ': article_spheres})

table.to_csv('./Leninka_3.csv')