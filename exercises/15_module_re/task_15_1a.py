import re
# -*- coding: utf-8 -*-
"""
Задание 15.1a

Скопировать функцию get_ip_from_cfg из задания 15.1 и переделать ее таким образом,
чтобы она возвращала словарь:
* ключ: имя интерфейса
* значение: кортеж с двумя строками:
  * IP-адрес
  * маска

В словарь добавлять только те интерфейсы, на которых настроены IP-адреса.

Например (взяты произвольные адреса):
{'FastEthernet0/1': ('10.0.1.1', '255.255.255.0'),
 'FastEthernet0/2': ('10.0.2.1', '255.255.255.0')}

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла config_r1.txt.

Обратите внимание, что в данном случае, можно не проверять корректность IP-адреса,
диапазоны адресов и так далее, так как обрабатывается вывод команды,
а не ввод пользователя.

"""
# def get_ip_from_cfg(config_file):
#     """
#     The function receives a file name of the configuration file of a switch or router.
#     The function returns a dictionary: {interface name: a tuple of strings (ip_address, mask) assigned on the interfaces}
#     The function uses module re
#     """
#     res = {}
#     regex_int = r'interface (?P<intf>\S+)'
#     regex_ip = r'ip address (?P<ip>\S+) (?P<mask>\S+)'
#
#     with open(config_file) as f:
#         for line in f:
#             match_int = re.search(regex_int, line)
#             if match_int:
#                 intf = match_int.group('intf')
#             match_ip = re.search(regex_ip, line)
#             if match_ip:
#                 ip, mask = match_ip.groups()
#                 res[intf] = (ip, mask)
#     return res

def get_ip_from_cfg(config_file):
    """
    The function receives a file name of the configuration file of a switch or router.
    The function returns a dictionary: {interface name: a tuple of strings (ip_address, mask) assigned on the interfaces}
    The function uses module re
    """
    res = {}
    regex = (r'interface (?P<intf>\S+)\n'
             r'(?: .*\n)*'
             r' ip address (?P<ip>\S+) (?P<mask>\S+)')

    with open(config_file) as f:
        for m in re.finditer(regex, f.read()):
            # print(m)
            # print(m.groups())
            res[m.group('intf')] = (m.group('ip'), m.group('mask'), )
    return res

if __name__ == '__main__':
    print(get_ip_from_cfg('config_r1.txt'))