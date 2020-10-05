#!/usr/bin/env python3
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
import sys
import pickle


class Client(object):
    """
    The client class provides the following functionality:
    1. Connects to a TCP server 
    2. Send serialized data to the server by requests
    3. Retrieves and deserialize data from a TCP server
    """

    def __init__(self):
        """
        Class constractpr
        """
        # Creates the client socket
        # AF_INET refers to the address family ipv4.
        # The SOCK_STREAM means connection oriented TCP protocol.
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = None
        self.port = None
        self.name = None
        self.clientid = 0
        # self.menu = None

    def get_client_id(self):
        return self.clientid

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

    def connect(self, host="127.0.0.1", port=13000):
        """
        TODO: Connects to a server. Implements exception handler if connection is resetted. 
	    Then retrieves the cliend id assigned from server, and sets
        :param host: 
        :param port: 
        :return: VOID
        """
        try:
            self.getClientInfo(host, port)
            self.clientSocket.connect((host, port))
            print("\nSuccessfully connected to server at {host}/{port}".format(host=host, port=port))
            self.clientid = self.receive()['clientid']
            print("Client ID: {id}".format(id=self.clientid))
        except Exception as e:
            self.clientSocket.close()
            raise Exception("ERROR: connect --> {exception}".format(exception=e))

    def send(self, data):
        """
        TODO: Serializes and then sends data to server
        :param data:
        :return:
        """
        try:
            serialized_data = pickle.dumps(data)
            self.clientSocket.send(serialized_data)
        except Exception as e:
            self.clientSocket.close()
            raise Exception("ERROR: send --> {exception}".format(exception=e))

    def receive(self, MAX_BUFFER_SIZE=8192):
        """
        TODO: Desearializes the data received by the server
        :param MAX_BUFFER_SIZE: Max allowed allocated memory for this data
        :return: the deserialized data.
        """
        try:
            data_from_client = self.clientSocket.recv(MAX_BUFFER_SIZE)
            data = pickle.loads(data_from_client)
            return data
        except Exception as e:
            self.clientSocket.close()
            raise Exception("ERROR: receive --> {exception}".format(exception=e))

    def close(self):
        """
        TODO: close the client socket
        :return: VOID
        """
        try:
            self.clientSocket.close()
        except Exception as e:
            self.clientSocket.close()
            raise Exception("ERROR: close --> {exception}".format(exception=e))

    def run(self):
        while True:
            receiveData = self.receive()
            if (receiveData['id'] == self.clientid):
                # Get File
                if(receiveData['message'] == "new file"):
                    newFile = open(receiveData['file_name'], 'wb')
                    newFile.write(receiveData['file_content'])
                elif(receiveData['message'] == 'menu'):
                    menu = receiveData['data']
                    menu.show_menu()
                    option = input("Enter an option: ")
                    menu
            else:
                print("ERROR: Wrong ID")


if __name__ == '__main__':
    client = Client()
    client.connect()
    client.run()
