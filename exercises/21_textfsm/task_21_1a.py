# -*- coding: utf-8 -*-
"""
Задание 21.1a

Создать функцию parse_output_to_dict.

Параметры функции:
* template - имя файла, в котором находится шаблон TextFSM.
  Например, templates/sh_ip_int_br.template
* command_output - вывод соответствующей команды show (строка)

Функция должна возвращать список словарей:
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на выводе команды output/sh_ip_int_br.txt
и шаблоне templates/sh_ip_int_br.template.
"""

import textfsm
from task_21_1 import parse_command_output

# def parse_output_to_dict2(template, command_output):
#     """
#     """
#     res = parse_command_output(template, command_output)
#     res_dict = {key: [] for key in res[0]}
#     for line in res[1:]:
#         for i in range(len(line)):
#             res_dict[res[0][i]].append(line[i])
#
#     return res_dict

def parse_output_to_dict(template, command_output):
    with open(template) as tmpl_f:
        fsm = textfsm.TextFSM(tmpl_f)
    res = fsm.ParseText(command_output)
    keys = fsm.header

    return [dict(zip(keys, item)) for item in res]

if __name__ == '__main__':
    template = 'templates/sh_ip_int_br.template'
    output = 'output/sh_ip_int_br.txt'
    with open(output) as f:
        print(parse_output_to_dict(template, f.read()))