# -*- coding: utf-8 -*-
"""
Задание 18.1b

Скопировать функцию send_show_command из задания 18.1a и переделать ее таким образом,
чтобы обрабатывалось не только исключение, которое генерируется при ошибке
аутентификации на устройстве, но и исключение, которое генерируется, когда IP-адрес
устройства недоступен.

При возникновении ошибки, на стандартный поток вывода должно выводиться
сообщение исключения.

Для проверки измените IP-адрес на устройстве или в файле devices.yaml.
"""

import yaml
import netmiko
from netmiko.ssh_exception import NetmikoAuthenticationException, NetmikoTimeoutException

def send_show_command(device, command):
    """
    :params: device - a dictionary with the params to SSH to the device
    :params: command - a command (string) to be executed on the device
    """
    res = ''

    try:
        with netmiko.ConnectHandler(**device) as connect:
            res = connect.send_command(command)
            # print(res)
    except NetmikoAuthenticationException as auth_error:
        print(auth_error)
    except NetmikoTimeoutException as timeout_error:
        print(timeout_error)
    return res


if __name__ == "__main__":
    command = "sh ip int br"
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)

    for dev in devices:
        print(send_show_command(dev, command))
