from elasticsearch import Elasticsearch
from nltk.corpus import wordnet
import numpy as np
import pandas as pd
import encodings
from csv import DictReader
from datetime import datetime


es = Elasticsearch(HOST="http://localhost", PORT=9200)


def index_news(news_list):
    doc_id = 0
    #iterate over each page
    for news in news_list:
        #index the document
        es.index(index = "news" , doc_type = "content" , id=doc_id , body = news)
        doc_id += 1

def csv_to_dict(file_name):
        # open file in read mode
    with open(file_name, 'r' , encoding='mac_roman') as read_obj:
        # pass the file object to DictReader() to get the DictReader object
        dict_reader = DictReader(read_obj)
        # get a list of dictionaries from dct_reader
        news_list = list(dict_reader)
    return news_list

def expand_query(word):
    synonyms = set()

    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            synonyms.add(l.name()) 
    
    return synonyms


def make_format(query , out , with_expand):
    qr = "("
    for index, word in query.items():
        if(word == None):
            continue
        if(with_expand):
             qr += "("
        qr += word
        expand = expand_query(word)
        i = 0
        if(with_expand):
            for syn in expand:
                if(word == syn):
                    continue
                qr += " OR " + syn
                i = i + 1
                if(i == 3):
                    break
            qr += ")"
        qr += " AND " 
    out['query'] = qr[0:-5] + ")"
    print(out['query'])
    final_query = {"from": 0, "size": 10, "query": {"query_string": {"query": out['query']}}}
    return final_query



def output_format(found , out):
    out["title"] = found["_source"]["title"]
    out["url"] = found["_source"]["url"]
    out['score'] = found["_score"]
    out['text'] = found["_source"]["text"]
    out["Date"] = datetime(int(found["_source"]["publish year"]) ,
    int(datetime.strptime(found["_source"]["publish month"] , "%B").month),
    int(found["_source"]["publish day"]))

'''
news_list = csv_to_dict("news.csv")


index_news(news_list)
'''
queries = pd.read_csv("queries.csv")
queries = queries.where(pd.notnull(queries), None)
output = pd.DataFrame()



with_expanding = int(input("Enter 1 if you prefer to expand the query and 0 otherwise: "))

for index, query in queries.iterrows():
    # print(query)
    out = {}
    if(with_expanding):
        result = es.search(index='news', body = make_format(query , out , with_expanding))
    else:
        result = es.search(index='news', body = make_format(query , out , with_expanding))
    print(out['query'] , len(result['hits']['hits']))
    for found in result['hits']['hits']:
        output_format(found , out)
        output = output.append(out , ignore_index=True)

path = ""
if(with_expanding):
    path = "expanded query/result.csv"
else:
    path = "simple query/result.csv"
output.to_csv(path)









