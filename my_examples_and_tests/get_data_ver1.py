import sqlite3
import sys

db_file = 'dhcpDB.db'

key, value = sys.argv[1:]
keys = ['mac', 'ip', 'vlan', 'interface']
# print(key, value)
# print(type(key), type(value))

conn = sqlite3.connect(db_file)
query = f'select * from dhcp where {key}="{value}"'
conn.row_factory = sqlite3.Row
res = conn.execute(query)

print('\n' + '=' * 40)
for row in res:
    print('-' * 40)
    for k in keys:
        if k != key:
            print('{:12} {}'.format(k, row[k]))
