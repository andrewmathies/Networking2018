#!/bin/bash

SSH="ssh -i geni -o StrictHostKeyChecking=no"

RTR1="awmathie@pc2.genirack.nyu.edu -p 29052"

RTR2="awmathie@pc3.lan.sdn.uky.edu -p 26372"

$SSH $RTR1 "sudo ip route replace 10.10.1.0/24 via 10.10.100.3"
$SSH $RTR2 "sudo ip route replace 10.10.100.1 via 10.10.102.3; \
            sudo ip route replace 10.10.0.0/24 via 10.10.102.3"

echo "rerouted traffic from site1 to site2 to go through rtr3"