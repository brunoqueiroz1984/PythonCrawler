'''
Created on 1 de fev de 2018

@author: Bruno
'''
import threading
from urllib.request import urlopen
from link_finder import LinkFinder
from queue import Queue
#from spider import Spider
from domain import *
#from general import create_csv_file

PROJECT_NAME = 'Celebratio'
HOMEPAGE = 'https://agendasorocaba.com.br/baladas/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 1

# queue = Queue()
# #Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)
# 
# def create_spiders():
#     for _ in range(NUMBER_OF_THREADS):
#         t = threading.Thread(target=work)
#         t.daemon = True
#         t.start()
#         
# def work():
#     while True:
#         url = queue.get()
#         Spider.crawl_page(threading.current_thread().name, url)
#         queue.task_done()
# 
# def create_jobs():
#     for link in file_to_set(QUEUE_FILE):
#         queue.put(link)
#     queue.join()
#     crawl()
# 
# def crawl():
#     queued_links = file_to_set(QUEUE_FILE)
#     if len(queued_links) > 0:
#         print(str(len(queued_links))+ ' links na fila')
#         create_jobs()

def gather_events(page_url):
        html_string =''
        try:
            response = urlopen(page_url)
            print('conectado')
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode('utf-8')
            finder = LinkFinder(page_url, page_url)
            finder.feed(html_string)
        except:
            print('Error: can not crawl page')
            return set()
        return finder.get_events()


events = gather_events(HOMEPAGE)
with open('events.csv', 'w') as f:
    for item in events:
        f.write(item)
# create_spiders()
# crawl()