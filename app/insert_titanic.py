import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv
import json
from psycopg2.extras import execute_values

df = pd.read_csv('https://github.com/LambdaSchool/DS-Unit-3-Sprint-2-SQL-and-Databases/raw/master/module2-sql-for-analysis/titanic.csv')

load_dotenv() # look in the .env file for env vars, and add them to the env
DB_NAME = os.getenv("DB_NAME1", default="OOPS_name")
DB_USER = os.getenv("DB_USER1", default="OOPS_user")
DB_PASSWORD = os.getenv("DB_PASSWORD1", default="OOPS_password")
DB_HOST = os.getenv("DB_HOST1", default="OOPS_host")

connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)

cursor = connection.cursor()

# 
# TABLE 1 CREATION
#
query = """
CREATE TABLE IF NOT EXISTS survival_status (
  id SERIAL PRIMARY KEY
  ,survived int NOT NULL
);
"""
cursor.execute(query)
cursor.execute("SELECT * from titanic_table;")
result = cursor.fetchall()
print("RESULT:", result)

# 
# TABLE 2 CREATION
# 
attribute_query="""
CREATE TYPE sex AS ENUM ('male', 'female');
CREATE TABLE IF NOT EXISTS attributes (
  id SERIAL PRIMARY KEY
  ,Pclass int NOT NULL
  ,Name varchar(40) NOT NULL
  ,Sex sex
  ,Age int NOT NULL
  ,Sibling/Spouses_Aboard int NOT NULL
  ,Parents/Children_Aboard int NOT NULL
  ,Fare numeric NOT NULL
);
"""

# Insert data into table 1
insertion_query = "INSERT INTO survival_status (id, data) VALUES %s"

