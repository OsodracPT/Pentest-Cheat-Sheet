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
    connect = s.connect(('192.168.232.1',31337))
    s.send(string + '\r\n')
    data = s.recv(1024)
    s.close()