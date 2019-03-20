import block
import transaction as tr
import threading
import copy
import json
from flask import jsonify

CAPACITY = 10

class Blockchain:
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.ring = []
        self.node_id = 0

    def add_ring_and_id(self, ring, id):
        self.ring = copy.deepcopy(ring)
        self.node_id = id

    def create_genesis (self, first):
        self.current_transactions.append(first)
        genesis_block=block.Block(0, "1")
        genesis_block.add_transactions_to_block(self.current_transactions)
        self.current_transactions = []
        self.chain.append(genesis_block)

    def add_transaction (self, transaction): # transaction as dict
        self.current_transactions.append(transaction)
        if (len(current_transactions) == CAPACITY):
            new_block = block.Block(self.chain[-1].index + 1, self.chain[-1].currentHash)
            new_block.add_transactions_to_block(self.current_transactions)
            self.current_transactions = []
            self.e = threading.Event()
            self.e.clear()
            extra_thread = threading.Thread(target = dummy , name = 'miner', args = (new_block, ))    # an kano ego to mine
            #if(not self.e.isSet()) self.chain.append(new_block)

    def dummy(self, new_block):
        new_block.proof_of_work(self.e)
        if (not self.e.isSet()):
            # add my block and broadcast
            self.chain.append(new_block)
            # broadcast mined block and set e in api handle
            for i, address in enumerate(self.ring):
                if (i != self.node_id):
                    message = {
                        'blockchain': self.chain.output()
                    }
                    jsonify(message)
                    print (message)
                    r = requests.post(address + '/nodes/mined_block', data = message)
                    print (r)
        return self


    def output (self):
        outlist = []
        for bl in self.chain:
            outlist.append(bl.output())
        return outlist
