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
            Thread(target=discover, args=   None).start()
        else:
            print cli_template("You have already triggered discovery request!")
    elif command == "exit"
        print cli_template("Bye!")
        sys.exit(0)

def discover(interface_name=None):
    max_discover_requests=5
    while max_discover_requests:
        if interface_name:
            interface_address = netifaces.ifaddresses(interface_name)[netifaces.AF_LINK]
            broadcast_ip_address = netifaces.ifaddresses(interface_name)[netifaces.AF_INET]['broadcast']
            my_ip_addr = netifacs.ifaddresses(inteface_name[netifaces.AF_INET])['addr']
            # example message="00:02:55:7b:b2:f6::192.168.1.10::john"
            # where params are split by ::
            message = "{}::{]::{}".format(interface_address, my_ip_addr, my_name)
            sock = socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.send(message, (broadcast_ip_address, UDP_PORT))
            max_discover_requests -= 1
    time.sleep(10)


def cli_template(message=""):
    return "p2p_chat> {}".format(message)


def startServer(ip, port):
    udp_ip = ip
    udp_port = port
    sock = socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(udp_ip, udp_port)

    while True:
        data, addr = sock.recvfrom(1024)
        print "Received {}".format(data)
        if "::" in data:
            peer_node_mac_address, peer_node_ip_addr, peer_node_name = data.split("::")
            if not peerMap.get(peer_node_name, None):
                #peer is not there in our map, lets add it in our map
                peerMap[peer_node_name] = peer_node_ip_addr
            else:
                #the item is already there in the map, could be two scenarios
                #the node could be restarted in a dhcp with a new node ip or sending a periodic broadcast request
                #anyways lets save inside the mao
                peerMap[peer_node_name] = peer_node_ip_addr
        else:
            #could be a normal send request from a peer node,
            #message from a peer node
            final_message = ": ".join(data.split(">"))
            print cli_template(final_message)

def startClient():
    global commandList
    print cli_template("Welcome to p2p chat!")
    print cli_template("Type help for commands")
    #start discover client and let it discover peers
    while True:
        command = raw_input(cli_template())
        switch(command)



def startCli():
    Thread(startServer, args=(ip, port)).start()
    Thread(startClient, args=None).start()

def chatCli():
    command = raw_input(cli_template())


def start():
    startCli()


if __name__ == "__main__":
    start()
