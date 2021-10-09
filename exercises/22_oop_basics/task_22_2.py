# -*- coding: utf-8 -*-

"""
Задание 22.2

Создать класс CiscoTelnet, который подключается по Telnet к оборудованию Cisco.

При создании экземпляра класса, должно создаваться подключение Telnet, а также
переход в режим enable.
Класс должен использовать модуль telnetlib для подключения по Telnet.

У класса CiscoTelnet, кроме __init__, должно быть, как минимум, два метода:
* _write_line - принимает как аргумент строку и отправляет на оборудование строку
  преобразованную в байты и добавляет перевод строки в конце. Метод _write_line должен
  использоваться внутри класса.
* send_show_command - принимает как аргумент команду show и возвращает вывод
  полученный с обрудования

Параметры метода __init__:
* ip - IP-адрес
* username - имя пользователя
* password - пароль
* secret - пароль enable

Пример создания экземпляра класса:
In [2]: from task_22_2 import CiscoTelnet

In [3]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}
   ...:

In [4]: r1 = CiscoTelnet(**r1_params)

In [5]: r1.send_show_command("sh ip int br")
Out[5]: 'sh ip int br\r\nInterface                  IP-Address      OK? Method Status                Protocol\r\nEthernet0/0                192.168.100.1   YES NVRAM  up                    up      \r\nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \r\nEthernet0/2                unassigned      YES manual up                    up      \r\nEthernet0/3                192.168.130.1   YES NVRAM  up                    up      \r\nR1#'


Подсказка:
Метод _write_line нужен для того чтобы можно было сократить строку:
self.telnet.write(line.encode("ascii") + b"\n")

до такой:
self._write_line(line)

Он не должен делать ничего другого.
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


if __name__ == '__main__':
    # t = CiscoTelnet('192.168.100.1', 'cisco', 'cisco', 'cisco')
    # print(t)
    params = {'ip': '192.168.100.1',
              'username': 'cisco',
              'password': 'cisco',
              'secret': 'cisco'}
    t = CiscoTelnet(**params)

    ver = t.send_show_command('show version')
    print(ver)

    int_br = t.send_show_command('sh ip int br')
    print(int_br)