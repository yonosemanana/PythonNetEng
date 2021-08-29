import subprocess
import os
import ipaddress
import tabulate
import pprint

res = subprocess.run('pwd')
print(type(res), res)
print(res.stdout)
print(res.returncode)

print()
res2 = subprocess.run('pwd', stdout=subprocess.PIPE)
print(res2.stdout)
res2_1 = subprocess.run('pwd', stdout=subprocess.PIPE, encoding='Utf-8')
print(res2_1.stdout)

ping_res = subprocess.run(['ping', '-c', '3', 'google.com'], stdout=subprocess.PIPE)
print(ping_res.stdout.decode('utf-8'))

ping_res2 = subprocess.run(['ping', '-c', '3', 'google1.com'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print(ping_res2.stdout.decode('utf-8'))
print(ping_res2.stderr.decode('utf-8'))
#
# try:
#     print(ping_res2.stdout.decode('utf-8'))
# except AttributeError:
#     print(ping_res2.stderr.decode('utf-8'))
#     print(ping_res2.returncode)


#print(dir(os))
pprint.pprint(os.getenv('PATH'))
pprint.pprint(os.getcwd())
pprint.pprint(sorted(os.listdir()))
pprint.pprint(os.mkdir('testdir'))
pprint.pprint(sorted(os.listdir()))
pprint.pprint(os.rmdir('testdir'))
pprint.pprint(sorted(os.listdir()))

