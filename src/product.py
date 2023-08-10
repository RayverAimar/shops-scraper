from connection import *
from config import *

class Product:
    def __init__(self, name, amazon_url, ebay_url, amazon_price, ebay_price) -> None:
        self.name = name
        self.amazon_url = amazon_url
        self.ebay_url = ebay_url
        self.amazon_price = amazon_price
        self.ebay_price = ebay_price

    def store_product(self):
        try:
            conn = connect()
            cursor = conn.cursor()
            sql_query = 'insert into products (name, amazon_url, ebay_url, amazon_price, ebay_price) values (%s, %s, %s, %s, %s)'
            values = (self.name, self.amazon_url, self.ebay_url, self.amazon_price, self.ebay_price)
            cursor.execute(sql_query, values)
            conn.commit()
            conn.close()
            print('Product stored successfully!')
            return SUCCESS
        except mysql.Error as e:
            print('There were an error while storing the product.')
            print(e)
            return ERROR 