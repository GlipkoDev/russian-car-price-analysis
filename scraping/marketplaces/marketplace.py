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

# Delay in requests
import time

class TlsAdapter(HTTPAdapter):

    CIPHERS = """ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-SHA256:AES256-SHA"""

    def __init__(self, ssl_options=0, **kwargs):
        self.ssl_options = ssl_options
        super(TlsAdapter, self).__init__(**kwargs)

    def init_poolmanager(self, *pool_args, **pool_kwargs):
        ctx = ssl_.create_urllib3_context(ciphers=self.CIPHERS, cert_reqs=ssl.CERT_REQUIRED, options=self.ssl_options)
        self.poolmanager = PoolManager(*pool_args, ssl_context=ctx, **pool_kwargs)

class Marketplace():
    
    def __init__(self, url_to_parse, max_pages, logger, delay):

        self.marketplace_name = type(self).__name__
        self.url_to_parse = url_to_parse
        self.max_pages = max_pages
        self.logger = logger
        self.delay = delay

        self.offers_count = 0
        self.broken_offers_count = 0
        
        self.logger = logger

        self.session = requests.session()
        adapter = TlsAdapter(ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1)
        self.session.mount("https://", adapter)

    def parse_all_pages(self):
        was_interrupted = False
        interruption_reason = None
        for i in range(1, self.max_pages+1):
            print(f'{self.marketplace_name} - {i}')
            try:
                page = self.get_page(i)
            except Exception as e:
                was_interrupted = True
                interruption_reason = e
                break
            time.sleep(self.delay)
            yield None
        self.logger.save_parser_summary(self.marketplace_name, self.offers_count, self.broken_offers_count, was_interrupted, interruption_reason)
        
    
    def get_page(self, page_num):
        response = self.session.get(self.url_to_parse.format(page_num))
        if response.status_code == 200:
            return response.content
        else:
            raise Exception(f'Response code differs from 200: {response.status_code}')

    def parse_page(self, page):

        page = bs(page, 'html.parser')

        offers = self.get_offers_on_page(page)
        self.offers_count += len(offers)
        
        cars_info = []
        for offer in offers:

            try:
                car_info = self.parse_offer(offer)
                cars_info.append(car_info)
            except Exception as e:
                
                self.broken_offers_count += 1
                self.logger.save_broken_offer(self.marketplace_name, offer)
                    
        self.logger.save_cars_info(cars_info)

    def get_offers_on_page(self, page):
        raise Exception('Not Implemented')
    
    def parse_offer(self, offer):

        mileage, engine_capacity, horsepower, body_type, drive_type, engine_type, transmission = self.get_main_params(offer)

        return {
            'price' : self.get_price(offer),
            'name' : self.get_name(offer),
            'year' : self.get_year(offer),
            'mileage' : mileage,
            'engine_capacity' : engine_capacity,
            'horsepower' : horsepower,
            'body_type' : body_type,
            'drive_type' : drive_type,
            'engine_type' : engine_type,
            'transmission' : transmission,
            'offer_location' : self.get_offer_location(offer),
            'is_offer_vip' : self.is_offer_vip(offer),
            'offer_url' : self.get_offer_url(offer),
            'marketplace' : self.marketplace_name,
            'scraping_time' : date.today()
        }
        
    def get_price(self, offer):
        raise Exception('Not Implemented')
            
    def get_name(self, offer):
        raise Exception('Not Implemented')
            
    def get_year(self, offer):
        raise Exception('Not Implemented')
            
    def get_main_params(self, offer):
        raise Exception('Not Implemented')
            
    def get_offer_location(self, offer):
        raise Exception('Not Implemented')
            
    def is_offer_vip(self, offer):
        raise Exception('Not Implemented')
            
    def get_offer_url(self, offer):
        raise Exception('Not Implemented')