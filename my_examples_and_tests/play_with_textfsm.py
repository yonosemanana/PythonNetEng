import textfsm
from textfsm import clitable
from tabulate import tabulate

def parse_output(template_fname, output_fname):
    """
    """
    with open(template_fname) as template, open(output_fname) as command_output:
        fsm = textfsm.TextFSM(template)
        res = fsm.ParseText(command_output.read())

        return tabulate(res, headers=fsm.header)

traceroute = '''
alper@Lighthouse:~/tmp$ traceroute 8.8.8.8 -n
traceroute to 8.8.8.8 (8.8.8.8), 30 hops max, 60 byte packets
 1  * * *
 2  10.5.5.25  189.578 ms  190.802 ms  190.858 ms
 3  * * *
 4  192.168.234.1  197.092 ms  200.783 ms  200.827 ms
 5  * * *
 6  192.168.115.249  205.051 ms  80.311 ms  99.937 ms
 7  195.149.232.62  109.146 ms  98.945 ms  95.879 ms
 8  142.250.37.193  95.177 ms  104.199 ms 108.170.250.209  52.659 ms
 9  216.239.41.165  77.505 ms 209.85.253.225  114.307 ms 172.253.68.29  114.163 ms
10  8.8.8.8  113.960 ms  110.768 ms  108.362 ms
'''

traceroute2 = '''
r2#traceroute 90.0.0.9 source 33.0.0.2
traceroute 90.0.0.9 source 33.0.0.2
Type escape sequence to abort.
Tracing the route to 90.0.0.9
VRF info: (vrf in name/id, vrf out name/id)
  1 10.0.12.1 1 msec 0 msec 0 msec
  2 15.0.0.5  0 msec 5 msec 4 msec
  3 57.0.0.7  4 msec 1 msec 4 msec
  4 79.0.0.9  4 msec *  1 msec
'''

with open('textfsm_templates/traceroute.template') as template:
    fsm = textfsm.TextFSM(template)
    res = fsm.ParseText(traceroute)
    print(fsm.header)
    print(res)
    fsm2 = textfsm.TextFSM(template)
    res2 = fsm2.ParseText(traceroute2)
    print(fsm2.header)
    print(res2)

# res = parse_output('textfsm_templates/traceroute.template', 'traceroute_output.txt')
# print(res)
# print()
#
# res = parse_output('textfsm_templates/show_clock.template', 'show_clock_output.txt')
# print(res)
# print()
#
# res = parse_output('textfsm_templates/show_ip_int_br.template', 'show_ip_int_br_output.txt')
# print(res)
# print()
#
# res = parse_output('textfsm_templates/show_cdp_neighbor.template', 'show_cdp_neighbor_output.txt')
# print(res)
# print()
#
# res = parse_output('textfsm_templates/show_ip_route_ospf.template', 'show_ip_route_ospf_output.txt')
# print(res)
# print()
#
#


myclitable = clitable.CliTable('textfsm_index', 'textfsm_templates')

commands = ['show clock', 'show ip int br', 'show cdp neighb de', 'show ip ro osp']
output_files = ['show_clock_output.txt', 'show_ip_int_br_output.txt', 'show_cdp_neighbor_output.txt', 'show_ip_route_ospf_output.txt']

for command, output_file in zip(commands, output_files):
    attributes = {'Command': command, 'Vendor': 'Cisco'}
    with open(output_file) as f:
        myclitable.ParseCmd(f.read(), attributes)
        print(myclitable)
        print(myclitable.FormattedTable(width=200))

    print(list(myclitable.header))
    for row in myclitable:
        print(list(row))