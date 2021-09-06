import re
# -*- coding: utf-8 -*-
"""
Задание 15.1

Создать функцию get_ip_from_cfg, которая ожидает как аргумент имя файла,
в котором находится конфигурация устройства.

Функция должна обрабатывать конфигурацию и возвращать IP-адреса и маски,
которые настроены на интерфейсах, в виде списка кортежей:
* первый элемент кортежа - IP-адрес
* второй элемент кортежа - маска

Например (взяты произвольные адреса):
[('10.0.1.1', '255.255.255.0'), ('10.0.2.1', '255.255.255.0')]

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла config_r1.txt.


Обратите внимание, что в данном случае, можно не проверять корректность IP-адреса,
диапазоны адресов и так далее, так как обрабатывается вывод команды,
а не ввод пользователя.

"""

### My function version 1
# def get_ip_from_cfg(config_file):
#     """
#     The function receives a file name of the configuration file of a switch or router.
#     The function returns a list of tuples of strings (ip_address, mask) assigned on the interfaces
#     The function uses module re
#     """
#     res = []
#     # That regex included IPs and wildcard masks from ACLs too, what is wrong in the task.
#     #regex = r'(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) (?P<mask>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
#     regex = r'ip address (?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) (?P<mask>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
#     with open(config_file) as f:
#         for line in f:
#             match = re.search(regex, line)
#             if match:
#                 res.append((match.group('ip'), match.group('mask'),))
#     return res

def get_ip_from_cfg(config_file):
    """
    The function receives a file name of the configuration file of a switch or router.
    The function returns a list of tuples of strings (ip_address, mask) assigned on the interfaces
    The function uses module re
    """
    res = []
    regex = r'ip address (?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) (?P<mask>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    with open(config_file) as f:
        res = re.findall(regex, f.read())
    return res


if __name__ == '__main__':
    print(get_ip_from_cfg('config_r1.txt'))