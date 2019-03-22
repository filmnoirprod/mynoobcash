import binascii
import block
import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
import requests
from flask import Flask, jsonify, request, render_template
from collections import OrderedDict
import hashlib
from time import time
import json
from urllib.parse import urlparse
from uuid import uuid4
import transaction as tr
import node
import threading
import copy

CAPACITY = 4

class Blockchain():
    def __init__(self):
        self.list = []
        self.listoftr = []
        self.e = threading.Event()

    def get_addresses(self, ring, id): 
        self.ring = copy.deepcopy(ring)
        self.id = id
        return

    def create_genesis(self, number, address):
        gen_block = block.Block(len(self.list), nonce = 0, previousHash = 1)
        trans = tr.Transaction("0", "0", address, 100 * (number+1),[])
        gen_block.add_transaction_block(trans.to_dict())
        gen_block.myHash()
        self.list.append(gen_block)

    def add_transaction(self, trans):
        self.listoftr.append(trans.to_dict())
        if(len(self.listoftr) == CAPACITY):
            node.no_mine.clear()
            new = block.Block(len(self.list),nonce = 0, previousHash = self.list[len(self.list)-1].hash)
            new.add_transaction_block(self.listoftr)
            self.listoftr = []
            self.e.clear()
            miner = threading.Thread(name = 'miner', target = self.helper, args = (new, ))
            miner.start()
            return

    def helper(self, new_block):
        print("Start Mining")
        new_block.mine_block(self.e)
        if (not self.e.isSet()):
            self.list.append(new_block)
            print("Nonce found")
            for address in self.ring:
                if (address != self.ring[self.id]):
                    message = {
                        'last_block': self.list[-1].output()
                    }
                    m = json.dumps(message)
                    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                    r = requests.post(address + '/nodes/mined_block', data = m, headers = headers)
                    node.no_mine.set()
        return

    def output (self):
        blockchain_aslist = []
        for block_item in self.list:
            blockchain_aslist.append(block_item.output())
        return blockchain_aslist