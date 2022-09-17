import sys

from marketplaces.market_logger import MarketplaceLogger
from marketplaces.postman import Postman

from marketplaces.avito import Avito
from marketplaces.drom import Drom
from marketplaces.auto import Auto

pages_to_scrape = int(sys.argv[1])
delay = int(sys.argv[2])

try:
    logger = MarketplaceLogger()
    marketplaces = [
        Avito('https://www.avito.ru/rossiya/avtomobili?p={}', pages_to_scrape, logger, delay),
        Drom('https://auto.drom.ru/all/page{}/', pages_to_scrape, logger, delay),
        Auto('https://auto.ru/rossiya/cars/all/?page={}', pages_to_scrape, logger, delay)
        ]

    generators = [marketplace.parse_all_pages() for marketplace in marketplaces]

    while len(generators) > 0:
        try:
            for generator in generators:
                next(generator)
        except StopIteration:
            generators.remove(generator)

    postman = Postman(logger)
    postman.send_logs()
except Exception as e:
    print(e)
    logger.clear_logs()