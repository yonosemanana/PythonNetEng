# -*- coding: utf-8 -*-

"""
Задание 23.3a

В этом задании надо сделать так, чтобы экземпляры класса Topology
были итерируемыми объектами.
Основу класса Topology можно взять из любого задания 22.1x или задания 23.3.

После создания экземпляра класса, экземпляр должен работать как итерируемый объект.
На каждой итерации должен возвращаться кортеж, который описывает одно соединение.
Порядок вывода соединений может быть любым.


Пример работы класса:

In [1]: top = Topology(topology_example)

In [2]: for link in top:
   ...:     print(link)
   ...:
(('R1', 'Eth0/0'), ('SW1', 'Eth0/1'))
(('R2', 'Eth0/0'), ('SW1', 'Eth0/2'))
(('R2', 'Eth0/1'), ('SW2', 'Eth0/11'))
(('R3', 'Eth0/0'), ('SW1', 'Eth0/3'))
(('R3', 'Eth0/1'), ('R4', 'Eth0/0'))
(('R3', 'Eth0/2'), ('R5', 'Eth0/0'))


Проверить работу класса.
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

    def __add__(self, other_topology):
        sum_topology = Topology(self.topology.copy())
        for local, remote in other_topology.topology.items():
            sum_topology.add_link(local, remote)
        return sum_topology

    def __iter__(self):
        # return iter([(local, remote) for local, remote in self.topology.items()])
        return iter(self.topology.items())


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
    t1 = Topology(topology_example)
    for link in t1:
        print(link)

