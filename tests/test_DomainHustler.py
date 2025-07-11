import os
import sys
from unittest import mock
import pytest

TEST_DIR = os.path.dirname(__file__)
STUB_PATH = os.path.join(TEST_DIR, "stubs")
sys.path.insert(0, STUB_PATH)
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import DomainHustler

def test_resolve_dns():
    # Mock dns.resolver.resolve
    with mock.patch('DomainHustler.dns.resolver.resolve') as mock_resolve:
        mock_resolve.side_effect = [
            ['192.168.1.1'],
            [mock.Mock(exchange='mail.example.com')],
            [mock.Mock(target='ns.example.com')]
        ]
        domain = 'example.com'
        records = DomainHustler.resolve_dns(domain)
        assert records['A'] == ['192.168.1.1']
        assert records['MX'] == ['mail.example.com']
        assert records['NS'] == ['ns.example.com']

def test_whois_lookup():
    # Mock whois.whois
    with mock.patch('DomainHustler.whois.whois') as mock_whois:
        mock_whois.return_value = {'domain_name': 'example.com', 'registrar': 'Example Registrar'}
        domain = 'example.com'
        whois_info = DomainHustler.whois_lookup(domain)
        assert whois_info['domain_name'] == 'example.com'
        assert whois_info['registrar'] == 'Example Registrar'

def test_get_subdomains():
    # Mock requests.get
    with mock.patch('DomainHustler.requests.get') as mock_get:
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {'common_name': 'sub1.example.com', 'name_value': 'sub2.example.com'},
            {'common_name': 'sub3.example.com', 'name_value': 'sub4.example.com'}
        ]
        mock_get.return_value = mock_response
        domain = 'example.com'
        subdomains = DomainHustler.get_subdomains(domain)
        assert 'sub1.example.com' in subdomains
        assert 'sub2.example.com' in subdomains
        assert 'sub3.example.com' in subdomains
        assert 'sub4.example.com' in subdomains
        mock_get.assert_called_once_with(
            f'https://crt.sh/?q={domain}&output=json', timeout=10)

def test_resolve_dns_error():
    # Simulate DNS resolution error
    with mock.patch('DomainHustler.dns.resolver.resolve') as mock_resolve:
        mock_resolve.side_effect = Exception("DNS resolution failed")
        domain = 'example.com'
        records = DomainHustler.resolve_dns(domain)
        assert "Error resolving A records" in records['A']
        assert "Error resolving MX records" in records['MX']
        assert "Error resolving NS records" in records['NS']

def test_get_subdomains_error():
    # Simulate crt.sh error
    with mock.patch('DomainHustler.requests.get') as mock_get:
        mock_get.side_effect = Exception("Request failed")
        domain = 'example.com'
        subdomains = DomainHustler.get_subdomains(domain)
        assert "Error retrieving subdomains" in subdomains
        mock_get.assert_called_once_with(
            f'https://crt.sh/?q={domain}&output=json', timeout=10)
