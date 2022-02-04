import sqlite3
import re
import os

db_file = 'dhcpDB.db'
data_file = 'dhcp_snooping.txt'
schema_file = 'dhcp_snooping_schema.sql'

if not os.path.exists(db_file):
    print('Creating database...')
    con = sqlite3.connect(db_file)
    print('Creating schema...')
    with open(schema_file) as f:
        con.executescript(f.read())
        con.commit()

    tables = con.execute('select * from sqlite_master where type="table"')
    for t in tables:
        print(t)
    con.close()
    print('Done')




print('Inserting DHCP Snooping data...')
regex = r'(?P<mac>\S+)\s+(?P<ip>[\d\.]+)\s+\d+\s+\S+\s+(?P<vlan>\d+)\s+(?P<interface>\S+)'
with open(data_file) as f:
    bindings = re.findall(regex, f.read())

with sqlite3.connect(db_file) as con:
    try:
        query = 'insert into dhcp (mac, ip, vlan, interface) values (?, ?, ?, ?)'
        con.executemany(query, bindings)
    except sqlite3.IntegrityError as e:
        print(e)

print('Requesting data...')
sql_bindings = con.execute('select * from dhcp')
for b in sql_bindings:
    print(b)



