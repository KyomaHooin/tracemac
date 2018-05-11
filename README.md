
DESCRIPTION

Trace MAC/IP within STP/LLDP topology.

REQUIRE

python-netsnmp, arping

FILE

<pre>
tracemac - Main program.
</pre>

OUTPUT

<pre>
root@localhost:/home# ./tracemac 10.10.x.y 00:50:56:b5:84:3b
Probing LLDP topology.. 
-> 10.10.x.y
-> 10.10.x.y
-> 10.10.x.y
-> 10.10.x.y
-> 10.10.x.y
-> 10.10.x.y
-> 10.10.x.y
-> 10.10.x.y
-> 10.10.x.y
Probing STP topology.. 
-> 10.10.x.y
-> 10.10.x.y
-> 10.10.x.y
-> 10.10.x.y
-> 10.10.x.y
-> 10.10.x.y
-> 10.10.x.y
-> 10.10.x.y
-> 10.10.x.y
Candidate CAM entry..
10.10.x.x [ 5 ] -> [ 42 ] B18
</pre>

SOURCE

https://github.com/KyomaHooin/tracemac

