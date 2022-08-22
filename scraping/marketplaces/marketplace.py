# Scraping
import requests
from bs4 import BeautifulSoup as bs

# Moving to newer TSL protocol
import ssl
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
from requests.packages.urllib3.util import ssl_

# Scraping timestamp
from datetime import date

# Saving scraped info
import csv
import os.path

class TlsAdapter(HTTPAdapter):

    CIPHERS = """ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-SHA256:AES256-SHA"""

    def __init__(self, ssl_options=0, **kwargs):
        self.ssl_options = ssl_options
        super(TlsAdapter, self).__init__(**kwargs)

    def init_poolmanager(self, *pool_args, **pool_kwargs):
        ctx = ssl_.create_urllib3_context(ciphers=self.CIPHERS, cert_reqs=ssl.CERT_REQUIRED, options=self.ssl_options)
        self.poolmanager = PoolManager(*pool_args, ssl_context=ctx, **pool_kwargs)

class Marketplace():
    
    headers = ['price', 'name', 'year', 'mileage', 
               'engine_capacity', 'horsepower', 'body_type', 'drive_type', 'engine_type', 
               'offer_location', 'is_offer_vip', 'offer_url', 'marketplace', 'scraping_time']
    data_file = 'data.csv'
    logs_file = 'logs.txt'
    
    def __init__(self, marketplace_name, url_to_parse):

        self.marketplace_name = marketplace_name
        self.url_to_parse = url_to_parse

        self.session = requests.session()
        adapter = TlsAdapter(ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1)
        self.session.mount("https://", adapter)
    
    def parse_all_pages(self):
        raise Exception('Not Implemented')
    
    def parse_page(self, page):
        response = self.session.get(self.url_to_parse.format(page))

        if response.status_code == 200:
            page = bs(response.content, 'html.parser')
            offers = self.get_offers_on_page(page)
            cars_info = []
            for offer in offers:
                car_info = self.parse_offer(offer)
                if car_info:
                    cars_info.append(car_info)
            self.save_cars_info(cars_info)
        else:
            raise Exception('Response code differs from 200')

    def get_offers_on_page(self, page):
        raise Exception('Not Implemented')
    
    def parse_offer(self, offer):
        try:
            return {
                'price' : self.get_price(offer),
                'name' : self.get_name(offer),
                'year' : self.get_year(offer),
                'mileage' : self.get_mileage(offer),
                'engine_capacity' : self.get_engine_capacity(offer),
                'horsepower' : self.get_horsepower(offer),
                'body_type' : self.get_body_type(offer),
                'drive_type' : self.get_drive_type(offer),
                'engine_type' : self.get_engine_type(offer),
                'transmission' : self.get_transmission(offer),
                'offer_location' : self.get_offer_location(offer),
                'is_offer_vip' : self.is_offer_vip(offer),
                'offer_url' : self.get_offer_url(offer),
                'marketplace' : self.marketplace_name,
                'scraping_time' : date.today()
            }
        except Exception as e:
            logs = open(self.logs_file, 'a', encoding='utf-8')
            logs.write('Failed to parse offer:\n{0}\n due to this error:\n{1}\n'.format(offer, str(e)))
            logs.close()
            return None
        
    def get_price(self, offer):
        raise Exception('Not Implemented')
            
    def get_name(self, offer):
        raise Exception('Not Implemented')
            
    def get_year(self, offer):
        raise Exception('Not Implemented')
            
    def get_mileage(self, offer):
        raise Exception('Not Implemented')
            
    def get_engine_capacity(self, offer):
        raise Exception('Not Implemented')
            
    def get_horsepower(self, offer):
        raise Exception('Not Implemented')
            
    def get_body_type(self, offer):
        raise Exception('Not Implemented')
            
    def get_drive_type(self, offer):
        raise Exception('Not Implemented')
            
    def get_engine_type(self, offer):
        raise Exception('Not Implemented')

    def get_transmission(self, offer):
        raise Exception('Not Implemented')
            
    def get_offer_location(self, offer):
        raise Exception('Not Implemented')
            
    def is_offer_vip(self, offer):
        raise Exception('Not Implemented')
            
    def get_offer_url(self, offer):
        raise Exception('Not Implemented')    
        
    def save_cars_info(self, cars_info):
        need_headers = not os.path.exists(self.data_file)
        
        with open(self.data_file, 'a') as f:
            writer = csv.DictWriter(f, delimiter=',', lineterminator='\n', fieldnames = self.headers)
            
            if need_headers:
                writer.writeheader()
                
            for car_info in cars_info:
                writer.writerow(car_info)