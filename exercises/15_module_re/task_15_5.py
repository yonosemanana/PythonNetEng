import re
# -*- coding: utf-8 -*-
"""
Задание 15.5

Создать функцию generate_description_from_cdp, которая ожидает как аргумент
имя файла, в котором находится вывод команды show cdp neighbors.

Функция должна обрабатывать вывод команды show cdp neighbors и генерировать
на основании вывода команды описание для интерфейсов.

Например, если у R1 такой вывод команды:
R1>show cdp neighbors
Capability Codes: R - Router, T - Trans Bridge, B - Source Route Bridge
                  S - Switch, H - Host, I - IGMP, r - Repeater

Device ID        Local Intrfce     Holdtme    Capability  Platform  Port ID
SW1              Eth 0/0           140          S I      WS-C3750-  Eth 0/1

Для интерфейса Eth 0/0 надо сгенерировать такое описание
description Connected to SW1 port Eth 0/1

Функция должна возвращать словарь, в котором ключи - имена интерфейсов,
а значения - команда задающая описание интерфейса:
'Eth 0/0': 'description Connected to SW1 port Eth 0/1'


Проверить работу функции на файле sh_cdp_n_sw1.txt.
"""

def generate_description_from_cdp(filename):
    """
    The function parses output of 'show cdp neighbors' and returns commands to configure descriptions on the device interfaces.
    Input: a name of file with 'show cdp neighbors' output.
    Output: a dictionary with keys - interfaces names (strings) and values - commands to configure interface descriptions (strings).

    E.g.
    R1>show cdp neighbors
    Capability Codes: R - Router, T - Trans Bridge, B - Source Route Bridge
                      S - Switch, H - Host, I - IGMP, r - Repeater

    Device ID        Local Intrfce     Holdtme    Capability  Platform  Port ID
    SW1              Eth 0/0           140          S I      WS-C3750-  Eth 0/1

    {'Eth 0/0': 'description Connected to SW1 port Eth 0/1'}
    """
    res = {}

    ### My regex version 1
    # regex = r'\n(?P<nei_name>\S+) +(?P<loc_port>\S+ \S+) +\d+ .* (?P<nei_port>\S+ \S+)'
    regex = r'(?P<nei_name>\S+) +(?P<loc_port>\S+ \S+) +\d+ +(?:\S+ )* +\S+ +(?P<nei_port>\S+ \S+)'
    descr_command = 'description Connected to {} port {}'
    with open(filename) as f:
        for m in re.finditer(regex,f.read()):
            args = m.group('nei_name', 'nei_port')
            res[m.group('loc_port')] = descr_command.format(*args)

    return res

if __name__ == '__main__':
    print(generate_description_from_cdp('sh_cdp_n_sw1.txt'))