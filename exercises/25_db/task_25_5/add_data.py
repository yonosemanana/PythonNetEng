import sqlite3
import os
import yaml
import re

DB_FILE = 'dhcp_snooping.db'
SWITCHES_FILE = 'switches.yml'
DHCP_SNOOPING_FILES = ['sw1_dhcp_snooping.txt', 'sw2_dhcp_snooping.txt', 'sw3_dhcp_snooping.txt']

def add_data_switches(db_file, switches_file):
    if not os.path.exists(DB_FILE):
        print("The database doesn't exist. Create the database before adding data!")
    else:
        with sqlite3.connect(DB_FILE) as conn, open(switches_file) as sw_file:
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

def add_data_dhcp_snooping(db_file, dhcp_snooping_files):
    if not os.path.exists(DB_FILE):
        print("The database doesn't exist. Create the database before adding data!")
    else:
        with sqlite3.connect(DB_FILE) as conn:
            print('Updating "active" field...')
            query_upd = 'update dhcp set active = 0'
            conn.execute(query_upd)

            query = 'insert or replace into dhcp (mac, ip, vlan, interface, switch, active, last_active) values (?, ?, ?, ?, ?, 1, datetime("now"))'
            print('Adding data to table "dhcp"...')
            for dhcp_file in dhcp_snooping_files:
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

if __name__ == '__main__':
    add_data_switches(DB_FILE, SWITCHES_FILE)
    add_data_dhcp_snooping(DB_FILE, DHCP_SNOOPING_FILES)

    new_data_dir = 'new_data/'
    new_dhcp_snooping_files = [new_data_dir + dhcp_file for dhcp_file in DHCP_SNOOPING_FILES]
    add_data_dhcp_snooping(DB_FILE, new_dhcp_snooping_files)
