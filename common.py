import psycopg2
import re
from psycopg2.extras import execute_values

db_params = {
    'host' : 'localhost',
    'port' : '5433',
    'database' : 'films',
    'user' : 'postgres',
    'password' : '1'
}

def insert_f(lst, table_name):
    
    # connection to db
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    # insert query
    insert_q = f"insert into {table_name} values %s" 
    execute_values(cursor, insert_q, lst)

    # commit changes 
    conn.commit()

    # close connection
    cursor.close()
    conn.close()


