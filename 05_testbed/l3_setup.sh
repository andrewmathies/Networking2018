#!/bin/bash

# add -f to run ssh in background, parallellize
SSH="ssh -i geni -o StrictHostKeyChecking=no"

# update these entries to match your username and allocated resources!
RTR1="awmathie@pc2.genirack.nyu.edu -p 29052"
NODE11="awmathie@pc2.genirack.nyu.edu -p 29050"
NODE12="awmathie@pc2.genirack.nyu.edu -p 29051"

RTR2="awmathie@pc3.lan.sdn.uky.edu -p 26372"
NODE21="awmathie@pc3.lan.sdn.uky.edu -p 26370"
NODE22="awmathie@pc3.lan.sdn.uky.edu -p 26371"

RTR3="awmathie@pc1.instageni.utdallas.edu -p 27908"
NODE31="awmathie@pc1.instageni.utdallas.edu -p 27906"
NODE32="awmathie@pc1.instageni.utdallas.edu -p 27907"

ALL_NODES=("$RTR1" "$RTR2" "$RTR3"
	   "$NODE11" "$NODE12"
	   "$NODE21" "$NODE22"
	   "$NODE31" "$NODE32")

RTRS=("$RTR1" "$RTR2" "$RTR3")

HOSTS=("$NODE11" "$NODE12"
       "$NODE21" "$NODE22"
       "$NODE31" "$NODE32")

# Run commands below
# For example, this clears all IPs from dataplane interfaces
# and resets /etc/hosts

# map of which ethX interfaces connect to each other w/ original ip's
# rtr1:eth4 < 10.1.6.1 - 10.1.6.2 > rtr2:eth3
# rtr1:eth3 < 10.0.250.1 - 10.0.250.2 > rtr3:eth4
# rtr2:eth4 < 10.1.0.1 - 10.1.0.2 > rtr3:eth3

for h in "${RTRS[@]}"; do
    $SSH $h "hostname; sudo ip addr flush dev eth1; \
    	    	       sudo ip addr flush dev eth2; \
		       sudo ip addr flush dev eth3; \
		       sudo ip addr flush dev eth4; \
		       head -n 1 /etc/hosts | sudo tee /etc/hosts"
done

for h in "${HOSTS[@]}"; do
    $SSH $h "hostname; sudo ip addr flush dev eth1; \
    	     head -n 1 /etc/hosts | sudo tee /etc/hosts"
done

# Next step: assign desired IPs to each site hosts and routers
# Update /etc/hosts if desired

$SSH $NODE11 "hostname; sudo ip addr add 10.10.0.11/24 dev eth1; \
			  sudo ip route add 10.10.0.0/16 via 10.10.0.1"
#$SSH $NODE12 "hostname; sudo ip addr add 10.10.0.12/24 dev eth1"

echo "created gateway for node 1-1"

$SSH $NODE21 "hostname; sudo ip addr add 10.10.1.21/24 dev eth1; \
			  sudo ip route add 10.10.0.0/16 via 10.10.1.1"
#$SSH $NODE22 "hostname; sudo ip addr add 10.10.1.22/24 dev eth1"

echo "created gateway for node 2-1"

$SSH $NODE31 "hostname; sudo ip addr add 192.168.0.31/24 dev eth1; \
			  sudo ip route add 10.10.0.0/16 via 192.168.0.1"
#$SSH $NODE32 "hostname; sudo ip addr add 192.168.0.32/24 dev eth1"

echo "created gateway for node 3-1"

$SSH $RTR1 "hostname; sudo ip addr add 10.10.0.1/24 dev eth1; \
		      sudo ip addr add 10.10.100.1/24 dev eth3; \
		      sudo ip addr add 10.10.101.1/24 dev eth4; \
			  sudo ip route replace 10.10.0.11 dev eth2; \
			  sudo ip route replace 10.10.1.0/24 via 10.10.101.2"

echo "replaced interface for route from router 1 to node 1-1"
echo "routing traffic from router1 to router2 through relevant core addresses"

$SSH $RTR2 "hostname; sudo ip addr add 10.10.1.1/24 dev eth1; \
		      sudo ip addr add 10.10.101.2/24 dev eth3; \
		      sudo ip addr add 10.10.102.2/24 dev eth4; \
			  sudo ip route replace 10.10.1.21 dev eth2; \
			  sudo ip route replace 10.10.0.0/24 via 10.10.101.1"

echo "replaced interface for route from router 2 to node 2-1"
echo "routing traffic from router2 to router1 through relevant core address"

$SSH $RTR3 "hostname; sudo ip addr add 192.168.0.1/24 dev eth1; \
		      sudo ip addr add 10.10.102.3/24 dev eth3; \
		      sudo ip addr add 10.10.100.3/24 dev eth4; \
			  sudo ip route add 10.10.0.0/24 via 10.10.100.1; \
			  sudo ip route add 10.10.1.0/24 via 10.10.102.2"

echo "routing traffic from router3 to router1 through relevant core address"
echo "routing traffic from router3 to router2 through relevant core address"