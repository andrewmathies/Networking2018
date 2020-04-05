#**************************************************************
# p2p.py - Andrwe Mathies (awmathie)
# CREATED: 12/10/2018
#**************************************************************

import logging as log
import socket
import sys
import time
import select
import threading

# this method creates a UDP socket to be used for a server,
# if two clients send messages then it sends their IP address
# and port to each other
def server(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    addr = (host, int(port))

    clients = []

    log.info("address is: %s", addr)
    log.info("binding")
    sock.bind(addr)

    while True:
        log.info("waiting for a message")
        data, clientAddr = sock.recvfrom(256)

        if clientAddr not in clients:
            clients.append(clientAddr)
        if len(clients) is 2:
            log.info("we've seen both clients now!")
            sock.sendto((clients[0][0] + " " + str(clients[0][1])).encode(), clients[1])
            sock.sendto((clients[1][0] + " " + str(clients[1][1])).encode(), clients[0])
            del clients[:]

        if data:
            decodedMsg = data.decode()
            log.info("recieved data: %s", decodedMsg)


# this method creates a UDP socket to be used for a client.
# first it sends a message to the specified server, then tries
# to connect to a peer by sending messages to the address it
# recieved from the server and listening to messages as well
def client(host, port):
    addr = (host, int(port))
    log.info("server address is: %s", addr)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        sock.sendto("yo".encode(), addr)

        data, serverAddr = sock.recvfrom(256)
        addrSplit = data.decode().split()
        
        peerAddr = (addrSplit[0], int(addrSplit[1]))
        log.info("peer address is: %s", peerAddr)

        sock.sendto("hello".encode(), peerAddr)
        data, aaddr = sock.recvfrom(256)
        log.info("connected to peer!")

        ListenThread(sock).start()
        print("Type and press enter to speak to the peer.\n")
        
        while True:
            msg = input()

            if not msg:
                continue

            sock.sendto(msg.encode(), peerAddr)

    finally:
        sock.close()

# this class is used by the client to listen to messages
# from the peer so peers can simultaneously send and recieve
class ListenThread(threading.Thread):

    def __init__(self, socket):
        self.sock = socket
        threading.Thread.__init__(self)

    def run(self):
        while True:
            data, rcvAddr = self.sock.recvfrom(256)
            print(data.decode())

