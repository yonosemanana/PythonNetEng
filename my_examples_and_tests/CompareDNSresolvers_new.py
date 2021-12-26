from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import time
from pprint import pprint
import dns.resolver
import yaml
import os
import sys
import csv
import re

MAX_WORKERS = 100 # Number of threads running in parallel to resolve DNS queries of a zone by multiple resolvers

def resolve_query(resolver_ip, query):
    """
    :param query: a tuple (domain name, record type)
    :resolver_ip: a string with IP address of the DNS resolver

    :return: a list of RRsets returned by the resolver as answers to the queries
    """
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [resolver_ip]

    rname, rtype = query
    response = resolver.resolve(rname, rtype).rrset

    return response

def resolve_queries(resolver_ip, queries):
    """
    :param queries: a list of tuples of queries (domain name, record type)
    :resolver_ip: a string with IP address of the DNS resolver

    :return: a list of RRsets returned by the resolver as answers to the queries
    """
    responses = []

    resolver = dns.resolver.Resolver()
    resolver.nameservers = [resolver_ip]

    # responses = [resolver.resolve(query[0], query[1]).rrset for query in queries]
    responses = []

    for rname, rtype in queries:
        response = resolver.resolve(rname, rtype).rrset
        responses.append(response)
    return responses

def convert_rrset(rrset):
    """The function converts either RRset or some DNS exception object to a string with DNS data or error code
    :param rrset: either RRset or some DNS exception object
    :return: a tuple of string with either DNS response data or error code and boolean flag if there was an error / Exception
    """
    regex_value = r'\S+ \d+ \S+ \S+ (?P<value>[ \S]+)'
    lookup_error = True

    if isinstance(rrset, dns.resolver.NoNameservers):
        response = 'Failed (REFUSED)'
    elif isinstance(rrset, dns.resolver.NXDOMAIN):
        response = 'NXDOMAIN'
    elif isinstance(rrset, dns.exception.Timeout):
        response = 'Timeout'
    elif isinstance(rrset, dns.resolver.NoAnswer):
        response = 'NoAnswer'
    elif isinstance(rrset, dns.rrset.RRset):
        response = '\n'.join(sorted(re.findall(regex_value, rrset.to_text())))
        lookup_error = False
    else:
        response = str(rrset)
    return response, lookup_error


def compare_dns_lookups(queries, results):
    """
    :param queries: a list of tuples of queries (domain name, record type)
    :param lookup_results: a dictionary {'Resolver IP': list of RRsets}
    :return: The function returns a tuple of three lists:
    'matched' - if rrsets from all resolvers match
    'mismatched' - if rrset of at least one resolver doesn't match with other resolvers
    'not_resolved' - if rrset of at least one resolver doesn't match with other resolvers
    """

    matched = [] # A list of query responses from resolvers (for tabulate module)
    mismatched = [] # A list of query responses from resolvers (for tabulate module)
    not_resolved = [] # A list of query responses from resolvers (for tabulate module)

    # We will compare output of all resolvers with output of the first resolver. We are interested in match of output of all resolvers.
    resolver_pattern = list(results.keys())[0]

    # pprint(queries)
    # pprint(results)

    # We use the fact that the following lists have the same length: queries, result[<resolver>] - for all resolvers.
    for i in range(len(queries)):
        output_line = {}  # A dictionary representing output line (for tabulate module)
        output_line['Name and Type'] = queries[i]

        rrset_pattern = results[resolver_pattern][i]
        response_pattern, _ = convert_rrset(rrset_pattern)
        all_matched = True
        lookup_error = False

        for resolver in results:
            rrset = results[resolver][i] # Either RRSet object or NXDomain exception or NoNameservers exception
            response, current_error = convert_rrset(rrset)
            if current_error:
                lookup_error = True
            output_line['DNS server {}:'.format(resolver)] = response
            if response != response_pattern:
                all_matched = False

        if all_matched:
            matched.append(output_line)
        else:
            mismatched.append(output_line)
        if lookup_error:
            not_resolved.append(output_line)

    return matched, mismatched, not_resolved

def write_csv_files(zone, matched, mismatched, not_resolved):
    """ The function writes output of the lists of data to CSV files.
    :param zone: Name of the DNS zone being validated
    :param matched:
    :param mismatched:
    :param not_resolved:
    :return: The function creates three files in the current directory:
    '<zone>_names_matched_<timestamp>.txt' - if rrsets from all resolvers match
    '<zone>_names_mismatched_<timestamp>.txt' - if rrset of at least one resolver doesn't match with other resolvers
    '<zone>_names_not_resolved_<timestamp>.txt' - if rrset of at least one resolver doesn't match with other resolvers
    """
    timestamp_now = datetime.now()

    if matched:
        headers = matched[0].keys()
    elif mismatched:
        headers = mismatched[0].keys()
    elif not_resolved:
        headers = not_resolved[0].keys()
    else:
        headers = ''

    with open(f'{zone}_names_matched_{timestamp_now}.csv', 'w') as f_matched:
        csv_writer = csv.DictWriter(f_matched, fieldnames=headers)
        csv_writer.writeheader()
        for row in matched:
            csv_writer.writerow(row)
    with open(f'{zone}_names_mismatched_{timestamp_now}.csv', 'w') as f_mismatched:
        csv_writer = csv.DictWriter(f_mismatched, fieldnames=headers)
        csv_writer.writeheader()
        for row in mismatched:
            csv_writer.writerow(row)
    with open(f'{zone}_names_not_resolved_{timestamp_now}.csv', 'w') as f_not_resolved:
        csv_writer = csv.DictWriter(f_not_resolved, fieldnames=headers)
        csv_writer.writeheader()
        for row in not_resolved:
            csv_writer.writerow(row)


