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
        ##set
        #self.private_key = self.priv_key()
        #self.public_key = self.pub_key()
        self.private_key, self.public_key = self.keys()
        self.address = self.public_key
        self.transactions = []
        #self.priv = 0

    def mybalance(self):
    	mysum = 0
    	for i in range(0, len(self.transactions)):
    		mysum = mysum + self.transactions[i]['value']
    	return mysum

    def keys(self):
        random_gen = Crypto.Random.new().read
        priv = RSA.generate(1024, random_gen)
        pub = priv.publickey()
        return binascii.hexlify(priv.exportKey(format='DER')).decode('ascii'), binascii.hexlify(pub.exportKey(format='DER')).decode('ascii')

    def add_genesis(self,block_dict):
        newlist=block_dict['transactions']
        #print("add genesis ",newlist)
        t1 = {'myid': newlist[0]['transaction_id'], 'value' : newlist[0]['value'] , 'receiver' : newlist[0]['receiver_address']}
        self.transactions.append(t1)


"""
    def priv_key(self):
        random_gen = Crypto.Random.new().read
        self.priv = RSA.generate(1024, random_gen)
        return  binascii.hexlify(self.priv.exportKey(format='DER')).decode('ascii')

    def pub_key(self):
        pub = self.priv.publickey()
        return binascii.hexlify(pub.exportKey(format='DER')).decode('ascii')
"""
