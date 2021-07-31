# -*- coding: utf-8 -*-
"""
Задание 7.2a

Сделать копию скрипта задания 7.2.

Дополнить скрипт: Скрипт не должен выводить на стандартрый поток вывода команды,
в которых содержатся слова из списка ignore.

При этом скрипт также не должен выводить строки, которые начинаются на !.

Проверить работу скрипта на конфигурационном файле config_sw1.txt.
Имя файла передается как аргумент скрипту.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

from sys import argv


ignore = ["duplex", "alias", "configuration"]


filename = argv[1]

with open(filename) as f:
    for line in f:
        if not line.startswith('!'):
            # ignore_flag = False
            # for word in ignore:
            #     if word in line:
            #         ignore_flag = True
            #         break
            # if not ignore_flag:
            #     print(line.rstrip())
            words = line.split()
            if not set(words) & set(ignore):
                print(line.rstrip())