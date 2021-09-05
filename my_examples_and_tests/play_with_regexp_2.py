import re
from pprint import pprint

show_cdp_neighbors = """SW1#show cdp neighbors detail
-------------------------
Device ID: SW2
Entry address(es):
  IP address: 10.1.1.2
Platform: cisco WS-C2960-8TC-L,  Capabilities: Switch IGMP
Interface: GigabitEthernet1/0/16,  Port ID (outgoing port): GigabitEthernet0/1
Holdtime : 164 sec

Version :
Cisco IOS Software, C2960 Software (C2960-LANBASEK9-M), Version 12.2(55)SE9, RELEASE SOFTWARE (fc1)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2014 by Cisco Systems, Inc.
Compiled Mon 03-Mar-14 22:53 by prod_rel_team

advertisement version: 2
VTP Management Domain: ''
Native VLAN: 1
Duplex: full
Management address(es):
  IP address: 10.1.1.2"""

neighbors = {}
regex_name = r'Device ID: (?P<name>\S+)'
regex_platform = r'Platform: (?P<platform>.*),.*'
regex_ios = r'Cisco IOS Software, (?P<ios>.*), RELEASE SOFTWARE.*'
regex_ip = r'IP address: (?P<ip>\S+)'

for line in show_cdp_neighbors.split('\n'):
    match = re.search(regex_name, line)
    if match:
        name = match.group('name')
        neighbors[name] = {}
    match = re.search(regex_platform, line)
    if match:
        neighbors[name]['platform'] = match.group('platform')
    match = re.search(regex_ios, line)
    if match:
        neighbors[name]['ios'] = match.group('ios')
    match = re.search(regex_ip, line)
    if match:
        neighbors[name]['ip'] = match.group('ip')

pprint(neighbors)

neighbors1 = {}
match = re.search(regex_name, show_cdp_neighbors)
if match:
    name = match.group('name')
    neighbors1[name] = {}
match = re.search(regex_platform, show_cdp_neighbors)
if match:
    neighbors1[name]['platform'] = match.group('platform')
match = re.search(regex_ios, show_cdp_neighbors)
if match:
    neighbors1[name]['ios'] = match.group('ios')
match = re.search(regex_ip, show_cdp_neighbors)
if match:
    neighbors1[name]['ip'] = match.group('ip')

pprint(neighbors1)


devices = {}
regex_all = (r'Device ID: (?P<name>\S+)|'
             r'Platform: (?P<platform>.*),.*|'
             r'Cisco IOS Software, (?P<ios>.*), RELEASE SOFTWARE.*|'
             r'IP address: (?P<ip>\S+).*')
with open('../examples/15_module_re/sh_cdp_neighbors_sw1.txt') as f:
    # This is wrong code!
    #devices = [m.groupdict() for m in re.finditer(regex_all, f.read())]
    #devices = re.findall(regex_all, f.read())
    #pprint(devices)
    for line in f:
        match = re.search(regex_all, line)
        if match:
            if match.lastgroup == 'name':
                name = match.group('name')
                devices[name] = {}
            else:
                devices[name][match.lastgroup] = match.group(match.lastgroup)

pprint(devices)



devices2 = {}
regex_all2 = (r'Device ID: (?P<name>\S+)|'
             r'Platform: (?P<platform>.*),.*|'
             r'Cisco IOS Software, (?P<ios>.*), RELEASE SOFTWARE.*|'
             r'Entry address\(es\):\s+IP address: (?P<ip>\S+).*')
with open('../examples/15_module_re/sh_cdp_neighbors_sw1.txt') as f:
    for match in re.finditer(regex_all2, f.read()):
            if match.lastgroup == 'name':
                name = match.group('name')
                devices2[name] = {}
            else:
                devices2[name][match.lastgroup] = match.group(match.lastgroup)

pprint(devices2)

# By default dot (.) in regular expressions doesn't include \n, i.e. new line symbol!
# But re.DOTALL flag tells re.search() and other functions of re module to include \n in dot (.) expression.
# And that behaviour makes sense for me, because by default regular expressions work with one line, than with the next line, etc.
regex_all3 = (r'Device ID: (?P<name>\S+).*?'
              r'Entry address\(es\):\s+IP address: (?P<ip>\S+).*?'
              r'Platform: (?P<platform>.*?),.*?'
              r'Cisco IOS Software, (?P<ios>.*?), RELEASE SOFTWARE.*?'
              )
with open('../examples/15_module_re/sh_cdp_neighbors_sw1.txt') as f:
    devices3 = re.findall(regex_all3, f.read(), re.DOTALL)

pprint(devices3)

ospf_route = 'O     10.0.24.0/24 [110/41] via 10.0.13.3, 3d18h, FastEthernet0/0'
regex_o = r'[ \[\],]'
regex_o1 = r'[ \[\],]+'
regex_o2 = r'(via[ \[\],])'
regex_o3 = r'(?:[via \[\],]+)'
regex_o4 = r'(?:via|[ \[\],])+'
pprint(ospf_route.split())
pprint(re.split(regex_o, ospf_route))
pprint(re.split(regex_o1, ospf_route))
pprint(re.split(regex_o2, ospf_route))
pprint(re.split(regex_o3, ospf_route))
pprint(re.split(regex_o4, ospf_route))

regex_os = r'[\[\],]'
regex_os2 = r'via|[\[\],]'
pprint(re.sub(regex_os, ' ', ospf_route))
pprint(re.sub(regex_os2, ' ', ospf_route))