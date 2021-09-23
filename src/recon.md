# Information Gathering (Reconnaissance)

Target Validation WHOIS, nslookup, dnsrecon

Finding Subdomains Google FU, dig, Nmap, Sublist3r, Bluto, crt.sh, etc

Fingerprinting Nmap, Wappalyzer, WhatWeb, BuiltWith, Netcat

Data Breaches HaveIBeenPwned, Breach-Parse, WeLeakInfo

Email Gathering Hunter.io

## DNS Enumeration
### DNS Recon

```
dnsrecon -r 127.0.0.0/24 -n IP -d anything(domain)
```

## Domain Lookups
### The Harvester
```
theharvester -d tesla.com -l 500 -b google
```

## Web Information Gathering