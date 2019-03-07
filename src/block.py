
import blockchain
import datetime as date
import hashlib as hasher



class Block:
	def __init__(self, previousHash):
		##set

		self.previousHash = previousHash
		self.timestamp = date.datetime.now()
		self.listOfTransactions = []
		self.nonce
		self.hash

	def myHash(self):
		#calculate self.hash
		sha = hasher.sha256()
	    sha.update(str(self.previous_hash) +
	               str(self.timestamp) +
	               str(self.listOfTransactions) +
	               str(self.nonce))
		self.hash = sha.hexdigest()

	def add_transaction(transaction transaction, blockchain blockchain):
		#add a transaction to the block
