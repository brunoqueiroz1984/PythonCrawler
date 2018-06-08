'''
Created on 1 de fev de 2018
@author: Bruno
'''
from urllib.request import urlopen
from link_finder import LinkFinder
from domain import get_domain_name
from pymongo import mongo_client

PROJECT_NAME = 'Celebratio'
HOMEPAGE = 'https://agendasorocaba.com.br/baladas/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 1

DB_NAME = 'celebration' 
DB_HOST = 'ds161529.mlab.com'
DB_PORT = 61529
DB_USER = 'admin' 
DB_PASS = '1234'

connection = mongo_client.MongoClient(DB_HOST, DB_PORT)
db = connection[DB_NAME]
db.authenticate(DB_USER, DB_PASS)

def gather_events(page_url):
        html_string =''
        try:
            response = urlopen(page_url)
            print('conected')
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode('utf-8')
            finder = LinkFinder(page_url, page_url)
            finder.feed(html_string)
        except:
            print('Error: can not crawl page')
            return set()
        return finder.get_events()

def saveDB(eventType):
    for event in events:
        if(collection.find({'name':event['name']}).count() == 0 ):
            event['type'] = eventType
            collection.insert_one(event)
        else:
            print('test')
    

collection = db['events']

events = gather_events('https://agendasorocaba.com.br/baladas/')
saveDB('balada')
events = gather_events('https://agendasorocaba.com.br/bares/')
saveDB('bar')
events = gather_events('https://agendasorocaba.com.br/comidas/brasileiro/')
saveDB('restaurante')
events = gather_events('https://agendasorocaba.com.br/comidas/diversos/')
saveDB('restaurante')

print("events inserted")