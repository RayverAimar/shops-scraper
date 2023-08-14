from manager import DatabaseManager
from quoter import Quoter

def main():
    DatabaseManager.create_database()
    DatabaseManager.create_products_table()

    while True:
        str_product = input('Type the product you want to be quoted: ')
        Quoter.add_product_to_quote(str_product)

if __name__ == '__main__':
    main()