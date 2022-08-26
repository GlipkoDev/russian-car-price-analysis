from marketplaces.market_logger import MarketplaceLogger

from marketplaces.avito import Avito
from marketplaces.drom import Drom
from marketplaces.auto import Auto

logger = MarketplaceLogger()
parsers = [
    Avito('https://www.avito.ru/rossiya/avtomobili?p={}', 2, logger),
    Drom('https://auto.drom.ru/all/page{}/', 2, logger),
    Auto('https://auto.ru/rossiya/cars/all/?page={}', 2, logger)
    ]

for parser in parsers:
    parser.parse_all_pages()

