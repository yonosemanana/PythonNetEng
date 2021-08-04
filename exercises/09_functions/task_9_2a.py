# -*- coding: utf-8 -*-
"""
Задание 9.2a

Сделать копию функции generate_trunk_config из задания 9.2

Изменить функцию таким образом, чтобы она возвращала не список команд, а словарь:
- ключи: имена интерфейсов, вида 'FastEthernet0/1'
- значения: список команд, который надо
  выполнить на этом интерфейсе

Проверить работу функции на примере словаря trunk_config и шаблона trunk_mode_template.

Пример итогового словаря, который должна возвращать функция (перевод строки
после каждого элемента сделан для удобства чтения):
{
    "FastEthernet0/1": [
        "switchport mode trunk",
        "switchport trunk native vlan 999",
        "switchport trunk allowed vlan 10,20,30",
    ],
    "FastEthernet0/2": [
        "switchport mode trunk",
        "switchport trunk native vlan 999",
        "switchport trunk allowed vlan 11,30",
    ],
    "FastEthernet0/4": [
        "switchport mode trunk",
        "switchport trunk native vlan 999",
        "switchport trunk allowed vlan 17",
    ],
}

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""


trunk_mode_template = [
    "switchport mode trunk",
    "switchport trunk native vlan 999",
    "switchport trunk allowed vlan",
]

trunk_config = {
    "FastEthernet0/1": [10, 20, 30],
    "FastEthernet0/2": [11, 30],
    "FastEthernet0/4": [17],
}


def generate_trunk_config(intf_vlan_mapping, trunk_template):
    """
    Создать функцию generate_trunk_config, которая генерирует
    конфигурацию для trunk-портов.

    У функции должны быть такие параметры:

    - intf_vlan_mapping: ожидает как аргумент словарь с соответствием интерфейс-VLANы
      такого вида:
        {'FastEthernet0/1': [10, 20],
         'FastEthernet0/2': [11, 30],
         'FastEthernet0/4': [17]}
    - trunk_template: ожидает как аргумент шаблон конфигурации trunk-портов в виде
      списка команд (список trunk_mode_template)

    Изменить функцию таким образом, чтобы она возвращала не список команд, а словарь:
    - ключи: имена интерфейсов, вида 'FastEthernet0/1'
    - значения: список команд, который надо
      выполнить на этом интерфейсе
    """
    result = {}
    for intf, vlans in intf_vlan_mapping.items():
        result[intf] = []
        for command in trunk_template:
            if command == 'switchport trunk allowed vlan':
                vlans_str = [str(vlan) for vlan in vlans]
                command = command + ' ' + ','.join(vlans_str)
            result[intf].append(command)
    return result


for intf, commands in generate_trunk_config(trunk_config, trunk_mode_template).items():
    print('interface ' + intf)
    for command in commands:
        print(command)

