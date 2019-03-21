import sys
import hashlib
import json
import time
from urllib.parse import urlparse
from uuid import uuid4
#import wallet
import block
import transaction as tr
import myblockchain
import copy

import wallet
import threading
import requests
from flask import Flask, jsonify, request

class node:
    def __init__(self, bootstrap, number_of_nodes, port):
        self.number_of_nodes = number_of_nodes
        self.chain=myblockchain.Blockchain()
        self.current_id_count = 0
        self.wallet = wallet.wallet()
        self.ring = ["http://0.0.0.0:5000"]
        self.public_key_list = []
        self.port = port
        if (bootstrap == "0"):
            self.node_id = 0
            self.public_key_list = [self.wallet.public_key]
            first = tr.Transaction("0", "0", self.ring[0], 100*number_of_nodes, [], 100*number_of_nodes) # 100 *number_of_nodes from wallet 0
            first = first.to_dict()
            self.wallet.add_genesis(first)
            # MALAKA add first to wallet dictionary
            self.chain.create_genesis(first)
            self.registered_everybody = threading.Event()
            self.registered_everybody.clear()
            extra_thread = threading.Thread(target = self.init_transactions, name="exta")
            extra_thread.start()
        else:
            self.register_self()

    def init_transactions(self):
        self.registered_everybody.wait()
        time.sleep(2)
        print("yes")
        # wait on a condition
        self.wallet_dictionary = {}
        for key in self.public_key_list:
            self.wallet_dictionary[key] = []
        for i, address in enumerate(self.ring[1:]):
            self.send_init_info(i+1, address)

        # send addresses to blockchain
        self.chain.add_ring_and_id(self.ring, self.node_id, self.public_key_list)

        for address in self.ring[1:]:
            continue
            # create ...
            # self.add_transaction(...)
            # peirazoume to wallet_dictionary
        return self

    def send_init_info(self, i, address): # used by bootstrap to send node id and ring
        message = {
            'node_id': i,
            'ring': self.ring,
            'public_key_list': self.public_key_list,
            'genesis': self.chain.chain[0].output()
        }
        m = json.dumps(message)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(address + '/nodes/register_ack', data = m, headers=headers)
        #r = flask.Request()
        print (r)
        return self

    def receive_init_info(self, i, ring, public_key_list, genesis):
        self.ring = copy.deepcopy(ring)
        self.public_key_list = copy.deepcopy(public_key_list)
        self.wallet_dictionary = {}
        for key in public_key_list:
            self.wallet_dictionary[key] = []
        self.node_id = i
        new = block.Block(0, "1")
        new.input(genesis)
        self.chain.chain.append(new)
        # send addresses to blockchain
        self.chain.add_ring_and_id(self.ring, self.node_id, self.public_key_list)
        return self

    def register_self(self): # used by others to register their self to bootstrap
        message = {
            'address' : "http://0.0.0.0:" + self.port,
            'public_key' : self.wallet.public_key
        }
        print(self.ring[0] + "/nodes/register")
        r = requests.post(self.ring[0] + "/nodes/register", data = message)
        print(message)
        print(r)
        return r

    def register_node(self, address, key): # used by boostrap to handle incoming registers
        self.ring.append(address)
        self.public_key_list.append(key)
        self.current_id_count = self.current_id_count + 1
        if (self.current_id_count == self.number_of_nodes):
            self.registered_everybody.set()
            # condision is set to true

    def create_new_block(): # vlepe blockchain
        print(1)


    def create_transaction(self, value, receiver, signature):
        list_of_input, sum = self.wallet.input_transactions(value)
        if (list_of_input == []):
            return "Out of money"
        else:
            mytransaction = tr.Transaction(self.wallet.public_key , self.wallet.private_key, receiver, value, list_of_input, sum)
            if mytransaction.transaction_outputs[1]['value'] != 0 :
                self.wallet.transactions.append(mytransaction.transaction_outputs[1])
            mytransaction = mytransaction.sign_transaction()
            self.chain.add_transaction(mytransaction.to_dict())
            self.broadcast_transaction(mytransaction)

    def receive_trans(sender,receiver,value,myid,in_list,out_list,sign):
        new_tr = tr.Transaction(sender, "0", receiver, value, in_list)
        new_tr.transaction_outputs = out_list


    def broadcast_transaction():
        print(1)


    def validdate_transaction():
    #use of signature and NBCs balance
        print(1)


    def add_transaction_to_block():
    #if enough transactions  mine
        print(1)



    def mine_block():
        print(1)



    def broadcast_block():
        print(1)




    #def valid_proof(.., difficulty=MINING_DIFFICULTY):
    #    print(1)

    #concencus functions

    def valid_chain(self, chain):
        #check for the longer chain accroose all nodes
        print(1)


    def resolve_conflicts(self):
        #resolve correct chain
        print(1)
