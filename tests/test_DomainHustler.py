import pytest
from pytest_mock import MockerFixture
import DomainHustler

def test_resolve_dns(mocker):
    # Mock dns.resolver.resolve
    mock_resolve = mocker.patch('DomainHustler.dns.resolver.resolve')
    mock_resolve.side_effect = [
        [mocker.Mock(to_text=lambda: '192.168.1.1')],
        [mocker.Mock(exchange='mail.example.com')],
        [mocker.Mock(target='ns.example.com')]
    ]
    domain = 'example.com'
    records = DomainHustler.resolve_dns(domain)
    assert records['A'] == ['192.168.1.1']
    assert records['MX'] == ['mail.example.com']
    assert records['NS'] == ['ns.example.com']

def test_whois_lookup(mocker):
    # Mock whois.whois
    mock_whois = mocker.patch('DomainHustler.whois.whois')
    mock_whois.return_value = {'domain_name': 'example.com', 'registrar': 'Example Registrar'}
    domain = 'example.com'
    whois_info = DomainHustler.whois_lookup(domain)
    assert whois_info['domain_name'] == 'example.com'
    assert whois_info['registrar'] == 'Example Registrar'

def test_get_subdomains(mocker):
    # Mock requests.get
    mock_get = mocker.patch('DomainHustler.requests.get')
    mock_response = mocker.Mock()
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

def test_resolve_dns_error(mocker):
    # Simulate DNS resolution error
    mock_resolve = mocker.patch('DomainHustler.dns.resolver.resolve')
    mock_resolve.side_effect = Exception("DNS resolution failed")
    domain = 'example.com'
    records = DomainHustler.resolve_dns(domain)
    assert "Error resolving A records" in records['A']
    assert "Error resolving MX records" in records['MX']
    assert "Error resolving NS records" in records['NS']

def test_get_subdomains_error(mocker):
    # Simulate crt.sh error
    mock_get = mocker.patch('DomainHustler.requests.get')
    mock_get.side_effect = Exception("Request failed")
    domain = 'example.com'
    subdomains = DomainHustler.get_subdomains(domain)
    assert "Error retrieving subdomains" in subdomains


    mock_get.side_effect = Exception("Request failed")
    domain = 'example.com'
    subdomains = DomainHustler.get_subdomains(domain)
    assert "Error retrieving subdomains" in subdomains
