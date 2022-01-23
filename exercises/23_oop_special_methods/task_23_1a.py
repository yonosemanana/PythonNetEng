# -*- coding: utf-8 -*-

"""
Задание 23.1a

Скопировать и изменить класс IPAddress из задания 23.1.

Добавить два строковых представления для экземпляров класса IPAddress.
Как дожны выглядеть строковые представления, надо определить из вывода ниже:

Создание экземпляра
In [5]: ip1 = IPAddress('10.1.1.1/24')

In [6]: str(ip1)
Out[6]: 'IP address 10.1.1.1/24'

In [7]: print(ip1)
IP address 10.1.1.1/24

In [8]: ip1
Out[8]: IPAddress('10.1.1.1/24')

In [9]: ip_list = []

In [10]: ip_list.append(ip1)

In [11]: ip_list
Out[11]: [IPAddress('10.1.1.1/24')]

In [12]: print(ip_list)
[IPAddress('10.1.1.1/24')]

"""

import re

regex = r'^(?P<ip>\S+)/(?P<mask>\d+)$'
regex_ip = r'^(?P<ip>(\d+\.){3}\d+)$'

class IPAddress:
    def __init__(self, addr_mask):
        match = re.search(regex, addr_mask)
        if not match:
            raise ValueError
        else:
            mask = match.group('mask')
            if int(mask) < 0 or int(mask) > 32:
                raise ValueError('Incorrect mask')
            else:
                match_ip = re.search(regex_ip, match.group('ip'))
                if not match_ip:
                    raise ValueError('Incorrect IPv4 address')
                else:
                    ip = match_ip.group('ip')
                    for octet in ip.split('.'):
                        if int(octet) < 0 or int(octet) > 255:
                            raise ValueError('Incorrect IPv4 address')
                    self.ip = ip
                    self.mask = int(mask)

    def __str__(self):
        return f'IP address {self.ip}/{self.mask}'

    def __repr__(self):
        return f"IPAddress('{self.ip}/{self.mask}')"


if __name__ == '__main__':
    ip1 = IPAddress('10.1.1.1/24')
    print(ip1)
    ips = []
    ips.append(ip1)
    print(ips)