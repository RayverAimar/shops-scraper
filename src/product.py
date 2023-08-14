from connection import *
from config import *

class Product:
    def __init__(self, name, amazon_url, ebay_url, amazon_price, ebay_price) -> None:
        self.name = name
        self.amazon_url = amazon_url
        self.ebay_url = ebay_url
        self.amazon_price = amazon_price
        self.ebay_price = ebay_price