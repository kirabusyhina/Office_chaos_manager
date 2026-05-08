import mysql.connector

def get_connection():

    return mysql.connector.connect(
        host="10.200.10.14",
        user="root",
        password="2808200",
        database="office_chaos_manager"
    )