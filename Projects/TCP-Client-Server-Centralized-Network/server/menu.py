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

    def __init__(self, client):
        self.client = client

    def set_client(self, client):
        self.client = client

    def show_menu(self):
        print(self.get_menu())

    def process_user_data(self):
        data = {}
        option = self.option_selected()
        if 1 <= option <= 6:  # validates a valid option
            if (option == 1):
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
                # send disconnect option to CH
                data = self.option6()
                self.client.send(data)

                # print message from server
                data = self.client.receive()
                print(data['message'])

                # close the client's socket
                self.client.close()

                # exit the runtime
                exit()

            # send, receive, then print
            self.client.send(data)
            data = self.client.receive()
            print(data['message'])
        else:
            print('INVALID OPTION')
            return self.process_user_data()

    def option_selected(self):
        option = input('\nYour option <enter a number>: ')
        return int(option)


    def get_menu(self):
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
        data = {}
        data['option'] = 1
        return data

    def option2(self):
        data = {}
        data['option'] = 2
        data['message'] = input("Enter your message: ")
        data['id'] = int(input("Enter recipient id: "))
        return data

    def option3(self):
        data = {}
        data['option'] = 3
        return data

    def option4(self):
        # send the server our options
        data = {}
        data['option'] = 4
        data['room_id'] = int(input("Enter new chat room id: "))
        self.client.send(data)

        # print the chat header
        data = self.client.receive()
        if 'exit' not in data:
            roomTitle = data['message']
            print(roomTitle)

            # enter chat logic
            self.chat('exit')
        else:
            print(data['exit'])

    def option5(self):
        # send the server our options
        data = {}
        data['option'] = 5
        data['room_id'] = int(input("Enter chat room id to join: "))
        self.client.send(data)

        # print the chat header
        roomTitle = self.client.receive()['message']
        print(roomTitle)

        # enter chat logic
        self.chat('bye')

    def option6(self):
        data = {}
        data['option'] = 6
        return data

    # client side chat logic
    def chat(self, end_word):
        # create a new thread to handle incoming messages
        t = Thread(target=self.chatRecv, args=())
        t.start()

        # use this thread to handle client's new messages
        self.chatSend(end_word)

        # join the receive thread back into this thread
        t.join()

    def chatRecv(self):
        while True:
            # get message from server
            message = self.client.receive()
            if 'exit' in message:
                # break out of this loop
                print(message['exit'])
                return
            print(message['message'])

    def chatSend(self, end_word):
        sendData = {}
        while True:
            # get user input
            message = input()

            # send message to server
            sendData['message'] = message
            self.client.send(sendData)
            if message == end_word:
                # break out of this loop
                return
