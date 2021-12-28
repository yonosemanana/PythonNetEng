# -*- coding: utf-8 -*-
"""
Задание 19.3

Создать функцию send_command_to_devices, которая отправляет разные
команды show на разные устройства в параллельных потоках, а затем записывает
вывод команд в файл. Вывод с устройств в файле может быть в любом порядке.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* commands_dict - словарь в котором указано на какое устройство отправлять
  какую команду. Пример словаря - commands
* filename - имя файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Вывод команд должен быть записан в файл в таком формате (перед выводом
команды надо написать имя хоста и саму команду):

R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh int desc
Interface                      Status         Protocol Description
Et0/0                          up             up
Et0/1                          up             up
Et0/2                          admin down     down
Et0/3                          admin down     down
Lo9                            up             up
Lo19                           up             up
R3#sh run | s ^router ospf
router ospf 1
 network 0.0.0.0 255.255.255.255 area 0


Для выполнения задания можно создавать любые дополнительные функции.

Проверить работу функции на устройствах из файла devices.yaml и словаре commands
"""

# Этот словарь нужен только для проверки работа кода, в нем можно менять IP-адреса
# тест берет адреса из файла devices.yaml
import logging
import yaml
from concurrent.futures import ThreadPoolExecutor, as_completed
from netmiko import ConnectHandler

def send_show_command(device, command):
    """
    """
    ssh = ConnectHandler(**device)
    ssh.enable()
    prompt = ssh.find_prompt()
    output = prompt + ssh.send_command(command, strip_prompt=True, strip_command=False)
    logging.info(output)

def send_command_to_devices(devices, commands_dict, filename, limit=3):
    """
    """
    logging.basicConfig(filename=filename, filemode='w', format='%(message)s', level=logging.INFO, force=True)
    logging.getLogger('paramiko').setLevel(logging.WARNING)

    with ThreadPoolExecutor(max_workers=limit) as executor:
        for device in devices:
            command = commands_dict[device['host']]
            executor.submit(send_show_command, device, command)


commands = {
    "192.168.100.3": "sh run | s ^router ospf",
    "192.168.100.1": "sh ip int br",
    "192.168.100.2": "sh int desc",
}

if __name__ == '__main__':
    with open('devices.yaml') as f:
        devices = yaml.safe_load(f)

    params = {'devices': devices,
              'commands_dict': commands,
              'filename': 'test_19_3.txt',
              'limit': 3}
    send_command_to_devices(**params)