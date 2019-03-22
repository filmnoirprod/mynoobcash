import requests
from flask import Flask, jsonify, request, render_template
#from flask_cors import CORS

from collections import OrderedDict

import binascii
import block
import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
import hashlib
from time import time
import json

from urllib.parse import urlparse
from uuid import uuid4
import transaction
import node
import threading
import copy

Capacity = 4

class Blockchain():
    def __init__(self):
        self.list = []
        self.listoftr = []
        self.e = threading.Event()

    def get_addresses(self, addresses, id): # ring, node_id is node.id
        #print("aaaaaaaaaaaaaaaaaaaaaaaaa")
        self.ring = copy.deepcopy(addresses)
        self.id = id
        return

    def create_genesis(self, number, address):
        b = block.Block(len(self.list),nonce = 0, previousHash = 1)
        tr = transaction.Transaction("0", "0", address, 100 * (number+1),[])
        b.add_transaction_block(tr.to_dict())
        #print(b.listOfTransactions)
        b.myHash()
        self.list.append(b)

    def add_transaction(self, transaction):
        self.listoftr.append(transaction.to_dict())
        if(len(self.listoftr) == Capacity):
            node.no_mine.clear()
            new = block.Block(len(self.list),nonce = 0, previousHash = self.list[len(self.list)-1].hash)
            new.add_transaction_block(self.listoftr)
            self.listoftr = []
            self.e.clear()
            miner = threading.Thread(name = 'miner', target = self.dummy, args = (new, ))
            miner.start()
            return

    def dummy(self, new_block):
        print("start mining")
        new_block.mine_block(self.e) # mallon oxi to 2o orisma
        if (not self.e.isSet()): # we mined first the block, so we add it to our blockchain and broadcast it
            self.list.append(new_block)
            print("I found nonce")
            for address in self.ring:

                if (address != self.ring[self.id]):

                    message = {
                        'last_block': self.list[-1].output() # to JSON
                    }
                    m = json.dumps(message) #jsonify(message)
                    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                    #print (message)
                    # add headers

                    r = requests.post(address + '/nodes/mined_block', data = m, headers = headers)
                    print (r)
                    node.no_mine.set()
        return

    def output (self):
        outlist = []
        for bl in self.list:
            outlist.append(bl.output())
        return outlist
