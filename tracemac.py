#!/usr/bin/python

import netsnmp,argparse,sys,re

from scapy.layers.inet import ARP
from scapy.sendrecv import sr

target_ip=False

#OID
# http://www.mibdepot.com/cgi-bin/getmib3.cgi?i=1&n=LLDP-MIB&r=cisco&f=LLDP-MIB-V1SMI.my&v=v1&t=tree
lldp_remote_mac	='.1.0.8802.1.1.2.1.4.1.1.5'
lldp_portid	='.1.0.8802.1.1.2.1.4.1.1.7'
lldp_portdesc	='.1.0.8802.1.1.2.1.4.1.1.8'
lldp_sys	='.1.0.8802.1.1.2.1.4.1.1.9'
lldp_sysdesc	='.1.0.8802.1.1.2.1.4.1.1.10'
lldp_remoteip	='.1.0.8802.1.1.2.1.4.2.1.3'

lldp_localmac	='.1.0.8802.1.1.2.1.3.2.0'
lldp_localsys	='.1.0.8802.1.1.2.1.3.3.0'
lldp_localdesc	='.1.0.8802.1.1.2.1.3.4.0'

local_cam	='.1.3.6.1.2.1.17.4.3.1.1'
local_ifid	='.1..3.6.1.2.1.17.4.3.1.2'
local_ifindex	='.1.3.6.1.2.1.17.4.3.1.2'

#ARGS

parser = argparse.ArgumentParser(description="Trace IP/MAC within L2 segment using LLDP and CAM/MAC table.")
parser.add_argument("-c","--community", help="SNMP community.", default="public")
parser.add_argument("-v","--version", help="SNMP version.", default="2")
parser.add_argument("hop", help="First hop IP address.")
parser.add_argument("target", help="Target IP/MAC address.")
args = parser.parse_args()

#IP
if not re.match('^\d{1,3}(\.\d{1,3}){3}$',args.hop):# simple IP check
	print "Invalid hop address."
	sys.exit(1)

#MAC
if re.match('^\d{1,3}(\.\d{1,3}){3}$',args.target):
	target_ip=True

if not ( target_ip or re.match('[a-fA-F0-9]{2}(:[a-fA-F0-9]{2}){5}',args.target)):
	print "Invalid target address."
	sys.exit(2)

#ARP
#if target_ip:
#	ret = sr(ARP(op=ARP.who_has, psrc=args.target, pdst='255.255.255.255'))
#	print ret
#MAIN

#var = netsnmp.Varbind(lldp_remote_mac)
#res = netsnmp.snmpwalk(var,Version=2,DestHost='10.10.2.10',Community='public')

#print res[0].encode('hex')

