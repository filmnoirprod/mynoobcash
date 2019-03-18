import blockchain
from time import time
import hashlib
import json



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
		print(string)
		return hashlib.sha224(string).hexdigest()

	def add_transaction(self, transaction):
		#add a transaction to the block
		self.listOfTransactions.append(transaction.to_dict())
		return self