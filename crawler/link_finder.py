'''
Created on 31 de jan de 2018

@author: Bruno
'''
from html.parser import HTMLParser
from urllib import parse

class LinkFinder(HTMLParser):
    
    isEvent = 0
    events = set()
    
    def __init__(self, base_url, page_url):
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()

    def handle_starttag(self, tag, attrs):
        if tag == 'div' and self.isEvent == 0:
            for (attribute, value) in attrs:
                if attribute == 'class' and value == 'loc_tit':
                    isEvent = 2
        elif self.isEvent > 0:
            if tag == 'h3' and self.isEvent > 0:
                self.events.add(self.get_starttag_text())
            if tag == 'p' and self.isEvent > 0:
                self.events.add(self.get_starttag_text())
    
    def handle_endtag(self, tag):
        if tag == 'div' and self.isEvent > 0:
            self.isEvent-=1
                    
                    
    def page_links(self):
        return self.links
    
    def events(self):
        return self.events
    
    def error(self, message):
        pass
