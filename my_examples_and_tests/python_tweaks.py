import string

table = [['100', 'a1b2.ac10.7000', 'DYNAMIC', 'Gi0/1'],
 ['200', 'a0d4.cb20.7000', 'DYNAMIC', 'Gi0/2'],
 ['300', 'acb4.cd30.7000', 'DYNAMIC', 'Gi0/3'],
 ['100', 'a2bb.ec40.7000', 'DYNAMIC', 'Gi0/4'],
 ['500', 'aa4b.c550.7000', 'DYNAMIC', 'Gi0/5'],
 ['200', 'a1bb.1c60.7000', 'DYNAMIC', 'Gi0/6'],
 ['300', 'aa0b.cc70.7000', 'DYNAMIC', 'Gi0/7']]

# for line in table:
#  vlan, mac, _, intf = line
#  print(f'{vlan:10}{mac:15}{intf:>8}')

print('\n' + '=' * 30)
for vlan, mac, _, intf in table:
 print(f'{vlan:10}{mac:15}{intf:>8}')


london_co = {'r1': {'hostname': 'london_r1',
  'location': '21 New Globe Walk',
  'vendor': 'Cisco',
  'model': '4451',
  'IOS': '15.4',
  'IP': '10.255.0.1'},
 'r2': {'hostname': 'london_r2',
  'location': '21 New Globe Walk',
  'vendor': 'Cisco',
  'model': '4451',
  'IOS': '15.4',
  'IP': '10.255.0.2'},
 'sw1': {'hostname': 'london_sw1',
  'location': '21 New Globe Walk',
  'vendor': 'Cisco',
  'model': '3850',
  'IOS': '3.6.XE',
  'IP': '10.255.0.101'}}

print('\n' + '-' * 30)
l = []
# for device in london_co.keys():
#  l.append(london_co[device]['IOS'])
# print(l)

l = [london_co[device]['IOS'] for device in london_co]
print(l)

squares = {n : n**2 for n in range(0, 10)}
print(squares)

alphabet = [a for a in string.ascii_letters if a.islower()]
print(alphabet)

vlans = [vlan for line in table for vlan in line if vlan.isnumeric()]
print(vlans)

# new_london_co_test = {device : london_co[device] for device in london_co}
# print(new_london_co_test)

# new_london_co = {device : {key.lower() : value for key, value in london_co[device].items()} for device in london_co}
# print(new_london_co)

new_london_co2 = {device : {key.lower() : london_co[device][key] for key in london_co[device]} for device in london_co}
print(new_london_co2)

numbers = [num for num in range(10, 21)]
vlans = ['vlan' for i in range(10, 21)]
z = zip(vlans, numbers)
print(z)

for vlan, number in zip(vlans, numbers):
 print(f'{vlan} {number}')