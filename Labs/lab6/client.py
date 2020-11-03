# copy and paste your code from your client.py file
# !/usr/bin/env python3
#######################################################################
# File:             client.py
# Author:           Jose Ortiz
# Purpose:          CSC645 Assigment #1 TCP socket programming
# Description:      Template client class. You are free to modify this
#                   file to meet your own needs. Additionally, you are 
#                   free to drop this client class, and add yours instead. 
# Running:          Python 2: python client.py 
#                   Python 3: python3 client.py
#
########################################################################
import socket
import pickle


class Client(object):
    def __init__(self, host, port):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = host
        self.port = port
        self.name = None
        self.clientid = 0
        self.menu = None

    def get_client_id(self):
        return self.clientid

    # get new client info and server specs
    def getClientInfo(self, host, port):
        self.host = input("Enter the server IP Address: ")
        if self.host == "":
            self.host = host
        self.port = input("Enter the server port: ")
        if self.port == "":
            self.port = port
        self.name = input("Your id key (i.e your name): ")
        if self.name == "":
            self.name = "anonymous"

    # connect to the server
    def connect(self, host="127.0.0.1", port=13000):
        self.getClientInfo(host, port)
        self.clientSocket.connect((host, port))  # connect is done here
        print("\nSuccessfully connected to server at {host}/{port}".format(host=host, port=port))

        # handshake between client and server
        # client gets its client_id
        self.clientid = self.receive()['clientid']

        # send the name of the client to the server
        self.send(self.name)

        # log some info for the client
        print("Your client info is:")
        print("Client Name: {name}".format(name=self.name))
        print("Client ID: {id}".format(id=self.clientid))

    # send data from client to CH
    def send(self, data):
        print('***Client: send()')
        serialized_data = pickle.dumps(data)
        self.clientSocket.send(serialized_data) \
 \
    # receive data from CH
    def receive(self, MAX_BUFFER_SIZE=8192):
        print('***Client: receive()')
        data_from_client = self.clientSocket.recv(MAX_BUFFER_SIZE)
        data = pickle.loads(data_from_client)
        return data

    # close the client
    def close(self):
        print('***Client: close()')
        self.clientSocket.close()

    def run(self):
        print('***Client: run()')
        self.clientSocket.bind((self.host, self.port))
        # self.clientSo
        print('bind')
        # self.clientSocket.listen(2)
        # print('listen')
        # clienthandler, addr = self.clientSocket.accept()
        # print('accept')
        # receiveData = self.receive()
        data = self.clientSocket.recvfrom(1024)
        print(data)
        print('receive')


# if __name__ == '__main__':
#     try:
#         client = Client()
#         client.connect()
#         client.run()
#     except KeyboardInterrupt as err:
#         print('\n(x) You left abruptly')
#     except Exception as err:
#         print('\n(x) Client Error --> {err}'.format(err=err))
#     finally:
#         exit()
