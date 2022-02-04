import os
import sqlite3

DB_FILE = 'dhcp_snooping.db'
SCHEMA_FILE = 'dhcp_snooping_schema.sql'

def create_database(db_file, schema_file):
    if not os.path.exists(db_file):
        print('Creating database...')
        with sqlite3.connect(db_file) as conn, open(schema_file) as schema:
            conn.executescript(schema.read())
        print('Done!')
    else:
        print('The database exists')

if __name__ == '__main__':
    create_database(DB_FILE, SCHEMA_FILE)