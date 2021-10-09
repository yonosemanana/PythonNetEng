# -*- coding: utf-8 -*-

"""
Задание 22.2b

Скопировать класс CiscoTelnet из задания 22.2a и добавить метод send_config_commands.


Метод send_config_commands должен уметь отправлять одну команду конфигурационного
режима и список команд.
Метод должен возвращать вывод аналогичный методу send_config_set у netmiko
(пример вывода ниже).

Пример создания экземпляра класса:
In [1]: from task_22_2b import CiscoTelnet

In [2]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [3]: r1 = CiscoTelnet(**r1_params)

Использование метода send_config_commands:

In [5]: r1.send_config_commands('logging 10.1.1.1')
Out[5]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#logging 10.1.1.1\r\nR1(config)#end\r\nR1#'

In [6]: r1.send_config_commands(['interface loop55', 'ip address 5.5.5.5 255.255.255.255'])
Out[6]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#interface loop55\r\nR1(config-if)#ip address 5.5.5.5 255.255.255.255\r\nR1(config-if)#end\r\nR1#'

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

    def send_config_commands(self, commands):
        self._write_line('configure terminal')
        time.sleep(1)

        if type(commands) == str:
            commands = [commands]

        for command in commands:
            self._write_line(command)
        time.sleep(1)
        output = self.session.read_very_eager().decode('utf-8')

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

    config_command = 'ip domain-lookup'
    config_commands = ['interface Lo123', 'ip address 1.1.1.1 255.255.255.255', 'end']
    res = t.send_config_commands(config_command)
    print(res)
    res = t.send_config_commands(config_commands)
    print(res)