import blockchain
import transaction
import requests
from flask import Flask, jsonify, request, render_template
import hashlib
from time import time
import copy
import json

MINING_DIFFICULTY = 4

class Block():
    def __init__(self, i, nonce, previousHash): 
        self.timestamp = time()
        self.index = i
        self.nonce = nonce
        self.previousHash = previousHash
        self.listOfTransactions = []
        self.hash = 0

    def myHash(self):
        block = {'index': self.index,
                'timestamp': self.timestamp,
                'transactions': self.listOfTransactions,
                'nonce': self.nonce,
                'previous_hash': self.previousHash}
        string = json.dumps(block, sort_keys=True).encode()
        self.hash =  hashlib.sha224(string).hexdigest()
        return self.hash

    def verify_hash(self, supposed_hash):
        return self.myHash() == supposed_hash

    def output(self):
        self.myHash()
        return {'index': self.index,
                'timestamp': self.timestamp,
                'transactions': self.listOfTransactions,
                'nonce': self.nonce,
                'previous_hash': self.previousHash,
                'current_hash': self.hash
                }

    def add_transaction_block(self, transaction):
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

    def input (self, Info):
        self.index = Info['index']
        self.timestamp = Info['timestamp']
        self.listOfTransactions = Info['transactions']
        self.nonce = Info['nonce']
        self.previousHash = Info['previous_hash']