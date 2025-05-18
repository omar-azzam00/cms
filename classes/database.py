import pyodbc
from dotenv import load_dotenv
from os import environ


class Database:
    def __init__(self):
        self.__connect()
        self.__create_db()
        
    def query_execute(self, query):
        try:
            self.cursor.execute(query)
            return self.cursor
        except Exception as e:
            print(f"An error accorded: {e}")
                   
    def modify_query_execute(self, query):
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            print(f"An error accorded: {e}")
            self.conn.rollback()
    
    def __connect(self):
        DRIVER = environ.get("DRIVER")
        SERVER = environ.get("SERVER")

        conn_str = f"Driver={DRIVER};Server={SERVER};Trusted_Connection=yes;"
        
        try:
            self.conn = pyodbc.connect(conn_str)
            self.cursor = self.conn.cursor()
            # print("Connection successful!")
        except Exception as e:
            print(f"Error connecting to database: {e}")
            
    def __create_db(self):        
        try:
            ddl_file = open("./extras/ddl.sql")
            ddl = ddl_file.read()
            self.cursor.execute(ddl)
            
        except FileNotFoundError as e:
            print("Please Include the correct path for the ddl.sql file")
            print(e)
        except Exception as e:
            print("Error while executing ddl!")
    
            

