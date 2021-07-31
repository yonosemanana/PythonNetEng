def show_ip_int_br(filename):
    """
    The function receives a name of file with "show ip interface brief" output.
    Returns a dictionary {'interface': 'IP address'} and doesn't add interfacess with unassigned IPs

    R1#show ip interface brief
    Interface                  IP-Address      OK? Method Status                Protocol
    FastEthernet0/0            15.0.15.1       YES manual up                    up
    FastEthernet0/1            10.0.12.1       YES manual up                    up
    FastEthernet0/2            10.0.13.1       YES manual up                    up
    FastEthernet0/3            unassigned      YES unset  up                    down
    Loopback0                  10.1.1.1        YES manual up                    up
    Loopback100                100.0.0.1       YES manual up                    up
    """

    result = {}
    with open(filename) as f:
        lines = f.readlines()

    #Skip the command and outupt header
    for line in lines[2:]:
        # l = line.split()
        # if l[1] != 'unassigned':
        #     result[l[0]] = l[1]
        intf, ip, *other = line.split()
        if ip != 'unassigned':
            result[intf] = ip

    return result

def show_int_mtu(filename):
    """
    The function receives a name of file with "show interface" output.
    Returns a dictionary {'interface': MTU}

    R1#show interface
    Ethernet0/0 is up, line protocol is up
      Internet address is 192.168.100.1/24
      Broadcast address is 255.255.255.255
      Address determined by non-volatile memory
      MTU is 1500 bytes
      Helper address is not set
      ...
    Ethernet0/1 is up, line protocol is up
      Internet address is 192.168.200.1/24
      Broadcast address is 255.255.255.255
      Address determined by non-volatile memory
      MTU is 1500 bytes
      Helper address is not set
      ...
    Ethernet0/2 is up, line protocol is up
      Internet address is 19.1.1.1/24
      Broadcast address is 255.255.255.255
      Address determined by non-volatile memory
      MTU is 1500 bytes
      Helper address is not set
    """
    result = {}
    with open(filename) as f:
        lines = f.readlines()

    # Skip the command and outupt header
    for line in lines[1:]:
        l = line.split()
        if 'Ethernet' in l[0]:
            intf = l[0]
        if l[0] == 'MTU':
            mtu = l[2]
            result[intf] = mtu

    return result

def show_int_ip_mtu(filename):
    """
    The function receives a name of file with "show interface" output.
    Returns a dictionary of dictionaries {'interface': {'ip_address' : ip, 'mtu' : MTU}}

    R1#show interface
    Ethernet0/0 is up, line protocol is up
      Internet address is 192.168.100.1/24
      Broadcast address is 255.255.255.255
      Address determined by non-volatile memory
      MTU is 1500 bytes
      Helper address is not set
      ...
    Ethernet0/1 is up, line protocol is up
      Internet address is 192.168.200.1/24
      Broadcast address is 255.255.255.255
      Address determined by non-volatile memory
      MTU is 1500 bytes
      Helper address is not set
      ...
    Ethernet0/2 is up, line protocol is up
      Internet address is 19.1.1.1/24
      Broadcast address is 255.255.255.255
      Address determined by non-volatile memory
      MTU is 1500 bytes
      Helper address is not set
    """
    result = {}
    with open(filename) as f:
        lines = f.readlines()

    # Skip the command and outupt header
    for line in lines[1:]:
        l = line.split()
        if 'Ethernet' in l[0]:
            intf = l[0]
        if 'Internet address' in line:
            ip_address = l[3]
        if l[0] == 'MTU':
            mtu = l[2]
            result[intf] = {'ip_address' : ip_address, 'mtu' : mtu}

    return result




filename = 'sh_ip_int_br.txt'
print(show_ip_int_br(filename))

filename2 = 'show_interface.txt'
print(show_int_mtu(filename2))
print(show_int_ip_mtu(filename2))