# -*- coding: utf-8 -*-
"""
Задание 5.2a

Всё, как в задании 5.2, но, если пользователь ввел адрес хоста, а не адрес сети,
надо преобразовать адрес хоста в адрес сети и вывести адрес сети и маску,
как в задании 5.2.

Пример адреса сети (все биты хостовой части равны нулю):
* 10.0.1.0/24
* 190.1.0.0/16

Пример адреса хоста:
* 10.0.1.1/24 - хост из сети 10.0.1.0/24
* 10.0.5.195/28 - хост из сети 10.0.5.192/28

Если пользователь ввел адрес 10.0.1.1/24, вывод должен быть таким:

Network:
10        0         1         0
00001010  00000000  00000001  00000000

Mask:
/24
255       255       255       0
11111111  11111111  11111111  00000000


Проверить работу скрипта на разных комбинациях хост/маска, например:
    10.0.5.195/28, 10.0.1.1/24

Вывод сети и маски должен быть упорядочен также, как в примере:
- столбцами
- ширина столбца 10 символов (в двоичном формате
  надо добавить два пробела между столбцами
  для разделения октетов между собой)


Подсказка:
Есть адрес хоста в двоичном формате и маска сети 28. Адрес сети это первые 28 бит
адреса хоста + 4 ноля.
То есть, например, адрес хоста 10.1.1.195/28 в двоичном формате будет
bin_ip = "00001010000000010000000111000011"

А адрес сети будет первых 28 символов из bin_ip + 0000 (4 потому что всего
в адресе может быть 32 бита, а 32 - 28 = 4)
00001010000000010000000111000000

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

prefix = input('Enter prefix in format "10.1.1.0/24": ')
network, mask = prefix.split('/')

host_octets = network.split('.') # A list of octets, i.e. strings of decimals
prefix_len = int(mask.lstrip('/')) # An integer - prefix length
mask_bin = prefix_len * '1' + (32 - prefix_len) * '0' # The mask as string of binary digits

# Mask 4 octets in decimal (int)
m1 = int(mask_bin[:8], 2)
m2 = int(mask_bin[8:16], 2)
m3 = int(mask_bin[16:24], 2)
m4 = int(mask_bin[24:], 2)

# Host 4 octets in decimal (int)
h1 = int(host_octets[0])
h2 = int(host_octets[1])
h3 = int(host_octets[2])
h4 = int(host_octets[3])


net_bin = f'{h1:08b}{h2:08b}{h3:08b}{h4:08b}'[:prefix_len] + (32 - prefix_len) * '0' # The network in binary (str)

# Network 4 octets in decimal (int)
n1 = int(net_bin[:8], 2)
n2 = int(net_bin[8:16], 2)
n3 = int(net_bin[16:24], 2)
n4 = int(net_bin[24:], 2)

tmplt = ('{0:<10}{1:<10}{2:<10}{3:<10}\n'
            '{0:>08b}  {1:>08b}  {2:>08b}  {3:>08b}')

print('Network:')
print(tmplt.format(n1, n2, n3, n4))

print()
print('Mask:')
print('/' + mask)
print(tmplt.format(m1, m2, m3, m4))
