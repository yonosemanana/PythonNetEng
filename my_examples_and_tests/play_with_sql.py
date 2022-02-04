import sqlite3

connection = sqlite3.Connection('testDB.db')
cursor = connection.cursor()

query1 = 'select * from sites order by sitecode'
res1 = cursor.execute(query1)
print(res1.fetchall())

print()
query3 = 'select * from sites'
res3 = cursor.execute(query3)
while True:
    line = res3.fetchone()
    if line:
        print(line)
    else:
        break

new_sites = [('il01', 'Shaumburg', 'Isaac', 1, 200),
             ('ca172', 'Vesta', 'Nathan', 2, 50)]
query2 = 'insert into sites values (?, ?, ?, ?, ?)'
try:
    for site in new_sites:
        res2 = cursor.execute(query2, site)
    connection.commit()
except sqlite3.IntegrityError as e:
    print(e)

query_del = 'delete from switch where hostname in ("SW6", "SW7", "SW8")'
connection.execute(query_del)

switches = connection.execute('select * from switch')
for sw in switches:
    print(sw)



new_switches = [('SW6', '01:02:0A:BB:CC:06', 'Cisco 3750', 'Stockholm'),
                ('SW7', '01:02:0A:BB:CC:07', 'Cisco 9300', 'Dublin'),
                ('SW8', '01:02:0A:BB:CC:08', 'Cisco 9200L', 'Newcastle')]
query_sw = 'insert into switch values (?, ?, ?, ?)'
connection.executemany(query_sw, new_switches)
connection.commit()

print()
switches = connection.execute('select * from switch')
for sw in switches:
    print(sw)


connection.close()







