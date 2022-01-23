from paramiko import SSHClient, AutoAddPolicy
import time

class ConnectSSH:
    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password
        self._MAX_RCV = 65535

        self.ssh = SSHClient()
        self.ssh.set_missing_host_key_policy(AutoAddPolicy())
        self.ssh.connect(hostname=self.hostname, port=22, username=self.username, password=self.password, allow_agent=False, look_for_keys=False)
        self.session = self.ssh.invoke_shell()

    def send_command(self, command):
        self.session.send(command + '\n')
        time.sleep(1)
        output = self.session.recv(self._MAX_RCV).decode('utf-8')
        return output

class CiscoSSH(ConnectSSH):
    def __init__(self, hostname, username, password, enable_password):
        self.enable_password = enable_password
        super().__init__(hostname, username, password)

    def __enter__(self):
        self.send_command('enable')
        self.send_command(self.enable_password)
        self.send_command('terminal length 0')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.ssh.close()

    def conf_t(self):
        output = self.send_command('configure terminal')
        return output

    def exit_config(self):
        output = self.send_command('end')
        return output

    def send_config_commands(self, commands):
        if isinstance(commands, str):
            commands = [commands]
        else:
            self.conf_t()
            for command in commands:
                super().send_command(command)
            self.exit_config()




if __name__ == '__main__':
    params = {'hostname': '192.168.100.1',
              'username': 'cisco',
              'password': 'cisco',
              'enable_password': 'cisco'}
    command = 'show version'
    config_commands = ['interface loopback101', 'ip address 1.1.1.1 255.255.255.255']

    with CiscoSSH(**params) as r1:
        print(r1.send_command(command))
        print()
        print(r1.send_command('show ip int br'))
        r1.send_config_commands(config_commands)
        print(r1.send_command('show ip int br'))