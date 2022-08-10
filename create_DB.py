import psycopg2
from psycopg2 import OperationalError

con = psycopg2.connect(
    database="union",
    user="postgres",
    password="rEtyuol44",
    host="localhost",
    port="5432"
)
cur = con.cursor()


def execute_query(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")

create_users_table = """
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  login text, 
  password text
)
"""

execute_query(con, create_users_table)

