import re

int_line = '  MTU 1500 bytes, BW 10000 Kbit, DLY 1000 usec,'
log2 = 'Oct  3 12:49:15.941: %SW_MATM-4-MACFLAP_NOTIF: Host f04d.a206.7fd6 in vlan 1 is flapping between port Gi0/5 and port Gi0/16'


m = re.search('MTU', int_line)
m1 = re.search('MU', int_line)
mbw = re.search('BW \d+', int_line)
mvm = re.search('Host (\S+) in vlan (\d+) is flapping between port (\S+) and port (\S+)', log2)

print(type(m), m, m.group(), m.groups(), m.groupdict())
print(m1)
print(mbw.group())
print(mvm.groups())



ip = '192.168.1.100'
ipa = '192a168b1c100'

mip = re.search('\d+.\d+.\d+.\d+', ip)
print(mip.group())
mipa = re.search('\d+.\d+.\d+.\d+', ipa)
print(mipa.group())

mip1 = re.search('\d+\.\d+\.\d+\.\d+', ip)
print(mip1.group())
mipa1 = re.search('\d+\.\d+\.\d+\.\d+', ipa)
print(mipa1)

mip2 = re.search('(\d+\.){3}\d+', ip)
print(mip2.group())
mipa2 = re.search('(\d+\.){3}\d+', ipa)
print(mipa2)

ip1 = 'ip address = 10.1.10.10/24'
ipa1 = 'fake ip address = 10x1x10x10'
mip3 = re.search('(\d{1,3}\.){3}\d{1,3}', ip1)
print(mip3.group())
mipa3 = re.search('(\d{1,3}\.){3}\d{1,3}', ipa1)
print(mipa3)

mail1 = 'Mail: user1.test@example.com, Name: Alex P.'
mm1 = re.search('\w+\.?\w+@\w+\.\w+', mail1)
print(mm1.group())
mm2 = re.search('(\w+\.)+\w+@(\w+\.)+\w+', mail1)
print(mm2.group())

mac1 = 'VLAN 1000: MAC 0001.abcd.1234 - interface Gi2/5'
mmac1 = re.search('(\w{4}\.){2}\w{4}', mac1)
print(mmac1.group())
print(mmac1.groups())
print(mmac1.group(0,1))

ip2 = 'ip address = 10.1.10.10/24'
ipa2 = 'fake ip address = 10x1x10x10'
mip4 = re.search('(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})', ip2)
print(mip4.group())
print(mip4.group(0,1,2,3,4))

# Error! Match object is not iterable!
# for m in mip4:
#     print(m)
print(mip4[0], mip4[1], mip4[2], mip4[3], mip4[4])

line = "FastEthernet0/1            10.0.12.1       YES manual up                    up"
ml = re.search(r'(?P<intf>\S+)\s+(?P<ip_addr>\S+)\s+\w+\s+\w+\s+(?P<admin_status>up|down)\s+(?P<line>up|down)', line)
print(ml.groups())
print(ml.group('intf'), ml.group('ip_addr'), ml.group('admin_status'), ml.group('line'))
print(ml.groupdict())


show_dhcp_snooping = ['MacAddress          IpAddress     Lease(sec)  Type           VLAN  Interface' ,
'------------------  ------------  ----------  -------------  ----  --------------------',
'00:09:BB:3D:D6:58   10.1.10.2     86250       dhcp-snooping   10    FastEthernet0/1',
'00:04:A3:3E:5B:69   10.1.5.2      63951       dhcp-snooping   5     FastEthernet0/10',
'00:05:B3:7E:9B:60   10.1.5.4      63253       dhcp-snooping   5     FastEthernet0/9',
'00:09:BC:3F:A6:50   10.1.10.6     76260       dhcp-snooping   10    FastEthernet0/3',
'Total number of bindings: 4']

regex = r'(?P<mac>([0-9A-F]{2}:){5}[0-9A-F]{2})\s+(?P<ip>(\d{1,3}\.){3}(\d{1,3}))\s+(?P<lease_time>\d+)\s+\S+\s+(?P<vlan>\d+)\s+(?P<intf>\S+)'
# regex1 = r'(?P<mac>([0-9A-F]{2}:){5}[0-9A-F]{2})'
# regex2 = r'(?P<mac>00:\S+)'

# Using groups without capturing values
regex_n = r'(?P<mac>(?:[0-9A-F]{2}:){5}[0-9A-F]{2})\s+(?P<ip>(?:\d{1,3}\.){3}\d{1,3})\s+(?P<lease_time>\d+)\s+\S+\s+(?P<vlan>\d+)\s+(?P<intf>\S+)'
for line in show_dhcp_snooping:
    mdhcp = re.search(regex_n, line)
    if mdhcp:
        print(mdhcp.groups())
        print(mdhcp.groupdict())

print(re.findall(regex_n, '\n'.join(show_dhcp_snooping)))


bgp = '''
   R9# sh ip bgp | be Network
      Network          Next Hop       Metric LocPrf Weight Path
   *  192.168.66.0/24  192.168.79.7                       0 500 500 500 500 i
   *>                  192.168.89.8                       0 800 700 i
   *  192.168.67.0/24  192.168.79.7         0             0 700 700 700 i
   *>                  192.168.89.8                       0 800 700 i
   *  192.168.88.0/24  192.168.79.7                       0 700 700 700 i
   *>                  192.168.89.8         0             0 800 800 i
   '''
regex_b = r'(?P<as>\d+) \1'
regex_b1 = r'(?P<as>\d+) \1 \1 \1'
for line in bgp.split('\n'):
    mbgp = re.search(regex_b1, line)
    if mbgp:
        print(mbgp.groupdict())

print(re.findall(regex_b, bgp))