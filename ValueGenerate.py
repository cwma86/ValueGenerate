#! /usr/bin/env python
import argparse
import socket



class options():
    def __init__(self):
        parser = argparse.ArgumentParser(description='creates and publishes position data')
        parser.add_argument('--inputData', dest='inputData', type=str, 
                            nargs='?', help='input file to drive valueGeneration')
        args = parser.parse_args()
        self.inputText = args.inputData

class position:
    def __init__(self, x, y, z, time):
        self.x = x
        self.y = y
        self.z = z
        self.time = time

class velocity:
    def __init__(self, velocityX, velocityY, velocityZ):
        self.x = velocityX
        self.y = velocityY
        self.z = velocityZ

def main():
    inputArgs = options()
    host_ip, server_port = "127.0.0.1", 9999
    data = "position data"
    initPosition = position(1, 0, 0, 0)

    # TODO make the convert to string a class method
    data = str(initPosition.x) + " " + str(initPosition.y) + " " + \
            str(initPosition.z) + " " + str(initPosition.time)
    # TODO establish connection
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        tcp_client.connect((host_ip, server_port))
        # TODO populate data with the simulated positon
        tcp_client.sendall(bytes(data + "\n" , "ASCII"))

        received = tcp_client.recv(1024)
        # TODO do i need error handling for missed response? 
    finally:
        tcp_client.close()
    print("sent : {}".format(data))
    print("received: {}".format(received.decode))
    # TODO Publish data via TCP

    initVelocity = velocity(1,0,0) 
    startTime = initPosition.time
    endTime = 100
    newPosition = initPosition
    for time in range(startTime, endTime):
        timeDelta = time - initPosition.time
        newPosition.x = initPosition.x + initVelocity.x * timeDelta 
        newPosition.y = initPosition.y + initVelocity.y * timeDelta 
        newPosition.z = initPosition.z + initVelocity.z * timeDelta 
        newPosition.time = initPosition.time + timeDelta 
        print("position x = %s y = %s z = %s at time = %s" %(newPosition.x,
                                                 newPosition.y, newPosition.z, 
                                                 newPosition.time))
        # TODO publish next position

        initPosition = newPosition

if __name__ == "__main__":
    main()
