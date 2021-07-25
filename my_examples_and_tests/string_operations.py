l = []
vlan_base = 200
mac_base = '0000.A01B.1234'
intf_base = 'GigabitEthernet0/1'

for i in range(20):
    if i % 2 == 0:
        vlan = vlan_base
    else:
        vlan = vlan_base + i
    mac_parts = mac_base.split('.')
    mac_parts[-1] = "{:X}".format(int(mac_parts[-1], 16) + i)
    mac = ".".join(mac_parts)
    intf_index = intf_base.find('/')
    intf = intf_base[:intf_index + 1] + str(int(i % 3))
    l.append('{vlan:<10}{mac:<20}{interf:<25}'.format(vlan=str(vlan), interf=intf, mac=mac))

# for line in l:
#     print(line)

int_conf_template = ('interface {speed}Ethernet{unit}/{slot}/{number}\n'
                       ' no switchport\n'
                       ' ip address {ip} {mask}\n'
                       ' no shutdown\n')
print(int_conf_template)

intfs = [{'speed' : 'Fast', 'unit' : 0, 'slot' : 1, 'number' : 1, 'ip' : '10.0.1.1', 'mask' : '255.255.255.252'},
            {'speed' : 'Gigabit', 'unit' : 1, 'slot' : 1, 'number' : 2, 'ip' : '172.16.1.254', 'mask' : '255.255.255.0'}]

for intf in intfs:
    print(int_conf_template.format(speed=intf['speed'], unit=intf['unit'], slot=intf['slot'], number=intf['number'],
          ip=intf['ip'], mask=intf['mask']))

print("And now using f-strings!\n================================")
for intf in intfs:
    speed = intf['speed']
    unit = intf['unit']
    slot = intf['slot']
    number = intf['number']
    ip = intf['ip']
    mask = intf['mask']
    int_conf_new_template = (f'interface {speed}Ethernet{unit}/{slot}/{number}\n'
                             ' no switchport\n'
                             f' ip address {ip} {mask}\n'
                             ' no shutdown\n')
    print(int_conf_new_template)

print("Hello, world!")