#######################################################################
# File:             client_handler.py
# Author:           Jose Ortiz
# Purpose:          CSC645 Assigment #1 TCP socket programming
# Description:      Template ClientHandler class. You are free to modify this
#                   file to meet your own needs. Additionally, you are
#                   free to drop this client handler class, and use a version of yours instead.
# Running:          Python 2: python server.py
#                   Python 3: python3 server.py
#                   Note: Must run the server before the client.
########################################################################
import pickle
import datetime
import threading
from menu import Menu


class ClientHandler(object):
    """
    The ClientHandler class provides methods to meet the functionality and services provided
    by a server. Examples of this are sending the menu options to the client when it connects,
    or processing the data sent by a specific client to the server.
    """

    def __init__(self, server_instance, clientsocket, addr):
        """
        Class constructor already implemented for you
        :param server_instance: normally passed as self from server object
        :param clientsocket: the socket representing the client accepted in server side
        :param addr: addr[0] = <server ip address> and addr[1] = <client id>
        """
        self.server_ip = addr[0]
        self.client_id = addr[1]
        self.server = server_instance
        self.clientsocket = clientsocket
        self.unread_messages = []

        self.print_lock = threading.Lock()
        self.clients_lock = threading.Lock()
        self.names_lock = threading.Lock()
        self.rooms_lock = threading.Lock()

    def _sendMenu(self):
        """
        Already implemented for you.
        sends the menu options to the client after the handshake between client and server is done.
        :return: VOID
        """
        fp = open('menu.py', 'rb')

        menuFile = {
            'message': 'new file',
            'file_name': 'menu.py',
            'file_content': fp.read()
        }

        menu = Menu(self.client_id)
        menuObj = {
            'message': 'menu',
            'menu': menu
        }
        self.send(menuFile)
        self.send(menuObj)

        self.thread_print('\t* Sent Menu to: {id}'.format(id=self.client_id))

    def process_options(self):
        """
        Process the option selected by the user and the data sent by the client related to that
        option. Note that validation of the option selected must be done in client and server.
        In this method, I already implemented the server validation of the option selected.
        :return:
        """
        while True:
            data = self.receive()

            self.thread_print(
                "(+) Received Data from: {id} --> option {message}".format(id=self.client_id, message=data['option']))
            if ('option' in data.keys()) and (1 <= data['option'] <= 6):  # validates a valid option selected
                option = data['option']
                if option == 1:
                    self._send_user_list()
                elif option == 2:
                    recipient_id = data['id']
                    message = data['message']
                    self._save_message(recipient_id, message)
                elif option == 3:
                    self._send_messages()
                elif option == 4:
                    room_id = data['room_id']
                    self._create_chat(room_id)
                elif option == 5:
                    room_id = data['room_id']
                    self._join_chat(room_id)
                elif option == 6:
                    self._disconnect_from_server()
                    return
            else:
                self.thread_print("The option selected is invalid")

    def _send_user_list(self):
        """
        TODO: send the list of users (clients ids) that are connected to this server.
        :return: VOID
        """
        self.clients_lock.acquire()
        message = "Users in server:"
        for client in self.server.clients.keys():
            message += " {name}:{id},".format(name=self.server.names[client], id=client)
        message = message.rstrip(',')
        self.clients_lock.release()
        data = {
            "message": message
        }
        self.send(data)

    def _save_message(self, recipient_id, message):
        """
        TODO: link and save the message received to the correct recipient. handle the error if recipient was not found
        :param recipient_id:
        :param message:
        :return: VOID
        """

        if recipient_id in self.server.clients:
            self.clients_lock.acquire()
            recipient_handler = self.server.clients[recipient_id]
            currentDatetime = datetime.datetime.now().replace(second=0, microsecond=0)
            recipient_handler.unread_messages.append((currentDatetime, message, self.server.names[self.client_id]))
            self.clients_lock.release()
            self.send({
                'message': "(+) Message Sent"
            })
        else:
            self.thread_print("(x) No user {id}".format(id=recipient_id))
            self.send({
                'message': "(x) No user {id}".format(id=recipient_id)
            })

    def _send_messages(self):
        """
        TODO: send all the unread messages of this client. if non unread messages found, send an empty list.
        TODO: make sure to delete the messages from list once the client acknowledges that they were read.
        :return: VOID
        """
        message = "My messages:"
        for msg in self.unread_messages:
            message += "\n{date}: {sent} (from: {sender})".format(date=msg[0], sent=msg[1], sender=msg[2])
        try:
            self.send({
                'message': message
            })
            self.unread_messages.clear()
        except Exception as e:
            self.thread_print("(x) Failed to get Messages from {id}".format(id=self.client_id))

    def _create_chat(self, room_id):
        """
        TODO: Creates a new chat in this server where two or more users can share messages in real time.
        :param room_id:
        :return: VOID
        """
        self.clients_lock.acquire()
        name = self.server.names[self.client_id]
        self.clients_lock.release()

        self.rooms_lock.acquire()
        self.server.rooms[room_id] = [self.client_id]
        self.rooms_lock.release()

        message = "----------------------- Chat Room {room_id} ------------------------ \r\n\r\nType \'exit\' to close the chat room.\r\nChat room created by: {name}\r\nWaiting for other users to join....".format(
            room_id=room_id, name=name)

        self.send({
            'message': message
        })

        self.chat(room_id)

    def _join_chat(self, room_id):
        """
        TODO: join a chat in a existing room
        :param room_id:
        :return: VOID
        """
        self.rooms_lock.acquire()
        self.server.rooms[room_id].append(self.client_id)
        self.rooms_lock.release()

        message = "----------------------- Chat Room {room_id} ------------------------\r\nJoined to chat room {room_id}\r\nType 'bye' to exit this chat room.".format(
            room_id=room_id)
        self.send({
            'message': message
        })

        self.rooms_lock.acquire()
        data = {}
        name = self.server.names[self.client_id]
        for client_id in self.server.rooms[room_id]:
            if self.client_id != client_id:
                client_handler = self.server.clients[client_id]
                data['message'] = "{name} joined".format(name=name)
                client_handler.send(data)
        self.rooms_lock.release()

        self.chat(room_id)

    def delete_client_data(self):
        """
        TODO: delete all the data related to this client from the server.
        :return: VOID
        """
        self.clients_lock.acquire()

        # delete client from server 'clients' & 'names'
        del self.server.clients[self.client_id]
        del self.server.names[self.client_id]

        # delete client from rooms if applicable
        for room in self.server.rooms:
            if self.client_id in room:
                room.remove(self.client_id)

        self.clients_lock.release()

    def _disconnect_from_server(self):
        """
        TODO: call delete_client_data() method, and then, disconnect this client from the server.
        :return: VOID
        """
        # print("_disconnect_from_server")
        self.delete_client_data()
        self.send({
            'message': 'Successfully Disconnected'
        })
        self.clientsocket.close()

    def chat(self, room_id):
        data = {}
        while True:
            # get new sent message
            recvMessage = self.receive()

            # send message to everyone in room
            self.rooms_lock.acquire()
            for client_id in self.server.rooms[room_id]:
                if self.client_id != client_id:
                    client_handler = self.server.clients[client_id]
                    client_handler.send(recvMessage)
            self.rooms_lock.release()

    def init(self):
        # log new client to server terminal
        self.thread_print("\n(+) Accept Client: {id}".format(id=self.client_id))
        if self.client_id not in self.server.clients:
            self.thread_print("\t* New Client ")
        else:
            self.thread_print("\t* Old Client ")

        # send ID, get client Name
        data = {'clientid': self.client_id}
        self.send(data)
        name = self.receive()

        # add to server clients (key: id) (value: CH)
        self.clients_lock.acquire()
        self.server.clients[self.client_id] = self
        self.clients_lock.release()

        # add to server names (key: id) (value: name)
        self.names_lock.acquire()
        self.server.names[self.client_id] = name
        self.names_lock.release()

        # log server's client list
        self.clients_lock.acquire()
        print("\t* Client List:")
        for client in self.server.clients:
            print("\t\t- {client}".format(client=client))
        self.clients_lock.release()

    def run(self):
        # main process
        self._sendMenu()
        self.process_options()

    def thread_print(self, str):
        self.print_lock.acquire()
        print(str)
        self.print_lock.release()

    def send(self, data):
        serialized_data = pickle.dumps(data)
        self.clientsocket.send(serialized_data)

    def receive(self, max_mem_alloc=4096):
        raw_data = self.clientsocket.recv(max_mem_alloc)
        data = pickle.loads(raw_data)
        return data
