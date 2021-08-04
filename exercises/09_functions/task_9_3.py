# -*- coding: utf-8 -*-
"""
Задание 9.3

Создать функцию get_int_vlan_map, которая обрабатывает конфигурационный
файл коммутатора и возвращает кортеж из двух словарей:
* словарь портов в режиме access, где ключи номера портов,
  а значения access VLAN (числа):
{'FastEthernet0/12': 10,
 'FastEthernet0/14': 11,
 'FastEthernet0/16': 17}

* словарь портов в режиме trunk, где ключи номера портов,
  а значения список разрешенных VLAN (список чисел):
{'FastEthernet0/1': [10, 20],
 'FastEthernet0/2': [11, 30],
 'FastEthernet0/4': [17]}

У функции должен быть один параметр config_filename, который ожидает как аргумент
имя конфигурационного файла.

Проверить работу функции на примере файла config_sw1.txt

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

def get_int_vlan_map(config_filename):
    '''
    Создать функцию get_int_vlan_map, которая обрабатывает конфигурационный
    файл коммутатора и возвращает кортеж из двух словарей:
    * словарь портов в режиме access, где ключи номера портов,
      а значения access VLAN (числа):
    {'FastEthernet0/12': 10,
     'FastEthernet0/14': 11,
     'FastEthernet0/16': 17}

    * словарь портов в режиме trunk, где ключи номера портов,
      а значения список разрешенных VLAN (список чисел):
    {'FastEthernet0/1': [10, 20],
     'FastEthernet0/2': [11, 30],
     'FastEthernet0/4': [17]}

    У функции должен быть один параметр config_filename, который ожидает как аргумент
    имя конфигурационного файла.
    '''
    access_ports = {}
    trunk_ports = {}

    with open(config_filename) as config_file:
        for line in config_file:
            if line.lstrip().startswith('interface'):
                _, intf = line.split()
            if line.strip().startswith('switchport access vlan'):
                vlan = int(line.split()[-1])
                access_ports[intf] = vlan
            if line.strip().startswith('switchport trunk allowed vlan'):
                vlans = [int(vlan) for vlan in line.split()[-1].split(',')]
                trunk_ports[intf] = vlans

    return access_ports, trunk_ports

print(get_int_vlan_map('config_sw1.txt'))