import psycopg2
import os
from dotenv import load_dotenv
import json
from psycopg2.extras import execute_values

load_dotenv() # look in the .env file for env vars, and add them to the env
DB_NAME = os.getenv("DB_NAME", default="OOPS")
DB_USER = os.getenv("DB_USER", default="OOPS")
DB_PASSWORD = os.getenv("DB_PASSWORD", default="OOPS")
DB_HOST = os.getenv("DB_HOST", default="OOPS")

connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
print("CONNECTION:", connection)

cursor = connection.cursor()
print("CURSOR:", cursor)

#
# TABLE CREATION
#
query = """
CREATE TABLE IF NOT EXISTS test_table (
  id SERIAL PRIMARY KEY,
  name varchar(40) NOT NULL,
  data JSONB
);
"""
cursor.execute(query)
cursor.execute("SELECT * from test_table;")
result = cursor.fetchall()
print("RESULT:", len(result))

#
# DATA INSERTION
#
#
# APPROACH 1 (hard-coded)
#
#insertion_query = """
#INSERT INTO test_table (name, data)
#VALUES
#    ('A row name', null),
#    ('Another row, with JSON', '{ "a": 1, "b": ["dog", "cat", 42], "c": true }'::JSONB)
#"""

#
# APPROACH 2 (needs updating / wasn't working sorry!)
#
#my_dict = { "a": 1, "b": ["dog", "cat", 42], "c": 'true' }
#insertion_query = f"INSERT INTO test_table (name, data) VALUES (%s, %s)"
#cursor.execute(insertion_query,
#  ('A rowwwww', 'null')
#)
#cursor.execute(insertion_query,
#  ('Another row, with JSONNNNN', json.dumps(my_dict))
#)
#cursor.execute(insertion_query)

#
# APPROACH 3 (multi-row insert!)
#
my_dict = { "a": 1, "b": ["dog", "cat", 42], "c": 'true' }
# h/t: https://stackoverflow.com/questions/8134602/psycopg2-insert-multiple-rows-with-one-query
insertion_query = "INSERT INTO test_table (name, data) VALUES %s"
execute_values(cursor, insertion_query, [
  ('A rowwwww', 'null'),
  ('Another row, with JSONNNNN', json.dumps(my_dict)),
  ('Third row', "3")
])
cursor.execute("SELECT * from test_table;")
result = cursor.fetchall()
print("RESULT:", len(result))

# ACTUALLY SAVE THE TRANSACTIONS
connection.commit()