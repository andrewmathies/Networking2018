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

# Import the p2p modules
from p2p import *

DEFAULT_PORT=12345

# If we are a server, launch the appropriate methods to handle server
# functionality based on the input arguments.
def run_server(host, port):
    server(host, port)

# If we are a client, launch the appropriate methods to handle client
# functionality based on the input arguments
def run_client(host, port):
    client(host, port)

def main():
    parser = argparse.ArgumentParser(description="SICE Network netster")
    parser.add_argument('-p', '--port', type=str, default=DEFAULT_PORT,
                        help='listen on/connect to port <port> (default={}'
                        .format(DEFAULT_PORT))
    parser.add_argument('-i', '--iface', type=str, default='0.0.0.0',
                        help='listen on interface <dev>')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Produce verbose output')
    parser.add_argument('host', metavar='host', type=str, nargs='?',
                        help='connect to server at <host>')

    args = parser.parse_args()

    # configure logging level based on verbose arg
    level = log.DEBUG if args.verbose else log.INFO

    # Here we determine if we are a client or a server depending
    # on the presence of a "host" argument.
    if args.host:
        log.basicConfig(format='%(levelname)s:client: %(message)s',
                        level=level)
        run_client(args.host, args.port)
    else:
        log.basicConfig(format='%(levelname)s:server: %(message)s',
                        level=level)
        run_server('172.31.28.182', args.port)
        
if __name__ == "__main__":
    main()
