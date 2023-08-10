import mysql.connector as mysql

def connect():
    try:
        connection = mysql.connect(
            host = 'localhost',
            user = 'root',
            password = '',
            database = 'shop_scraper',
        )
        print('Connected to the database.')
        return connection
    except mysql.Error as e:
        print('There was an error during connection.')
        print(e)