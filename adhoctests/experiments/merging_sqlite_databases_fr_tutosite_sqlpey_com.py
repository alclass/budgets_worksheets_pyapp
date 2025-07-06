"""
https://sqlpey.com/question/merging-sqlite-databases/
"""

import sqlite3
import os

def merge_databases(db1, db2):
    con3 = sqlite3.connect(db1)

    con3.execute("ATTACH '" + db2 +  "' as dba")

    con3.execute("BEGIN")
    for row in con3.execute("SELECT * FROM dba.sqlite_master WHERE type="table""):
        combine = "INSERT OR IGNORE INTO "+ row[1] + " SELECT * FROM dba." + row[1]
        print(combine)
        con3.execute(combine)
    con3.commit()
    con3.execute("detach database dba")

def read_files(directory):
    file_list = os.listdir(directory)
    databases = []

    for file in file_list:
        if file.endswith('.db'):
            databases.append(os.path.join(directory, file))

    if len(databases) == 0:
        print("No databases found in the directory")
    elif len(databases) == 1:
        print("Only one database found, nothing to merge")
    else:
        for i in range(len(databases)-1):
            merge_databases(databases[0], databases[i+1])

read_files('/path/to/database/files')
