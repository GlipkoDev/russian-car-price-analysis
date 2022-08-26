from marketplaces.marketplace import Marketplace

class Avito(Marketplace):
        
    def get_offers_on_page(self, page):
        return page.select('*[itemtype="http://schema.org/Product"]')
    
    def get_price(self, offer):
        # 2 Possibilities:
        # First: price-text (contains min price) and price-noaccent (price withous discount),
        # Second: just price-text (price withous discount)
        # For start I check the first case, then the second one
        without_discount_price = offer.select_one('span[class*=price-noaccent]')
        if without_discount_price:
            return float(without_discount_price.get_text().replace('\xa0', '').replace(' ₽ без скидки', ''))
        else:
            return float(offer.select_one('[class*=price-text]').get_text().replace('\xa0', '')[:-1])
    
    # Title has car's name and year, so I save it inside object to use in future (get_name called before get_year)
    def get_name(self, offer):
        self.title = offer.select_one('div[class*=title]').get_text().split(', ')
        return self.title[0]
    
    def get_year(self, offer):
        return int(self.title[1])

    def get_main_params(self, offer):
        main_params = offer.select_one('div[class*=autoParams]')

        # If offer is vip, then additional info is on the upper line and separated from main params with <br>,
        # because vip offers stand together in a row of three
        # Otherwise, if offer is not vip, it have its own line, 
        # and extra info is in the same line with main params divided by ', '
        for line_break in offer.findAll('br'):     
            line_break.replaceWith(', ')

        main_params = main_params.get_text().replace('\xa0', '').split(', ')
        main_params = main_params[-5:]

        snippets = offer.select_one('div[class*=SnippetBar]')
        is_new = False
        if snippets:
            snippets = snippets.get_text()
            is_new = 'Новый' in snippets
        mileage = 0 if is_new else float(main_params[-5][:-2])

        modification = main_params[-4].split(' ')
        engine_capacity = float(modification[0])
        horsepower = float(modification[2][1:-5]) # remove brackets and postfix 'л.с.'

        body_type = main_params[-3] 
        drive_type = main_params[-2] 
        engine_type = main_params[-1] 
        transmission = None

        return mileage, engine_capacity, horsepower, body_type, drive_type, engine_type, transmission

    def get_offer_location(self, offer):
        return offer.select_one('div[class*=geo]').get_text()
    
    def is_offer_vip(self, offer):
        return 'items-vip' in offer.parent['class'][0]
    
    def get_offer_url(self, offer):
        return 'https://avito.ru/' + offer.select_one('a[data-marker=item-title]')['href']