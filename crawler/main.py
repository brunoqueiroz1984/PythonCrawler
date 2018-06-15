'''
Created on 1 de fev de 2018
@author: Bruno
'''
from urllib.request import urlopen
from link_finder import LinkFinder
from pymongo import mongo_client

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
        event['type'] = eventType
        collection.update_one({'name':event['name']},{'$set': event}, upsert = True)
    

collection = db['events']

events = gather_events('https://agendasorocaba.com.br/baladas/')
saveDB('balada')
events = gather_events('https://agendasorocaba.com.br/bares/')
saveDB('bar')
events = gather_events('https://agendasorocaba.com.br/comidas/brasileiro/')
saveDB('restaurante')
events = gather_events('https://agendasorocaba.com.br/comidas/diversos/')
saveDB('restaurante')
events = gather_events("https://agendasorocaba.com.br/comidas/vegetarianos/")
saveDB('restaurante')
events = gather_events("https://agendasorocaba.com.br/comidas/batatarias/")
saveDB('restaurante')
events = gather_events("https://agendasorocaba.com.br/comidas/japones/")
saveDB('restaurante')
events = gather_events('https://agendasorocaba.com.br/comidas/pizzarias/')
saveDB('restaurante')
events = gather_events('https://agendasorocaba.com.br/comidas/massas/')
saveDB('restaurante')
events = gather_events('https://agendasorocaba.com.br/cultura/')
saveDB('cultura')

print("events inserted")