# -*- coding: utf-8 -*-
"""
Задание 17.3

Создать функцию parse_sh_cdp_neighbors, которая обрабатывает
вывод команды show cdp neighbors.

Функция ожидает, как аргумент, вывод команды одной строкой (не имя файла).
Функция должна возвращать словарь, который описывает соединения между устройствами.

Например, если как аргумент был передан такой вывод:
R4>show cdp neighbors

Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID
R5           Fa 0/1          122           R S I           2811       Fa 0/1
R6           Fa 0/2          143           R S I           2811       Fa 0/0

Функция должна вернуть такой словарь:
{'R4': {'Fa 0/1': {'R5': 'Fa 0/1'},
        'Fa 0/2': {'R6': 'Fa 0/0'}}}

Интерфейсы должны быть записаны с пробелом. То есть, так Fa 0/0, а не так Fa0/0.


Проверить работу функции на содержимом файла sh_cdp_n_sw1.txt
"""

import re

def parse_sh_cdp_neighbors(sh_cdp_output):
    """
    Input: a string with 'show cdp neighbors' output
    Input example:
        R4>show cdp neighbors

    Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID
    R5           Fa 0/1          122           R S I           2811       Fa 0/1
    R6           Fa 0/2          143           R S I           2811       Fa 0/0

    Output: a dictionary with topology.
    Output example:
    {'R4': {'Fa 0/1': {'R5': 'Fa 0/1'},
        'Fa 0/2': {'R6': 'Fa 0/0'}}}
    """
    topology = {}
    hostname = re.search(r'(?:^|\n)(\S+)[>#]', sh_cdp_output).group(1)
    topology[hostname] = {}

    regex = r'(?P<neighbor>\S+) +(?P<local_intf>\S+ \S+) +\d+ +[\S ]+ (?P<neighbor_intf>\S+ \S+)\n'
    match = re.finditer(regex, sh_cdp_output)
    for m in match:
        topology[hostname][m.group('local_intf')] = {m.group('neighbor'): m.group('neighbor_intf')}

    return topology

if __name__ == '__main__':
    with open('sh_cdp_n_sw1.txt') as f:
        print(parse_sh_cdp_neighbors(f.read()))