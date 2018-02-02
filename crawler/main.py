'''
Created on 1 de fev de 2018

@author: Bruno
'''
import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *

PROJECT_NAME = 'falandotec teste'
HOMEPAGE = 'https://falandodetecnologia.com/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 6

queue = Queue()
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)

def create_spiders():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()
        
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()

def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()

def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links))+ ' links na fila')
        create_jobs()

create_spiders()
crawl()