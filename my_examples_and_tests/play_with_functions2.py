import time
from string import ascii_lowercase
from pprint import pprint

def ignore_command(command):
    '''
    Функция проверяет содержится ли в команде слово из списка ignore.
    * command - строка. Команда, которую надо проверить
    * Возвращает True, если в команде содержится слово из списка ignore, False - если нет
    '''
    ignore = ['duplex', 'alias', 'Current configuration']

    for word in ignore:
        if word in command:
            return True
    return False

def ignore_command_2(command):
    '''
    Функция проверяет содержится ли в команде слово из списка ignore.
    * command - строка. Команда, которую надо проверить
    * Возвращает True, если в команде содержится слово из списка ignore, False - если нет
    '''
    ignore = ['duplex', 'alias', 'Current configuration']

    return any(word in command for word in ignore)


s1 = 'Hello, world!'
s2 = 'I love you!'
print(s1, s2)
print(s1, s2, sep=' ### ')
print(s1, s2, sep=' | ', end=' ?$@&%@!#$@TQ@#@')
print('a')

with open('print_file.txt', 'w') as f:
    print('''Hello, world!
    This is my first time I use print() to write to a file!''', file=f)


for num in range(10):
    print(num)
    time.sleep(0.5)

# for num in range(10):
#     print(num, end=' ')
#     time.sleep(1)

print()
print(type(enumerate(ascii_lowercase)))

for num, letter in enumerate(ascii_lowercase, 1):
    print(num, letter)

l1 = ['a', 'b', 'c']
l2 = [1, 2, 3, 4, 5]
z = zip(l1, l2)
print(z)
lz = list(z)
print(lz)

l = ['model', 'OS', 'version', 'mgmt IP']
device1 = ['ISR4431', 'IOS XE', '3.6.0', '10.200.10.1']

d = dict(zip(l, device1))
print(d, type(d))


d_keys = ['hostname', 'location', 'vendor', 'model', 'IOS', 'IP']

data = {
'r1': ['london_r1', '21 New Globe Walk', 'Cisco', '4451', '15.4', '10.255.0.1'],
'r2': ['london_r2', '21 New Globe Walk', 'Cisco', '4451', '15.4', '10.255.0.2'],
'sw1': ['london_sw1', '21 New Globe Walk', 'Cisco', '3850', '3.6.XE', '10.255.0.101']
}

london_co = {}

for key, item in data.items():
    london_co[key] = dict(zip(d_keys, item))

print(london_co)

print(ignore_command('duplex 1000'))
print(ignore_command('vlan 100'))
print(ignore_command_2('duplex 1000'))
print(ignore_command_2('vlan 100'))

ip_1 = '10.1.1.10'
ip_2 = '10.1.1.a'
print(all(octet.isdigit() for octet in ip_1.split('.')))
print(all(octet.isdigit() for octet in ip_2.split('.')))

l = [1, 2, 7, 5, 10, -1, 3]
rev_sort = lambda l: sorted(l,reverse=True)
print(rev_sort(l))

macs = []
with open('show_mac.txt') as f:
    for line in f:
        if 'Port' not in line:
            mac, port, _, _, vlan = line.split()
            macs.append((mac, port, vlan))

pprint(sorted(macs))
print('='*30)
pprint(sorted(macs, key = lambda t: t[2]))

l_sq2 = [n ** 2 for n in range(1, 10)]
print(l_sq2)
l_sq = list(map(lambda x: x ** 2, range(1, 10)))
print(l_sq)

l_even = list(filter(lambda x: x % 2 ==0, range(1, 10)))
print(l_even)

l1 = [3, 1, 7, 5, 10, 6]
l2 = [0, 4, 2, 5, 9, 4]
print(list(map(lambda x, y: x <= y, l1, l2)))
print(list(map(str, l1)))
