
DESCRIPTION

Trace MAC/IP winin LLDP topology.

REQUIREMENT

python-netsnmp

FILE

<pre>
 tracemac.py - Main program.
</pre>

OUTPUT

<pre>
root@localhost:/home# ./tracemac 10.10.x.x 00:50:56:b5:84:3b
LLDP topology
probing.. 10.10.x.x
probing.. 10.10.x.x
probing.. 10.10.x.x
probing.. 10.10.x.x
probing.. 10.10.x.x
probing.. 10.10.x.x
probing.. 10.10.x.x
probing.. 10.10.x.x
probing.. 10.10.x.x
CAM entry
10.10.x.x -> 46 [ B22 ]
10.10.x.x -> 32 [ B8 ]
10.10.x.x -> 48 [ B22 ]
10.10.x.x -> 389 [ Trk100 ]
10.10.x.x -> 48 [ B22 ]
10.10.x.x -> 48 [ B22 ]
10.10.x.x -> 1 [ A1 ]
10.10.x.x -> 48 [ B22 ]
10.10.x.x Target not in CAM table.
</pre>

CONTACT

Author: richard_bruna@nm.cz<br>
Source: https://github.com/KyomaHooin/tracemac

