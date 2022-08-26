from marketplaces.marketplace import Marketplace

class Drom(Marketplace):
    
    def get_offers_on_page(self, page):
        return page.select('a[data-ftid=bulls-list_bull]')
    
    def get_price(self, offer):
        return float(offer.select_one('span[data-ftid=bull_price]').get_text().replace('\xa0', ''))
    
    def get_name(self, offer):
        self.title = offer.select_one('span[data-ftid=bull_title]').get_text().split(', ')
        return self.title[0]
    
    def get_year(self, offer):
        return int(self.title[1])
    
    def get_main_params(self, offer):
        main_params = offer.select_one('div[data-ftid="component_inline-bull-description"]').get_text().split(', ')
        
        engine_horse = main_params[0].split(' ')
        engine_capacity = float(engine_horse[0])
        horsepower = float(engine_horse[2][1:])


        engine_type = main_params[1]

        is_new = offer.select_one('div[data-ftid*=bull_label_new]')                           
        if is_new:
            mileage = 0
        else:
            mileage = float(main_params[4].replace(' тыс. км', '') + '000')

        drive_type = main_params[3]
        transmission = main_params[2]

        body_type = None

        return mileage, engine_capacity, horsepower, body_type, drive_type, engine_type, transmission
    
    def get_offer_location(self, offer):
        return offer.select_one('span[data-ftid=bull_location]').get_text()
    
    def is_offer_vip(self, offer):
        return None
    
    def get_offer_url(self, offer):
        return offer['href']