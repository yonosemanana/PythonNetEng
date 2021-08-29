import subprocess
import ipaddress

# -*- coding: utf-8 -*-
"""
Задание 12.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.

Функция ожидает как аргумент список IP-адресов.

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для проверки доступности IP-адреса, используйте команду ping.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

def ping_ip_addresses(ips):
    """ The function checks if the given IPs are pingable or not.
    Input: a list of IP addresses
    Output: a tuple with two lists: pingable and not pingable IPs
    """
    pingable = []
    not_pingable = []

    for ip in ips:
        try:
            ipaddress.ip_address(ip)
            ping_res = subprocess.run(['ping', '-c', '3', ip], stdout=subprocess.DEVNULL)
            if ping_res.returncode == 0:
                pingable.append(ip)
            else:
                not_pingable.append(ip)
        except ValueError:
            print(f'The IP address {ip} is not valid.')

    return pingable, not_pingable

if __name__ == '__main__':
    ip_addresses = ['8.8.8.8', '10.1.1.1', '10.a.1.2', '4.2.2.2']
    print(ping_ip_addresses(ip_addresses))