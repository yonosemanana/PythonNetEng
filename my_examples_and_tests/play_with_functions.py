def intf_config(intf, ip, mask='255.255.255.0'):
    '''
    The function receives interface name, ip and mask (default mask is 255.255.255.0) as strings.
    The function returns Cisco-like interface config (string).
    '''
    config = (f'interface {intf}\n'
              f' {ip} {mask}')
    return config


def intf_config_ip(intf, ip, mask='255.255.255.0'):
    '''
    The function receives interface name, ip and mask (default mask is 255.255.255.0) as strings.
    The function returns Cisco-like interface config and ip + mask (tuple of two strings)
    '''
    config = (f'interface {intf}\n'
              f' {ip} {mask}')
    return config, f'{ip} {mask}'


def print_list(l=[]):
    '''
    The function receives a list and prints it elements one by one.
    '''
    for item in l:
        print(item)

def my_print_l(*args):
    '''
    This is a test function. It receives arbitrary tuple of arguments and print them one by one.
    '''

    # args == tuple of the rest of the function parameters not listed explicitly.
    # *args (or *<name>) syntax in the function parameters creates a tuple with name 'args' (or '<name>') of the arguments.
    print(type(args), args)
    for item in args:
        print(item)


def my_print_d(**args):
    '''
    This is a test function. It receives arbitrary dictionary of keyword arguments and print them one by one.
    '''

    # args == tuple of the rest of the function parameters not listed explicitly.
    print(type(args), args)
    for key, item in args.items():
        print(key, ' : ', item)


def print_dict(**kwargs):
    '''number
    This is a test function. It receives arbitrary dictionary of keyword arguments and print them one by one.
    '''
    # **kwargs (or **<name>) syntax in the function parameters creates a dictionary with name 'kwargs' (or '<name>') of the arguments.
    print(type(kwargs), kwargs)
    for key, value in kwargs.items():
        print(key, ' : ', value)

def print_five(one, two, three, four, five):
    '''
    This function receives five arguments and prints them
    '''
    s = (f'One: {one}, '
         f'Two: {two}, '
         f'Three: {three}, '
         f'Four: {four}, '
         f'Five: {five}'
         )
    print(s)

def print_three_vars(var1, var2, var3):
    '''
    This is a test function. It receives three any vars and prints them.
    '''
    print(var1, var2, var3)

def len_l(l=[]):
    '''
    This is a test function. It receives a list and returns its length. If no argument given, it creates an empty list.
    '''
    return len(l)

# Default parameters are created when the function is defined. Therefore if the parameter is changable, it should be created inside the function, not in the list of arguments.
# Otherwise you will use the same object in all function calls, when the function is called with the default parameter value.
# Summary: it's a bad practice to use changable type variables as default parameters.
def append_l(item, l=[]):
    '''
    This is a test function. It receives an item and a list and returns the list with the item append. If no argument given, it creates an empty list.
    '''
    l.append(item)
    return l

intf_name = 'GigabitEthernet0/1'
ip = '10.10.10.1'
mask = '255.255.224.0'

# print(intf_config(intf_name, ip, mask))
print(intf_config(intf_name, ip, mask))

print(intf_config_ip(intf_name, ip))

l = [i for i in range(0, 10) if i % 2 == 1]
print_list(l)

ll = ['one', 'two', 'three', 'four', 'five']
my_print_l('a')
my_print_l('a', 'b')
my_print_l([1, 2, 3])
my_print_l([1, 2, 3], 10, 'a')

# We can use *<name> syntax when calling a function even the function doesn't use *args syntax.
# In this case number of items in the tuple of arguments must be exactly the same as number of the function parameters!
print_five(*ll)





vars = {'var1' : 100, 'var2' : 200, 'var3' : 1000}

# We can use **<name> syntax when calling a function even the function doesn't use **kwargs syntax.
# In this case number of (key, value) pairs in the dictionary of arguments must be exactly the same as number of the function parameters!
# And names of the keys in the dictionary must match with the names of parameters of the function!
print_three_vars(**vars)


print('\n' + '-' * 30)
# This code treats ll as a tuple with one element of type 'list' and it prints the list!
my_print_l(ll)
# This code treats ll as a tuple of strings and it prints many strings!
my_print_l(*ll)



# The code below doesn't work, because a and b are positional arguments and **kwargs expects keywords arguments.
# a = 'a'
# b = 'b'
# my_print_d(a, b)

# This code prints dictionary {'d_a' : {1 : 'a'}}. I.e. **kwargs uses names of arguments as the dictionary keys
my_print_d(d_a={1: 'a'})

d = {'a' : 1, 'b' : 2}
# This code doesn't work because d is a positional argument.
# my_print_d(d)

# This code does work, because with **<name> we can give the function <name> as a dictionary of arguments.
my_print_d(**d)

print_dict(**d)


l3 = [1, 2, 3]
print(len_l(l3))
print(len_l())
print(len_l(l3[:2]))

print(append_l(10, l3))
l1 = append_l(1)
print(id(l1))
print(l1)
l2 = append_l(2)
print(l2)
print(id(l2))