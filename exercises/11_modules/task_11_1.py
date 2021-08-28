# -*- coding: utf-8 -*-
"""
Задание 11.1

Создать функцию parse_cdp_neighbors, которая обрабатывает
вывод команды show cdp neighbors.

У функции должен быть один параметр command_output, который ожидает как аргумент
вывод команды одной строкой (не имя файла). Для этого надо считать все содержимое
файла в строку, а затем передать строку как аргумент функции (как передать вывод
команды показано в коде ниже).

Функция должна возвращать словарь, который описывает соединения между устройствами.

Например, если как аргумент был передан такой вывод:
R4>show cdp neighbors

Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID
R5           Fa 0/1          122           R S I           2811       Fa 0/1
R6           Fa 0/2          143           R S I           2811       Fa 0/0

Функция должна вернуть такой словарь:

    {("R4", "Fa0/1"): ("R5", "Fa0/1"),
     ("R4", "Fa0/2"): ("R6", "Fa0/0")}

В словаре интерфейсы должны быть записаны без пробела между типом и именем.
То есть так Fa0/0, а не так Fa 0/0.

Проверить работу функции на содержимом файла sh_cdp_n_sw1.txt. При этом функция должна
работать и на других файлах (тест проверяет работу функции на выводе
из sh_cdp_n_sw1.txt и sh_cdp_n_r3.txt).

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
def parse_line(s):
    """
    The function parses a data line from 'show cdp neighbor' output from Cisco device.
    It returns a tuple with three values: neighbor_name, local_interface, neighbor_interface
    Input example: "R1           Eth 0/1         122           R S I           2811       Eth 0/0"
    Output example: (R1, Eth0/1, Eth0/0,)
    """
    neighbor, loc_intf_type, loc_intf_num, *rest, rem_intf_type, rem_intf_num = s.split()
    return neighbor, loc_intf_type + loc_intf_num, rem_intf_type + rem_intf_num

def parse_cdp_neighbors(command_output):
    """
    Тут мы передаем вывод команды одной строкой потому что именно в таком виде будет
    получен вывод команды с оборудования. Принимая как аргумент вывод команды,
    вместо имени файла, мы делаем функцию более универсальной: она может работать
    и с файлами и с выводом с оборудования.
    Плюс учимся работать с таким выводом.
    """
    command_index = command_output.index('show cdp neighbors')
    loc_name = command_output[:command_index - 1].strip()

    header_index = command_output.index('Device ID')
    all_lines = command_output[header_index:].split('\n')[1:]
    lines = list(filter(lambda s: s.strip() != '', all_lines))
    neighbors = list(map(parse_line, lines))
    #print(neighbors)

    result = {}
    for neighbor in neighbors:
        rem_name, loc_intf, rem_intf = neighbor
        result[(loc_name, loc_intf,)] = (rem_name, rem_intf,)

    return result

if __name__ == "__main__":
    with open("sh_cdp_n_sw1.txt") as f:
        print(parse_cdp_neighbors(f.read()))
