# UDI-Sonos-Poly

This is a Polyglot v2 NodeServer for the ISY 994i version 5+ to control your Sonos speakers.

Install through the NodeServer Store in Polyglot v2.

Please report any issues on the [UDI user forum](https://forum.universal-devices.com/topic/18643-polyglot-sonos-nodeserver/).


If the default discovery of the Sonos speakers does not work, you can use 2 alternate methods seperately or together.  These are helpful when you are running a VLAN and can't see the discovery messages from the Sonos speakers but can control them by IP address.


Manual Hub Entries Method

If the discover does not work, or you prefer to not use it, you can add customParms in the Polyglot Web UI to tell it about your hubs.

Create a param(s) with:

name = sonos_"uniqueid" where uniqueid is the address that will be used for the ISY node, example.  sonos_LivingSonos
value like: { "name": "Sonos Living Room", "host": "192.168.1.86" }

Anytime these params are added or modified you need to run the 'Discover' on the HarmonyController node.


Extended network scanning method

You an instruct the server to scan other networks than the network your EISY or Polisy are running Polyglot 3

Create a param with:


name = network_to_scan
value = a subnet in CIDR Subnet mask notation.  

example:
name = network_to_scan
value = 192.168.20.1/24   - No quotes around the text, no brackets, just the text 

If you want to scan multiple subnets you can use list multiple

example:
name = network_to_scan
value = 192.168.20.1/24,192.168.30.1/24    - No quotes around the text, no brackets, just the text

So if your EISY is running on 192.168.1.1, then it will search all IP addresses on 192.168.1.1 by default and then 
search on subnets listed.

