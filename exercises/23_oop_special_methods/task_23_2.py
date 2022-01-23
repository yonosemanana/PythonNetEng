# -*- coding: utf-8 -*-

"""
Задание 23.2

Скопировать класс CiscoTelnet из задания 22.2 и добавить классу поддержку
работы в менеджере контекста.
При выходе из блока менеджера контекста должно закрываться соединение.

Пример работы:

In [14]: r1_params = {
    ...:     'ip': '192.168.100.1',
    ...:     'username': 'cisco',
    ...:     'password': 'cisco',
    ...:     'secret': 'cisco'}

In [15]: from task_23_2 import CiscoTelnet

In [16]: with CiscoTelnet(**r1_params) as r1:
    ...:     print(r1.send_show_command('sh clock'))
    ...:
sh clock
*19:17:20.244 UTC Sat Apr 6 2019
R1#

In [17]: with CiscoTelnet(**r1_params) as r1:
    ...:     print(r1.send_show_command('sh clock'))
    ...:     raise ValueError('Возникла ошибка')
    ...:
sh clock
*19:17:38.828 UTC Sat Apr 6 2019
R1#
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-17-f3141be7c129> in <module>
      1 with CiscoTelnet(**r1_params) as r1:
      2     print(r1.send_show_command('sh clock'))
----> 3     raise ValueError('Возникла ошибка')
      4

ValueError: Возникла ошибка
"""

import telnetlib
import time

class CiscoTelnet:
    def __init__(self, ip, username, password, secret):
        self.ip = ip
        self.username = username
        self.password = password
        self.secret = secret

        # self.session = telnetlib.Telnet(ip)
        # self.session.read_until(b'Username: ')
        # self.session.write(username.encode('ascii') + b'\n')
        # self.session.read_until(b'Password: ')
        # self.session.write(password.encode('ascii') + b'\n')
        # self.session.read_until(b'>')
        # self.session.write(b'enable\n')
        # self.session.read_until(b'Password: ')
        # self.session.write(secret.encode('ascii') + b'\n')

        self.session = telnetlib.Telnet(ip)
        self.session.read_until(b'Username: ')
        self._write_line(username)
        self.session.read_until(b'Password: ')
        self._write_line(password)
        self.session.read_until(b'>')
        self._write_line('enable')
        self.session.read_until(b'Password: ')
        self._write_line(secret)
        self.session.read_until(b'#')

        self._write_line('terminal length 0')
        # time.sleep(1)
        # self.session.read_very_eager()
        self.session.read_until(b'#')


    def _write_line(self, command):
        self.session.write(command.encode('ascii') + b'\n')

    def send_show_command(self, show_command):
        self._write_line(show_command)

        # time.sleep(1)
        # return self.session.read_very_eager().decode('utf-8')

        return self.session.read_until(b'#').decode('utf-8')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()


if __name__ == '__main__':
    r1_params = {'ip': '192.168.100.1',
                 'username': 'cisco',
                 'password': 'cisco',
                 'secret': 'cisco'}
    command = 'show ip route'
    with CiscoTelnet(**r1_params) as r1:
        res = r1.send_show_command(command)
        print(res)
