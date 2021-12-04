import pexpect

from getpass import getpass

# out1 = pexpect.run('pwd').decode('utf-8')
# print(out1)
# out2 = pexpect.run('ls -l').decode('utf-8')
# print(out2)

password = getpass('Input password: ')

pwd = pexpect.spawn('pwd')
# print(pwd)
print(pwd.before)
pwd.expect(pexpect.EOF)
print(pwd.before.decode('utf-8'))

connection = pexpect.spawn('ssh cisco@192.168.100.3', encoding='utf-8')

code1 = connection.expect(['Password: ', pexpect.TIMEOUT, pexpect.EOF])
print(code1)
connection.sendline(password)
connection.expect('>')
print(connection.before)

connection.sendline('enable')
code2 = connection.expect(['Password: ', pexpect.TIMEOUT, pexpect.EOF])
print(code2)

connection.sendline(password)
code3 = connection.expect(['#', pexpect.TIMEOUT, pexpect.EOF])
print(code3)
print(connection.before)

connection.sendline('terminal length 0')
code4 = connection.expect(['#', pexpect.TIMEOUT, pexpect.EOF])
print(code4)
print(connection.before)

connection.sendline('show ip interface brief')
code5 = connection.expect(['#', pexpect.TIMEOUT, pexpect.EOF])
print(code5)
print(connection.before)
