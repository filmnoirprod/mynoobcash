import block
import transaction as tr

CAPACITY = 10

class Blockchain:
    def __init__(self):
        self.current_transactions = []
        self.chain = []

    def create_genesis (self, first):
        self.current_transactions.append(first)
        genesis_block=block.Block(0, "1")
        genesis_block.add_transactions_to_block(self.current_transactions)
        self.current_transactions = []
        self.chain.append(genesis_block)
        
    def add_transaction (self, transaction): # transaction as dict
        self.current_transactions.append(transaction) 
        if (len(current_transactions)==CAPACITY):
            new_block = block.Block(self.chain[-1].index + 1, self.chain[-1].currentHash)
            new_block.add_transactions_to_block(self.current_transactions)
            self.current_transactions = []
            new_block.proof_of_work()   # an kano ego to mine
            self.chain.append(new_block)
