import pyodbc
from dotenv import load_dotenv
from os import environ

DRIVER = environ.get("DRIVER")
SERVER = environ.get("SERVER")
DATABASE = environ.get("DATABASE")

conn_str = f"Driver={DRIVER};Server={SERVER};Database={DATABASE};Trusted_Connection=yes;"

try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    # print("Connection successful!")
except Exception as e:
    print(f"Error connecting to database: {e}")


def db_modify_query_execute(query):
    try:
        cursor.execute(query)
        conn.commit()
    except Exception as e:
        print(f"An error accorded: {e}")
        conn.rollback()


def db_query_execute(query):
    try:
        query_cursor = cursor.execute(query)
        return query_cursor
    except Exception as e:
        print(f"An error accorded: {e}")
