import telnetlib

telnet = telnetlib.Telnet('192.168.100.1')
prompt = telnet.read_until(b'Username:')
print(prompt)
telnet.write(b'cisco\n')
telnet.read_until(b'Password:')
telnet.write(b'cisco\n')
enable, match, line = telnet.expect([b'>', b'#'])
if enable == 0:
    telnet.write(b'enable\n')
index, match, line = telnet.expect([b'Password:', b'#'])
if index == 0:
    telnet.write(b'cisco\n')
index, match, line = telnet.expect([b'Password:', b'#'])
print(match.group())
telnet.close()
