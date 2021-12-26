#!/bin/python3


from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import dns.resolver
import itertools
import string
import dns
from datetime import datetime

DNS_NAME_LENGTH = 2
NUM_THREADS = 100


def gen_record_names(length, domain):
    """

    """
    chars = string.ascii_lowercase + string.digits + '-'

    for l in range(length + 1):
        for item in itertools.product(chars, repeat=l):
            yield ''.join(item)  + '.' + domain

def dns_query(rname, rtype, resolver):
    """

    """
    # resolver.timeout = 3
    response = resolver.resolve(rname, rtype)
    return resolver_ip, rname, rtype, response.rrset


if __name__ == '__main__':

    start_time = datetime.now()

    base_domain = 'hp.com'
    resolver_ips = ['8.8.8.8', '1.1.1.1', '4.2.2.2']
    # resolver_ips = ['8.8.8.8']
    record_types = ['A', 'CNAME', 'TXT', 'MX', 'NS']
    # record_types = ['A']

    results = {}

    # for rec in gen_record_names(DNS_NAME_LENGTH, base_domain):
    #     print(rec)

    timestamp = datetime.now()

    with open(f'resolved_records_{timestamp}.txt', 'w') as data_out, \
        open(f'errors_{timestamp}.log', 'w') as err_out:

        with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:

            for resolver_ip in resolver_ips:
                resolver = dns.resolver.Resolver()
                resolver.nameservers = [resolver_ip]
                for rtype in record_types:
                    futures = []
                    for rec in gen_record_names(DNS_NAME_LENGTH, base_domain):
                        # print(resolver_ip, rtype, rec)
                        f = executor.submit(dns_query, rec, rtype, resolver)
                        futures.append(f)

                    for future in futures:
                        try:
                            resolver_ip, rname, rtype, rdata = future.result()
                            result = rdata.to_text()
                            # print(resolver_ip, rname, rtype, result)
                            data_out.write(f"DNS server: {resolver_ip} - Record: {rname} - Type '{rtype}': {result}\n")
                        except (dns.exception.Timeout, dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers, dns.name.EmptyLabel) as e:
                            error = e.msg
                            err_out.write(f"Error: {error}\n")

    end_time = datetime.now()
    print(f'The program finished in {(end_time-start_time)}')