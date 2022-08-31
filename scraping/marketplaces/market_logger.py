import os
from shutil import make_archive, rmtree

from datetime import date

from csv import DictWriter

from uuid import uuid4

class MarketplaceLogger():

    data_headers = ['price', 'name', 'year', 'mileage', 
               'engine_capacity', 'horsepower', 'body_type', 'drive_type', 'engine_type', 'transmission',
               'offer_location', 'is_offer_vip', 'offer_url', 'marketplace', 'scraping_time']

    def __init__(self):

        self.current_date = str(date.today())

        os.mkdir(self.current_date)
        os.mkdir(f'{self.current_date}/broken_offers')

    def save_parser_summary(self, marketplace_name, offers_counts, broken_offers_count, was_interrupted, interruption_reason):
        with open(f'{self.current_date}/logs.txt', 'a', encoding='utf-8') as f:
            f.write(f'{marketplace_name}\nGot in total {offers_counts} offers, {broken_offers_count} of them are broken\n')
            if was_interrupted:
                f.write(f'{marketplace_name} parser was stopped due to \n{interruption_reason}\n')

    def save_broken_offer(self, marketplace_name, offer):

        offer_uuid = str(uuid4())
        offer = str(offer).replace('\u20bd', 'Р')

        with open(f'{self.current_date}/broken_offers/{marketplace_name}_{offer_uuid}.txt', 'w', encoding='utf-8') as f:
            f.write(str(offer))

    def save_cars_info(self, cars_info):
        need_headers = not os.path.exists(f'{self.current_date}/data.csv')
        
        with open(f'{self.current_date}/data.csv', 'a', encoding='utf-8') as f:
            writer = DictWriter(f, delimiter=',', lineterminator='\n', fieldnames = self.data_headers)
            
            if need_headers:
                writer.writeheader()
                
            for car_info in cars_info:
                writer.writerow(car_info)

    def zip_logs(self):
        make_archive(self.current_date, 'zip', self.current_date)

    def clear_logs(self):
        rmtree(self.current_date, ignore_errors=True)
        if os.path.exists(f'{self.current_date}.zip'):
            os.remove(f'{self.current_date}.zip')

    

            