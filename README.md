# DomainHustler 🚀

DomainHustler is a lightweight Python 3 tool for hustling information from a domain. It uncovers DNS records, WHOIS data, and subdomains from certificate transparency logs. Perfect for network geeks, cybersecurity enthusiasts and anyone curious about what is behind a domain.

## Features ✨
- **DNS Resolution**: Automatically retrieves A, MX and NS records for a domain.
- **WHOIS Lookup**: Fetches WHOIS information to provide domain registration details.
- **Subdomain Enumeration**: Discovers subdomains using certificate transparency logs via `crt.sh`.
- **Command-line Interface**: Easy-to-use CLI for quick domain enumeration with a single command.

## Installation
Install the required dependencies using `pip`:

```bash
pip install dnspython python-whois requests
```

## Usage

```bash
python3 DomainHustler.py example.com
```

## Example Output

```bash
[+] DNS Records:
A Records: ['192.0.2.1']
MX Records: ['mail.example.com']
NS Records: ['ns1.example.com', 'ns2.example.com']

[+] WHOIS Information:
Domain Name: EXAMPLE.COM
Registrar: EXAMPLE REGISTRAR, INC.
...

[+] Subdomains found:
sub.example.com
test.example.com
www.example.com
...
```

## Testing
Run the unit tests with:

```bash
pytest
```

## Contributions

Feel free to fork this repository, submit issues, or suggest new features via pull requests!

## License

DomainHustler is licensed under the [GNU General Public License v3](LICENSE).

Stay Sharp! Keep Hustling with **DomainHustler**
