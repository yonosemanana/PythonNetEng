import sys
import sqlite3
from tabulate import tabulate

DB_FILE = 'dhcp_snooping.db'

def get_data(key=None, value=None):
    if not key:
        query = 'select * from dhcp where active = {}'
        msg = 'All entries in DHCP snooping table:'
    else:
        query = f'select * from dhcp where {key}="{value}" ' + 'and active = {}'
        msg = f'Information about device with {key} = {value}'
    # print(query, msg)

    with sqlite3.connect(DB_FILE) as conn:
        print(msg)
        active = 1
        data = [row for row in conn.execute(query.format(active))]
        if len(data) > 0:
            print('Active bindings:')
            print(tabulate(data))

        active = 0
        data = [row for row in conn.execute(query.format(active))]
        if len(data) > 0:
            print('Inactive bindings:')
            print(tabulate(data))


def parse_args(*args):
    keys = ['mac', 'ip', 'vlan', 'interface', 'switch', 'active']
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