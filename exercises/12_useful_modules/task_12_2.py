import ipaddress
from pprint import pprint

# -*- coding: utf-8 -*-
"""
Задание 12.2


Функция ping_ip_addresses из задания 12.1 принимает только список адресов,
но было бы удобно иметь возможность указывать адреса с помощью диапазона,
например, 192.168.100.1-10.

В этом задании необходимо создать функцию convert_ranges_to_ip_list,
которая конвертирует список IP-адресов в разных форматах в список,
где каждый IP-адрес указан отдельно.

Функция ожидает как аргумент список, в котором содержатся IP-адреса
и/или диапазоны IP-адресов.

Элементы списка могут быть в формате:
* 10.1.1.1
* 10.1.1.1-10.1.1.10
* 10.1.1.1-10

Если адрес указан в виде диапазона, надо развернуть диапазон в отдельные
адреса, включая последний адрес диапазона.
Для упрощения задачи, можно считать, что в диапазоне всегда меняется только
последний октет адреса.

Функция возвращает список IP-адресов.

Например, если передать функции convert_ranges_to_ip_list такой список:
['8.8.4.4', '1.1.1.1-3', '172.21.41.128-172.21.41.132']

Функция должна вернуть такой список:
['8.8.4.4', '1.1.1.1', '1.1.1.2', '1.1.1.3', '172.21.41.128',
 '172.21.41.129', '172.21.41.130', '172.21.41.131', '172.21.41.132']

"""

def convert_ranges_to_ip_list(ip_addresses):
    """
    The function expands IP ranges and converts list of IP addresses and ranges to list of individual IP addresses.
    Input: a list of IP addresses and IP ranges in format:
        * 10.1.1.1
        * 10.1.1.1-10.1.1.10
        * 10.1.1.1-10
    Output: a list of individual IP addresses (as strings)
    """
    result = []
    for ip in ip_addresses:
        if '-' in ip:
            dash = ip.index('-')
            start = ip[:dash]
            end = ip[dash + 1:]

            if '.' not in end:
                end = start[:start.rfind('.') + 1] + end
            next_ip = start
            while next_ip != str(ipaddress.ip_address(end) + 1):
                result.append(next_ip)
                current_ip = ipaddress.ip_address(next_ip)
                next_ip = str(current_ip + 1)
        else:
            result.append(ip)

    return result

if __name__ == '__main__':
    test_ip_list = [
        '10.1.1.1',
        '10.1.2.1-10.1.2.10',
        '10.1.3.1-10'
    ]
    ip_list = convert_ranges_to_ip_list(test_ip_list)
    pprint(ip_list)