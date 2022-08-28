from marketplaces.market_logger import MarketplaceLogger
from marketplaces.postman import Postman

from marketplaces.avito import Avito
from marketplaces.drom import Drom
from marketplaces.auto import Auto

logger = MarketplaceLogger()
marketplaces = [
    Avito('https://www.avito.ru/rossiya/avtomobili?p={}', 1, logger),
    Drom('https://auto.drom.ru/all/page{}/', 1, logger),
    Auto('https://auto.ru/rossiya/cars/all/?page={}', 1, logger)
    ]

for marketplace in marketplaces:
    marketplace.parse_all_pages()

postman = Postman(logger)
postman.send_logs()

