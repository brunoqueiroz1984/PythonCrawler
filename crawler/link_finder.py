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
        self.isTitle = False
        self.isAddress = False
        self.dic = {}

    def handle_starttag(self, tag, attrs):
        if tag == 'div' and self.isEvent == 0:
            for (attribute, value) in attrs:
                if attribute == 'class' and value == 'loc_tit':
                    self.isEvent = 2
        if self.isEvent > 0:
            if tag == 'h3' and self.isEvent > 0:
                self.hasEvent = True
                self.isTitle = True
            if tag == 'p' and self.isEvent > 0:
                self.hasEvent = True
                self.isAddress = True
                
                
    def handle_data(self, data):
        if(self.hasEvent and self.isTitle):
            self.dic['name'] = data
        elif(self.hasEvent and self.isAddress):
            self.dic['address'] = data
            self.events.append(self.dic)
            self.dic = {}
    
    def handle_endtag(self, tag):
        self.hasEvent=False
        self.isTitle = False
        self.isAddress = False
        if tag == 'div' and self.isEvent > 0:
            self.isEvent-=1
                    
                    
    def page_links(self):
        return self.links
    
    def get_events(self):
        return self.events
    
    def error(self, message):
        pass
