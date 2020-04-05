#!/usr/bin/env python3

#**************************************************************
# netster.py - Andrew Mathies (awmathie)
# CREATED: 09/30/2018
# 
# This file contains logic for handling command line arguements. 
#**************************************************************

import argparse
import logging as log
import socket
import sys

# Import the assignment modules.
# These imports can be specialized as necessary.
#from a2 import *
from a3 import *
from a4 import *


DEFAULT_PORT=12345

# If we are a server, launch the appropriate methods to handle server
# functionality based on the input arguments.
# NOTE: The arguments should be extended with a custom dict or **kwargs
def run_server(host, port, useUdp, mcast):
    server(host, port, useUdp, mcast)

# If we are a client, launch the appropriate methods to handle client
# functionality based on the input arguments
# NOTE: The arguments should be extended with a custom dict or **kwargs
def run_client(host, port, useUdp, mcast):
    client(host, port, useUdp, mcast)

def main():
    parser = argparse.ArgumentParser(description="SICE Network netster")
    parser.add_argument('-p', '--port', type=str, default=DEFAULT_PORT,
                        help='listen on/connect to port <port> (default={}'
                        .format(DEFAULT_PORT))
    parser.add_argument('-i', '--iface', type=str, default='0.0.0.0',
                        help='listen on interface <dev>')
    parser.add_argument('-f', '--file', type=str,
                        help='file to read/write')
    parser.add_argument('-u', '--udp', action='store_true',
                        help='use UDP (default TCP)')
    parser.add_argument('-r', '--rudp', type=int, default=0,
                        help='use RUDP (1=stopwait, 2=gobackN)')
    parser.add_argument('-m', '--mcast', type=str, default='226.0.0.1',
                        help='use multicast with specified group address')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Produce verbose output')
    parser.add_argument('host', metavar='host', type=str, nargs='?',
                        help='connect to server at <host>')

    args = parser.parse_args()

    # configure logging level based on verbose arg
    level = log.DEBUG if args.verbose else log.INFO

    f = None
    # open the file if specified
    if args.file:
        try:
            mode = "rb" if args.host else "wb"
            f = open(args.file, mode)
        except Exception as e:
            print("Could not open file: {}".format(e))
            exit(1)

    # Here we determine if we are a client or a server depending
    # on the presence of a "host" argument.
    if args.host:
        log.basicConfig(format='%(levelname)s:client: %(message)s',
                        level=level)
        run_client(args.host, args.port, args.udp, args.mcast)
    else:
        log.basicConfig(format='%(levelname)s:server: %(message)s',
                        level=level)
        run_server('localhost', args.port, args.udp, args.mcast)

    if args.file:
        f.close()
        
if __name__ == "__main__":
    main()
