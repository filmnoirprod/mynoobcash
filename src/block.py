
import blockchain
import requests
from flask import Flask, jsonify, request, render_template
#from flask_cors import CORS
import hashlib
import transaction
from time import time
import copy
import json

MINING_DIFFICULTY = 4

class Block():
    def __init__(self, index, nonce, previousHash): # index = len(Blockchain.list)
        ##set

        self.previousHash = previousHash
        self.timestamp = time()
        self.nonce = nonce
        self.listOfTransactions = []
        self.index = index
        self.hash = 0 # myHash()

    def myHash(self):
        #calculate self.hash
        block = {'index': self.index,
                'timestamp': self.timestamp,
                'transactions': self.listOfTransactions,
                'nonce': self.nonce,
                'previous_hash': self.previousHash}
        string = json.dumps(block, sort_keys=True).encode()
        self.hash =  hashlib.sha224(string).hexdigest()
        return self.hash

    def output(self):
        self.myHash()
        return {'index': self.index,'timestamp': self.timestamp,'transactions': self.listOfTransactions,'nonce': self.nonce,'previous_hash': self.previousHash,'current_hash': self.hash}

    def add_transaction_block(self, transaction):
        #add a transaction to the block
        #print("transaction genesis",transaction)
        self.listOfTransactions.append(transaction)
        self.myHash()
        return self

    def mine_block(self, e):
        while self.valid_proof() is False and not e.isSet():
        	self.nonce += 1
        return self

    def valid_proof(self, difficulty = MINING_DIFFICULTY):
        guess_hash = self.myHash()
        return guess_hash[:difficulty] == '0'*difficulty

    def input (self, orderedInfo):
        self.index = orderedInfo['index']
        self.timestamp = orderedInfo['timestamp']
        self.listOfTransactions = orderedInfo['transactions']
        self.nonce = orderedInfo['nonce']
        self.previousHash = orderedInfo['previous_hash']

    def verify_hash(self, supposed_hash):
        return self.myHash() == supposed_hash
