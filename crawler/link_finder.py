'''
Created on 31 de jan de 2018

@author: Bruno
'''
from html.parser import HTMLParser
from urllib.request import urlopen
import requests

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
        self.isLink = False
        self.isImg = False
        self.dic = {}

    def handle_starttag(self, tag, attrs):
        if tag == 'div' and self.isEvent == 0:
            for (attribute, value) in attrs:
                if attribute == 'class' and value == 'loc_tit':
                    self.isEvent = 2
        
        if tag == 'ul':
            for (attribute, value) in attrs:
                if attribute == 'class' and value == 'blocks blocks_locais':
                    self.isLink = True
                    
        if tag == 'a' and self.isLink:
            for (attribute, value) in attrs:
                if attribute == 'href':
                    self.dic = self.getDetails(value)
                    
        
        if tag == 'div' and self.isLink:
            for (attribute, value) in attrs:
                if attribute == 'class' and value == 'loc_img':
                    self.isImg = True
                elif self.isImg and (attribute == 'style' or attribute == 'data-img'):
                    self.dic['img'] = self.formatImgName(str(value))
                    self.isImg = False
        
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
            self.dic['latitude'],self.dic['longitude'] = self.getCoordinates(data)
            self.events.append(self.dic)
            print(str(self.dic).encode(encoding='utf_8'))
            self.dic = {}
    
    def handle_endtag(self, tag):
        self.hasEvent=False
        self.isTitle = False
        self.isAddress = False
        if tag == 'ul':
            self.isLink = False
        if tag == 'div' and self.isEvent > 0:
            self.isEvent-=1
    
    def getDetails(self, link):
        html_string =''
        try:
            response = urlopen(link)
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode('utf-8')
        except:
            print('couldn`t get details')
            return
        finder = DetailFinder()
        finder.feed(html_string)
        return finder.getInfo()
        
    
    def getCoordinates(self, address):
        api_key = 'AIzaSyAYHzy6jKAUjUcVGjnokOwBN65gkx6OfqE'
        api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(address, api_key))
        api_response_dict = api_response.json()
        
        if api_response_dict['status'] == 'OK':
            latitude = api_response_dict['results'][0]['geometry']['location']['lat']
            longitude = api_response_dict['results'][0]['geometry']['location']['lng']
            return (latitude, longitude)
        else:
            return ('error', 'error')
    
    def formatImgName(self, imgName):
        return imgName.replace("background-image:url(","").replace(");opacity:1;", "")
        
        
    
    def page_links(self):
        return self.links
    
    def get_events(self):
        return self.events
    
    def error(self, message):
        pass


class DetailFinder(HTMLParser):
    
    def __init__(self):
        super().__init__()
        self.dic = {}
        self.isDetail = False
        self.isDetailText = False
        self.isDetailServico = False
        self.isTel = False
        self.isTelData = False
        self.getTel = False
        self.isWebData = False
        self.getSite = False
        self.text = ''
        
    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            for (attribute, value) in attrs:
                if attribute == 'class' and value =='bigcon':
                    self.isDetail = True
                if attribute == 'class' and value =='watributos':
                    self.isDetail = False
                if attribute == 'class' and value == 'cdivi':
                    self.isDetail = True
                    
        if self.isDetail and not self.isDetailServico and tag == 'p':
            self.isDetailText = True
            
        if self.isDetailText and tag == 'div':
            for (attribute, value) in attrs:
                if attribute == 'class' and value =='servico':
                    self.isDetailText = False
                    self.isDetailServico = True
        if self.isDetailServico and tag == 'p':
            for (attribute, value) in attrs:
                if attribute == 'class' and value == 'tel':
                    self.isTelData = True
                elif attribute == 'class' and value == 'ste':
                    self.isWebData = True
                    
        if self.isTelData and tag =='a':
            self.getTel = True
        elif self.isWebData and tag =='a':
            self.getSite = True
        
    
    
    def handle_data(self, data):
        if self.isDetailText:
            self.text+= data
        if self.getTel:
            self.dic['tel'] = data
        elif self.getSite:
            self.dic['site'] = data
            
    def handle_endtag(self, tag):
        if tag == 'div' and self.isDetailServico:
            self.isDetail = False
            self.isDetailText = False
            self.isDetailServico = False
            self.dic['desc'] = self.text
            self.text = ''
        self.isTel = False
        self.isTelData = False
        self.getTel = False
        self.isWebData = False
        self.getSite = False
        
    def getInfo(self):
        return self.dic
            
            
