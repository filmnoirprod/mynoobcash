# Currently NOT in USE, just don't care

import sys
import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4
import wallet
import myblockchain

import threading
import requests
from flask import Flask, jsonify, request

NODES = 5

class node:
    def __init__(self):
        self.chain=myblockchain.Blockchain()
        self.current_id_count = 0
        self.wallet = wallet.wallet()
        self.ring = ["http://0.0.0.0:5000"]
    
    def start(self, argument, number_of_nodes):
        if (argument=="0"):
            print ("geia sou mano")
            self.node_id = 0
            self.chain.create_genesis(number_of_nodes, self.ring[0]) # 100 *number_of_nodes from wallet 0
            '''
            while (self.current_id_count < number_of_nodes):
                continue
            for i, address in enumerate(self.ring[1:]):
                self.send_init_info(i, address)
            for address in self.ring[1:]:
                continue
                # self.add_transaction(...)
            '''
        else:
            self.register_self()
        return self

    def send_init_info(self, i, address):
        message = {
            "node_id": i,
            "ring": self.ring
        }
        r = requests.post(address + '/nodes/register_ack', data = message)
        return self

    def register_self(self):
        message = {
            "address" : "http://0.0.0.0:5001"
        }
        r= request.post(self.ring[0] + '/nodes/register', data = message)
        return r


    def register_node(self, add):
        print ("alyziaki bravo")
        self.ring.append(add)
        self.current_id_count = self.current_id_count + 1
        if (self.current_id_count==NODES):
            for i, address in enumerate(self.ring[1:]):
                self.send_init_info(i, address)
            for address in self.ring[1:]:
                continue
                # self.add_transaction(...)