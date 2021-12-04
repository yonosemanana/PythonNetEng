import telnetlib

telnet = telnetlib.Telnet('192.168.100.1')
prompt = telnet.read_until(b'Username:')
print(prompt)
telnet.write(b'cisco\n')
telnet.read_until(b'Password:')
telnet.write(b'cisco\n')
prompt2 = telnet.read_until(b'>')
print(prompt2)