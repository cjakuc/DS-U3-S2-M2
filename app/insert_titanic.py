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

temp = """
DROP TABLE survival_status, attributes;
"""
cursor.execute(temp)

# 
# TABLE 1 CREATION
#
survival_query = """
CREATE TABLE IF NOT EXISTS survival_status (
  id INTEGER PRIMARY KEY NOT NULL
  ,Survived INTEGER NOT NULL
);
"""
cursor.execute(survival_query)

# Insert values into survival_status table
survival_insertion_query = """INSERT INTO survival_status (id, Survived)
VALUES %s
ON CONFLICT DO NOTHING
"""
survival_df = df['Survived']
survival_list = list(zip(survival_df.index,survival_df))
execute_values(cursor, survival_insertion_query, survival_list)



# 
# TABLE 2 CREATION
# 
attribute_query="""
CREATE TABLE IF NOT EXISTS attributes (
  id INTEGER REFERENCES survival_status (id)
  ,Pclass INTEGER NOT NULL
  ,Name TEXT NOT NULL
  ,Sex TEXT NOT NULL
  ,Age INTEGER NOT NULL
  ,Sibling_Spouses_Aboard INTEGER NOT NULL
  ,Parents_Children_Aboard INTEGER NOT NULL
  ,Fare REAL NOT NULL
);
"""
cursor.execute(attribute_query)



# Insert data into attributes table
attributes_insertion_query = """INSERT INTO attributes (Pclass,Name,Sex,Age,Sibling_Spouses_Aboard,Parents_Children_Aboard,Fare)
VALUES %s
ON CONFLICT DO NOTHING
"""
attributes_df = df.drop(columns=['Survived'])
attributes_list = list(attributes_df.itertuples(index=False))
execute_values(cursor, attributes_insertion_query, attributes_list)


# ACTUALLY SAVE THE TRANSACTIONS
connection.commit()