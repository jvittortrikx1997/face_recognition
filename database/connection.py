import mysql.connector

def get_db_connection():
    db_config = {
        'user': 'root',
        'password': '',
        'host': 'localhost',
        'database': 'tcc'
    }
    return mysql.connector.connect(**db_config)