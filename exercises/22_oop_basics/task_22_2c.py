# -*- coding: utf-8 -*-

"""
Задание 22.2c

Скопировать класс CiscoTelnet из задания 22.2b и изменить метод send_config_commands
добавив проверку команд на ошибки.

У метода send_config_commands должен быть дополнительный параметр strict:
* strict=True значит, что при обнаружении ошибки, необходимо сгенерировать
  исключение ValueError (значение по умолчанию)
* strict=False значит, что при обнаружении ошибки, надо только вывести
  на стандартный поток вывода сообщене об ошибке

Метод дожен возвращать вывод аналогичный методу send_config_set
у netmiko (пример вывода ниже). Текст исключения и ошибки в примере ниже.

Пример создания экземпляра класса:
In [1]: from task_22_2c import CiscoTelnet

In [2]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [3]: r1 = CiscoTelnet(**r1_params)

In [4]: commands_with_errors = ['logging 0255.255.1', 'logging', 'a']
In [5]: correct_commands = ['logging buffered 20010', 'ip http server']
In [6]: commands = commands_with_errors+correct_commands

Использование метода send_config_commands:

In [7]: print(r1.send_config_commands(commands, strict=False))
При выполнении команды "logging 0255.255.1" на устройстве 192.168.100.1 возникла ошибка -> Invalid input detected at '^' marker.
При выполнении команды "logging" на устройстве 192.168.100.1 возникла ошибка -> Incomplete command.
При выполнении команды "a" на устройстве 192.168.100.1 возникла ошибка -> Ambiguous command:  "a"
conf t
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#logging 0255.255.1
                   ^
% Invalid input detected at '^' marker.

R1(config)#logging
% Incomplete command.

R1(config)#a
% Ambiguous command:  "a"
R1(config)#logging buffered 20010
R1(config)#ip http server
R1(config)#end
R1#

In [8]: print(r1.send_config_commands(commands, strict=True))
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-8-0abc1ed8602e> in <module>
----> 1 print(r1.send_config_commands(commands, strict=True))

...

ValueError: При выполнении команды "logging 0255.255.1" на устройстве 192.168.100.1 возникла ошибка -> Invalid input detected at '^' marker.

"""


import telnetlib
import time
import ntc_templates.parse
import os
import re

class CiscoTelnet:
    def __init__(self, ip, username, password, secret):
        self.ip = ip
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

    def send_config_commands(self, commands, strict=True):
        self._write_line('configure terminal')
        time.sleep(1)

        output_parts = [self.session.read_very_eager().decode('utf-8')]

        if type(commands) == str:
            commands = [commands]

        for command in commands:
            self._write_line(command)
            time.sleep(1)

            output = self.session.read_very_eager().decode('utf-8')
            # print(f'Command: {command}', f'Output: {output}')
            match = re.search('% ([\S ]+\r\n)', output)
            if match:
                if strict:
                    raise ValueError(f'При выполнении команды "{command}" на устройстве {self.ip} возникла ошибка -> {match.group(1)}')
                else:
                    print(f'При выполнении команды "{command}" на устройстве {self.ip} возникла ошибка -> {match.group(1)}')

            output_parts.append(output)
        return ''.join(output_parts)


if __name__ == '__main__':
    params = {'ip': '192.168.100.2',
              'username': 'cisco',
              'password': 'cisco',
              'secret': 'cisco'}
    t = CiscoTelnet(**params)

    # ver = t.send_show_command('show version', parse=False)
    # print(ver)
    #
    # int_br = t.send_show_command('sh ip int br', parse=True)
    # print(int_br)

    config_command = 'ip domain-lookup'
    res = t.send_config_commands(config_command, strict=False)
    print(res)
    config_command = 'ip'
    config_commands = ['interface Lo123', 'ip address 1.1.1.1 255.255.255.255', 'xxx']
    res = t.send_config_commands(config_command, strict=False)
    print(res)
    res = t.send_config_commands(config_commands, strict=False)
    print(res)