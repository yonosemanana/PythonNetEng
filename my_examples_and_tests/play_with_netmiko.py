import netmiko

device2_params = {
    'device_type': 'cisco_ios',
    'host': '192.168.100.2',
    'port': '22',
    'username': 'cisco',
    'password': 'cisco',
    'secret': 'cisco'
}

with netmiko.ConnectHandler(**device2_params) as ssh:
    ssh.enable()
    if ssh.check_enable_mode():
        print("Netmiko connection is in 'enable' mode!")
    else:
        print("Go to 'enable' mode!")

    sh_ip_int_br = ssh.send_command('show ip int br')
    print(sh_ip_int_br)

    config_commands = ['interface loopback123',
                       'ip address 172.31.255.1 255.255.255.255']
    output = ssh.send_config_set(config_commands)
    print(output)
    sh_ip_int_br = ssh.send_command('show ip int br')
    print(sh_ip_int_br)

