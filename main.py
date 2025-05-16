import pyodbc

conn_str = ("Driver={ODBC Driver 17 for SQL Server};"
            "Server=DESKTOP-KFM6TH5;"
            "Trusted_Connection=yes;")

conn = pyodbc.connect(conn_str, autocommit=True)
cursor = conn.cursor()

ddl = open("ddl.sql").read()
cursor.execute(ddl)
