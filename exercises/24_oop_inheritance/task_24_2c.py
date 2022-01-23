# -*- coding: utf-8 -*-

"""
Задание 24.2c

Скопировать класс MyNetmiko из задания 24.2b.
Проверить, что метод send_command кроме команду, принимает еще и дополнительные
аргументы, например, strip_command.

Если возникает ошибка, переделать метод таким образом, чтобы он принимал
любые аргументы, которые поддерживает netmiko.


In [2]: from task_24_2c import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [4]: r1.send_command('sh ip int br', strip_command=False)
Out[4]: 'sh ip int br\nInterface                  IP-Address      OK? Method Status                Protocol\nEthernet0/0                192.168.100.1   YES NVRAM  up                    up      \nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \nEthernet0/2                190.16.200.1    YES NVRAM  up                    up      \nEthernet0/3                192.168.230.1   YES NVRAM  up                    up      \nEthernet0/3.100            10.100.0.1      YES NVRAM  up                    up      \nEthernet0/3.200            10.200.0.1      YES NVRAM  up                    up      \nEthernet0/3.300            10.30.0.1       YES NVRAM  up                    up      '

In [5]: r1.send_command('sh ip int br', strip_command=True)
Out[5]: 'Interface                  IP-Address      OK? Method Status                Protocol\nEthernet0/0                192.168.100.1   YES NVRAM  up                    up      \nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \nEthernet0/2                190.16.200.1    YES NVRAM  up                    up      \nEthernet0/3                192.168.230.1   YES NVRAM  up                    up      \nEthernet0/3.100            10.100.0.1      YES NVRAM  up                    up      \nEthernet0/3.200            10.200.0.1      YES NVRAM  up                    up      \nEthernet0/3.300            10.30.0.1       YES NVRAM  up                    up      '

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
    print(r1.send_command('show ip int br', strip_command=False))

    # commands = ['int Loopback 102 ', 'ip address 101.1.1.1 255.255.255.255', 'e']
    # print(r1.send_config_set(commands))
    # commands = 'no int Loopback 102'
    # print(r1.send_config_set(commands))