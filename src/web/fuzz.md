# Fuzzing

## Wfuzz

```
wfuzz -u http://URL/page.pgp?code=FUZZ -w /usr/share/seclists/Fuzzing/special-chars.txt

--hc 404 (ignore 404 results)
--hl=2 (ignore length 2 results)
```

### Post data
```
wfuzz -c -w /wordlist.txt -d "username=FUZZ&password=password" --hs "No acount found with that username" http://IP
```