def parse_yaml_file(yaml_file):
    """
    :param yaml_file: a name of YAML file with records of the DNS zone (in OctoDNS format).
    The filename must be <zone>.yaml
    :return: a list of tuples (domain name, record type) for dns_query() function + the zone name (string)
    """
    queries = []

    with open(yaml_file) as f:
        basename = os.path.basename(yaml_file)
        zone = os.path.splitext(basename)[0]
        records = yaml.safe_load(f)
        # pprint(records)

    for rec in records:
        if rec == '':
            fqdn = f'{zone}.'
        else:
            fqdn = f'{rec}.{zone}.'

        if isinstance(records[rec], list):
            for item in records[rec]:
                rtype = item['type']
                queries.append((fqdn, rtype,))
        elif isinstance(records[rec], dict):
            rtype = records[rec]['type']
            queries.append((fqdn, rtype,))

    return queries, zone

def validate_zone(zone_file, resolvers):
    """
    :param zone_file: a name of YAML file with records of the DNS zone (in OctoDNS format).
    The filename MUST be <zone>.yaml
    :param resolvers: a list of IPs of DNS resolvers (strings)
    :return: tuple of bool - flags, if there are records matched, mismatched, not_resolved
    """
    queries, zone = parse_yaml_file(zone_file)
    # print(queries, zone, resolvers)
    res = {}  # A dictionary {'Resolver IP': [list of RRSets]}

    ### Here we should use multithreading!!!
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        for resolver in resolvers:
            futures = []
            for query in queries:
                f = executor.submit(resolve_query, resolver, query)
                futures.append(f)

            results = []
            for f in futures:
                try:
                    response = f.result()
                except dns.resolver.NoNameservers:
                    response = 'Failed (REFUSED)'
                except dns.resolver.NXDOMAIN:
                    response = 'NXDOMAIN'
                except dns.exception.Timeout:
                    response = 'Timeout'
                except dns.resolver.NoAnswer:
                    response = 'NoAnswer'
                results.append(response)
            res[resolver] = results

    # pprint(res)
    matched, mismatched, not_resolved = compare_dns_lookups(queries, res)

    #write_tabulate_files(zone,matched, mismatched, not_resolved)
    write_csv_files(zone,matched, mismatched, not_resolved)

    return tuple(map(lambda x: len(x) > 0, [matched, mismatched, not_resolved]))

def validate_zones_dir(zones_dir, resolver_ips):
    """
    :param zones_dir: Name of the directory with YAML zone configuration files with records to validate.
    The YAML file MUST have <zone>.yaml name. And the file MUST be in OctoDNS format
    :param resolver_ips: A list of IPs or names of the DNS servers which will be used as resolvers
    :return: The function creates a directory <zones_dir>_validation_<timestamp> and for each zone put there three CSV files:
    '<zone>_names_matched_<timestamp>.txt' - if rrsets from all resolvers match
    '<zone>_names_mismatched_<timestamp>.txt' - if rrset of at least one resolver doesn't match with other resolvers
    '<zone>_names_not_resolved_<timestamp>.txt' - if rrset of at least one resolver doesn't match with other resolvers
    """

    timestamp = datetime.now()
    output_dir = f'{os.path.basename(zones_dir)}_validation_{timestamp}'
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    zones_dir = os.path.abspath(zones_dir)
    os.chdir(output_dir)

    f_sum_mismatched = f'_Summary_mismatched_{timestamp}.txt'
    with open(f_sum_mismatched, 'w') as f:
        f.write('Zones with records mismatched between at least two DNS servers:\n')

    f_sum_not_resolved = f'_Summary_not_resolved_{timestamp}.txt'
    with open(f_sum_not_resolved, 'w') as f:
        f.write('Zones with records not resolved by at least one DNS server:\n')

    for subdir, dir, files in os.walk(zones_dir):
        for zone_file in sorted(files):
            print(zone_file)
            # validate_zone(subdir + os.sep + zone_file, resolver_ips)
            _, is_mismatched, is_notresolved = validate_zone(subdir + os.sep + zone_file, resolver_ips)

            zone = os.path.splitext(os.path.basename(zone_file))[0]
            if is_mismatched:
                with open(f_sum_mismatched, 'a') as f:
                    f.write(zone + '\n')
            if is_notresolved:
                with open(f_sum_not_resolved, 'a') as f:
                    f.write(zone + '\n')





if __name__ == '__main__':
    print('Enter a directory name with zone files in YAML format + IP addresses of DNS resolvers')
    zones_dir, *resolvers = sys.argv[1:]
    validate_zones_dir(zones_dir, resolvers)
