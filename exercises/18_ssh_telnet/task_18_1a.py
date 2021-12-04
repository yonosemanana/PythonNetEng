# -*- coding: utf-8 -*-
"""
Задание 18.1a

Скопировать функцию send_show_command из задания 18.1 и переделать ее таким образом,
чтобы обрабатывалось исключение, которое генерируется при ошибке аутентификации
на устройстве.

При возникновении ошибки, на стандартный поток вывода должно выводиться
сообщение исключения.

Для проверки измените пароль на устройстве или в файле devices.yaml.
"""
import yaml
import netmiko

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
    except netmiko.ssh_exception.NetmikoAuthenticationException as e:
        print(e)
    return res


if __name__ == "__main__":
    command = "sh ip int br"
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)

    for dev in devices:
        print(send_show_command(dev, command))
