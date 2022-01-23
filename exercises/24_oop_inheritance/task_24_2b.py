# -*- coding: utf-8 -*-

"""
Задание 24.2b

Скопировать класс MyNetmiko из задания 24.2a.

Дополнить функционал метода send_config_set netmiko и добавить в него проверку
на ошибки с помощью метода _check_error_in_command.

Метод send_config_set должен отправлять команды по одной и проверять каждую на ошибки.
Если при выполнении команд не обнаружены ошибки, метод send_config_set возвращает
вывод команд.

In [2]: from task_24_2b import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [4]: r1.send_config_set('lo')
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-2-8e491f78b235> in <module>()
----> 1 r1.send_config_set('lo')

...
ErrorInCommand: При выполнении команды "lo" на устройстве 192.168.100.1 возникла ошибка "Incomplete command."

"""

from netmiko.cisco.cisco_ios import CiscoIosSSH
import re

class ErrorInCommand(Exception):
    """
    Исключение генерируется, если при выполнении команды на оборудовании,
    возникла ошибка.
    """

class MyNetmiko(CiscoIosSSH):
    def __init__(self, **params):
        super().__init__(**params)
        # super().enable()
        self.enable()

    def send_command(self, command, *args, **kwargs):
        output = super().send_command(command, *args, **kwargs)
        self._check_error_in_command(command, output)
        return output

    def _check_error_in_command(self, command, output):
        regex = r'%(?P<error>.*)'
        match = re.search(regex, output)
        if match:
            error_msg = match.group('error')
            raise ErrorInCommand(f'ErrorInCommand: При выполнении команды "{command}" на устройстве {self.host} возникла ошибка "{error_msg}"')

    def send_config_set(self, commands, *args, **kwargs):
        total_output = ''
        if isinstance(commands, str):
            commands = [commands]
        for command in commands:
            output = super().send_config_set(command, *args, exit_config_mode=False, **kwargs)
            self._check_error_in_command(command, output)
            total_output += output
        return total_output


device_params = {
    "device_type": "cisco_ios",
    "ip": "192.168.100.1",
    "username": "cisco",
    "password": "cisco",
    "secret": "cisco",
}

if __name__ == '__main__':
    r1 = MyNetmiko(**device_params)
    # print(r1.send_command('show'))
    # print(r1.send_command('show verxsion'))
    # print(r1.send_command('show interface Ethernet'))
    commands = ['int Loopback 102 ', 'ip address 101.1.1.1 255.255.255.255', 'e']
    print(r1.send_config_set(commands))
    commands = 'no int Loopback 102'
    print(r1.send_config_set(commands))