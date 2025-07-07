#!/usr/bin/env python3
"""
adhoctests/experiments/db/dbfetcher_adhoc.py

  The fetching after a cursor.execute(SELECT) can be done in 3 ways, they are:
    1 -> rows = cursor.fetchall()  # fetch all rows found
    2 -> rows = cursor.fetchone()  # fetch one from the rows found
    3 -> rows = cursor.fetchmany(n)  # fetch the 'n' first rows found
      where n is the amount of rows to fetch

"""
# import mysql.connector
import settings as sett


def adhoctest1():
  """
  connection = mysql.connector.connect(host='localhost', database='test_db', user='user', password='password')

  """
  # Establish connection
  connection = sett.get_sqlite_connection()
  # Create cursor
  cursor = connection.cursor()
  # Execute query
  cursor.execute("SELECT * FROM your_table")
  # Fetch all rows
  rows = cursor.fetchall()
  # Process rows
  for row in rows:
      print(row)
  # Close cursor and connection
  cursor.close()
  connection.close()


def adhoctest2():
  pass


def process():
  pass


if __name__ == '__main__':
  """
  adhoctest1()
  adhoctest2()
  """
  process()
