#! /usr/bin/env python
import argparse
import socket
import random
from Position import Position
from Velocity import Velocity


class options():
    def __init__(self):
        parser = argparse.ArgumentParser(description='creates and publishes position data')
        parser.add_argument('--host', dest='host', type=str, 
        nargs='?', help='Host IP address that data will be received')
        parser.add_argument('--port', '-p', dest='port', type=int, 
        nargs='?', help='Host port that data will be received')
        args = parser.parse_args()
        if args.host:
            self.host = args.host
        else:
            self.host = "127.0.0.1"
        if args.port:
            self.port = args.port
        else:
            self.port = 9999


def sendData(data, host, port):
    host_ip, server_port = host, port
    # Establish connection
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        tcp_client.connect((host_ip, server_port))
        # Populate data with the simulated positon
        tcp_client.sendall(bytes(data + "\n" , "ASCII"))

        received = tcp_client.recv(1024)
    finally:
        tcp_client.close()
    print("sent : {}".format(data))
    print("received: {}".format(received.decode))


def simulatePosition():
    inputArgs = options()
    initPosition = Position(1, 0, 0, 0)
    initVelocity = Velocity(1,0,0) 
    startTime = initPosition.time
    endTime = 20
    newPosition = initPosition

    for time in range(startTime, endTime):

        # Predict next position
        timeDelta = time - initPosition.time
        xNoise = random.uniform(-.3, .3)
        yNoise = random.uniform(-.3, .3)
        zNoise = random.uniform(-.3, .3)
        newPosition.x = initPosition.x + initVelocity.x * timeDelta + xNoise
        newPosition.y = initPosition.y + initVelocity.y * timeDelta + yNoise
        newPosition.z = initPosition.z + initVelocity.z * timeDelta + zNoise
        newPosition.time = initPosition.time + timeDelta 
        print("position x = %s y = %s z = %s at time = %s" %(newPosition.x,
                                                 newPosition.y, newPosition.z, 
                                                 newPosition.time))
        
        # Publish position data via TCP
        sendData(str(newPosition), inputArgs.host, inputArgs.port)
        initPosition = newPosition

if __name__ == "__main__":
    simulatePosition()
