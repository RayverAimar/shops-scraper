import mysql.connector as mysql
from config import DATABASE_NAME

def connect():
    try:
        connection = mysql.connect(
            host = 'localhost',
            user = 'root',
            password = '',
            database = DATABASE_NAME,
        )
        print(f'Connected to {DATABASE_NAME} database.')
        return connection
    except mysql.Error as e:
        print('There was an error during connection.')
        print(e)