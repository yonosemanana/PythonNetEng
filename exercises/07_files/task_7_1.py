# -*- coding: utf-8 -*-
"""
Задание 7.1

Обработать строки из файла ospf.txt и вывести информацию по каждой строке в таком
виде на стандартный поток вывода:

Prefix                10.0.24.0/24
AD/Metric             110/41
Next-Hop              10.0.13.3
Last update           3d18h
Outbound Interface    FastEthernet0/0

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

str_template = '''Prefix                {prefix}
AD/Metric             {metric}
Next-Hop              {next_hop}
Last update           {last_update}
Outbound Interface    {out_intf}
'''

with open('ospf.txt') as f:
    for line in f:
        _, prefix, metric, _, next_hop, last_update, out_intf = line.split()
        metric = metric.strip('[]')
        next_hop = next_hop.rstrip(',')
        last_update = last_update.rstrip(',')
        print(str_template.format(prefix=prefix, metric=metric, next_hop=next_hop, last_update=last_update, out_intf=out_intf))


