f = open('test1.txt', 'w')

f.write(('Hello!\n'
         'I love my family!'))
f.close()

f = open('test1.txt', 'r')
print(f.read())
print("Is the file closed? " + str(f.closed))
print()

print('Reading the file second time:\n' + '-' * 30)
f.seek(7)
print(f.read())
f.close()
print("Is the file closed now? " + str(f.closed))

print('\n' + '=' * 30)
with open('test1.txt', 'r') as f, open('output1.txt', 'w') as out:
    s = f.read()
    out.write(s)

with open('output1.txt') as o:
    print(o.read())
    # for line in o:
    #     print(line)


