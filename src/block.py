import myblockchain
from time import time
import hashlib
import json
import copy
from collections import OrderedDict

MINING_DIFFICULTY = 4

class Block:
	def __init__(self, i, previousHash):
		##set
		self.index = i
		self.timestamp = time()
		self.listOfTransactions = []
		self.nonce = 0
		self.previousHash = previousHash


	def myHash(self):
		#calculate self.hash
		block = {'index': self.index,
				'timestamp': self.timestamp,
				'transactions': self.listOfTransactions,
				'nonce': self.nonce,
				'previous_hash': self.previousHash}
		string = json.dumps(block, sort_keys=True).encode()
		self.currentHash = hashlib.sha224(string).hexdigest()
		return self.currentHash
		
	def add_transactions_to_block(self, transactions):
		#add the transactions list to the block when we reach the MAX capacity
		self.listOfTransactions = copy.deepcopy(transactions)
		self.myHash()
		return self

	def proof_of_work(self):
		while self.valid_proof() is False:
			self.nonce += 1
		return self

	def valid_proof(self, difficulty = MINING_DIFFICULTY):
		guess_hash = self.myHash()
		return guess_hash[:difficulty] == '0'*difficulty

	def output (self):
		return {'index': self.index,
				'timestamp': self.timestamp,
				'transactions': self.listOfTransactions,
				'nonce': self.nonce,
				'previous_hash': self.previousHash}

	def input (self, orderedInfo):
		self.index = orderedInfo['index']
		self.timestamp = orderedInfo['timestamp']
		self.listOfTransactions = orderedInfo['transactions']
		self.nonce = orderedInfo['nonce']
		self.previousHash = orderedInfo['previous_hash']