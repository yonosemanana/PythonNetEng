# -*- coding: utf-8 -*-

"""
Задание 23.1

В этом задании необходимо создать класс IPAddress.

При создании экземпляра класса, как аргумент передается IP-адрес и маска,
а также должна выполняться проверка корректности адреса и маски:
* Адрес считается корректно заданным, если он:
   - состоит из 4 чисел разделенных точкой
   - каждое число в диапазоне от 0 до 255
* маска считается корректной, если это число в диапазоне от 8 до 32 включительно

Если маска или адрес не прошли проверку, необходимо сгенерировать
исключение ValueError с соответствующим текстом (вывод ниже).

Также, при создании класса, должны быть созданы два атрибута экземпляра:
ip и mask, в которых содержатся адрес и маска, соответственно.

Пример создания экземпляра класса:
In [1]: ip = IPAddress('10.1.1.1/24')

Атрибуты ip и mask
In [2]: ip1 = IPAddress('10.1.1.1/24')

In [3]: ip1.ip
Out[3]: '10.1.1.1'

In [4]: ip1.mask
Out[4]: 24

Проверка корректности адреса (traceback сокращен)
In [5]: ip1 = IPAddress('10.1.1/24')
---------------------------------------------------------------------------
...
ValueError: Incorrect IPv4 address

Проверка корректности маски (traceback сокращен)
In [6]: ip1 = IPAddress('10.1.1.1/240')
---------------------------------------------------------------------------
...
ValueError: Incorrect mask

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


if __name__ == '__main__':
    ip1 = IPAddress('10.1.1.1/24')
    # ip2 = IPAddress('10.1.1/24')
    # ip3 = IPAddress('10.1.1.1/240')

