from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import itertools
from datetime import datetime
import logging
import subprocess
import ipaddress

NUM_THREADS = 20

logging.basicConfig(filename=f'play_with_threads_log_{datetime.now()}.log', filemode='w',
                    format='%(threadName)s %(name)s %(levelname)s %(message)s', level=logging.INFO)

def ping_ip(ip, count=5, timeout=1):
    """
    """
    # print(f'Pinging IP {ip}')
    logging.info(f'Pinging IP {ip}')

    ping = subprocess.run(['ping',f'-c {count}', f'-W {timeout}', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    if ping.returncode:
        return False, {'ip': ip, 'output': ping.stderr + ping.stdout}
    else:
        return True, {'ip': ip, 'output': ping.stdout}

def iter_ip_range(ip_range):
    """
    """
    return [str(host) for host in ipaddress.ip_network(ip_range).hosts()]

def ping_range_without_threads(ip_range, count=5):
    """
    """
    pingable = []
    non_pingable = []

    for ip in iter_ip_range(ip_range):
        success, response = ping_ip(ip)
        if success:
            pingable.append(response['ip'])
        else:
            non_pingable.append(response['ip'])

    return pingable, non_pingable

def ping_range_with_map(ip_range, count=5):
    """
    """
    pingable = []
    non_pingable = []

    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        results = executor.map(ping_ip, iter_ip_range(ip_range))

        for res in results:
            success, response = res
            if success:
                pingable.append(response['ip'])
            else:
                non_pingable.append(response['ip'])

    return pingable, non_pingable


def ping_range_with_submit(ip_range, count=5):
    """
    """
    pingable = []
    non_pingable = []

    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        futures = []
        for ip in iter_ip_range(ip_range):
            f = executor.submit(ping_ip, ip)
            futures.append(f)

        for f in futures:
            success, response = f.result()
            if success:
                pingable.append(response['ip'])
            else:
                non_pingable.append(response['ip'])

    return pingable, non_pingable

def ping_range_with_processes(ip_range, count=5):
    """
    """
    pingable = []
    non_pingable = []

    with ProcessPoolExecutor(max_workers=NUM_THREADS) as executor:
        results = executor.map(ping_ip, iter_ip_range(ip_range))

        for res in results:
            success, response = res
            if success:
                pingable.append(response['ip'])
            else:
                non_pingable.append(response['ip'])

    return pingable, non_pingable

def measure_time(func, *args, **kwargs):
    """
    """
    start_time = datetime.now()
    res = func(*args, **kwargs)

    end_time = datetime.now()
    duration = end_time - start_time

    return duration, res

def run_ping_test(func, ip_range):
    """
    """
    duration, result = measure_time(func, ip_range)
    pingable, non_pingable = result
    print('\n' + '=' * 100)
    print(f'Executing pings with "{func.__name__}()" function!')
    print(f'The program finished in: {duration}')
    print('Responded to pings: ', pingable)
    print("Didn't respond to pings: ", non_pingable)
    print('\n' * 2)

if __name__ == '__main__':
    # ips = ['8.8.8.8', '140.101.84.151', 'fsdfadf', '1.1.1.1']
    # for ip in ips:
    #     print(ping_ip(ip))

    ip_range1 = '144.190.0.0/16'
    ip_range2 = '144.190.72.0/27'

    # print(ping_ip('144.190.0.1'))

    # for ip_addr in ipaddress.ip_network(ip_range2).hosts():
    #     print(ping_ip(str(ip_addr)))

    # pingable, non_pingable = ping_range_without_threads(ip_range2)
    # print(pingable, non_pingable)

    run_ping_test(ping_range_with_map, ip_range2)
    run_ping_test(ping_range_with_submit, ip_range2)
    run_ping_test(ping_range_without_threads, ip_range2)
    run_ping_test(ping_range_with_processes, ip_range2)
