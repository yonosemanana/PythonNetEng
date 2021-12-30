# -*- coding: utf-8 -*-
"""
Задание 20.5a

Создать функцию configure_vpn, которая использует
шаблоны из задания 20.5 для настройки VPN на маршрутизаторах
на основе данных в словаре data.

Параметры функции:
* src_device_params - словарь с параметрами подключения к устройству 1
* dst_device_params - словарь с параметрами подключения к устройству 2
* src_template - имя файла с шаблоном, который создает конфигурацию для строны 1
* dst_template - имя файла с шаблоном, который создает конфигурацию для строны 2
* vpn_data_dict - словарь со значениями, которые надо подставить в шаблоны

Функция должна настроить VPN на основе шаблонов
и данных на каждом устройстве с помощью netmiko.
Функция возвращает кортеж с выводом команд с двух
маршрутизаторов (вывод, которые возвращает метод netmiko send_config_set).
Первый элемент кортежа - вывод с первого устройства (строка),
второй элемент кортежа - вывод со второго устройства.

При этом, в словаре data не указан номер интерфейса Tunnel,
который надо использовать.
Номер надо определить самостоятельно на основе информации с оборудования.
Если на маршрутизаторе нет интерфейсов Tunnel,
взять номер 0, если есть взять ближайший свободный номер,
но одинаковый для двух маршрутизаторов.

Например, если на маршрутизаторе src такие интерфейсы: Tunnel1, Tunnel4.
А на маршрутизаторе dest такие: Tunnel2, Tunnel3, Tunnel8.
Первый свободный номер одинаковый для двух маршрутизаторов будет 5.
И надо будет настроить интерфейс Tunnel 5.

Для этого задания тест проверяет работу функции на первых двух устройствах
из файла devices.yaml. И проверяет, что в выводе есть команды настройки
интерфейсов, но при этом не проверяет настроенные номера тунелей и другие команды.
Они должны быть, но тест упрощен, чтобы было больше свободы выполнения.
"""

from task_20_5 import create_vpn_config
from netmiko import ConnectHandler
import yaml
import re

data = {
    "tun_num": None,
    "wan_ip_1": "192.168.100.1",
    "wan_ip_2": "192.168.100.2",
    "tun_ip_1": "10.0.1.1 255.255.255.252",
    "tun_ip_2": "10.0.1.2 255.255.255.252",
}

def configure_vpn(src_device_params, dst_device_params, src_template, dst_template, vpn_data_dict):
    """
    """

    command = 'show ip int br'
    regex = re.compile(r'Tunnel(?P<tun>\d+)')

    with ConnectHandler(**src_device_params) as ssh1:
        ssh1.enable()
        prompt1 = ssh1.find_prompt()
        show_int_1 = prompt1 + ssh1.send_command(command, strip_prompt=True, strip_command=False)
    tunnels1 = regex.findall(show_int_1)

    with ConnectHandler(**dst_device_params) as ssh2:
        ssh2.enable()
        prompt2 = ssh2.find_prompt()
        show_int_2 = prompt2 + ssh2.send_command(command, strip_prompt=True, strip_command=False)
    tunnels2 = regex.findall(show_int_2)

    # Searching for the least tunnel number common on both source and destination routers.
    n = 0
    while True:
        if str(n) not in tunnels1 and str(n) not in tunnels2:
            break
        else:
            n += 1
    vpn_data_dict['tun_num'] = n

    config1, config2 = create_vpn_config(src_template, dst_template, vpn_data_dict)
    config1 = config1.split('\n')
    config2 = config2.split('\n')

    with ConnectHandler(**src_device_params) as ssh1:
        ssh1.enable()
        prompt1 = ssh1.find_prompt()
        output1 = prompt1 + ssh1.send_config_set(config1, strip_prompt=True, strip_command=False)

    with ConnectHandler(**dst_device_params) as ssh2:
        ssh2.enable()
        prompt2 = ssh2.find_prompt()
        output2 = prompt2 + ssh2.send_config_set(config2, strip_prompt=True, strip_command=False)

    return output1, output2

if __name__ == '__main__':
    template1 = 'templates/gre_ipsec_vpn_1.txt'
    template2 = 'templates/gre_ipsec_vpn_2.txt'

    with open('devices.yaml') as f:
        device1, device2, _ = yaml.safe_load(f)

    output1, output2 = configure_vpn(device1, device2, template1, template2, data)
    print(output1)
    print(output2)

