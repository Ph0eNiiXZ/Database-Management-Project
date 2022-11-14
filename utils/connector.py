# used for sqlite3 connection (.db)
import sqlite3

def connect(db):
    return sqlite3.connect(db)

def execute_query_file(connector: sqlite3.Connection, sql_file: str):
    with open(sql_file, 'r', encoding='utf-8') as f:
        sql = f.read()
    
    connector.execute(sql)
