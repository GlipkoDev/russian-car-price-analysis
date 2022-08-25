import os
import shutil

from datetime import date

from csv import DictWriter

from uuid import uuid4

class MarketplaceLogger():

    data_headers = ['price', 'name', 'year', 'mileage', 
               'engine_capacity', 'horsepower', 'body_type', 'drive_type', 'engine_type', 'transmission',
               'offer_location', 'is_offer_vip', 'offer_url', 'marketplace', 'scraping_time']

    def __init__(self):

        self.current_date = str(date.today())
        if os.path.exists(self.current_date):
            shutil.rmtree(self.current_date)

        os.mkdir(self.current_date)
        os.mkdir(f'{self.current_date}/broken_offers')

    def log_parser_work(self, marketplace_name, offers_counts, broken_offers_count):
        with open(f'{self.current_date}/logs.txt', 'a') as f:
            f.write(f'{marketplace_name} - got in total {offers_counts} offers, {broken_offers_count} of them are broken')

    def save_broken_offer(self, marketplace_name, offer):

        offer_uuid = str(uuid4())

        with open(f'{self.current_date}/broken_offers/{self.marketplace_name}_{offer_uuid}.txt', 'w') as f:
            f.write(str(offer))

    def save_cars_info(self, cars_info):
        need_headers = not os.path.exists(f'{self.current_date}/data.csv')
        
        with open(f'{self.current_date}/data.csv', 'a') as f:
            writer = DictWriter(f, delimiter=',', lineterminator='\n', fieldnames = self.data_headers)
            
            if need_headers:
                writer.writeheader()
                
            for car_info in cars_info:
                writer.writerow(car_info)
        

    

            