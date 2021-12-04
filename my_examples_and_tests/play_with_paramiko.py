import paramiko
import time

connection = paramiko.SSHClient()
connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())

connection.connect(hostname='192.168.100.3', username='cisco', password='cisco', allow_agent=False, look_for_keys=False)
ssh = connection.invoke_shell()
ssh.send('enable\n')
time.sleep(1)
print(ssh.recv(1000))
ssh.send('cisco\n')
time.sleep(1)
prompt = ssh.recv(1000)
print(prompt.decode('utf-8'))

