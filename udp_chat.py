#!/usr/bin/python
import os
import sys
import socket
from threading import Thread
import netifaces
import time


peerMap ={}
isdiscoverTriggered = False
commandList=["discover", "connect", "disconnect", "exit"]
peerMap = {}
UDP_LISTEN_PORT=5062


def switch(command="default"):
    global isdiscoverTriggered
    if command == "help":
        print cli_template(", ".join(commandList))
    elif command == "exit":
        return cli_template("Bye!")
    elif command == "discover":
        if not isdiscoverTriggered:
            isdiscoverTriggered=True
            Thread(target=discover).start()
        else:
            print cli_template("You have already triggered discovery request!")
    elif command == "exit":
        print cli_template("Bye!")
        sys.exit(0)

def discover():
    interface_name="en0"
    my_node_name="diljit"
    max_discover_requests=5
    while max_discover_requests:
        if interface_name:
            interface_address = netifaces.ifaddresses(interface_name)[netifaces.AF_LINK][0]['addr']
            print "diljit :",interface_address
            broadcast_ip_address =  (netifaces.ifaddresses(interface_name))[netifaces.AF_INET][0]['broadcast']
            my_ip_addr =  (netifaces.ifaddresses(interface_name))[netifaces.AF_INET][0]['addr']
            # example message="00:02:55:7b:b2:f6::192.168.1.10::john"
            # where params are split by ::
            message = "{}::{}::{}".format(interface_address, my_ip_addr, my_node_name)
            print "Sending discover request with self info {}".format(message)
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            print "broadcast ", broadcast_ip_address
            sock.sendto(message, (broadcast_ip_address, UDP_LISTEN_PORT))
            max_discover_requests -= 1
        time.sleep(10)


def cli_template(message=""):
    return "p2p_chat> {}".format(message)


def startServer(interface_name):
    print "interface name {}".format(interface_name)
    udp_ip = (netifaces.ifaddresses(interface_name))[netifaces.AF_INET][0]['addr']
    print "udp _ip {}".format(udp_ip)
    udp_port = UDP_LISTEN_PORT
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((udp_ip, udp_port))

    while True:
        print "Receiving..."
        data, addr = sock.recvfrom(1024)
        print "Received {}".format(data)
        if "::" in data:
            peer_node_mac_address, peer_node_ip_addr, peer_node_name = data.split("::")
            print "received peer info {} {} {}".format(peer_node_mac_address, peer_node_ip_addr, peer_node_name)
            if not peerMap.get(peer_node_name, None):
                #peer is not there in our map, lets add it in our map
                peerMap[peer_node_name] = peer_node_ip_addr
            else:
                #the item is already there in the map, could be two scenarios
                #the node could be restarted in a dhcp with a new node ip or sending a periodic broadcast request
                #anyways lets save inside the mao
                peerMap[peer_node_name] = peer_node_ip_addr
                print peerMap
        else:
            #could be a normal send request from a peer node,
            #message from a peer node
            final_message = ": ".join(data.split(">"))
            print cli_template(final_message)

def startClient(interface_name, my_node_name):
    global commandList
    print cli_template("Welcome to p2p chat!")
    print cli_template("Type help for commands")
    #start discover client and let it discover peers
    while True:
        command = raw_input(cli_template())
        switch(command)



def startCli(my_node_name, interface_name):
    print "Node name {}".format(my_node_name)
    print "Interface name {}".format(interface_name)
    #t1 = Thread(target=startServer, args=(interface_name,)).start()
    t2 = Thread(target=startClient, args=(interface_name, my_node_name)).start()

def chatCli():
    command = raw_input(cli_template())


def start(my_node_name, interface_name):
    print "Starting client chat"
    startCli(my_node_name, interface_name)


if __name__ == "__main__":
    my_node_name=sys.argv[2]
    interface_name=sys.argv[1]
    start(my_node_name, interface_name)
