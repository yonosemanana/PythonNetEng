import ipaddress
import paramiko

class Switch(object):
    vendor = 'cisco'

    __test_var = 'test'

    def __test_func(self):
        print("From class Switch____")

    def test_func_2(self):
        print("From class Switch!")

class CiscoSwitch(Switch):

    def __test_func(self):
        print("From class CiscoSwitch____!")

    def test_func_2(self):
        print("From class CiscoSwitch!")


class IPAddress:
    def __init__(self, ip):
        self.ip = ip

    def __str__(self):
        return f"IP address is: {self.ip}"

    def __repr__(self):
        return f"In __repr__ function IP address is {self.ip} too."

    def __add__(self, n):
        if not isinstance(n, int):
            raise TypeError(f'unsupported operand type(s) for +: "IPAddress" and "{type(n).__name__}"')
        else:
            return IPAddress(ipaddress.IPv4Address(self.ip) + n)

class Network:
    def __init__(self, network):
        self.addresses = [str(ip) for ip in ipaddress.IPv4Network(network).hosts()]
        self.index = 0

    def __next__(self):
        print('Running __next__')
        if self.index < len(self.addresses):
            current_address = self.addresses[self.index]
            self.index += 1
            return current_address
        else:
            raise StopIteration

    def __iter__(self):
        print('Running __iter__')
        # return self
        return iter(self.addresses)

    def __getitem__(self, n):
        print('Running __getitem__')
        return self.addresses[n]

    def __len__(self):
        print('Running __len__')
        return len(self.addresses)

class CiscoSSH:
    def __init__(self, hostname, username, password):
        print('Running __init__')
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.hostname = hostname
        self.username = username
        self.password = password
        self.ssh.connect(hostname=self.hostname, port=22, username=self.username, password=self.password, look_for_keys=False, allow_agent=False)

    def send_command(self, command):
        stdin, stdout, stderr = self.ssh.exec_command(command)
        return stdin, stdout, stderr

    def __enter__(self):
        print('Running __enter__')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print('Running __exit__')
        print(f'Exception type: {exc_type}', f'Exception value: {exc_value}', f'Traceback: {traceback}', sep='\n')
        self.ssh.close()


print(__name__)
print(__file__)

sw1 = Switch()
sw2 = CiscoSwitch()
print(type(sw1))
print(type(sw2))
print(dir(sw1))
print(dir(sw2))
sw2.test_func_2()

ip1 = IPAddress('10.10.1.1')
ip2 = IPAddress('10.10.1.2')

ips = [ip1, ip2]
print(ip1)
print(ip2)
print(ips)
print(f'ip1 + 10 = {ip1 + 10}')
print(type(ip2 + 20))
# print(ip2 + 'x')
# print(ip1 + ip2)

net1 = Network('10.1.0.0/29')
print(next(net1))
for n in net1:
    print(n)
print('Repeat the iterator again')
for n in net1:
    print(n)

print(net1[0])
print(net1[1])
print(net1[2:5])
# print(net1[10])
print(len(net1))

params = {'hostname': '192.168.100.1',
          'username': 'cisco',
          'password': 'cisco'
          }

command = 'show ip int br'

ssh_r1 = CiscoSSH(**params)
stdin, stdout, stderr = ssh_r1.send_command(command)
print(stdout.read().decode('utf-8'))

params_r2 = {'hostname': '192.168.100.2',
          'username': 'cisco',
          'password': 'cisco'
          }
command2 = 'show version'
with CiscoSSH(**params_r2) as ssh_r2:
    stdin, stdout, stderr = ssh_r2.send_command(command2)
    print(stdout.read().decode('utf-8'))

with CiscoSSH('192.168.100.3', 'cisco', 'cisco') as ssh_r3:
    stdin, stdout, stderr = ssh_r3.send_command(command2)
    stderr / 2
    print(stdout.read().decode('utf-8'))