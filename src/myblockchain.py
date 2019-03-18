import block
import transaction as tr
CAPACITY = 10

class Blockchain:
    def __init__(self):
        #self.current_transactions = []
        self.chain = []

    def create_genesis (self, number_of_nodes, recipient_address):
        first = tr.Transaction("0", "0", recipient_address, 100*number_of_nodes)
        genesis_block=block.Block(0, 1)
        genesis_block.add_transaction(first)
        genesis_block.myHash()
        self.chain.append(genesis_block)
        


