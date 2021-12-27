# Enumeration

## Finding Subdomains with Assetfinder

```
go get -u github.com/tomnomnom/assetfinder
```

```
assetfinder tesla.com &gt;&gt; tesla-subs.txt
```

## Finding Subdomains with Amass

```
export GO111MODULE=on

go get -v github.com/OWASP/Amass/v3/...

amass enum -d tesla.com
```

## Finding Subdomains with WFuzz

```
sudo wfuzz -c -f sub-fighter -w /usr/share/SecLists/Discovery/DNS/subdomains-top1million-5000.txt -u 'http://10.10.10.197/' -H "Host: FUZZ.sneakycorp.htb" --hw 290
```

## Finding Subdomains with Gobuster

```
gobuster vhost -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt -u http://
```

## Finding Subdomains with ffuf

```
ffuf -w /usr/share/SecLists/Discovery/DNS/namelist.txt -H "Host: FUZZ.acmeitsupport.thm" -u http://10.10.181.76 -fs 2395
```

-fs ignores results with that size must be run before without this flag

## Finding Alive Domains with Httprobe

```
go get -u github.com/tomnomnom/httprobe
```

Sort domains and find out which are alive.

## Enumerating HTTP/HTTPS

### GoBuster

```
gobuster dir -u http://IP -w wordlist -o gobuster.log -t 50
-x for extension (-x php)
-c for cookie ( -c 'PHPSESSID=3852937265978')
```

-s 302,307...403 to add status codes
-x sh,pl to add file extensions
-k to ignore ssl certificate

#### Wordlists

```
Better one
/opt/SecLists/Discovery/Web-Content/raft-small-words.txt

/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
/usr/share/wordlists/dirb/small
```

### Nikto

```
nikto -host IP -port PORT
```

### Dirb

```
dirb http://IP wordlist
```

### WPScan

```
wpscan -u "url" --disable-tls-checks
wpscan --url http://IP/wp -e ap,t,u --log wpscan.out
```

`--enumerate p,t,u` option to enumerate plugins, themes, and users

```
For brute forcing a user
wpscan --url http://10.10.212.130:80/blog -e p,t,u --usernames admin --passwords /usr/share/wordlists/rockyou.txt --max-threads 50

Multiple users
wpscan -U users.txt -P /usr/share/wordlists/fasttrack.txt --url URL
```

### Fuzzing parameters with FFuf

```
ffuf -u "http://url/?FUZZ=id;whoami||ls" -w /usr/seclist/discovery/web-content/burp-parameter-names.txt -fs 5829

ffuf -u "http://url/?FUZZ=/etc/passwd" -w /usr/seclist/discovery/web-content/burp-parameter-names.txt -fs 5829
```

## DNS

```
dig axfr @10.10.10.13 cronos.htb
```

```
nslookup
>server 10.10.10.13
>cronos.htb
```

## Scripts that merge these tools

The cyber mentor script

https://pastebin.com/MhE6zXVt
