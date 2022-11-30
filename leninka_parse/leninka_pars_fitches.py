import requests

import json
from pandas import DataFrame
import pandas as pd


class LeninkeaFitchesParser():
    def __init__(self):
        self.ids = []
        self.names = []
        self.annotations = []
        self.authors = []
        self.years = []
        self.links = []
        self.journals = []
        self.journal_links = []
        self.catalogs = []
        self.article_fitches = []

        self.error_pars_fitches_for_previously_one = []

    def pars_for_one(self, query, size = 10000):
        error_pars_fitches = []

        raw = requests.post('https://cyberleninka.ru/api/search',
        json = {"terms":[8],
        "mode":"articles",
        "q":query,
        "size":size,
        "from":0})
        fs = raw.json()

        try:
            articles = fs["articles"]
            print(fs.keys())
            print(query)

            for one_article in articles:
                self.names.append(one_article['name'])
                self.annotations.append(one_article['annotation'].replace('<b>', '').replace('</b>', ''))
                self.authors.append(one_article['authors'])
                self.years.append(one_article['year'])
                link = one_article['link']
                self.links.append(link)
                self.ids.append(link.replace('/article/n/', ''))
                self.journals.append(one_article['journal'])
                self.journal_links.append(one_article['journal_link'])
                self.catalogs.append(one_article['catalogs'])
                self.article_fitches.append(query)
        except:
            print(f'\n****************\nError_query: {query}\n****************\n')
            if not fs["found"] == 0:
                error_pars_fitches.append(query)
            else:
                print('****************\nОшибка поиска\n****************\n')

        self.error_pars_fitches_for_previously_one = error_pars_fitches

    def pars_full_list(self, query_list, size = 10000):
        count = 0

        self.error_pars_fitches_for_previously_one.clear()
        self.error_pars_fitches_for_previously_one.append('nechto')

        while self.error_pars_fitches_for_previously_one:
            if count == 0:
                pass
            else:
                query_list = self.error_pars_fitches_for_previously_one

            for one_query in query_list:
                self.pars_for_one(one_query, size)

            count += 1
        

# small_categories = ['C++', 'C' , 'Brainfuck', 'Go', 'C#', 'Qt', 'F#' , 'Haxe', 'Ember.js', 'SvelteJS', 'Elixir/Phoenix', 'Meteor.JS' , 'Derby.js', 'Kohana', 'Developmend for Java ME']

# for_parse = small_categories

fitches = pd.read_csv('fitches2_4.csv')

fitches.dropna(inplace = True)
for_parse = fitches['title'].to_numpy()

# for_parse = ['С++']

my_parser = LeninkeaFitchesParser()
my_parser.pars_full_list(for_parse)

table = DataFrame({'ID': my_parser.ids,
                    'Name':my_parser.names,
                    'Annotations': my_parser.annotations,
                    'Authors':my_parser.authors,
                    'Years':my_parser.years,
                    'Links':my_parser.links,
                    'Journals':my_parser.journals,
                    'Journal_links':my_parser.journal_links,
                    'Catalogs':my_parser.catalogs, 
                    'Fitches':my_parser.article_fitches})

table.to_csv('./Leninka_fitches.csv')
