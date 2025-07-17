# Initialize the database
db = SQLiteDB('example.db')

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
db.execute('INSERT INTO users (name, email, age) VALUES (?, ?, ?)', 
           ('Alice', 'alice@example.com', 30))

# Insert multiple records
users = [
    ('Bob', 'bob@example.com', 25),
    ('Charlie', 'charlie@example.com', 35)
]
db.executemany('INSERT INTO users (name, email, age) VALUES (?, ?, ?)', users)

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