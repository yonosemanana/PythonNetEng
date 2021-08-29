import subprocess
import os
import ipaddress
import tabulate
import pprint

from task_12_1 import ping_ip_addresses
from task_12_2 import convert_ranges_to_ip_list

def print_ip_table(reachable, unreachable):
    """
    Input: two lists (of strings) of pingable IPs and not_pingable IPs
    Output: the function doesn't return a result, but print on STDOUT a table with pingable and not pingable IPs:
    Reachable    Unreachable
    -----------  -------------
    10.1.1.1     10.1.1.7
    10.1.1.2     10.1.1.8
                 10.1.1.9
    """
    table_columns = {'Reachable' : reachable, 'Unreachable' : unreachable}
    print(tabulate.tabulate(table_columns, headers='keys', ))

if __name__ == '__main__':
    ip_addresses = ['8.8.8.8', '10.1.1.1', '10.a.1.2', '4.2.2.2']
    test_ip_list = [
        '10.1.1.1',
        '10.1.2.1-10.1.2.10',
        '10.1.3.1-10'
    ]
    #print(convert_ranges_to_ip_list((ip_addresses + test_ip_list)))
    #print(ping_ip_addresses(convert_ranges_to_ip_list(ip_addresses + test_ip_list)))
    print_ip_table(*ping_ip_addresses(convert_ranges_to_ip_list(ip_addresses + test_ip_list)))

# res = subprocess.run('pwd')
# print(type(res), res)
# print(res.stdout)
# print(res.returncode)
#
# print()
# res2 = subprocess.run('pwd', stdout=subprocess.PIPE)
# print(res2.stdout)
# res2_1 = subprocess.run('pwd', stdout=subprocess.PIPE, encoding='Utf-8')
# print(res2_1.stdout)
#
# ping_res = subprocess.run(['ping', '-c', '3', 'google.com'], stdout=subprocess.PIPE)
# print(ping_res.stdout.decode('utf-8'))
#
# ping_res2 = subprocess.run(['ping', '-c', '3', 'google1.com'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# print(ping_res2.stdout.decode('utf-8'))
# print(ping_res2.stderr.decode('utf-8'))
# #
# # try:
# #     print(ping_res2.stdout.decode('utf-8'))
# # except AttributeError:
# #     print(ping_res2.stderr.decode('utf-8'))
# #     print(ping_res2.returncode)
#
#
# #print(dir(os))
# pprint.pprint(os.getenv('PATH'))
# pprint.pprint(os.getcwd())
# pprint.pprint(sorted(os.listdir()))
# pprint.pprint(os.mkdir('testdir'))
# pprint.pprint(sorted(os.listdir()))
# pprint.pprint(os.rmdir('testdir'))
# pprint.pprint(sorted(os.listdir()))

