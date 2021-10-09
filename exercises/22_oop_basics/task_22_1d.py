# -*- coding: utf-8 -*-

"""
Задание 22.1d

Изменить класс Topology из задания 22.1c

Добавить метод add_link, который добавляет указанное соединение, если его еще
 нет в топологии.
Если соединение существует, вывести сообщение "Такое соединение существует",
Если одна из сторон есть в топологии, вывести сообщение
"Cоединение с одним из портов существует"


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

In [9]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))

In [10]: t.topology
Out[10]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R1', 'Eth0/4'): ('R7', 'Eth0/0'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [11]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))
Такое соединение существует

In [12]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/5'))
Cоединение с одним из портов существует


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

    def delete_node(self, node):
        not_found = True
        tmp_topology = self.topology.copy()
        for local, remote in tmp_topology.items():
            if local[0] == node or remote[0] == node:
                self.delete_link(local, remote)
                not_found = False
        if not_found:
            print('Такого устройства нет')

    def add_link(self, local, remote):
        ports = set(self.topology.keys()) | set(self.topology.values())
        if self.topology.get(local) == remote or self.topology.get(remote) == local:
            print('Такое соединение существует')
        elif local in ports or remote in ports:
            print('Cоединение с одним из портов существует')
        else:
            self.topology[local] = remote

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
    t.add_link(('R1', 'Eth0/0'), ('SW10', 'Eth1/1'))
    t.add_link(('SW10', 'Eth1/2'), ('R5', 'Eth0/0'))
    t.add_link(('R1', 'Eth0/0'), ('SW1', 'Eth0/1'))
    t.add_link(('R4', 'Eth0/1'), ('SW10', 'Eth1/4'))
    print(t.topology)