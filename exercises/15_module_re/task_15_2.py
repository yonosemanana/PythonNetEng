import re
# -*- coding: utf-8 -*-
"""
Задание 15.2

Создать функцию parse_sh_ip_int_br, которая ожидает как аргумент
имя файла, в котором находится вывод команды show ip int br

Функция должна обрабатывать вывод команды show ip int br и возвращать такие поля:
* Interface
* IP-Address
* Status
* Protocol

Информация должна возвращаться в виде списка кортежей:
[('FastEthernet0/0', '10.0.1.1', 'up', 'up'),
 ('FastEthernet0/1', '10.0.2.1', 'up', 'up'),
 ('FastEthernet0/2', 'unassigned', 'down', 'down')]

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла sh_ip_int_br.txt.

"""

def parse_sh_ip_int_br(filename):
    """
    The function parses "show ip int brief" command output.
    Input: a name of the file with "show ip int brief" output.
    Output: the function returns a list of tuples of strings, e.g.:
    [('FastEthernet0/0', '10.0.1.1', 'up', 'up'),
     ('FastEthernet0/1', '10.0.2.1', 'up', 'up'),
     ('FastEthernet0/2', 'unassigned', 'down', 'down')]
    """
    res = []
    regex = re.compile(r'(?P<intf>\S+) +(?P<ip>unassigned|[\d\.]+) +\w+ +\w+ +(?P<status>up|down|(?:administratively down)) +(?P<protocol>up|down)')
    with open(filename) as f:
        res = regex.findall(f.read())
    return res

if __name__ == '__main__':
    print(parse_sh_ip_int_br('sh_ip_int_br.txt'))