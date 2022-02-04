import sqlite3
import os
import yaml
import re
from datetime import datetime, timedelta
from tabulate import tabulate

def create_db(db_file, schema_file):
    if not os.path.exists(db_file):
        print('Creating database...')
        with sqlite3.connect(db_file) as conn, open(schema_file) as schema:
            conn.executescript(schema.read())
        print('Done!')
    else:
        print('The database exists')

def add_data_switches(db_file, switches_files):
    if not os.path.exists(db_file):
        print("The database doesn't exist. Create the database before adding data!")
    else:
        for switches_file in switches_files:
            with sqlite3.connect(db_file) as conn, open(switches_file) as sw_file:
                switches = yaml.safe_load(sw_file)
                # print(switches)
                query = 'insert into switches (hostname, location) values (?, ?)'
                print('Adding data to table "switches"...')
                for sw in switches['switches']:
                    try:
                        data = (sw, switches['switches'][sw])
                        conn.execute(query, data)
                    except sqlite3.IntegrityError as e:
                        print(f'Error "{e}" was generated when adding data: {data}')

def add_data(db_file, dhcp_files):
    if not os.path.exists(db_file):
        print("The database doesn't exist. Create the database before adding data!")
    else:
        with sqlite3.connect(db_file) as conn:
            print('Updating "active" field...')
            query_upd = 'update dhcp set active = 0'
            conn.execute(query_upd)

            print('Deleting entries older than 7 days...')
            week_ago = datetime.today().replace(microsecond=0) - timedelta(days=7)
            query_del = f'delete from dhcp where last_active < "{week_ago}"'
            conn.execute(query_del)

            query = 'insert or replace into dhcp (mac, ip, vlan, interface, switch, active, last_active) values (?, ?, ?, ?, ?, 1, datetime("now"))'
            print('Adding data to table "dhcp"...')

            for dhcp_file in dhcp_files:
                sw_name = re.search('^(\S+)_dhcp', os.path.split(dhcp_file)[1]).group(1)
                with open(dhcp_file) as f:
                    bindings = re.findall('(\S+)\s+(\S+)\s+\d+\s+\S+\s+(\d+)\s+(\S+)', f.read())
                    for b in bindings:
                        row = b + (sw_name,)
                        # print(row)
                        try:
                            conn.execute(query, row)
                        except sqlite3.IntegrityError as e:
                            print(f'Error "{e}" was generated when adding data: {row}')

def get_data(db_file, key, value):
    query = f'select * from dhcp where {key}="{value}" ' + 'and active = {}'
    msg = f'Information about device with {key} = {value}'
    # print(query, msg)

    with sqlite3.connect(db_file) as conn:
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

def get_all_data(db_file):
    query = 'select * from dhcp where active = {}'
    msg = 'All entries in DHCP snooping table:'
    # print(query, msg)

    with sqlite3.connect(db_file) as conn:
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