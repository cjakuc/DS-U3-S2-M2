import psycopg2
import os
from dotenv import load_dotenv
import json
from psycopg2.extras import execute_values
import sqlite3

# Save the sqlite filepath for the DB to a variable
DB_FILEPATH = os.path.join(os.path.dirname(__file__), "..","..","M1/rpg_db.sqlite3")

# Intanstiate the connection
lite_connection = sqlite3.connect(DB_FILEPATH)

# Instantiate the cursor
lite_cursor = lite_connection.cursor()

# Open the connection to the postgres DB
load_dotenv() # look in the .env file for env vars, and add them to the env
DB_NAME = os.getenv("DB_NAME", default="OOPS")
DB_USER = os.getenv("DB_USER", default="OOPS")
DB_PASSWORD = os.getenv("DB_PASSWORD", default="OOPS")
DB_HOST = os.getenv("DB_HOST", default="OOPS")

post_connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)

post_cursor = post_connection.cursor()

#
### charactercreator_character table
#

# Take the first table, character, out of the sqlite DB
char_query = """
SELECT
    *
FROM
    charactercreator_character
"""
char_result = lite_cursor.execute(char_query).fetchall()

# Create the character table in the pg DB
char_create = """
CREATE TABLE IF NOT EXISTS charactercreator_character (
  character_id INTEGER PRIMARY KEY NOT NULL
  ,name varchar(30) NOT NULL
  ,level INTEGER NOT NULL
  ,exp INTEGER NOT NULL
  ,hp INTEGER NOT NULL
  ,strength INTEGER NOT NULL
  ,intelligence INTEGER NOT NULL
  ,dexterity INTEGER NOT NULL
  ,wisdom INTEGER NOT NULL
);
"""
post_cursor.execute(char_create)

# Put character table into the pg DB
char_insertion_query = """
INSERT INTO charactercreator_character (character_id ,name, level, exp, hp, strength, intelligence, dexterity, wisdom)
VALUES %s
ON CONFLICT DO NOTHING
"""
execute_values(post_cursor, char_insertion_query, char_result)

#
### armory_item table
#

# Take the table, armory_item, out of the sqlite DB
item_query = """
SELECT
    *
FROM
    armory_item
"""
item_result = lite_cursor.execute(item_query).fetchall()

# Create the item table in the pg DB
item_create = """
CREATE TABLE IF NOT EXISTS armory_item (
  item_id INTEGER PRIMARY KEY NOT NULL
  ,name varchar(30) NOT NULL
  ,value INTEGER NOT NULL
  ,weight INTEGER NOT NULL
);
"""
post_cursor.execute(item_create)

# Put character table into the pg DB
item_insertion_query = """INSERT INTO armory_item (item_id, name, value, weight)
VALUES %s
ON CONFLICT DO NOTHING
"""
execute_values(post_cursor, item_insertion_query, item_result)

#
## armory_weapon table
#

# Take the table, armory_weapon, out of the sqlite DB
weapon_query = """
SELECT
    *
FROM
    armory_weapon
"""
weapon_result = lite_cursor.execute(weapon_query).fetchall()

# Create the weapon table in the pg DB
weapon_create = """
CREATE TABLE IF NOT EXISTS armory_weapon (
  item_ptr_id INTEGER REFERENCES armory_item (item_id)
  ,power INTEGER NOT NULL
);
"""
post_cursor.execute(weapon_create)

# Put character table into the pg DB
weapon_insertion_query = """INSERT INTO armory_weapon (item_ptr_id, power)
VALUES %s
ON CONFLICT DO NOTHING
"""
execute_values(post_cursor, weapon_insertion_query, weapon_result)

#
## charactercreator_character_inventory table
#

# Take the table, charactercreator_character_inventory, out of the sqlite DB
ch_inv_query = """
SELECT
    *
FROM
    charactercreator_character_inventory
"""
ch_inv_result = lite_cursor.execute(ch_inv_query).fetchall()

# Create the charactercreator_character_inventory table in the pg DB
ch_inv_create = """
CREATE TABLE IF NOT EXISTS charactercreator_character_inventory (
  id INTEGER PRIMARY KEY NOT NULL
  ,character_id INTEGER REFERENCES charactercreator_character (character_id)
  ,item_id INTEGER REFERENCES armory_item (item_id)
);
"""
post_cursor.execute(ch_inv_create)

# Put character inventory table into the pg DB
ch_inv_insertion_query = """INSERT INTO charactercreator_character_inventory (id, character_id, item_id)
VALUES %s
ON CONFLICT DO NOTHING
"""
execute_values(post_cursor, ch_inv_insertion_query, ch_inv_result)

# temp = """
# DROP TABLE charactercreator_mage, charactercreator_thief;
# """
# post_cursor.execute(temp)

#
## charactercreator_mage table
#

# Take the table, charactercreator_mage, out of the sqlite DB
mage_query = """
SELECT
    *
FROM
    charactercreator_mage
"""
mage_result = lite_cursor.execute(mage_query).fetchall()

# Create the charactercreator_mage table in the pg DB
mage_create = """
CREATE TABLE IF NOT EXISTS charactercreator_mage (
  character_ptr_id INTEGER REFERENCES charactercreator_character (character_id)
  ,has_pet INTEGER NOT NULL
  ,mana INTEGER NOT NULL
);
"""
post_cursor.execute(mage_create)

