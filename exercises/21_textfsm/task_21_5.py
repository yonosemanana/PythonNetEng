# -*- coding: utf-8 -*-
"""
Задание 21.5

Создать функцию send_and_parse_command_parallel.

Функция send_and_parse_command_parallel должна запускать в
параллельных потоках функцию send_and_parse_show_command из задания 21.4.

Параметры функции send_and_parse_command_parallel:
* devices - список словарей с параметрами подключения к устройствам
* command - команда
* templates_path - путь к каталогу с шаблонами TextFSM
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция должна возвращать словарь:
* ключи - IP-адрес устройства с которого получен вывод
* значения - список словарей (вывод который возвращает функция send_and_parse_show_command)

Пример словаря:
{'192.168.100.1': [{'address': '192.168.100.1',
                    'intf': 'Ethernet0/0',
                    'protocol': 'up',
                    'status': 'up'},
                   {'address': '192.168.200.1',
                    'intf': 'Ethernet0/1',
                    'protocol': 'up',
                    'status': 'up'}],
 '192.168.100.2': [{'address': '192.168.100.2',
                    'intf': 'Ethernet0/0',
                    'protocol': 'up',
                    'status': 'up'},
                   {'address': '10.100.23.2',
                    'intf': 'Ethernet0/1',
                    'protocol': 'up',
                    'status': 'up'}]}

Проверить работу функции на примере вывода команды sh ip int br
и устройствах из devices.yaml.
"""

from concurrent.futures import ThreadPoolExecutor
from task_21_4 import send_and_parse_show_command
import yaml
from itertools import repeat
from pprint import pprint

def send_and_parse_command_parallel(devices, command, templates_path, limit=3):
    """
    """
    result = {}
    with ThreadPoolExecutor(max_workers=limit) as e:
        res = e.map(send_and_parse_show_command, devices, repeat(command), repeat(templates_path))

    hosts = [dev['host'] for dev in devices]
    return dict(zip(hosts, [item for item in res]))


if __name__ == '__main__':
    command = 'sh ip int br'
    template_path = 'templates'
    with open('devices.yaml') as f:
        devices = yaml.safe_load(f)
        pprint(send_and_parse_command_parallel(devices,command, template_path))
