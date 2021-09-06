import re
# -*- coding: utf-8 -*-
"""
Задание 15.4

Создать функцию get_ints_without_description, которая ожидает как аргумент
имя файла, в котором находится конфигурация устройства.

Функция должна обрабатывать конфигурацию и возвращать список имен интерфейсов,
на которых нет описания (команды description).

Пример итогового списка:
["Loopback0", "Tunnel0", "Ethernet0/1", "Ethernet0/3.100", "Ethernet1/0"]

Пример интерфейса с описанием:
interface Ethernet0/2
 description To P_r9 Ethernet0/2
 ip address 10.0.19.1 255.255.255.0
 mpls traffic-eng tunnels
 ip rsvp bandwidth

Интерфейс без описания:
interface Loopback0
 ip address 10.1.1.1 255.255.255.255

Проверить работу функции на примере файла config_r1.txt.
"""

def get_ints_without_description(filename):
    """
    The function finds interfaces without description in the configuration file.
    Input: a name of the configuration file of Cisco IOS device.
    Output: a list of strings with interfaces (without 'interface' keyword) with no description.
    """
    res = []
    regex = re.compile((r'\ninterface (?P<intf>\S+)\n|'
                        r' description (?P<descr>.*\n)'))
    with open(filename) as f:
        for match in regex.finditer(f.read()):
            if match.lastgroup == 'intf':
                res.append(match.group('intf'))
            elif match.lastgroup == 'descr':
                res.pop()

    return res
if __name__ == '__main__':
    print(get_ints_without_description('config_r1.txt'))