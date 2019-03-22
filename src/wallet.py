import binascii

import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4


class wallet:

    def __init__(self):
        self.private_key, self.public_key = self.create_keys()
        self.address = self.public_key
        self.transactions = []

    def mybalance(self):
    	s = 0
    	for tr in self.transactions:
    		s = s + tr['value']
    	return s

    def create_keys(self):
        random_gen = Crypto.Random.new().read
        priv = RSA.generate(1024, random_gen)
        pub = priv.publickey()
        return binascii.hexlify(priv.exportKey(format='DER')).decode('ascii'), binascii.hexlify(pub.exportKey(format='DER')).decode('ascii')

    def add_genesis(self,dict):
        trlist = dict['transactions']
        trans = {'myid': trlist[0]['transaction_id'], 
              'value' : trlist[0]['value'] , 
              'receiver' : trlist[0]['receiver_address']
              }
        self.transactions.append(trans)
        return self