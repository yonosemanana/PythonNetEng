from scrapli.driver.core import IOSXEDriver
from scrapli.exceptions import ScrapliException

iou1_params = {
    'host': '192.168.100.1',
    'auth_username': 'cisco',
    'auth_password': 'cisco',
    'auth_secondary': 'cisco',
    'auth_strict_key': False,
    'transport': 'paramiko'
}

with IOSXEDriver(**iou1_params) as ssh:
    print(ssh.get_prompt())

    sh_ver = ssh.send_command('show version')
    print(sh_ver)
    print(sh_ver.result)
    print(sh_ver.raw_result)
    print(sh_ver.elapsed_time)

    sh_ip_int_br = ssh.send_command('show ip interface brief')
    print(sh_ip_int_br.result)

    commands = ['interface loopback1',
                'ip address 172.16.0.1 255.255.255.255',
                'ruter bgp',
                'ntp servert time.nist.gov']

    output = ssh.send_configs(commands)
    if output.failed:
        print('Some commands failed!')
    print(output.result)

    sh_ip_int_br = ssh.send_command('show ip interface brief')
    print(sh_ip_int_br.result)
    print(sh_ip_int_br.textfsm_parse_output())

    save_config_commands = ['copy run start\n', 'show start']
    sh_start = ssh.send_commands(save_config_commands)
    # print(sh_start.result)
    print(sh_start[1].result)
