# File: tracker.py
# Author: <your name here>
# SID: <your student id here>
# Date: <the date when this file was last updated/created/edited>
# Description: this file contains the implementation of the tracker class.

import bencodepy
import socket
import threading

import time # for timestamp

class Tracker:
    """
    This class contains methods that provide implementations to support trackerless peers
    supporting the DHT and KRPC protocols
    """

    DHT_PORT = 12001

    def __init__(self, server, torrent, announce=True):
        """
        TODO: Add more work here as needed.
        :param server:
        :param torrent:
        :param announce:
        """
        self._server = server
        self._torrent = torrent
        self._is_announce = announce
        # self._clienthandler = server.clienthandlers[0]
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.udp_socket.bind(("", self.DHT_PORT))
        # will story a list of dictionaries representing entries in the routing table
        # dictionaries stored here are in the following form
        # {'nodeID': '<the node id is a SHA1 hash of the ip_address and port of the server node and a random uuid>',
        #  'ip_address': '<the ip address of the node>', 'port': '<the port number of the node',
        #  'info_hash': '<the info hash from the torrent file>', last_changed': 'timestamp'}
        self._routing_table = []

    def broadcast(self, message, self_broadcast_enabled=False):
        try:
            # print(f'Broadcast: {message}')
            encoded_message = self.encode(message)
            self.udp_socket.sendto(encoded_message, ('<broadcast>', self.DHT_PORT))
            print('Broadcasting...')
        except socket.error as error:
            print(error) 

    def send_udp_message(self, message, ip, port):
        try:
            new_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            message= self.encode(message)
            new_socket.sendto(message, (ip, port))
        except:
            print("Error sendinf UDP message")

    def broadcast_listener(self):
        try:
            print(f'Listening at DHT port --> {self.DHT_PORT}\n')
            while True:
                raw_data, sender_ip_and_port = self.udp_socket.recvfrom(4096)
                if raw_data:
                    data = self.decode(raw_data)
                    ip_sender = sender_ip_and_port[0]
                    port_sender = sender_ip_and_port[1]
                    print(f'data recieved by sender --> {data} | {ip_sender} | {port_sender}')
                    self.process_query(data, ip_sender, port_sender)
        except Exception as err:
            print("Error listening at DHT port")
            print(err)


    def encode(self, message):
        """
        bencodes a message
        :param message: a dictionary representing the message
        :return: the bencoded message
        """
        return bencodepy.encode(message)


    def decode(self, bencoded_message):
        """
        Decodes a bencoded message
        :param bencoded_message: the bencoded message
        :return: the original message
        """
        bc = bencodepy.Bencode(encoding='utf-8')
        return bc.decode(bencoded_message)



    def ping(self, t, y, a=None, r=None):
        """
        TODO: implement the ping method
        :param t:
        :param y:
        :param a:
        :return:
        """
        """
        TODO: implement the ping method. 
        :return:
        """
        # Send Ping
        message = {
            't': t,
            'y': y,
            'q': 'ping',
            'a': a
        }
        self.broadcast(message)


    def getNode(self, id):
        for node in self._routing_table:
            if node['id'] == id:
                return node
        return None

    def find_node(self, t, y, a=None, r=None):
        """
        TODO: implement the find_node method
        :return:
        """
        message = {"t":t, "y":y, "q":"find_node", "a": a}
        try:
            for node in self._routing_table:
                ip = node['ip_address']
                port = node['port']
                print(f'find_node --> {message} | {ip} | {port}')

                self.send_udp_message(message, ip, port) 
        except Exception as err:
            print(f'Failed to send find_node query --> {err}')

    def get_peers(self, t, y, a=None, r=None):
        """
        TODO: implement the get_peers method
        :return:
        """
        pass

    def announce_peers(self, t, y, a=None, r=None):
        """
        TODO: implement the announce_peers method
        :return:
        """
        pass

    def addNode(self, nodeID, ip_address, port, info_hash, last_changed):
        # will story a list of dictionaries representing entries in the routing table
        # dictionaries stored here are in the following form
        # {'nodeID': '<the node id is a SHA1 hash of the ip_address and port of the server node and a random uuid>',
        #  'ip_address': '<the ip address of the node>', 'port': '<the port number of the node',
        #  'info_hash': '<the info hash from the torrent file>', last_changed': 'timestamp'}
        node = {
            'nodeID': nodeID,
            'ip_address': ip_address,
            'port': port,
            'info_hash': info_hash,
            'last_changed': last_changed
        }
        self._routing_table.append(node)
        print(f'Added Node: {node}')

    def process_query(self, query, ip_sender, port_sender):
        """
        TODO: process an incoming query from a node
        :return: the response
        """
        print(f'Process: {query} | {ip_sender} | {port_sender}')
        
        # QUERY
        if(query['y'] == 'q'):
            # PING QUERY
            if(query['q'] == 'ping'):
                print('PING')

                # Add node to routing table
                try:
                    info_hash = self._torrent.info_hash()
                    timestamp = time.time()
                    self.addNode(query['a']['id'], ip_sender, port_sender, info_hash, timestamp)
                except Exception as err:
                    print(f'Failed to add node to routing table --> {err}')

                # Send response to ping
                try:
                    message = {
                        't': 'aa',
                        'y': 'r',
                        'r': {
                            "id":"0123456789abcdefghij", 
                            "nodes": "def456..."
                        }
                    }
                    self.send_udp_message(message, ip_sender, port_sender)
                except Exception as err:
                    print(f'Failed to send ping response --> {err}')

            # FIND_NODE QUERY     
            elif(query['q'] == 'find_node'):
                print('FIND_NODE')
                

        
        # RESPONSE
        elif(query['y'] == 'r'):
            print('RESPONSE')


    def send_response(self):
        """
        TODO: send a response to a specific node
        :return:
        """
        pass

    def run(self, start_with_broadcast=True):
        """
        TODO: This function is called from the peer.py to start this tracker
        :return: VOID
        """
        # FOR TESTING
        node = {}
        node['id'] = 'mnopqrstuvwxyz123456'
        node['ip'] = '10.0.0.222'
        node['port'] = 12001
        # self._routing_table.append(node)
        # ------------
        if self._is_announce:
            threading.Thread(target=self.broadcast_listener).start()
            if start_with_broadcast:
                # PING
                query = {
                    't': 'aa',
                    'y': 'q',
                    'q': 'ping',
                    'a': {
                        "id":"abcdefghij0123456789"
                    }
                }
                self.ping(t=query['t'], y=query['y'], a=query['a'])
                del query

                time.sleep(1)
                
                # FIND_NODE
                query = {
                    't': 'aa',
                    'y': 'q',
                    'q': 'find_node',
                    'a': {
                        'id': 'abcdefghij0123456789',
                        'target': 'mnopqrstuvwxyz123456'
                    }
                }
                self.find_node(t=query['t'], y=query['y'], a=query['a'])
                del query

                time.sleep(1)

                print('DONE')
        else:
            print('This tracker does not support DHT protocol')

# tracker = Tracker(None, None, True)
# tracker.run()

