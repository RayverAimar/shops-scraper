from connection import connect
import mysql.connector as mysql
from config import SUCCESS, ERROR, DATABASE_NAME
from product import Product

class DatabaseManager:
    products_table_created = False
    init = False

    @staticmethod
    def create_database():
        if DatabaseManager.init:
            print('Database already created!')
            return 
        try:
            connection = mysql.connect(
                host = 'localhost',
                user = 'root',
                password = '',
            )
            cursor = connection.cursor()
            sql_query = f'CREATE DATABASE {DATABASE_NAME}'
            cursor.execute(sql_query)
            DatabaseManager.init = True
            print(f'Database \'{DATABASE_NAME}\' successfully created!')
        except mysql.Error as e:
            DatabaseManager.init = False
            print('There were an error while creating the database.')
            print(e)
            return ERROR

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
    def create_products_table():
        if DatabaseManager.products_table_created:
            print('Products table already created!')
            return 
        try:
            conn = connect()
            cursor = conn.cursor()
            sql_query = """
                        create table products (\
                        id integer primary key auto_increment,\
                        name text not null,\
                        amazon_url text not null,\
                        ebay_url text not null,\
                        amazon_price decimal(10, 2) not null,\
                        ebay_price decimal(10, 2) not null)
                        """
                        
            cursor.execute(sql_query)
            conn.commit()
            conn.close()
            print('Table created successfully!')
            DatabaseManager.products_table_created = True
            return SUCCESS
        except mysql.Error as e:
            DatabaseManager.products_table_created = False
            print('There was an error while creating Products table.')
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