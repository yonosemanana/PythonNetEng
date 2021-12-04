import pexpect
import re
from pprint import pprint

def send_show_commands(ip, username, password, enable, commands, prompt='#'):
    with pexpect.spawn(f'ssh {username}@{ip}', timeout=10, encoding='utf-8') as ssh:
        ssh.expect('[Pp]assword:')
        ssh.sendline(password)
        enable_status = ssh.expect(['>', '#'])

        if enable_status == 0:
            ssh.sendline('enable')
            ssh.expect('[Pp]assword:')
            ssh.sendline(enable)
            ssh.expect(prompt)

        ssh.sendline('terminal length 0')
        ssh.expect(prompt)

        result = {}
        for command in commands:
            ssh.sendline(command)
            response = ssh.expect([prompt, pexpect.TIMEOUT, pexpect.EOF])
            if response == 2:
                print('Connection terminated by remote device!')
            elif response == 1:
                print('Timeout!')
            else:
                output = ssh.before
                result[command] = re.sub('\r\n', '\n', output)

        return result

def send_show_commands_2(ip, username, password, enable, commands, prompt='#'):
    with pexpect.spawn(f'ssh {username}@{ip}', timeout=10, encoding='utf-8') as ssh:
        ssh.expect('[Pp]assword:')
        ssh.sendline(password)
        enable_status = ssh.expect(['>', '#'])

        if enable_status == 0:
            ssh.sendline('enable')
            ssh.expect('[Pp]assword:')
            ssh.sendline(enable)
            ssh.expect(prompt)

        result = {}
        for command in commands:
            ssh.sendline(command)
            # ssh.sendline('') # Scroll "--More--" page
            output = ''

            while True:
                response = ssh.expect([prompt, '--More--', pexpect.TIMEOUT, pexpect.EOF])
                if response == 3:
                    print('Connection terminated by remote device!')
                elif response == 2:
                    print('Timeout!')
                elif response == 1:
                    output += ssh.before
                    ssh.send(' ') # Scrolling "--More--" page with "Space". Using send(), not sendline(), because sendline() adds '\n' at the end of the line.
                else:
                    output += ssh.before
                    result[command] = re.sub('\r\n', '\n', re.sub(' +\x08+', '', output))
                    break

        return result

if __name__ == '__main__':
    devices = ['192.168.100.1', '192.168.100.2', '192.168.100.3']
    commands = ['show version', 'show ip int br']
    for ip in devices:
        result = send_show_commands_2(ip,'cisco', 'cisco', 'cisco', commands)
        pprint(result, width=120)