# -*- coding: utf-8 -*-
"""
Задание 21.3

Создать функцию parse_command_dynamic.

Параметры функции:
* command_output - вывод команды (строка)
* attributes_dict - словарь атрибутов, в котором находятся такие пары ключ-значение:
 * 'Command': команда
 * 'Vendor': вендор
* index_file - имя файла, где хранится соответствие между командами и шаблонами.
  Значение по умолчанию - "index"
* templ_path - каталог, где хранятся шаблоны. Значение по умолчанию - "templates"

Функция должна возвращать список словарей с результатами обработки
вывода команды (как в задании 21.1a):
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на примере вывода команды sh ip int br.
"""

import textfsm
from textfsm import clitable

def parse_command_dynamic(command_output, attributes_dict, index_file='index', templ_path='templates'):
    cli_table = clitable.CliTable(index_file,templ_path)
    cli_table.ParseCmd(command_output,attributes_dict)
    header = list(cli_table.header)
    rows = [list(row) for row in cli_table]
    return [dict(zip(header, row)) for row in rows]

if __name__ == '__main__':
    template_dir = 'templates'
    index_file = 'index'
    output = 'output/sh_ip_int_br.txt'
    attributes = {'Command': 'sh ip int br'}

    with open(output) as f:
        print(parse_command_dynamic(f.read(), attributes, index_file, template_dir))