import sys
import sqlite3

DB_FILE = 'dhcp_snooping.db'

def get_data(key=None, value=None):

    query = 'select * from dhcp'
    query_k = f'select * from dhcp where {key}="{value}"'
    with sqlite3.connect(DB_FILE) as conn:
        if not key:
            data = conn.execute(query)
            print('All entries in DHCP snooping table:')
        else:
            data = conn.execute(query_k)
            print(f'Information about device with {key} = {value}')
        for row in data:
            print(row)

def parse_args(*args):
    keys = ['mac', 'ip', 'vlan', 'interface', 'switch']
    if len(args) == 0:
        get_data()
    elif len(args) == 2:
        if args[0] not in keys:
            print('This parameter is not supported!')
        else:
            get_data(*args)
    else:
        print('Please, enter 0 or 2 arguments!')

if __name__ == '__main__':
    parse_args(*sys.argv[1:])