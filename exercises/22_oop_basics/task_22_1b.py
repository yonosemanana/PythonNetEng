# -*- coding: utf-8 -*-

"""
Задание 22.1b

Изменить класс Topology из задания 22.1a или 22.1.

Добавить метод delete_link, который удаляет указанное соединение.
Метод должен удалять и "обратное" соединение, если оно есть (ниже пример).

Если такого соединения нет, выводится сообщение "Такого соединения нет".

Создание топологии
In [7]: t = Topology(topology_example)

In [8]: t.topology
Out[8]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Удаление линка:
In [9]: t.delete_link(('R3', 'Eth0/1'), ('R4', 'Eth0/0'))

In [10]: t.topology
Out[10]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Удаление "обратного" линка:
в словаре есть запись ``('R3', 'Eth0/2'): ('R5', 'Eth0/0')``, но вызов delete_link
с указанием ключа и значения в обратном порядке, должно удалять соединение:

In [11]: t.delete_link(('R5', 'Eth0/0'), ('R3', 'Eth0/2'))

In [12]: t.topology
Out[12]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3')}

Если такого соединения нет, выводится сообщение:
In [13]: t.delete_link(('R5', 'Eth0/0'), ('R3', 'Eth0/2'))
Такого соединения нет

"""

class Topology:
    def __init__(self, topology_dict):
        self.topology = self._normalize(topology_dict)

    def _normalize(self, topology_dict):
        topology = {}
        for local, remote in topology_dict.items():
            if not topology.get(local) == remote and not topology.get(remote) == local:
                topology[local] = remote
        return topology

    def delete_link(self, local, remote):
        if self.topology.get(local) == remote:
            self.topology.pop(local)
        elif self.topology.get(remote) == local:
            self.topology.pop(remote)
        else:
            print('Такого соединения нет')

topology_example = {
    ("R1", "Eth0/0"): ("SW1", "Eth0/1"),
    ("R2", "Eth0/0"): ("SW1", "Eth0/2"),
    ("R2", "Eth0/1"): ("SW2", "Eth0/11"),
    ("R3", "Eth0/0"): ("SW1", "Eth0/3"),
    ("R3", "Eth0/1"): ("R4", "Eth0/0"),
    ("R3", "Eth0/2"): ("R5", "Eth0/0"),
    ("SW1", "Eth0/1"): ("R1", "Eth0/0"),
    ("SW1", "Eth0/2"): ("R2", "Eth0/0"),
    ("SW1", "Eth0/3"): ("R3", "Eth0/0"),
}

if __name__ == '__main__':
    t = Topology(topology_example)
    print(t.topology)
    t.delete_link(('R5', 'Eth0/0'), ('R3', 'Eth0/2'))
    print(t.topology)
    t.delete_link(("R1", "Eth0/0"), ("SW1", "Eth0/1"))
    print(t.topology)