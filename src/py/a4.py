#**************************************************************
# a2.py - Andrwe Mathies (awmathie)
# CREATED: 09/30/2018
# 
# This file contains the functionality for running a simple
# TCP or UDP client and server.
#**************************************************************

import logging as log
import socket
import sys
import struct
import time
import errno
from socket import error as socket_error

MCAST_GRP = '226.0.0.1'
MCAST_TTL = 2

# this method creates a socket to be used for a server,
# and uses that socket to recieve data and send messages
# back based on the data we recieved
def server(host, port, useUdp, mcast):
    
    if mcast != MCAST_GRP:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MCAST_TTL)

        try:
            addr = (mcast, int(port))
            socket.inet_pton(socket.AF_INET, addr[0])
            sock.bind(addr)
            log.info("successfully bound to requested multicast address\n")
        except socket_error as serr:
            log.info("could not bind requested multicast address\n")
            addr = (MCAST_GRP, int(port))
            sock.bind(addr)

        log.info("addr is: %s\n", addr)
        
        sock.sendto("broadcast".encode(), addr)
        
        mreq = struct.pack("4sL", socket.inet_aton(addr[0]), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        clients = []
        startTime = time.time()

        while True:
            sock.sendto("broadcast".encode(), addr)
            data = sock.recv(1024)
            client = data.decode()
            if client != "broadcast":
                clients.append(client)
                log.info("recieved %s", client)

            if time.time() > startTime + 10:
                if not clients:
                    log.info("no active connections")
                else:
                    clientStr = ""
                    for hostname in clients:
                        clientStr += hostname + " "
                    log.info("current connections: %s", clientStr)
                    del clients[:]
                startTime = time.time()

        return

    # CODE NOT USED FOR ASSIGNMENT 4
    # | | | | |
    # v v v v v

    if useUdp:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    else:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    addr = (host, int(port))
    kill = False

    log.info("address is: %s", addr)
    log.info("binding")
    sock.bind(addr)

    if useUdp:
        while not kill:
            log.info("waiting for a message")
            data, clientAddr = sock.recvfrom(256)

            if data:
                decodedMsg = data.decode()
                log.info("recieved data:\n%s", decodedMsg)

                msgBack = decodedMsg + '\n'

                if decodedMsg == 'hello':
                    msgBack = 'world\n'
                elif decodedMsg == 'goodbye':
                    msgBack = 'farewell\n'
                    kill = True
                elif decodedMsg == 'exit':
                    msgBack = 'ok\n'
                    kill = True

                log.info("sending response")
                sock.sendto(msgBack.encode(), clientAddr)

    else:
        log.info("listening")
        sock.listen(1)

        while not kill:
            log.info("waiting for a client")
            conn, clientAddr = sock.accept()

            try:
                log.info("established connection")

                while not kill:
                    data = conn.recv(256)

                    if data:
                        decodedMsg = data.decode()
                        log.info("recieved data:\n%s", decodedMsg)

                        msgBack = decodedMsg + '\n'

                        if decodedMsg == 'hello':
                            msgBack = 'world\n'
                        elif decodedMsg == 'goodbye':
                            msgBack = 'farewell\n'
                            kill = True
                        elif decodedMsg == 'exit':
                            msgBack = 'ok\n'
                            kill = True

                        log.info("sending response")
                        conn.sendall(msgBack.encode())
            
            finally:
                conn.close()

# this method creates a socket to be used for a client.
# it uses the socket to send data to the server and then
# listens for a response
def client(host, port, useUdp, mcast):
    
    if mcast != MCAST_GRP:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try: 
            addr = (mcast, int(port))
            socket.inet_pton(socket.AF_INET, addr[0])
            sock.bind(addr)
            log.info("successfully bound specified multicast addres\n")
        except socket_error as serr:
            log.info("could not bind specified multicast address\n")
            addr = (MCAST_GRP, int(port))
            sock.bind(addr)

        log.info("address is: %s\n", addr)

        mreq = struct.pack("4sL", socket.inet_aton(addr[0]), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        while True:
            data, serverAddr = sock.recvfrom(1024)
            log.info("recieved msg: %s from %s", data.decode(), serverAddr)
            
            if data.decode() == "broadcast":
                break

        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MCAST_TTL)
        ack = socket.gethostname()
        #log.info("ack is: %s", ack)

        while True:
            sock.sendto(ack.encode(), addr)
            time.sleep(10)

        return
    # OLD CODE NOT USED IN ASSIGNMENT 4
    # | | | | |
    # v v v v v 

    addr = (host, int(port))
    log.info("address is: %s", addr)

    if useUdp:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    else:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        log.info("dialing")
        sock.connect(addr)

    try:
        while True:
            msg = input("What would you like to say to the server?\n")
            
            if not msg:
                continue

            if useUdp:
                sock.sendto(msg.encode(), addr)
                data, serverAddr = sock.recvfrom(256)
            else:
                log.info("sending data")
                sock.sendall(msg.encode())
                data = sock.recv(256)

            log.info("recieved data:")
            print(data.decode())

    finally:
        sock.close()
