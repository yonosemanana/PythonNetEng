# -*- coding: utf-8 -*-
"""
Задание 19.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.
Проверка IP-адресов должна выполняться параллельно в разных потоках.

Параметры функции ping_ip_addresses:
* ip_list - список IP-адресов
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для выполнения задания можно создавать любые дополнительные функции.

Для проверки доступности IP-адреса, используйте ping.

Подсказка о работе с concurrent.futures:
Если необходимо пинговать несколько IP-адресов в разных потоках,
надо создать функцию, которая будет пинговать один IP-адрес,
а затем запустить эту функцию в разных потоках для разных
IP-адресов с помощью concurrent.futures (это надо сделать в функции ping_ip_addresses).
"""

from concurrent.futures import ThreadPoolExecutor
import subprocess

def ping_ip(ip, count=5, timeout=1):
    """

    """

    res = subprocess.run(['ping', f'-c {count}', f'-W {timeout}', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if res.returncode:
        return False, {'ip': ip, 'output': res.stdout + res.stderr}
    else:
        return True, {'ip': ip, 'output': res.stdout}

def ping_ip_addresses(ip_list, limit=3):
    """

    """
    pingable = []
    non_pingable = []
    with ThreadPoolExecutor(max_workers=limit) as executor:
        results = executor.map(ping_ip, ip_list)

        for response, res in results:
            if response:
                pingable.append(res['ip'])
            else:
                non_pingable.append(res['ip'])

    return pingable, non_pingable