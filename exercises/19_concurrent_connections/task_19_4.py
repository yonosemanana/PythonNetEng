# -*- coding: utf-8 -*-
"""
Задание 19.4

Создать функцию send_commands_to_devices, которая отправляет команду show или config
на разные устройства в параллельных потоках, а затем записывает вывод команд в файл.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* filename - имя файла, в который будут записаны выводы всех команд
* show - команда show, которую нужно отправить (по умолчанию, значение None)
* config - команды конфигурационного режима, которые нужно отправить (по умолчанию None)
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Аргументы show, config и limit должны передаваться только как ключевые. При передачи
этих аргументов как позиционных, должно генерироваться исключение TypeError.

In [4]: send_commands_to_devices(devices, 'result.txt', 'sh clock')
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-4-75adcfb4a005> in <module>
----> 1 send_commands_to_devices(devices, 'result.txt', 'sh clock')

TypeError: send_commands_to_devices() takes 2 positional argument but 3 were given


При вызове функции send_commands_to_devices, всегда должен передаваться
только один из аргументов show, config. Если передаются оба аргумента, должно
генерироваться исключение ValueError.


Вывод команд должен быть записан в файл в таком формате
(перед выводом команды надо написать имя хоста и саму команду):

R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh arp
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  192.168.100.1          76   aabb.cc00.6500  ARPA   Ethernet0/0
Internet  192.168.100.2           -   aabb.cc00.6600  ARPA   Ethernet0/0
Internet  192.168.100.3         173   aabb.cc00.6700  ARPA   Ethernet0/0
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down

Пример вызова функции:
In [5]: send_commands_to_devices(devices, 'result.txt', show='sh clock')

In [6]: cat result.txt
R1#sh clock
*04:56:34.668 UTC Sat Mar 23 2019
R2#sh clock
*04:56:34.687 UTC Sat Mar 23 2019
R3#sh clock
*04:56:40.354 UTC Sat Mar 23 2019

In [11]: send_commands_to_devices(devices, 'result.txt', config='logging 10.5.5.5')

In [12]: cat result.txt
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#logging 10.5.5.5
R1(config)#end
R1#
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R2(config)#logging 10.5.5.5
R2(config)#end
R2#
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R3(config)#logging 10.5.5.5
R3(config)#end
R3#

In [13]: commands = ['router ospf 55', 'network 0.0.0.0 255.255.255.255 area 0']

In [13]: send_commands_to_devices(devices, 'result.txt', config=commands)

In [14]: cat result.txt
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#router ospf 55
R1(config-router)#network 0.0.0.0 255.255.255.255 area 0
R1(config-router)#end
R1#
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R2(config)#router ospf 55
R2(config-router)#network 0.0.0.0 255.255.255.255 area 0
R2(config-router)#end
R2#
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R3(config)#router ospf 55
R3(config-router)#network 0.0.0.0 255.255.255.255 area 0
R3(config-router)#end
R3#


Для выполнения задания можно создавать любые дополнительные функции.
"""

import logging
import yaml
from concurrent.futures import ThreadPoolExecutor, as_completed
from netmiko import ConnectHandler

def send_show_command(device, commands):
    """
    """
    ssh = ConnectHandler(**device)
    ssh.enable()
    output = ''
    for command in commands:
        prompt = ssh.find_prompt()
        output = output + '\n' + prompt + ssh.send_command(command, strip_prompt=True, strip_command=False)

    return output

def send_config_command(device, commands):
    """
    """
    ssh = ConnectHandler(**device)
    ssh.enable()
    output = ''
    prompt = ssh.find_prompt()
    output = output + '\n' + prompt + ssh.send_config_set(commands, strip_prompt=True, strip_command=False)

    return output

def send_commands_to_devices(devices, filename, *, show=None, config=None, limit=3):
    """
    """
    if show and config:
        raise ValueError

    if isinstance(show, str):
        commands = [show]
        send_func = send_show_command
    elif isinstance(show, list):
        commands = show
        send_func = send_show_command
    elif isinstance(config, str):
        commands = [config]
        send_func = send_config_command
    elif isinstance(config, list):
        commands = config
        send_func = send_config_command

    logging.basicConfig(filename=filename, filemode='a', format='%(message)s', level=logging.INFO, force=True)
    logging.getLogger('paramiko').setLevel(logging.WARNING)

    with ThreadPoolExecutor(max_workers=limit) as executor:
        futures = []
        for device in devices:
            future = executor.submit(send_func, device, commands)
            futures.append(future)

    for future in as_completed(futures):
        logging.info(future.result())




if __name__ == '__main__':
    with open('devices.yaml') as f:
        devices = yaml.safe_load(f)

    # show_commands = 'show version'
    show_commands = ['show ip int br', 'show clock']

    # config_commands = 'logging 10.10.5.5'
    config_commands = ['router ospf 1', 'network 10.0.0.0 0.0.0.255 area 0']

    params_show = {'devices': devices,
              'show': show_commands,
              'filename': 'test_19_4.txt',
              'limit': 3}
    send_commands_to_devices(**params_show)

    params_config = {'devices': devices,
              'config': config_commands,
              'filename': 'test_19_4.txt',
              'limit': 3}
    send_commands_to_devices(**params_config)