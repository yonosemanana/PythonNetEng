import paramiko
import time
from pprint import pprint

def send_show_commands(
        ip,
        username,
        password,
        enable_password,
        commands
    ):
    connection = paramiko.SSHClient()
    connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    connection.connect(hostname=ip,
                       username=username,
                       password=password,
                       allow_agent=False,
                       look_for_keys=False)

    results = {}
    
    with connection.invoke_shell() as ssh:
        ssh.send('enable\n')
        ssh.send(f'{enable_password}\n')
        ssh.send('terminal length 0\n')
        time.sleep(1)
        ssh.recv(1000000)

        for command in commands:
            ssh.send(command + '\n')
            time.sleep(1)
            output = ssh.recv(1000000).decode('utf-8')
            results[command] = output

    return results


if __name__ == '__main__':
    devices = ['192.168.100.1', '192.168.100.2', '192.168.100.3']
    commands = ['show version', 'show cdp neighbors']
    results = [send_show_commands(device, 'cisco', 'cisco', 'cisco', commands) for device in devices]
    pprint(results, width=120)