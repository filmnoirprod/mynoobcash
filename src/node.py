import block
import wallet

class node:
	def __init__():
		self.NBC=100;
		##set

		#self.chain
		#self.current_id_count
		#self.NBCs
		self.wallet

		#slef.ring[]   #here we store information for every node, as its id, its address (ip:port) its public key and its balance




	def create_new_block():
		print(1)

	def create_wallet(self):
		#create a wallet for this node, with a public key and a private key
			self.wallet = wallet()

	def register_node_to_ring():
		#add this node to the ring, only the bootstrap node can add a node to the ring after checking his wallet and ip:port address
		#bottstrap node informs all other nodes and gives the request node an id and 100 NBCs
		print(1)


	def create_transaction(sender, receiver, signature):
		#remember to broadcast it
		print(1)


	def broadcast_transaction():
		print(1)


	def validdate_transaction():
		#use of signature and NBCs balance
		print(1)


	def add_transaction_to_block():
		#if enough transactions  mine
		print(1)



	def mine_block():
		print(1)



	def broadcast_block():
		print(1)




	#def valid_proof(.., difficulty=MINING_DIFFICULTY):
	#	print(1)

	#concencus functions

	def valid_chain(self, chain):
		#check for the longer chain accroose all nodes
		print(1)


	def resolve_conflicts(self):
		#resolve correct chain
		print(1)
