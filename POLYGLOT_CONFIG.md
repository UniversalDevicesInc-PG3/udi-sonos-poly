In general, the speakers should be auto discovered when the Plugin starts.  However
this only works if the speakers are on the same subnet.  If the speakers are not
on the same subnet, you can add additional subnets to scane and/or specify the
speaksers directly.

To add additional subnets create parameters with the key set to "network_to_scan"
and the value set to a common delimited list of subnets.  For example:

network_to_scan : 192.168.20.1/24

or

network_to_scan: 192.168.20.1/24,192.168.30.1/24

You can also set parameters to specify the speakers directly.  Set the key to a
unique ID and the value to the speaker's name and IP address.  For example:

sonos_Living : { "name": "Sonos Living Room", "host": "192.168.1.86" }



