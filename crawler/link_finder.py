'''
Created on 31 de jan de 2018

@author: Bruno
'''
from html.parser import HTMLParser
from urllib import parse

class LinkFinder(HTMLParser):
    
    
    
    def __init__(self, base_url, page_url):
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()
        self.isEvent = 0
        self.events = list()
        self.num = 0
        self.hasEvent = False

    def handle_starttag(self, tag, attrs):
        if tag == 'div' and self.isEvent == 0:
            for (attribute, value) in attrs:
                if attribute == 'class' and value == 'loc_tit':
                    self.isEvent = 2
        if self.isEvent > 0:
            if tag == 'h3' and self.isEvent > 0:
                self.hasEvent=True
            if tag == 'p' and self.isEvent > 0:
                self.hasEvent=True
                
                
    def handle_data(self, data):
        if(self.hasEvent):
            self.events.append(data+'\n')
    
    def handle_endtag(self, tag):
        self.hasEvent=False
        if tag == 'div' and self.isEvent > 0:
            self.isEvent-=1
                    
                    
    def page_links(self):
        return self.links
    
    def get_events(self):
        return self.events
    
    def error(self, message):
        pass
