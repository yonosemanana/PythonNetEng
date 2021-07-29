# -*- coding: utf-8 -*-
"""
Задание 6.2b

Сделать копию скрипта задания 6.2a.

Дополнить скрипт: Если адрес был введен неправильно, запросить адрес снова.

Если адрес задан неправильно, выводить сообщение: 'Неправильный IP-адрес'
Сообщение "Неправильный IP-адрес" должно выводиться только один раз,
даже если несколько пунктов выше не выполнены.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""


# while True:
#     ip = input("Enter IP address in format '10.0.1.1': ")
#
#     octs = ip.split('.')
#
#     try:
#         if len(octs) != 4:
#             raise Exception("IP address must contain for octets divided by dots (.)!")
#
#         for o in octs:
#             o = int(o)
#             if not 0 <= o <= 255:
#                 raise Exception("Octets must be digits in range from 0 to 255!")
#     except Exception:
#         print("Неправильный IP-адрес")
#     else:
#         oct = int(octs[0])
#
#         if 1<= oct < 224:
#             print('unicast')
#         elif 224 <= oct < 240:
#             print('multicast')
#         elif ip == '255.255.255.255':
#             print('local broadcast')
#         elif ip == '0.0.0.0':
#             print('unassigned')
#         else:
#             print('unused')
#         break



correct_ip = False

while not correct_ip:
    ip = input("Enter IP address in format '10.0.1.1': ")

    octs = ip.split('.')

    try:
        if len(octs) != 4:
            raise Exception("IP address must contain for octets divided by dots (.)!")

        for o in octs:
            o = int(o)
            if not 0 <= o <= 255:
                raise Exception("Octets must be digits in range from 0 to 255!")
    except Exception:
        print("Неправильный IP-адрес")
    else:
        correct_ip = True

oct = int(octs[0])

if 1<= oct < 224:
    print('unicast')
elif 224 <= oct < 240:
    print('multicast')
elif ip == '255.255.255.255':
    print('local broadcast')
elif ip == '0.0.0.0':
    print('unassigned')
else:
    print('unused')
