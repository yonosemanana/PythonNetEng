import re
# -*- coding: utf-8 -*-
"""
Задание 15.1b

Проверить работу функции get_ip_from_cfg из задания 15.1a
на конфигурации config_r2.txt.

Обратите внимание, что на интерфейсе e0/1 назначены два IP-адреса:
interface Ethernet0/1
 ip address 10.255.2.2 255.255.255.0
 ip address 10.254.2.2 255.255.255.0 secondary

А в словаре, который возвращает функция get_ip_from_cfg, интерфейсу Ethernet0/1
соответствует только один из них.

Скопировать функцию get_ip_from_cfg из задания 15.1a и переделать ее таким
образом, чтобы в значении словаря она возвращала список кортежей
для каждого интерфейса.
Если на интерфейсе назначен только один адрес, в списке будет один кортеж.
Если же на интерфейсе настроены несколько IP-адресов, то в списке будет
несколько кортежей. Ключом остается имя интерфейса.

Проверьте функцию на конфигурации config_r2.txt и убедитесь, что интерфейсу
Ethernet0/1 соответствует список из двух кортежей.

Обратите внимание, что в данном случае, можно не проверять корректность
IP-адреса, диапазоны адресов и так далее, так как обрабатывается вывод команды,
а не ввод пользователя.

"""

### My function version #1
# def get_ip_from_cfg(config_file):
#     """
#     The function receives a file name of the configuration file of a switch or router.
#     The function returns a dictionary: {interface name: a list of tuples of strings (ip_address, mask) assigned on the interfaces, including secondary IP addresses}
#     The function uses module re
#     """
#     res = {}
#     regex_int = r'^interface (?P<intf>\S+)'
#     regex_ip = r' ip address (?P<ip>\S+) (?P<mask>\S+)'
#
#     with open(config_file) as f:
#         for line in f:
#             match_int = re.search(regex_int, line)
#             if match_int:
#                 intf = match_int.group('intf')
#             match_ip = re.search(regex_ip, line)
#             if match_ip:
#                 ip, mask = match_ip.groups()
#                 if intf in res:
#                     res[intf].append((ip, mask,))
#                 else:
#                     res[intf] = []
#                     res[intf].append((ip, mask,))
#     return res

### My function version #2
# def get_ip_from_cfg(config_file):
#     """
#     The function receives a file name of the configuration file of a switch or router.
#     The function returns a dictionary: {interface name: a list of tuples of strings (ip_address, mask) assigned on the interfaces, including secondary IP addresses}
#     The function uses module re
#     """
#     res = {}
#     regex_int = r'^interface (?P<intf>\S+)'
#     regex_ip = r' ip address (?P<ip>\S+) (?P<mask>\S+)'
#
#     with open(config_file) as f:
#         for line in f:
#             match_int = re.search(regex_int, line)
#             if match_int:
#                 intf = match_int.group('intf')
#             match_ip = re.search(regex_ip, line)
#             if match_ip:
#                 ip, mask = match_ip.groups()
#                 res.setdefault(intf,[])
#                 res[intf].append((ip, mask,))
#     return res

# My function version #3
def get_ip_from_cfg(config_file):
    """
    The function receives a file name of the configuration file of a switch or router.
    The function returns a dictionary: {interface name: a list of tuples of strings (ip_address, mask) assigned on the interfaces, including secondary IP addresses}
    The function uses module re
    """
    res = {}
    regex = re.compile(r'^interface (?P<intf>\S+)| ip address (?P<ip>\S+) (?P<mask>\S+)')

    with open(config_file) as f:
        for line in f:
            match = regex.search(line)
            if match:
                if match.lastgroup == 'intf':
                    intf = match.group('intf')
                if match.lastgroup == 'mask':
                    ip, mask = match.group('ip', 'mask')
                    res.setdefault(intf,[])
                    res[intf].append((ip, mask,))
    return res

if __name__ == '__main__':
    print(get_ip_from_cfg('config_r2.txt'))