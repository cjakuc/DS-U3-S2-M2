import psycopg2
import os
from dotenv import load_dotenv

load_dotenv() 

### Connect to ElephantSQL-hosted PostgreSQL
DB_NAME=os.getenv("DB_NAME", default ="OOPS")
DB_USER=os.getenv("DB_USER", default ="OOPS")
DB_PASSWORD=os.getenv("DB_PASSWORD", default ="OOPS")
DB_HOST=os.getenv("DB_HOST", default ="OOPS")

connection = psycopg2.connect(dbname=DB_NAME, user=DB_NAME,
                        password=DB_PASSWORD, host=DB_HOST)
### A "cursor", a structure to iterate over db records to perform queries
cursor = connection.cursor()
### An example query
cursor.execute('SELECT * from test_table;')
### Note - nothing happened yet! We need to actually *fetch* from the cursor
result = cursor.fetchone()
print("RESULT:", result)
