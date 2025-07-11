#!/usr/bin/env python3

import dns.resolver
import whois
import requests
import argparse
import logging

# Configure logging
logging.basicConfig(
    filename='domain_hustler.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s')

# Function to resolve DNS records (A, MX, NS)
def resolve_dns(domain):
    records = {}
    try:
        # A record
        a_records = dns.resolver.resolve(domain, 'A')
        records['A'] = [str(rdata) for rdata in a_records]
    except Exception as e:
        records['A'] = f"Error resolving A records: {e}"
        logging.error(f"Error resolving A records for {domain}: {e}")
    try:
        # MX record
        mx_records = dns.resolver.resolve(domain, 'MX')
        records['MX'] = [str(rdata.exchange) for rdata in mx_records]
    except Exception as e:
        records['MX'] = f"Error resolving MX records: {e}"
        logging.error(f"Error resolving MX records for {domain}: {e}")

    try:
        # NS record
        ns_records = dns.resolver.resolve(domain, 'NS')
        records['NS'] = [str(rdata.target) for rdata in ns_records]
    except Exception as e:
        records['NS'] = f"Error resolving NS records: {e}"
        logging.error(f"Error resolving NS records for {domain}: {e}")

    return records


# Function to perform a WHOIS lookup
def whois_lookup(domain):
    try:
        domain_info = whois.whois(domain)
        return domain_info
    except Exception as e:
        return f"Error performing WHOIS lookup: {e}"

# Function to get subdomains from crt.sh (certificate transparency logs)
def get_subdomains(domain):
    url = f'https://crt.sh/?q={domain}&output=json'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            subdomains = set()
            certs = response.json()
            for cert in certs:
                common_name = cert['common_name']
                name_value = cert['name_value']
                subdomains.update([common_name, name_value])
            return list(subdomains)
        else:
            return f"Error retrieving subdomains: Status code {response.status_code}"
    except Exception as e:
        return f"Error retrieving subdomains: {e}"

if __name__ == '__main__':
    # Using argparse to accept domain as a command-line argument
    parser = argparse.ArgumentParser(description="Domain Enumeration Tool")
    parser.add_argument("domain", help="The domain to enumerate")
    args = parser.parse_args()
    
    domain = args.domain

    # DNS resolution
    print("\n[+] DNS Records:")
    dns_records = resolve_dns(domain)
    for record_type, records in dns_records.items():
        print(f"{record_type} Records: {records}")

    # WHOIS lookup
    print("\n[+] WHOIS Information:")
    whois_info = whois_lookup(domain)
    print(whois_info)

    # Subdomain enumeration
    print("\n[+] Subdomains found:")
    subdomains = get_subdomains(domain)
    if isinstance(subdomains, list):
        for subdomain in subdomains:
            print(subdomain)
    else:
        print(subdomains)
