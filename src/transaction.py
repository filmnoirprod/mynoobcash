import requests
from flask import Flask, jsonify, request, render_template
import blockchain
import json
import hashlib
from collections import OrderedDict
import binascii
import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

class Transaction:

    def __init__(self, sender_addr, sender_private_key, rec_addr, value, transaction_inputs):
        self.sender_address = sender_addr
        self.receiver_address = rec_addr
        self.value = value
        self.transaction_inputs = transaction_inputs
        self.transaction_outputs = []
        self.transaction_id = self.hash()
        self.Signature = ""

    def hash(self):
        transaction = { 'sender' : self.sender_address,
                        'receiver': self.receiver_address, 
                        'value': self.value, 
                        'inputs': self.transaction_inputs
                      }
        string = json.dumps(transaction, sort_keys=True).encode()
        return hashlib.sha224(string).hexdigest()

    def to_dict(self):
        return OrderedDict({'sender_address': self.sender_address,
                           'receiver_address': self.receiver_address,
                           'value': self.value,
                           'transaction_id':self.transaction_id,
                           'transaction_inputs':self.transaction_inputs,
                           'transaction_outputs':self.transaction_outputs,
                           'Signature':self.Signature})

    def to_dict_nosign(self):
        return OrderedDict({'sender_address': self.sender_address,
                           'receiver_address': self.receiver_address,
                           'value': self.value,
                           'transaction_id':self.transaction_id,
                           'transaction_inputs':self.transaction_inputs,
                           'transaction_outputs':self.transaction_outputs})

    def sign_transaction(self,sender_private_key):
        private_key = RSA.importKey(binascii.unhexlify(sender_private_key))
        signer = PKCS1_v1_5.new(private_key)
        dictnosign = self.to_dict_nosign()
        h = SHA.new(str(dictnosign).encode('utf8'))
        return binascii.hexlify(signer.sign(h)).decode('ascii')