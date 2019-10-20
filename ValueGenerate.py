#! /usr/bin/env python
import argparse
import socket
import random
from Position import Position
from Velocity import Velocity


class options():
    def __init__(self):
        parser = argparse.ArgumentParser(description='creates and publishes position data')
        parser.add_argument('--host', dest='host', default= "127.0.0.1", type=str, 
        nargs='?', help='Host IP address that data will be received')
        parser.add_argument('--port', '-p', dest='port', default=9999, type=int, 
        nargs='?', help='Host port that data will be received')
        parser.add_argument('--initialX','-x', dest='x', default=0.0, type=float, 
        nargs='?', help='Host port that data will be received')
        parser.add_argument('--initialY','-y', dest='y', default=0.0, type=float, 
        nargs='?', help='Host port that data will be received')
        parser.add_argument('--initialZ','-z', dest='z', default=0.0, type=float, 
        nargs='?', help='Host port that data will be received')
        parser.add_argument('--velocityX','-vx', dest='velX', default=0.0, type=float, 
        nargs='?', help='Host port that data will be received')
        parser.add_argument('--velocityY','-vy', dest='velY', default=0.0, type=float, 
        nargs='?', help='Host port that data will be received')
        parser.add_argument('--velocityZ','-vz', dest='velZ', default=0.0, type=float, 
        nargs='?', help='Host port that data will be received')
        args = parser.parse_args()
        self.host = args.host
        self.port = args.port
        self.x = args.x
        self.y = args.y
        self.z = args.z
        self.velX = args.velX
        self.velY = args.velY
        self.velZ = args.velZ



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
    initPosition = Position(inputArgs.x, inputArgs.y, inputArgs.z, 0)
    initVelocity = Velocity(inputArgs.velX, inputArgs.velY, inputArgs.velZ) 
    startTime = initPosition.time
    endTime = 20
    newPosition = initPosition

    for time in range(startTime, endTime):

        # Predict next position
        timeDelta = time - initPosition.time
        NoiseRange = 0.1 # set default noiseRange
        # SetNoise to % of the velocity
        if initVelocity.x > 0.0:
            NoiseRange = initVelocity.x * 0.1 
        xNoise = random.uniform(NoiseRange * -1, NoiseRange)
        newPosition.x = initPosition.x + initVelocity.x * timeDelta + xNoise
        if initVelocity.y > 0.0:
            NoiseRange = initVelocity.y * 0.1 
        yNoise = random.uniform(NoiseRange * -1, NoiseRange)
        newPosition.y = initPosition.y + initVelocity.y * timeDelta + yNoise
        if initVelocity.z > 0.0:
            NoiseRange = initVelocity.z * 0.1 
        zNoise = random.uniform(NoiseRange * -1, NoiseRange)
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
