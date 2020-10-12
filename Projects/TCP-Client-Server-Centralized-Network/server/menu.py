#######################################################################################
# File:             menu.py
# Author:           Jose Ortiz
# Purpose:          CSC645 Assigment #1 TCP socket programming
# Description:      Template Menu class. You are free to modify this
#                   file to meet your own needs. Additionally, you are
#                   free to drop this Menu class, and use a version of yours instead.
# Important:        The server sends a object of this class to the client, so the client is
#                   in charge of handling the menu. This behaivor is strictly necesary since
#                   the client does not know which services the server provides until the
#                   clients creates a connection.
# Running:          This class is dependent of other classes.
# Usage :           menu = Menu() # creates object
#
########################################################################################

from threading import Thread

class Menu(object):
    """
    This class handles all the actions related to the user menu.
    An object of this class is serialized ans sent to the client side
    then, the client sets to itself as owner of this menu to handle all
    the available options.
    Note that user interactions are only done between client and user.
    The server or client_handler are only in charge of processing the
    data sent by the client, and send responses back.
    """

    def __init__(self, client):
        """
        Class constractor
        :param client: the client object on client side
        """
        self.client = client

    def set_client(self, client):
        self.client = client

    def show_menu(self):
        """
        TODO: 3. print the menu in client console.
        :return: VOID
        """
        print(self.get_menu())

    def process_user_data(self):
        """
        TODO: according to the option selected by the user, prepare the data that will be sent to the server.
        :param option:
        :return: VOID
        """
        data = {}
        option = self.option_selected()
        if 1 <= option <= 6:  # validates a valid option
            # TODO: implement your code here
            # (i,e  algo: if option == 1, then data = self.menu.option1, then. send request to server with the data)
            if(option == 1):
                data = self.option1()
            elif (option == 2):
                data = self.option2()
            elif (option == 3):
                data = self.option3()
            elif (option == 4):
                self.option4()
                return
            elif (option == 5):
                self.option5()
                return
            elif (option == 6):
                return self.option6()
            self.client.send(data)
            data = self.client.receive()
            print(data['message'])
        else:
            print('INVALID OPTION')
            return self.process_user_data()

    def option_selected(self):
        """
        TODO: takes the option selected by the user in the menu
        :return: the option selected.
        """
        # TODO: your code here.
        option = input('\nYour option <enter a number>: ')
        return int(option)

    def get_menu(self):
        """
        TODO: Inplement the following menu
        ****** TCP CHAT ******
        -----------------------
        Options Available:
        1. Get user list
        2. Sent a message
        3. Get my messages
        4. Create a new channel
        5. Chat in a channel with your friends
        6. Disconnect from server
        :return: a string representing the above menu.
        """
        menu = "\n****** TCP CHAT ******\r\n" \
               "-----------------------\r\n" \
               "Options Available:\r\n" \
               "1. Get user list\r\n" \
               "2. Send a message\r\n" \
               "3. Get my messages\r\n" \
               "4. Create a new channel\r\n" \
               "5. Chat in a channel with your friends\r\n" \
               "6. Disconnect from server"
        return menu

    def option1(self):
        """
        TODO: Prepare the user input data for option 1 in the menu
        :param option:
        :return: a python dictionary with all the data needed from user in option 1.
        """
        data = {}
        data['option'] = 1
        # Your code here.
        return data

    def option2(self):
        """
        TODO: Prepare the user input data for option 2 in the menu
        :param option:
        :return: a python dictionary with all the data needed from user in option 2.
        """
        data = {}
        data['option'] = 2
        # Your code here.
        data['message'] = input("Enter your message: ")
        data['id'] = int(input("Enter recipient id: "))
        return data

    def option3(self):
        """
        TODO: Prepare the user input data for option 3 in the menu
        :param option:
        :return: a python dictionary with all the data needed from user in option 3.
        """
        data = {}
        data['option'] = 3
        # Your code here.
        return data

    # special function
    def option4(self):
        """
        TODO: Prepare the user input data for option 4 in the menu
        :param option:
        :return: a python dictionary with all the data needed from user in option 4.
        """
        data = {}

        # Send send the server out options
        data['option'] = 4
        data['room_id'] = int(input("Enter new chat room id: "))
        self.client.send(data)

        # print the response "----------------------- Chat Room 23456 ------------------------"
        roomTitle = self.client.receive()['message']
        print(roomTitle)

        # basically I just need to figure out how to take input and print at the same time
        # Thread(target=self.chatSend(), args=()).start()
        # Thread(target=self.chatRecv(), args=()).start()

        while True:
            recv = self.client.receive()['message']
            print(recv)

        # while True:
        #     # recv = self.client.receive()
        #     # print(recv)
        #     send = input("> ")
        #     if send == "exit":
        #         break

    def option5(self):
        """
        TODO: Prepare the user input data for option 5 in the menu
        :param option:
        :return: a python dictionary with all the data needed from user in option 5.
        """
        data = {}
        data['option'] = 5
        data['room_id'] = int(input("Enter chat room id to join: "))
        self.client.send(data)

        roomTitle = self.client.receive()['message']
        print(roomTitle)

        sendData = {}
        while True:
            newMessage = input('> ')
            if newMessage == 'exit':
                break
            sendData['message'] = "{name}> {message}".format(name=self.client.name, message=newMessage)
            self.client.send(sendData)

        # Thread(target=self.chatSend(), args=()).start()
        # Thread(target=self.chatRecv(), args=()).start()

    def option6(self):
        """
        TODO: Prepare the user input data for option 6 in the menu
        :param option:
        :return: a python dictionary with all the data needed from user in option 6.
        """
        data = {}
        data['option'] = 6
        # Your code here.
        return data

    def chatRecv(self):
        while True:
            data = self.client.receive()
            print(data)

    def chatSend(self):
        data = {}
        while True:
            data['message'] = input('> ')
            self.client.send(data)
            if data['message'] == 'exit':
                break
