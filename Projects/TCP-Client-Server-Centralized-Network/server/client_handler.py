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

    def __init__(self, server_instance, clientsocket, addr):
        self.server_ip = addr[0]
        self.client_id = addr[1]  # important
        self.server = server_instance  # needed to use & alter <clients, names, rooms>
        self.clientsocket = clientsocket  # needed for sending and receiving
        self.unread_messages = []  # where this client's messages are stored

        self.print_lock = threading.Lock()  # for logging to server console.
        self.clients_lock = threading.Lock()  # for server.clients dictionary
        self.names_lock = threading.Lock()  # for server.names dictionary
        self.rooms_lock = threading.Lock()  # for server.rooms dictionary

    # send the menu file and object to the client, for the client to use
    def _sendMenu(self):
        # read the 'menu.py' file into a string
        fileContent = open('menu.py', 'rb').read()

        # create a 'menu.py' dictionary to send to client
        menuFile = {
            'message': 'new file',
            'file_name': 'menu.py',
            'file_content': fileContent
        }

        # send 'menu.py' to the client
        self.send(menuFile)
        self.thread_print('\t* Sent Menu File to: {id}'.format(id=self.client_id))

        # create a 'menu' obj dictionary to send to client
        menu = Menu(self.client_id)
        menuObj = {
            'message': 'menu',
            'menu': menu
        }

        # send 'menu' obj to client
        self.send(menuObj)
        self.thread_print('\t* Sent Menu Object to: {id}'.format(id=self.client_id))

    # main listening logic for incoming messages
    def process_options(self):
        # break out via option 6
        while True:
            # get data from client
            data = self.receive()

            # make sure data fits format
            if ('option' in data.keys()) and (1 <= data['option'] <= 6):
                option = data['option']

                # log to server
                self.thread_print(
                    "(+) Received Data from: {id} --> option {message}".format(id=self.client_id,
                                                                               message=option))
                # main option logic block
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
                    return  # breaks out of while True loop
            else:
                self.thread_print("The option selected is invalid")

    # send the client_id and name of everyone on the server
    def _send_user_list(self):
        self.clients_lock.acquire()

        # build the string to send
        message = "Users in server:"
        for client in self.server.clients.keys():
            message += " {name}:{id},".format(name=self.server.names[client], id=client)
        message = message.rstrip(',')

        self.clients_lock.release()

        # send the message to client
        data = {
            "message": message
        }
        self.send(data)

    # write a new message to the recipient's unread messages
    def _save_message(self, recipient_id, message):
        # check if client is in server
        if recipient_id in self.server.clients:

            # write message to recipient
            self.clients_lock.acquire()
            recipient_handler = self.server.clients[recipient_id]
            currentDatetime = datetime.datetime.now().replace(second=0, microsecond=0)
            recipient_handler.unread_messages.append((currentDatetime, message, self.server.names[self.client_id]))
            self.clients_lock.release()

            # inform client that their message was sent
            self.send({
                'message': "(+) Message Sent"
            })
        else:

            # inform server and client that there is no client with id <recipient_id>
            self.thread_print("(x) No user {id}".format(id=recipient_id))
            self.send({
                'message': "(x) No user {id}".format(id=recipient_id)
            })

    # send stored unread messages to the client
    def _send_messages(self):
        # Build a message string to send to the client
        message = "My messages:"
        self.clients_lock.acquire()
        for msg in self.unread_messages:
            message += "\n{date}: {sent} (from: {sender})".format(date=msg[0], sent=msg[1], sender=msg[2])
        self.clients_lock.release()

        # send messages to client
        self.send({
            'message': message
        })

        # clear all saved messages
        self.unread_messages.clear()

    # create a new chat room
    def _create_chat(self, room_id):
        # get the name of this client
        name = self.server.names[self.client_id]

        # handle logic if room_id is free or taken
        if room_id not in self.server.rooms:

            # create a new room with creator in it
            self.rooms_lock.acquire()
            self.server.rooms[room_id] = [self.client_id]
            self.rooms_lock.release()

            # send a title message to the creator client
            message = "----------------------- Chat Room {room_id} ------------------------ \r\n\r\nType \'exit\' to close the chat room.\r\nChat room created by: {name}\r\nWaiting for other users to join....".format(
                room_id=room_id, name=name)
            self.send({
                'message': message
            })

            # enter the main chat logic for a creator
            self.chat_create(room_id, 'exit')

        else:
            # send error message to client
            message = "Sorry, that room id is taken. Try a new room id"
            self.send({
                'exit': message
            })

    # Join an existing chat room
    def _join_chat(self, room_id):
        # Add client to chat room
        self.rooms_lock.acquire()
        self.server.rooms[room_id].append(self.client_id)
        self.rooms_lock.release()

        # send title message to client
        message = "----------------------- Chat Room {room_id} ------------------------\r\nJoined to chat room {room_id}\r\nType 'bye' to exit this chat room.".format(
            room_id=room_id)
        self.send({
            'message': message
        })

        # send 'user joined' message to everyone in room
        self.rooms_lock.acquire()
        data = {}
        name = self.server.names[self.client_id]
        for client_id in self.server.rooms[room_id]:
            if self.client_id != client_id:
                client_handler = self.server.clients[client_id]
                data['message'] = "{name} joined".format(name=name)
                client_handler.send(data)
        self.rooms_lock.release()

        # enter the main chat logic for a joiner
        self.chat_join(room_id, 'bye')

    # delete client data from server's global variables
    def delete_client_data(self):
        self.clients_lock.acquire()
        # delete client from server 'clients' & 'names'
        del self.server.clients[self.client_id]
        del self.server.names[self.client_id]

        # delete client from rooms if applicable
        for room in self.server.rooms:
            if self.client_id in room:
                room.remove(self.client_id)

        self.clients_lock.release()

    # Leave server
    def _disconnect_from_server(self):
        # delete all data related to client
        self.delete_client_data()

        # send success message to client
        self.send({
            'message': 'Successfully Disconnected'
        })

        # close the client socket
        self.clientsocket.close()

    # 'create' variant of chat logic
    def chat_create(self, room_id, end_word):
        data = {}
        while True:
            # get new message
            recvMessage = self.receive()

            # handle end word logic
            if recvMessage['message'] == end_word:
                self.rooms_lock.acquire()
                for client_id in self.server.rooms[room_id]:
                    if client_id != self.client_id:
                        # inform everyone that room is closed
                        client_handler = self.server.clients[client_id]
                        client_handler.send({
                            'exit': "Chatroom has been closed\nType 'bye' to leave"
                        })
                    else:
                        # inform client that his room is closed
                        self.send({
                            'exit': "Closed chatroom, bye."
                        })

                # delete the room
                del self.server.rooms[room_id]
                self.rooms_lock.release()
                return

            # send message to everyone in room
            self.rooms_lock.acquire()
            for client_id in self.server.rooms[room_id]:
                if self.client_id != client_id:
                    client_handler = self.server.clients[client_id]
                    message = "{name}> {message}".format(name=self.server.names[self.client_id],
                                                         message=recvMessage['message'])
                    client_handler.send({
                        'message': message
                    })
            self.rooms_lock.release()

    # 'join' variant of chat logic
    def chat_join(self, room_id, end_word):
        data = {}
        while True:
            # get new message
            recvMessage = self.receive()

            # check if client trying to leave
            if recvMessage['message'] == end_word:
                self.rooms_lock.acquire()
                if room_id in self.server.rooms:
                    # remove client from server.rooms
                    self.server.rooms[room_id].remove(self.client_id)
                    for client_id in self.server.rooms[room_id]:
                        if self.client_id != client_id:
                            # inform members of room that client has left
                            client_handler = self.server.clients[client_id]
                            client_handler.send({
                                'message': "{name} disconnected from the chat.".format(
                                    name=self.server.names[self.client_id])
                            })
                self.rooms_lock.release()

                # inform client that they have left the room
                self.send({
                    'exit': 'left chat'
                })
                return

            # send message to everyone in room
            self.rooms_lock.acquire()
            for client_id in self.server.rooms[room_id]:
                if self.client_id != client_id:
                    client_handler = self.server.clients[client_id]
                    message = "{name}> {message}".format(name=self.server.names[self.client_id],
                                                         message=recvMessage['message'])
                    client_handler.send({
                        'message': message
                    })
            self.rooms_lock.release()

    # initialize the client handler
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

    # A simple way to manage printing to console with threads
    def thread_print(self, str):
        self.print_lock.acquire()
        print(str)
        self.print_lock.release()

    # send method for this thread
    def send(self, data):
        serialized_data = pickle.dumps(data)
        self.clientsocket.send(serialized_data)

    # receive method for this thread
    def receive(self, max_mem_alloc=4096):
        raw_data = self.clientsocket.recv(max_mem_alloc)
        data = pickle.loads(raw_data)
        return data

    # main process
    def run(self):
        
        self._sendMenu()
        self.process_options()