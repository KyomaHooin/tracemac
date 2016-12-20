#!/usr/bin/perl
#
# MSMT 'tracemac' database crawler by R.Bruna
#
# Description: 
#
# Dumps network device bridge and intreface tables via SNMP
# and create ip,mac,port assignment database.
#
# TODO: 
#	-index.php empty search error
#	-index.php example(self)
#	-index.php No interface found !
#	-Bridge ID filter
#	-empty tables check
#	

use strict;
use warnings;
use Net::SNMP;

my $database="/var/www/tracemac/database.txt";
my $mapfile="/var/www/tracemac/map.txt";

my $oid_con = '1.3.6.1.2.1.1.4';		# sysContact
my $oid_name = '1.3.6.1.2.1.1.5';		# sysName ie. DNS hostname
my $oid_loc = '1.3.6.1.2.1.1.6';		# sysLocation 
my $oid_id = '1.3.6.1.2.1.17.1.1';		# dot1dBaseBridgeAddress  ie. switch BPDU ID

my $oid_mac = '1.3.6.1.2.1.17.4.3.1.1';		# dot1dTpFdbAddress
my $oid_bridge = '1.3.6.1.2.1.17.4.3.1.2';	# dot1dTpFdbPort
my $oid_iface = '1.3.6.1.2.1.17.1.4.1.2'; 	# PortIfIndex

my $device = {};				# Device information 
my $span = {};					# Spanning tree 
my $map = {};					# MAC map 
my @ip = ();					# IP list

### START ###

# read the IP database
open(CONFIG,"<",$database);
while(<CONFIG>) {
	chomp;
	push(@ip,$_);
}
close(CONFIG);

#create deice, MAC database
foreach (@ip){
	#Create SNMP v2 session
	my $session = Net::SNMP->session(
		hostname => $_,
		timeout => 3,
		version => 2,
		community => 'public',
		);
	# check connection
	if (defined $session) {

		#Get OID tables
		my $table_name = $session->get_table( baseoid => $oid_name );
		my $table_loc = $session->get_table( baseoid => $oid_loc );
		my $table_con = $session->get_table( baseoid => $oid_con );
		my $table_id = $session->get_table( baseoid => $oid_id );
		my $table_mac = $session->get_table( baseoid => $oid_mac );
		my $table_bridge = $session->get_table( baseoid => $oid_bridge );
		my $table_iface = $session->get_table( baseoid => $oid_iface );
		#store ip, bridge id, hostname, location and contact into device hash
		$device->{$_} = [
				${$table_id}{$oid_id . '.0'},
				${$table_name}{ $oid_name . '.0' },
				${$table_loc}{ $oid_loc . '.0' },
				${$table_con}{ $oid_con . '.0'}
				];

		#loop through MAC array
		foreach my $i (keys %{$table_mac}) {
			# non-empty and hex-only MAC(3Com fix)
			if ( ${$table_mac}{$i} =~ m/^0x.+$/ ) {
				#get the bridge OID string
				my $br_id = $oid_bridge . substr($i,length($oid_mac));
				#no zero interface ID (HP fix)
				if ( ${$table_bridge}{$br_id} != 0 ) {
					#get the interface OID string
					my $iface_id = $oid_iface . "." . ${$table_bridge}{$br_id};
					#write MAP database
					$map->{$_}->{${$table_mac}{$i}} = ${$table_iface}{$iface_id};
				}
			}
		}
		#Close SNMP session
		$session->close();
	}
}

#create spanning tree database
foreach my $j ( keys %{$map}) {
	foreach my $k ( keys %{${$map}{$j}} ) { 
		foreach my $l (@ip) {
			if ( $k eq ${$device}{$l}[0] ) {
				push( @{${$span}{$j}}, ${$map}{$j}{$k} );
			}
		}
	}
}

#filter the database
foreach my $m (keys %{$span}) {
        foreach(@{${$span}{$m}}) {
                foreach my $n (keys %{${$map}{$m}}) {
                        if ($_ eq ${$map}{$m}{$n}) {
                                delete(${$map}{$m}{$n});
                        }
                }
        }
}

#open MAP database for write
open(MAP,">", $mapfile);

#print the map filtered
foreach my $o (keys %{$map}) {
        foreach my $p (keys %{${$map}{$o}}) {
                print MAP  "$o;$p;${$map}{$o}{$p}\n";
        }
}

#close MAP database
close(MAP);

exit 0;

### END ###
