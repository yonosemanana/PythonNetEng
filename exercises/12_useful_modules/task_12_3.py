from tabulate import tabulate
from task_12_1 import ping_ip_addresses
from task_12_2 import convert_ranges_to_ip_list

# -*- coding: utf-8 -*-
"""
Задание 12.3

Создать функцию print_ip_table, которая отображает таблицу доступных
и недоступных IP-адресов.

Функция ожидает как аргументы два списка:
* список доступных IP-адресов
* список недоступных IP-адресов

Результат работы функции - вывод на стандартный поток вывода таблицы вида:

Reachable    Unreachable
-----------  -------------
10.1.1.1     10.1.1.7
10.1.1.2     10.1.1.8
             10.1.1.9

"""

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
    table_rows = [('Reachable', 'Unreachable')]
    if len(reachable) < len(unreachable):
        reachable = reachable + ['' for i in range((len(unreachable) - len(reachable)))]
    else:
        unreachable = unreachable + ['' for i in range ((len(reachable) - len(unreachable)))]
    #print(reachable, unreachable)
    table_rows = table_rows + list(map(lambda x, y: (x, y), reachable, unreachable))

    print(tabulate(table_rows, headers='firstrow', ))

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