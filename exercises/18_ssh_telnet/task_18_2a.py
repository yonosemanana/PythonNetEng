# -*- coding: utf-8 -*-
"""
Задание 18.2a

Скопировать функцию send_config_commands из задания 18.2 и добавить параметр log,
который контролирует будет ли выводится на стандартный поток вывода информация о том
к какому устройству выполняется подключение.
По умолчанию, результат должен выводиться.

Пример работы функции:

In [13]: result = send_config_commands(r1, commands)
Подключаюсь к 192.168.100.1...

In [14]: result = send_config_commands(r1, commands, log=False)

In [15]:

Скрипт должен отправлять список команд commands на все устройства
из файла devices.yaml с помощью функции send_config_commands.
"""


import yaml
from netmiko import ConnectHandler
from netmiko.ssh_exception import SSHException

def send_config_commands(device, commands, log=True):
    """
    :params: device - a dictionary with the params to SSH to the device
    :params: command - a command (string) to be executed on the device
    :params: log - whether print info about the current connection or not (default=True)
    """
    res = ''
    try:
        with ConnectHandler(**device) as ssh:
            if log:
                print(f'Подключаюсь к {device["host"]}...')
            ssh.enable()
            res = ssh.send_config_set(commands)

            # config_check = ssh.send_command('show run')
            # print(config_check)

    except SSHException as error:
        print(error)

    return res

commands = ["logging 10.255.255.1", "logging buffered 20010", "no logging console"]


if __name__ == '__main__':
    with open('devices.yaml') as f:
        devices = yaml.safe_load(f)
        # print(devices)

    for device in devices:
        print(send_config_commands(device, commands))
