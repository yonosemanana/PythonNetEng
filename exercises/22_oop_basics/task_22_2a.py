# -*- coding: utf-8 -*-

"""
Задание 22.2a

Скопировать класс CiscoTelnet из задания 22.2 и изменить
метод send_show_command добавив три параметра:

* parse - контролирует то, будет возвращаться обычный вывод команды или список словарей,
  полученный после обработки с помощью TextFSM.
  При parse=True должен возвращаться список словарей, а parse=False обычный вывод.
  Значение по умолчанию - True.
* templates - путь к каталогу с шаблонами. Значение по умолчанию - "templates"
* index - имя файла, где хранится соответствие между командами и шаблонами.
  Значение по умолчанию - "index"


Пример создания экземпляра класса:

In [1]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [2]: from task_22_2a import CiscoTelnet

In [3]: r1 = CiscoTelnet(**r1_params)

Использование метода send_show_command:
In [4]: r1.send_show_command("sh ip int br", parse=True)
Out[4]:
[{'intf': 'Ethernet0/0',
  'address': '192.168.100.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/1',
  'address': '192.168.200.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/2',
  'address': '192.168.130.1',
  'status': 'up',
  'protocol': 'up'}]

In [5]: r1.send_show_command("sh ip int br", parse=False)
Out[5]: 'sh ip int br\r\nInterface                  IP-Address      OK? Method Status
Protocol\r\nEthernet0/0                192.168.100.1   YES NVRAM  up
up      \r\nEthernet0/1                192.168.200.1   YES NVRAM  up...'


"""

import telnetlib
import time
import ntc_templates.parse
import os

class CiscoTelnet:
    def __init__(self, ip, username, password, secret):
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
        time.sleep(1)
        self.session.read_very_eager()

    def _write_line(self, command):
        self.session.write(command.encode('ascii') + b'\n')

    def send_show_command(self, show_command, parse=True, templates='templates', index='index'):
        self._write_line(show_command)
        time.sleep(1)
        output = self.session.read_very_eager().decode('utf-8')

        os.environ['NTC_TEMPLATES_DIR'] = templates
        if parse:
            return ntc_templates.parse.parse_output(platform='cisco_ios', command=show_command, data=output)
        else:
            return output

if __name__ == '__main__':
    params = {'ip': '192.168.100.1',
              'username': 'cisco',
              'password': 'cisco',
              'secret': 'cisco'}
    t = CiscoTelnet(**params)

    ver = t.send_show_command('show version', parse=False)
    print(ver)

    int_br = t.send_show_command('sh ip int br', parse=True)
    print(int_br)

