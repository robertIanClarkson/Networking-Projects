#######################################################################
# File:             server.py
# Author:           Jose Ortiz
# Purpose:          CSC645 Assigment #1 TCP socket programming
# Description:      Template server class. You are free to modify this
#                   file to meet your own needs. Additionally, you are
#                   free to drop this client class, and add yours instead.
# Running:          Python 2: python server.py
#                   Python 3: python3 server.py
#                   Note: Must run the server before the client.
########################################################################
from builtins import object
import socket
from threading import Thread
from client_handler import ClientHandler

class Server(object):
    MAX_NUM_CONN = 10

    def __init__(self, ip_address='127.0.0.1', port=13000):
        """
        Class constructor
        :param ip_address:
        :param port:
        """
        # create an INET, STREAMing socket
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # server state
        self.clients = {}  # key: client_id, value: clientHandler
        self.names = {}  # key: client_id, value: client_name
        self.rooms = {} # key: room_number, value: [client_id]

        # TODO: bind the socket to a public host, and a well-known port
        self.host = ip_address
        self.port = port

    def _bind(self):
        try:
            self.serversocket.bind((self.host, self.port))
        except Exception as e:
            self.serversocket.close()
            raise Exception("ERROR: _bind --> {exception}".format(exception=e))

    def _listen(self):
        """
        Private method that puts the server in listening mode
        If successful, prints the string "Listening at <ip>/<port>"
        i.e "Listening at 127.0.0.1/10000"
        :return: VOID
        """
        # TODO: your code here
        try:
            self.serversocket.listen(self.MAX_NUM_CONN)
            print("Server listening at {host}/{port}".format(host=self.host, port=self.port))
        except Exception as e:
            self.serversocket.close()
            raise Exception("ERROR: _listen --> {exception}".format(exception=e))

    def _accept_clients(self):
        """
        Accept new clients
        :return: VOID
        """
        while True:
            try:
                # TODO: Accept a client
                # TODO: Create a thread of this client using the client_handler_threaded class
                clienthandler, addr = self.serversocket.accept()
                Thread(target=self.client_handler_thread, args=(clienthandler, addr)).start()
            except Exception as e:
                # TODO: Handle exceptions
                self.serversocket.close()
                raise Exception("ERROR: _accept_clients --> {exception}".format(exception=e))

    def client_handler_thread(self, clientsocket, address):
        """
        Sends the client id assigned to this clientsocket and
        Creates a new ClientHandler object
        See also ClientHandler Class
        :param clientsocket:
        :param address:
        :return: a client handler object.
        """
        try:
            # TODO: create a new client handler object and return it
            # create the client handler
            client_handler = ClientHandler(self, clientsocket, address)

            # init the CH
            client_handler.init()

            # run the main logic
            client_handler.run()

        except Exception as e:
            self.serversocket.close()
            raise Exception("ERROR: client_handler_thread --> ", e)

    def run(self):
        """
        Already implemented for you. Runs this client
        :return: VOID
        """
        self._bind()
        self._listen()
        self._accept_clients()

if __name__ == '__main__':
    server = Server()
    server.run()
