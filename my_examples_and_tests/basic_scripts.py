#!/usr/bin/env python3

from sys import argv

access_template = ['switchport mode access',
                   'switchport access vlan {}',
                   'switchport nonegotiate',
                   'spanning-tree portfast',
                   'spanning-tree bpduguard enable']

print('\n'.join(access_template).format(100))

intf = argv[1]
vlan = argv[2]

print('\n' + '-' * 30)
print('interface {}\n '.format(intf) + '\n '.join(access_template).format(vlan))

print(argv)
print('The script file name: ' + argv[0])



intf2 = input("Enter interface name: ")
vlan2 = input("Enter vlan number: ")

print()
print('\n' + '-' * 30)
print('interface {}\n '.format(intf2) + '\n '.join(access_template).format(vlan2))