# Put mage table into the pg DB
mage_insertion_query = """INSERT INTO charactercreator_mage (character_ptr_id, has_pet, mana)
VALUES %s
ON CONFLICT DO NOTHING
"""
execute_values(post_cursor, mage_insertion_query, mage_result)

# Change has_pet to boolean
petbool_query = """
ALTER TABLE charactercreator_mage
    ALTER COLUMN has_pet TYPE BOOLEAN
    USING
        has_pet::boolean
"""
post_cursor.execute(petbool_query)

#
## charactercreator_thief table
#

# Take the table, charactercreator_thief, out of the sqlite DB
thief_query = """
SELECT
    *
FROM
    charactercreator_thief
"""
thief_result = lite_cursor.execute(thief_query).fetchall()

# Create the charactercreator_thief table in the pg DB
thief_create = """
CREATE TABLE IF NOT EXISTS charactercreator_thief (
  character_ptr_id INTEGER REFERENCES charactercreator_character (character_id)
  ,is_sneaking INTEGER NOT NULL
  ,energy INTEGER NOT NULL
);
"""
post_cursor.execute(thief_create)

# Put thief table into the pg DB
thief_insertion_query = """INSERT INTO charactercreator_thief (character_ptr_id, is_sneaking, energy)
VALUES %s
ON CONFLICT DO NOTHING
"""
execute_values(post_cursor, thief_insertion_query, thief_result)

# Change is_sneaking to boolean
sneakbool_query = """
ALTER TABLE charactercreator_thief
    ALTER COLUMN is_sneaking TYPE BOOLEAN
    USING
        is_sneaking::boolean
"""
post_cursor.execute(sneakbool_query)

#
## charactercreator_cleric table
#

# Take the table, charactercreator_cleric, out of the sqlite DB
cleric_query = """
SELECT
    *
FROM
    charactercreator_cleric
"""
cleric_result = lite_cursor.execute(cleric_query).fetchall()

# Create the charactercreator_cleric table in the pg DB
cleric_create = """
CREATE TABLE IF NOT EXISTS charactercreator_cleric (
  character_ptr_id INTEGER REFERENCES charactercreator_character (character_id)
  ,using_shield INTEGER NOT NULL
  ,mana INTEGER NOT NULL
);
"""
post_cursor.execute(cleric_create)

# Put cleric table into the pg DB
cleric_insertion_query = """INSERT INTO charactercreator_cleric (character_ptr_id, using_shield, mana)
VALUES %s
ON CONFLICT DO NOTHING
"""
execute_values(post_cursor, cleric_insertion_query, cleric_result)

# Change using_shield to boolean
shieldbool_query = """
ALTER TABLE charactercreator_cleric
    ALTER COLUMN using_shield TYPE BOOLEAN
    USING
        using_shield::boolean
"""
post_cursor.execute(shieldbool_query)

#
## charactercreator_fighter table
#

# Take the table, charactercreator_fighter, out of the sqlite DB
fighter_query = """
SELECT
    *
FROM
    charactercreator_fighter
"""
fighter_result = lite_cursor.execute(fighter_query).fetchall()

# Create the charactercreator_fighter table in the pg DB
fighter_create = """
CREATE TABLE IF NOT EXISTS charactercreator_fighter (
  character_ptr_id INTEGER REFERENCES charactercreator_character (character_id)
  ,using_shield INTEGER NOT NULL
  ,rage INTEGER NOT NULL
);
"""
post_cursor.execute(fighter_create)

# Put fighter table into the pg DB
fighter_insertion_query = """INSERT INTO charactercreator_fighter (character_ptr_id, using_shield, rage)
VALUES %s
ON CONFLICT DO NOTHING
"""
execute_values(post_cursor, fighter_insertion_query, fighter_result)

# Change using_shield to boolean
shieldbool1_query = """
ALTER TABLE charactercreator_fighter
    ALTER COLUMN using_shield TYPE BOOLEAN
    USING
        using_shield::boolean
"""
post_cursor.execute(shieldbool1_query)

# #
# ## charactercreator_necromancer table
# #

# # Take the table, charactercreator_necromancer, out of the sqlite DB
# necromancer_query = """
# SELECT
#     *
# FROM
#     charactercreator_necromancer
# """
# necromancer_result = lite_cursor.execute(necromancer_query).fetchall()

# # Create the charactercreator_necromancer table in the pg DB
# necromancer_create = """
# CREATE TABLE IF NOT EXISTS charactercreator_necromancer (
#   mage_ptr_id INTEGER REFERENCES charactercreator_mage (character_ptr_id)
#   ,talisman_charged INTEGER NOT NULL
# );
# """
# post_cursor.execute(necromancer_create)

# # Put necromancer table into the pg DB
# necromancer_insertion_query = """INSERT INTO charactercreator_necromancer (mage_ptr_id, talisman_charged)
# VALUES %s
# ON CONFLICT DO NOTHING
# """
# execute_values(post_cursor, necromancer_insertion_query, necromancer_result)


# ACTUALLY SAVE THE TRANSACTIONS
post_connection.commit()