import sqlite3
import sys

db_file = 'dhcpDB.db'

key, value = sys.argv[1:]
query_dict = {'mac': 'select * from dhcp where mac = ?',
                'ip': 'select * from dhcp where ip = ?',
                'vlan': 'select * from dhcp where vlan = ?',
                'interface': 'select * from dhcp where interface = ?',
              }

keys = query_dict.keys()
# print(key, value)
# print(type(key), type(value))

if not key in keys:
    print(f'There is no key {key} in the database!')
else:
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    res = conn.execute(query_dict[key], (value,))

print('\n' + '=' * 40)
for row in res:
    print('-' * 40)
    for k in keys:
        if k != key:
            print('{:12} {}'.format(k, row[k]))
