"""
This wrapper provides a clean, Pythonic interface to SQLite while handling
  all the low-level details of connection management and error handling.

"""
import lib.db.sqlite.db_sqlite_manager as sqlm  # sqlm.SQLiteDB
import settings as sett
# Initialize the database


def adhoctest1():
  db = sqlm.SqliteHandler('example.db')

  # Create a table
  db.execute('''
      CREATE TABLE IF NOT EXISTS users (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL,
          email TEXT UNIQUE NOT NULL,
          age INTEGER
      )
  ''')

  # Insert data
  db.execute('INSERT OR IGNORE INTO users (name, email, age) VALUES (?, ?, ?)',
             ('Alice', 'alice@example.com', 30))

  # Insert multiple records
  users = [
      ('Bob', 'bob@example.com', 25),
      ('Charlie', 'charlie@example.com', 35)
  ]
  db.executemany('INSERT OR IGNORE INTO users (name, email, age) VALUES (?, ?, ?)', users)

  # Query data
  all_users = db.fetch_all('SELECT * FROM users')
  print("All users:", all_users)

  # Get a single user
  user = db.fetch_one('SELECT * FROM users WHERE name = ?', ('Alice',))
  print("Single user:", user)

  # Get users as dictionaries
  users_dict = db.fetch_as_dict('SELECT * FROM users WHERE age > ?', (25,))
  print("Users over 25:", users_dict)

  # Update data
  db.execute('UPDATE users SET age = ? WHERE name = ?', (31, 'Alice'))

  # Check if table exists
  print("Table exists:", db.table_exists('users'))

  # Get table columns
  print("Table columns:", db.get_table_columns('users'))

  # Close the connection
  db.close()


def adhoctest2():
  """
  """
  sqlitefilepath = sett.get_exchange_rate_sqlite_filepath()
  db = sqlm.SqliteHandler(sqlitefilepath)
  tablename = 'bls_us_indices'
  inidate = '2024-06-15'
  tuplevalues = (inidate, )
  sql = f"""SELECT * FROM {tablename}
  WHERE refmonthdate > ? ;"""
  cursor = db.execute(sql, tuplevalues)
  for i, row in enumerate(cursor.fetchall()):
    print(i+1, row)


def adhoctest3():
  sqlitefilepath = sett.get_exchange_rate_sqlite_filepath()
  db = sqlm.SqliteHandler(sqlitefilepath)
  tablename = 'currencies_exchangerates'
  inidate = '2024-06-15'
  tuplevalues = (inidate, )
  sql = f"""SELECT * FROM {tablename}
  WHERE refdate > ? ;"""
  cursor = db.execute(sql, tuplevalues)
  for i, row in enumerate(cursor.fetchall()):
    print(i+1, row)


def process():
  """

  """
  pass


if __name__ == "__main__":
  """
  process()
  """
  process()
  adhoctest3()
