import sys
import os
import logging
from time import time

root_path = os.path.normpath(os.path.abspath(os.path.join(__file__,'..','..','..')))
sys.path.append(root_path)
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse
from crawler.parser import scrape_data


seen_links = set()

handler = logging.FileHandler(os.path.join(root_path,'crawler','logs',f'log_{int(time())//10}.txt'))
handler.setFormatter(logging.Formatter('%(asctime)s - [%(name)s] - {%(levelname)s} - %(message)s'))
logger = logging.getLogger(__name__)
logging.getLogger().addHandler(handler)


file_name = f'news_{str(int(time())//10)}.csv'
file_parent_dir = os.path.normpath(os.path.join(os.path.abspath(__file__),'..'))


class NewsSpider(scrapy.Spider):
    name = "news"

    def check_domain(self,link):
        domain = urlparse(link).netloc
        if domain == 'www.truthorfiction.com':
            return True
        return False

    def start_requests(self):
        urls = [
        'https://www.truthorfiction.com/'
        ]
        for url in urls:
            #this function returns responses from requests of urls.
            seen_links.add(url)
            yield  scrapy.Request(url=url, callback=self.parse)
        
    #We use this function as the callback for scrapy.Request function
    def parse(self, response):
        global seen_links
        # gets mime type 
        mime = response.headers.get('content-type').lower().decode('UTF-8')
        
        # Only responses with text mime type can be handled
        if mime[0:4] == "text":
            scrape_data(str(response.body),response.url)
            le = LinkExtractor()
            links = le.extract_links(response)
            for link in links:
                if not self.check_domain(link.url):
                    continue
                elif link.url in seen_links:
                    continue
                seen_links.add(link.url)
                yield scrapy.Request(link.url, callback=self.parse)
        


if __name__ == '__main__':

    process = CrawlerProcess()

    process.crawl(NewsSpider)
    process.start()  # the script will block here until the crawling is finished

