import subprocess
import os
import time

import paramiko
from getpass import getpass

s = subprocess.run(['ls', '-l'], stdout=subprocess.PIPE)
# print(s)
# print(type(s))
print(s.stdout)

s1 = s.stdout.decode('utf-8')
print(s1)

su1 = subprocess.run(['echo', '$PATH'], stdout=subprocess.PIPE, encoding='utf-8')
print(su1.stdout)
su2 = subprocess.run(['echo', '"$PATH"'], stdout=subprocess.PIPE, encoding='utf-8')
print(su2.stdout)
os_path = os.environ['PATH']
su3 = subprocess.run(['echo', os_path], stdout=subprocess.PIPE, encoding='utf-8')
print(su3.stdout)
os_path2 = os.getenv('PATH')
su4 = subprocess.run(['echo', os_path2], stdout=subprocess.PIPE, encoding='utf-8')
print(su4.stdout)

s2 = 'Привет!'
s3 = 'Cześć!'
s4 = 'Hello!'
b2 = s2.encode('utf-8')
b3 = s3.encode('utf-8')
b4 = s4.encode('utf-8')
#print(s2, b2, s2.encode('utf-16'), b2.decode('utf-8'), s2.encode('ascii', errors='strict'))
print(s2, b2, s2.encode('utf-16'), b2.decode('utf-8'), s2.encode('ascii', errors='replace'))
print(s2, b2, s2.encode('utf-16'), b2.decode('utf-8'), s2.encode('ascii', errors='ignore'))
#print(s3, b3, s3.encode('utf-16'), b3.decode('utf-8'),  s3.encode('utf-16').decode('utf-8', errors='strict'))
print(s3, b3, s3.encode('utf-16'), b3.decode('utf-8'),  s3.encode('utf-16').decode('utf-8', errors='replace'))
print(s3, b3, s3.encode('utf-16'), b3.decode('utf-8'),  s3.encode('utf-16').decode('utf-8', errors='ignore'))
print(s4, b4, s4.encode('utf-16'), b4.decode('utf-8'))

b5 = b'\x01\x02\xa0\xa1\xff\xfe\x00\00' # Python treats characters in this byte string as codes
b6 = b'adfadfasdfdsaf' # Python treats characters in this byte strings as symbols
b7 = b'\xd0\x9f\xd1\x80\xd0\xb8\xd0\xb2\xd0\xb5\xd1\x82!'
print(b5, b5.decode('utf-8', errors='replace'), str(b5), b5.decode('utf-16', errors='ignore'))
print(b6)
print(b7, b7.decode('utf-8'))

# #### Connecting to the network equipment. My first time!
#
# ### Enabling logging at DEBUG level
# paramiko.common.logging.basicConfig(level=paramiko.common.DEBUG)
#
# ### I have to kill ssh-agent to run this script! Otherwise Paramiko tries to use keys/password stored in SSH-agent and fails authentication.
# ### eval $(ssh-agent -k) from the virtual environment.
#
# ### Create an object of SSHClient class from Paramiko module
# session = paramiko.SSHClient()
#
# ### Adding SSH keys of unknown hosts by default.
# session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#
# ### Connecting to the host!
# hostname = input('IP or domain name of the device: ')
# username = input('Username: ')
# password = getpass('Password: ')
# command = input('Input a command to be run in the EXEC mode: ')
#
# ### Connecting to the given host!
# session.connect(hostname, username=username, password=password, look_for_keys=False)
#
# ### Creating a CLI shell for the SSH connection
# connection = session.invoke_shell()
#
# ### Disabling paging
# connection.send('terminal length 0\n')
#
# ### Sending a command to the device via SSH
# connection.send(command + '\n') # Adding \n in the end of each command!
#
# ### Waiting for some time for the command to be executed on the device.
# ### For some reason the script doesn't work with that time.sleep() command!
# time.sleep(5) # Waiting for 5 seconds
#
# ### Receiving a result from the command sent via SSH to the device
# cli_output = connection.recv(1024000) # The parameter is max number of bytes to read.
# print(cli_output) # The outuput is returned as 'byte' type
# print(cli_output.decode('utf-8')) # Converting 'byte' type to 'string' (i.e. to Unicode)
#
# ### Closing the SSH connection to the device
# connection.close()
#
# ### Close the SSHClient
# session.close()