class Switch:

### 'Self' is always the first parameter of any function in the class!!!
### It is allowed to use any other name if not 'self', but it is HIGHLY RECOMMENDED always use 'self' for code readability
    def info(self):
        print('Hostname {}, model: {}'.format(self.hostname, self.model))

sw1 = Switch()
print(sw1)

sw2 = Switch()
sw2.hostname = 'sw2'
sw2.model = 'Cisco Catalyst 3850-48T'

print(sw2.hostname, sw2.model)
sw2.info()