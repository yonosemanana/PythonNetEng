# -*- coding: utf-8 -*-

"""
Задание 24.2d

Скопировать класс MyNetmiko из задания 24.2c или задания 24.2b.

Добавить параметр ignore_errors в метод send_config_set.
Если передано истинное значение, не надо выполнять проверку на ошибки и метод должен
работать точно так же как метод send_config_set в netmiko.
Если значение ложное, ошибки должны проверяться.

По умолчанию ошибки должны игнорироваться.


In [2]: from task_24_2d import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [6]: r1.send_config_set('lo')
Out[6]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\nR1(config)#lo\n% Incomplete command.\n\nR1(config)#end\nR1#'

In [7]: r1.send_config_set('lo', ignore_errors=True)
Out[7]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\nR1(config)#lo\n% Incomplete command.\n\nR1(config)#end\nR1#'

In [8]: r1.send_config_set('lo', ignore_errors=False)
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-8-704f2e8d1886> in <module>()
----> 1 r1.send_config_set('lo', ignore_errors=False)

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

    def send_config_set(self, commands, ignore_errors=True, *args, **kwargs):
        total_output = ''
        if isinstance(commands, str):
            commands = [commands]
        for command in commands:
            output = super().send_config_set(command, *args, exit_config_mode=False, **kwargs)
            if not ignore_errors:
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
    commands = ['int Loopback 102 ', 'ip address 101.1.1.1 255.255.255.255', 'fdfd']
    print(r1.send_config_set(commands, ignore_errors=False))
    # commands = 'no int Loopback 102'
    # print(r1.send_config_set(commands))