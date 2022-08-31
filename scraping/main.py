from marketplaces.market_logger import MarketplaceLogger
from marketplaces.postman import Postman

from marketplaces.avito import Avito
from marketplaces.drom import Drom
from marketplaces.auto import Auto

try:
    logger = MarketplaceLogger()
    marketplaces = [
        Avito('https://www.avito.ru/rossiya/avtomobili?p={}', 2, logger, 0),
        Drom('https://auto.drom.ru/all/page{}/', 1, logger, 0),
        Auto('https://auto.ru/rossiya/cars/all/?page={}', 1, logger, 0)
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