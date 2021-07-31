# -*- coding: utf-8 -*-
"""
Задание 7.2b

Переделать скрипт из задания 7.2a: вместо вывода на стандартный поток вывода,
скрипт должен записать полученные строки в файл

Имена файлов нужно передавать как аргументы скрипту:
 * имя исходного файла конфигурации
 * имя итогового файла конфигурации

При этом, должны быть отфильтрованы строки, которые содержатся в списке ignore
и строки, которые начинаются на '!'.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

from sys import argv


ignore = ["duplex", "alias", "configuration"]


file_in, file_out = argv[1], argv[2]

with open(file_in) as f_in, open(file_out, 'w') as f_out:
    for line in f_in:
        if not line.startswith('!'):
            words = line.split()
            if not set(words) & set(ignore):
                f_out.write(line)