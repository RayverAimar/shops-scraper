from connection import connect
import mysql.connector as mysql
from config import SUCCESS, ERROR
from product import Product

class DatabaseManager:
    @staticmethod
    def store_product(product : Product):
        try:
            conn = connect()
            cursor = conn.cursor()
            sql_query = 'insert into products (name, amazon_url, ebay_url, amazon_price, ebay_price) values (%s, %s, %s, %s, %s)'
            values = (product.name, product.amazon_url, product.ebay_url, product.amazon_price, product.ebay_price)
            cursor.execute(sql_query, values)
            conn.commit()
            conn.close()
            print('Product stored successfully!')
            return SUCCESS
        except mysql.Error as e:
            print('There were an error while storing the product.')
            print(e)
            return ERROR

    @staticmethod
    def get_current_products():
        try:
            conn = connect()
            cursor = conn.cursor()
            sql_query = 'select * from products'
            cursor.execute(sql_query)
            products = cursor.fetchall()
            conn.close()
            print('Products loaded successfully!')
            return products
        except mysql.Error as e:
            print('There were an error while getting the products.')
            print(e)
            return ERROR