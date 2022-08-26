from marketplaces.marketplace import Marketplace

class Auto(Marketplace):
    
    def get_offers_on_page(self, page):
        return page.select('div[class=ListingItem__description]')
    
    def get_price(self, offer):
        prices = offer.select('.ListingItemPrice__content')
        if len(prices) == 1:
            # No discount
            price_block = prices[0]
        elif len(prices) == 2:
            # There is a discount price a base price. I take the second one.
            price_block = prices[1]
        else:
            raise Exception('There is no price found or more than two prices')
            
        return float(price_block.get_text().replace('без скидок ', '').replace('\xa0', '')[:-1])
            
    def get_name(self, offer):
        return offer.select_one('a').get_text()
    
    def get_year(self, offer):
        return int(offer.select_one('div[class=ListingItem__year]').get_text())
    
    def get_main_params(self, offer):
        mileage = offer.select_one('div[class=ListingItem__kmAge]').get_text()
        if mileage == 'Новый':
            mileage = 0
        else:
            mileage = float(mileage.replace('\xa0', '')[:-2])

        main_params = offer.select_one('div[class=ListingItem__summary] :nth-child(2)').get_text(', ').split(', ')   
            
        engine_horse_fuel = main_params[0].replace('\u2009', '').replace('\xa0', '').split('/')
        engine_capacity = float(engine_horse_fuel[0][:-2])
        horsepower = float(engine_horse_fuel[1][:-4])
        engine_type = engine_horse_fuel[2]

        transmission = main_params[1]
        body_type = main_params[2]
        drive_type = main_params[3]

        return mileage, engine_capacity, horsepower, body_type, drive_type, engine_type, transmission
    
    def get_offer_location(self, offer):
        return offer.select_one('span[class*=regionName]').get_text()
    
    def is_offer_vip(self, offer):
        return offer.select_one('div[class*=vas-icon-top-small]') is None
    
    def get_offer_url(self, offer):
        return offer.select_one('a')['href']