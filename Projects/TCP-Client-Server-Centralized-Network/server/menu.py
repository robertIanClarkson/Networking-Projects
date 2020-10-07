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
        # data = {}
        option = self.option_selected()
        if 1 <= option <= 6:  # validates a valid option
            # TODO: implement your code here
            # (i,e  algo: if option == 1, then data = self.menu.option1, then. send request to server with the data)
            if(option == 1):
                send_data = self.option1()
                self.client.send(send_data)
                data = self.client.receive()
                print('\n', data['message'])
                for client in data['clients']:
                    print('\t* ', client)
                print()
            elif (option == 2):
                self.option2()
            elif (option == 3):
                return self.option3()
            elif (option == 4):
                return self.option4()
            elif (option == 5):
                return self.option5()
            elif (option == 6):
                return self.option6()
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
        menu = "****** TCP CHAT ******\r\n" \
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

    def option4(self):
        """
        TODO: Prepare the user input data for option 4 in the menu
        :param option:
        :return: a python dictionary with all the data needed from user in option 4.
        """
        data = {}
        data['option'] = 4
        # Your code here.
        return data

    def option5(self):
        """
        TODO: Prepare the user input data for option 5 in the menu
        :param option:
        :return: a python dictionary with all the data needed from user in option 5.
        """
        data = {}
        data['option'] = 5
        # Your code here.
        return data

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
