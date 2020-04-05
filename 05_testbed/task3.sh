#!/bin/bash

SSH="ssh -i geni -o StrictHostKeyChecking=no"

RTR3="awmathie@pc1.instageni.utdallas.edu -p 27908" #192.168.0.1
NODE31="awmathie@pc1.instageni.utdallas.edu -p 27906" #192.168.0.31

$SSH $RTR3 "sudo echo \"1\" > /proc/sys/net/ipv4/ip_forward; \
            sudo modprobe ip_tables; \
            sudo modprobe ip_conntrack; \
            sudo iptables -t nat -A POSTROUTING -s 10.10.0.0/24 -o eth4 -j MASQUERADE; \
            sudo iptables -t nat -A POSTROUTING -s 10.10.1.0/24 -o eth3 -j MASQUERADE; \
            sudo iptables -t nat -A PREROUTING -p tcp -i eth4 --dport 501 -j DNAT --to 192.168.0.31; \
            sudo iptables -t nat -A PREROUTING -p tcp --dport 501 -j DNAT --to-destination 192.168.0.31:6969"

echo "completed nat commands"

$SSH $NODE31 "  pgrep python; \
                if [ \$? -ne 0 ]; then 
                    cd ./Net-Fall18/src/py
                    nohup python netster.py -p 6969 &> /dev/null &
                fi"

echo "started server on port 6969 of node"