# -*- coding: utf-8 -*-
"""
Задание 18.2c

Скопировать функцию send_config_commands из задания 18.2b и переделать ее таким образом:

Если при выполнении команды возникла ошибка, спросить пользователя надо ли выполнять
остальные команды.

Варианты ответа [y]/n:
* y - выполнять остальные команды. Это значение по умолчанию,
  поэтому нажатие любой комбинации воспринимается как y
* n или no - не выполнять остальные команды

Функция send_config_commands по-прежнему должна возвращать кортеж из двух словарей:
* первый словарь с выводом команд, которые выполнились без ошибки
* второй словарь с выводом команд, которые выполнились с ошибками

Оба словаря в формате
* ключ - команда
* значение - вывод с выполнением команд

Проверить работу функции можно на одном устройстве.

Пример работы функции:

In [11]: result = send_config_commands(r1, commands)
Подключаюсь к 192.168.100.1...
Команда "logging 0255.255.1" выполнилась с ошибкой "Invalid input detected at '^' marker." на устройстве 192.168.100.1
Продолжать выполнять команды? [y]/n: y
Команда "logging" выполнилась с ошибкой "Incomplete command." на устройстве 192.168.100.1
Продолжать выполнять команды? [y]/n: n

In [12]: pprint(result)
({},
 {'logging': 'config term\n'
             'Enter configuration commands, one per line.  End with CNTL/Z.\n'
             'R1(config)#logging\n'
             '% Incomplete command.\n'
             '\n'
             'R1(config)#',
  'logging 0255.255.1': 'config term\n'
                        'Enter configuration commands, one per line.  End with '
                        'CNTL/Z.\n'
                        'R1(config)#logging 0255.255.1\n'
                        '                   ^\n'
                        "% Invalid input detected at '^' marker.\n"
                        '\n'
                        'R1(config)#'})

"""

# списки команд с ошибками и без:

from pprint import pprint
from netmiko import ConnectHandler
from netmiko.ssh_exception import SSHException
import re

def send_config_commands(device, commands, log=True):
    """
    :params: device - a dictionary with the params to SSH to the device
    :params: command - a command (string) to be executed on the device
    :params: log - whether print info about the current connection or not (default=True)
    """
    res_okay = {}
    res_errors = {}

    err_msg_template = 'Команда "{command}" выполнилась с ошибкой "{error}" на устройстве {device}'

    try:
        with ConnectHandler(**device) as ssh:
            if log:
                print(f'Подключаюсь к {device["host"]}...')
            ssh.enable()

            for command in commands:
                res = ssh.send_config_set(command)
                m = re.search('% .*\n', res)
                if m:
                    res_errors[command] = res
                    print(err_msg_template.format(command=command, error=m.group().strip(), device=ssh.host))

                    question = input('Продолжать выполнять команды? [y]/n: ')
                    if question in ['n', 'no']:
                        break
                    else:
                        continue
                else:
                    res_okay[command] = res

    except SSHException as error:
        print(error)

    return res_okay, res_errors


# списки команд с ошибками и без:
commands_with_errors = ["logging 0255.255.1", "logging", "a"]
correct_commands = ["logging buffered 20010", "ip http server"]

commands = commands_with_errors + correct_commands


if __name__ == '__main__':
    device = {
       'device_type': 'cisco_ios',
        'host': '192.168.100.2',
        'username': 'cisco',
        'password': 'cisco',
        'secret': 'cisco',
        'timeout': 10
    }
    commands_ok, commands_err = send_config_commands(device, commands)
    pprint(commands_ok)
    pprint(commands_err)