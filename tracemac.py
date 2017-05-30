#!/usr/bin/python
#
# MAC/IP LLDP
#

import subprocess,argparse,netsnmp,sys,re

target_ip=False

#OID
lldp_neighbour	='.1.0.8802.1.1.2.1.4.1.1.5'
local_cam	='.1.3.6.1.2.1.17.4.3.1.1'
local_ifid	='.1.3.6.1.2.1.17.4.3.1.2'
if_desc		='.1.3.6.1.2.1.2.2.1.2'

#-----------------

def is_ip(ip):# very simple IP regexp..
	if re.match('^\d{1,3}(\.\d{1,3}){3}$', ip):
		return True

def is_mac(mac):# very simple MAC regexp..
	 if re.match('^[a-fA-F0-9]{2}(:[a-fA-F0-9]{2}){5}$', mac):
		return True

def get_addr(addr):# arping command call..
	try:
		return subprocess.check_output(['arping','-F','-r','-C 1','-c 1', addr]).rstrip()
	except: pass

def snmp_get(oid,ip):
	try:
		ret = netsnmp.snmpget(netsnmp.Varbind(oid),Version=args.version,DestHost=ip,Community=args.community,Retries=0)
		return ret[0]
	except: pass

def snmp_walk(oid,ip):
	try:
		ret = netsnmp.snmpwalk(netsnmp.Varbind(oid),Version=args.version,DestHost=ip,Community=args.community,Retries=0)
		return ret
	except: pass

def hex_to_mac(s):
	return re.sub('(..)','\\1:',s.encode('hex')).strip(':')

def mac_to_hex(m):
	return re.sub(':','',m).decode('hex')

def nbr_probe(hop):
	print 'probing..', hop
	for n in snmp_walk(lldp_neighbour, hop):
		nbr = get_addr(hex_to_mac(n))
		if nbr:
			if not nbr in NBT:
				NBT.append(nbr)
				nbr_probe(nbr)

#-----------------

#ARGS
parser = argparse.ArgumentParser(description="Trace IP/MAC within L2 segment using LLDP and CAM/MAC table.")
parser.add_argument("-c","--community", help="SNMP community.", default="public")
parser.add_argument("-v","--version", help="SNMP version.", default=2)
parser.add_argument("hop", help="First hop IP address.")
parser.add_argument("target", help="Target IP/MAC address.")
args = parser.parse_args()

#IP CONTROL
if not is_ip(args.hop):
	print "Invalid hop address."
	sys.exit(1)

#MAC CONTROL
if is_ip(args.target): target_ip=True

if not (target_ip or is_mac(args.target)):
	print "Invalid target address."
	sys.exit(2)

#MAIN

NBT =[]

NBT.append(args.hop)# first hop

print "LLDP topology"
nbr_probe(args.hop)

print "CAM entry"
if target_ip:
	target = mac_to_hex(get_addr(args.target))
else:
	get_addr(args.target)
	target = mac_to_hex(args.target)

for n in NBT:
	print n,
	if target:
		cam = snmp_walk(local_cam, n)
		ifid = snmp_walk(local_ifid, n)
		ifdesc = snmp_walk(if_desc, n)
		if target in cam:
			index = cam.index(target)
			if_index = ifid[index]
			if_name = snmp_get(if_desc + '.' + if_index, n)
			print "->", if_index, "[", if_name, "]"
		else:
			print "Target not in CAM table."

sys.exit(3)
