import csv
import datetime
import logging
import os
from time import time

import html5lib
from bs4 import BeautifulSoup
from lxml.html import fromstring, tostring

file_name = f'news_{str(int(time())//10)}.csv'
file_parent_dir = os.path.normpath(os.path.join(os.path.abspath(__file__),'..'))

logger = logging.getLogger(__name__)
passed_time = time()

def scrape_data(html, url):

    soup = BeautifulSoup(html, 'html5lib')
    fixed_html = soup.prettify()

    tree = fromstring(fixed_html)
    d = dict()


    d['url'] = url

    try:
        # title = tree.xpath('//div/header/div/h1/text()')[0]
        title = tree.xpath("//div/header/div/h1/text()")[0]
        d['title'] = str(title).strip("'")

        try:
            publish_date = str(tree.xpath('//div/header/div/div/span[3]/span[1]/text()')[0]).strip().split(" ")
            #publish_date = str(tree.xpath("//div/header/div/div/span[@class='posted-on']/span[@class='published']/text()")[0]).strip().split(" ")
            d['publish month'] = publish_date[0].strip(',')
            d['publish day']  = int(publish_date[1].strip(','))
            d['publish year'] = int(publish_date[2].strip(','))
        except:
            d['publish year'] = None
            d['publish month'] = None
            d['publish day'] = None

        try:
            # author = tree.xpath('//div/header/div[2]/div/span[2]/a/span/text()')[0]
            author = tree.xpath("//div/header/div/div/span[2]/a/span/text()")[0]
            d['author'] = str(author).strip()
        except:
            d['author'] = None

        try:
            
            # label = str(tree.xpath('//div/div/div[2]/div/span/text()')[0])
            # label = str(tree.xpath("//div/div/div/div/span/text()")[0])
            label = str(tree.xpath('/html/body/div/div/div/div/main/article/div/div/div/div/span/text()')[0])

            label = label.strip()
            if label not in ['Not True', 'True']:
                d['label'] = None
            else:
                d['label'] = label
        except:
            d['label'] = None

        try:
            text_list = tree.xpath('//div/div/p/text()')
            text = "\n".join(text_list)
            d['text'] = text
        except:
            d['text'] = None
# /html/body/div[1]/div[2]/div/div[1]/main/article/div/header/div[2]/div/span[1]/a
        try:
            topic_list = tree.xpath(f'//div/header/div/div/span[1]/a/text()')
            topic_list = list(map(lambda x : x.strip(), topic_list))
            topic = "\n-\t".join(topic_list)
            d['topic'] = topic
        except:
            d['topic'] = "None"


        columns = ['title', 'url', 'publish day', 'publish month', 'publish year', 'label', 'author', 'topic', 'text']
        file_path = os.path.join(file_parent_dir,'output',file_name)
        # file_path = os.path.join(os.path.abspath(__file__),'output',file_name)
        file_exists = os.path.isfile(file_path)

        # if not os.path.exists('output'):
        if not os.path.exists(os.path.join(file_parent_dir,'output')):
            # os.mkdir('output')
            os.mkdir(os.path.join(file_parent_dir,'output'))
        with open(file_path, 'a+', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns)
            if not file_exists:
                writer.writeheader()
            writer.writerow(d)
            logger.debug(f"File Parsed: {d['url']}")
        if time() % 100 == 0:
            logger.info(f"Time Passed Since start ($$LOL$$):  {time() - passed_time}")



    except:
        pass
