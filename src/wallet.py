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
        self.private_key = self.priv_key()
        self.public_key = self.pubc_key()
        self.address = self.public_key
        self.transactions = {}

	def input_transactions(self, value):
		sum = 0
		list_of_input = []
		for i in self.transactions.keys():
			sum += self.transactions[i]
			list_of_input.append(i)
			if sum >= value:
				break
		if sum < value:	# den iparxoun arketa lefta telika
			list_of_input = [] 
		else:
			for i in list_of_input:
				del self.transactions[i]
		return list_of_input, sum


    def mybalance(self):
		sum = 0
		for i in self.transactions:
			sum += i['value']
		return sum

    def priv_key(self):
        random_gen = Crypto.Random.new().read
        priv = RSA.generate(1024, random_gen)
        return  binascii.hexlify(priv.exportKey(format='DER')).decode('ascii')

    def pubc_key(self):
        pub = self.private_key.publickey()
        return binascii.hexlify(pub.exportKey(format='DER')).decode('ascii')

	def add_genesis(self, transaction):
		self.transactions[transaction['transaction_id']] = transaction
