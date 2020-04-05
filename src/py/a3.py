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

# this method creates a socket to be used for a server,
# and uses that socket to recieve data and send messages
# back based on the data we recieved
def server(host, port, useUdp, fileDescriptor):
    if useUdp:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    else:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    addr = (host, int(port))
    kill = False

    log.info("address is: %s", addr)
    log.info("binding")
    sock.bind(addr)

    if fileDescriptor is not None:
        sock.listen(5)

        conn, clientAddr = sock.accept()
        log.info("connected to client")
        data = conn.recv(256)
        while (data):
            log.info("recieving data")
            fileDescriptor.write(data)
            data = conn.recv(256)
        log.info("read entire file")
        fileDescriptor.close()
        conn.close()
        return

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
def client(host, port, useUdp, fileDescriptor):
    addr = (host, int(port))
    log.info("address is: %s", addr)

    sentFile = False

    if useUdp:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    else:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        log.info("dialing")
        sock.connect(addr)

    try:
        while True:
            if fileDescriptor is not None:
                data = fileDescriptor.read(256)
                while data:
                    if useUdp:
                        sock.sendto(data, addr)
                    else:
                        sock.send(data)
                    data = fileDescriptor.read(256)
                    log.info("sending data")
                
                fileDescriptor.close()
                log.info("finished sending file")
                return
            else: 
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
