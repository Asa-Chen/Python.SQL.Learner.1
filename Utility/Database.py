import sqlite3
import datetime

connection = sqlite3.Connection('data.db')

CREATE_TABLE = """CREATE TABLE IF NOT EXISTS 
    Journal (date, entry, notes)"""
INSERT_INTO_TABLE = "INSERT INTO Journal VALUES (?, ?, ?)"
SELECT_ALL_BY_DATA = "SELECT * FROM Journal ORDER BY date"
SELECT_A_DATE = "SELECT * FROM Journal WHERE date=?"
DELETE_BY_DATE = "DELETE FROM Journal WHERE date=?"
UPDATE_BY_DATE = "UPDATE Journal SET entry=?, notes=? WHERE date=?"

def create_table():
    with connection:
        connection.execute(CREATE_TABLE)

def select_all():
    with connection:
        return connection.execute(SELECT_ALL_BY_DATA).fetchall() #list of tuples

def insert(date, entry, notes):
    with connection:
        connection.execute(INSERT_INTO_TABLE, (date, entry, notes))
        connection.commit()

def delete(date):
    with connection:
        connection.execute(DELETE_BY_DATE, (date,))
        connection.commit()

def update(date, entry, notes):
    with connection:
        connection.execute(UPDATE_BY_DATE, (entry, notes, date))

def check_presense(date):
    with connection:
        return bool(connection.execute(SELECT_A_DATE, (date,)).fetchall())
