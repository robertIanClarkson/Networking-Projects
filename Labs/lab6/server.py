########################################################################################################################
# Class: Computer Networks
# Date: 02/03/2020
# Lab3: TCP Server Socket
# Goal: Learning Networking in Python with TCP sockets
# Student Name: Robert Clarkson
# Student ID: 915433914
# Student Github Username: robertIanClarkson
# Lab Instructions: No partial credit will be given in this lab
# Program Running instructions: python3 server.py # compatible with python version 3
#
########################################################################################################################

# don't modify this imports.
import socket
import pickle
# from client_handler import ClientHandler
from threading import Thread


class Server(object):
    """
    The server class implements a server socket that can handle multiple client connections.
    It is really important to handle any exceptions that may occur because other clients
    are using the server too, and they may be unaware of the exceptions occurring. So, the
    server must not be stopped when a exception occurs. A proper message needs to be show in the
    server console.
    """
    MAX_NUM_CONN = 10  # keeps 10 clients in queue

    def __init__(self, host="127.0.0.1", port=12000):
        """
        Class constructor
        :param host: by default localhost. Note that '0.0.0.0' takes LAN ip address.
        :param port: by default 12000
        """
        self.host = host
        self.port = port
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TODO: create the server socket
        self.client_handlers = {}  # initializes client_handlers list

    def _bind(self):
        """
        # TODO: bind host and port to this server socket
        :return: VOID
        """
        self.serversocket.bind((self.host, self.port))

    def _listen(self):
        """
        # TODO: puts the server in listening mode.
        # TODO: if succesful, print the message "Server listening at ip/port"
        :return: VOID
        """
        try:
            self._bind()
            self.serversocket.listen(self.MAX_NUM_CONN)
            print("Server listening at ", self.host, "/", self.port)
        except Exception as e:
            print("ERROR: _listen --> ", e)
            self.serversocket.close()

    def threaded_client(self, clientsocket, addr):
        client_id = addr[1]
        # client_handler = ClientHandler(self, clientsocket, addr)  # self is the server instance
        # client_handler.run()  # inits all the components in client handler object
        # #  adds the client handler object to the list of all the clients objects created by this server.
        # #  key: client id, value: client handler
        # self.client_handlers[client_id] = client_handler  # assumes dict was initialized in class constructor
        # print(self.client_handlers.keys())

    def _accept_clients(self):
        """
        #TODO: Handle client connections to the server
        :return: VOID
        """
        while True:
            try:
                clienthandler, addr = self.serversocket.accept()
                self._send_clientid(clienthandler, addr[1])
                # creeate new client thread.
                # print(clienthandler, " | ", addr)
                Thread(target=self.threaded_client, args=(clienthandler, addr)).start()
            except Exception as e:
                print("ERROR: _accept_clients --> ", e)
                self.serversocket.close()
                break

    def _send_clientid(self, clienthandler, clientid):
        """
        # TODO: send the client id to a client that just connected to the server.
        :param clienthandler:
        :param clientid:
        :return: VOID
        """
        data = {'clientid': clientid}
        self.send(clienthandler, data)

    def send(self, clienthandler, data):
        """
        # TODO: Serialize the data with pickle.
        # TODO: call the send method from the clienthandler to send data
        :param clienthandler: the clienthandler created when connection was accepted
        :param data: raw data (not serialized yet)
        :return: VOID
        """
        serialized_data = pickle.dumps(data)
        clienthandler.send(serialized_data)

    def run(self):
        """
        Already implemented for you
        Run the server.
        :return: VOID
        """
        self._listen()
        self._accept_clients()


# main execution
# if __name__ == '__main__':
#     server = Server()
#     server.run()
