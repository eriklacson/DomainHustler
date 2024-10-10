# DomainHustler 🚀

A lightweiht domain enumeration written in Python3 for hustling information from a domain. It uncovers DNS records, WHOIS data, and subdomains from certificate transparency logs. Made for network geeks, cybersecurity folks, or anyone curious about what's behind a domain.

## Features ✨
- **DNS Resolution**: Automatically retrieves A, MX, and NS records for a domain.
- **WHOIS Lookup**: Fetches WHOIS information to provide domain registration details.
- **Subdomain Enumeration**: Discovers subdomains using certificate transparency logs via `crt.sh`.
- **Command-line Interface**: Easy-to-use CLI for quick domain enumeration with a single command.

## Requirements 🛠️
Ensure you have the required libraries installed:

```bash
pip install dnspython whois python-whis requests
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
## Contributions

Feel free to fork this repository, submit issues, or suggest new features via pull requests! Let’s make domain recon as smooth as possible!

## License 

This project is licensed under the GNU Public License.


Stay Sharp! Keep Hustling with **DomainHustler**



