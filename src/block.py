
import blockchain
import datetime as date
import hashlib as hasher



class Block:
	def __init__(self, i, previousHash):
		##set
		self.index = i
		self.timestamp = date.datetime.now()
		self.listOfTransactions = []
		self.nonce = 0
		self.hash
		self.previousHash = previousHash


	def myHash(self):
		#calculate self.hash
		sha = hasher.sha256()
	    sha.update(str(self.index)+
				   str(self.previous_hash) +
	               str(self.timestamp) +
	               str(self.listOfTransactions) +
	               str(self.nonce))
		self.hash = sha.hexdigest()

	def add_transaction(self, transaction):
		#add a transaction to the block
		self.listOfTransactions.append(transaction)
