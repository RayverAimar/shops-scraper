from product import Product
from scraper import AmazonScraper, EbayScraper
from manager import DatabaseManager
from selenium.common.exceptions import TimeoutException
from notifypy import Notify
from time import sleep
from threading import Thread

def send_alert(msg):
    notification = Notify()
    notification.title = "Quoter has a new message"
    notification.message = msg
    notification.send()

class Quoter:
    def __init__(self) -> None:
        pass

    @staticmethod
    def add_product_to_quote(product_name):
        amazon_scraper = AmazonScraper(
            product_name=product_name
        )
        ebay_scraper = EbayScraper(
            product_name=product_name,
        )

        amazon_scraper.scrape()
        ebay_scraper.scrape()

        amazon_product = amazon_scraper.choose_product()
        ebay_product = ebay_scraper.choose_product()

        product = Product(
            name=product_name,
            amazon_url=amazon_product.url,
            ebay_url=ebay_product.url,
            amazon_price=amazon_product.price,
            ebay_price=ebay_product.price,
        )

        DatabaseManager.store_product(product)
    
    @staticmethod
    def quote():
        while True:
            products = DatabaseManager.get_current_products()
            for product in products:
                id, name, amazon_url, ebay_url, amazon_price, ebay_price = product
                try:
                    new_amazon_price = AmazonScraper.get_price_of_product(amazon_url)
                except  TimeoutException as TE:
                    print('Error while loading page. Skipping...')
                    continue
                new_ebay_price = EbayScraper.get_price_of_product(ebay_url)
                if new_amazon_price < float(amazon_price):
                    send_alert(f'The product {name} got a discount from {amazon_price} to {new_amazon_price} in Amazon!')
                if new_ebay_price < float(ebay_price):
                    send_alert(f'The product {name} got a discount from {amazon_price} to {new_amazon_price} in Amazon!')
                if new_amazon_price < new_ebay_price:
                    send_alert(f'The product {name} is cheaper in Amazon ({amazon_price}) than in eBay ({ebay_price})')
                else:
                    send_alert(f'The product {name} is cheaper in eBay ({ebay_price}) than in Amazon ({amazon_price})')
            sleep(3600)

def main():
    thread = Thread(target=Quoter.quote)
    print('Starting quoting...')
    thread.start()

if __name__ == '__main__':
    main()