import re
# -*- coding: utf-8 -*-
"""
Задание 15.3

Создать функцию convert_ios_nat_to_asa, которая конвертирует правила NAT
из синтаксиса cisco IOS в cisco ASA.

Функция ожидает такие аргументы:
- имя файла, в котором находится правила NAT Cisco IOS
- имя файла, в который надо записать полученные правила NAT для ASA

Функция ничего не возвращает.

Проверить функцию на файле cisco_nat_config.txt.

Пример правил NAT cisco IOS
ip nat inside source static tcp 10.1.2.84 22 interface GigabitEthernet0/1 20022
ip nat inside source static tcp 10.1.9.5 22 interface GigabitEthernet0/1 20023

И соответствующие правила NAT для ASA:
object network LOCAL_10.1.2.84
 host 10.1.2.84
 nat (inside,outside) static interface service tcp 22 20022
object network LOCAL_10.1.9.5
 host 10.1.9.5
 nat (inside,outside) static interface service tcp 22 20023

В файле с правилами для ASA:
- не должно быть пустых строк между правилами
- перед строками "object network" не должны быть пробелы
- перед остальными строками должен быть один пробел

Во всех правилах для ASA интерфейсы будут одинаковыми (inside,outside).
"""

### My function version #1.
# def convert_ios_nat_to_asa(in_file, out_file):
#     """
#     The function converts NAT rules from Cisco IOS syntax to Cisco ASA.
#     Input: a name of the input file (with Cisco IOS NAT config), a name of the output file (with Cisco ASA NAT config)
#     E.g. of input:
#         ip nat inside source static tcp 10.1.2.84 22 interface GigabitEthernet0/1 20022
#         ip nat inside source static tcp 10.1.9.5 22 interface GigabitEthernet0/1 20023
#     Output: the function writes Cisco ASA NAT config to the ouput file which name was given
#     E.g. of output:
#         object network LOCAL_10.1.2.84
#          host 10.1.2.84
#          nat (inside,outside) static interface service tcp 22 20022
#         object network LOCAL_10.1.9.5
#          host 10.1.9.5
#          nat (inside,outside) static interface service tcp 22 20023
#     """
#     regex = re.compile(r'ip nat inside source static (?P<proto>\S+) (?P<ip_int>\S+) (?P<dst_port_int>\d+) interface (?P<intf_ext>\S+) (?P<dst_port_ext>\d+)')
#     asa_nat_template = ('object network LOCAL_{ip_int}\n'
#     ' host {ip_int}\n'
#     ' nat (inside,outside) static interface service {proto} {dst_port_int} {dst_port_ext}\n')
#     with open(in_file) as f_in, open(out_file, 'w') as f_out:
#         for m in regex.finditer(f_in.read()):
#             f_out.writelines(asa_nat_template.format(ip_int=m.group('ip_int'),
#                                                      proto=m.group('proto'),
#                                                      dst_port_int=m.group('dst_port_int'),
#                                                      dst_port_ext=m.group('dst_port_ext')))


def convert_ios_nat_to_asa(in_file, out_file):
    """
    The function converts NAT rules from Cisco IOS syntax to Cisco ASA.
    Input: a name of the input file (with Cisco IOS NAT config), a name of the output file (with Cisco ASA NAT config)
    E.g. of input:
        ip nat inside source static tcp 10.1.2.84 22 interface GigabitEthernet0/1 20022
        ip nat inside source static tcp 10.1.9.5 22 interface GigabitEthernet0/1 20023
    Output: the function writes Cisco ASA NAT config to the ouput file which name was given
    E.g. of output:
        object network LOCAL_10.1.2.84
         host 10.1.2.84
         nat (inside,outside) static interface service tcp 22 20022
        object network LOCAL_10.1.9.5
         host 10.1.9.5
         nat (inside,outside) static interface service tcp 22 20023
    """
    regex = re.compile(r'ip nat inside source static (?P<proto>\S+) (?P<ip_int>\S+) (?P<dst_port_int>\d+) interface \S+ (?P<dst_port_ext>\d+)')
    asa_nat_template = ('object network LOCAL_{ip_int}\n'
    ' host {ip_int}\n'
    ' nat (inside,outside) static interface service {proto} {dst_port_int} {dst_port_ext}\n')
    with open(in_file) as f_in, open(out_file, 'w') as f_out:
        for m in regex.finditer(f_in.read()):
            #print(m.groupdict())
            kwargs = m.groupdict()
            f_out.writelines(asa_nat_template.format(**kwargs))

if __name__ == '__main__':
    convert_ios_nat_to_asa('cisco_nat_config.txt', 'mytest_out.txt')