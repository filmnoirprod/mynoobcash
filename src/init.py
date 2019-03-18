import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4

import requests
from flask import Flask, jsonify, request


class node:
    def __init__(self):
        self.node_id
        self.chain=blockchain()
        self.current_id_count = 0
        self.NBCs = 0
        self.wallet = wallet()
        self.ring = ["url"]
    
    def start(self, argument, number_of_nodes):
        if (argument==0):
            self.node_id = 0
            self.chain.create_genesis(number_of_nodes, ring[0]) # 100 *number_of_nodes from wallet 0
            while (self.current_id_count < number_of_nodes):
                continue
            for i, address in enumerate(ring[1:]):
                self.send_init_info(i, address)
            for address in ring[1:]:
                self.add_transaction(...)
        else:
            self.register_node()

    def send_init_info(self, i, address):
        message = {
            "node_id": i,
            "ring": self.ring
        }
        r = requests.post(address + '/nodes/register_ack', data = message)



    @app.route('/nodes/register', methods=['POST'])
    def register_nodes():
        if (self.node_id==0):
            values = request.get_json()

            node = values.get('node')
            if node is None:
                return "Error: Please supply a valid node", 400

            self.ring.append(node)
            self.current_id_count = self.current_id_count + 1

            response = {
                'message': 'New node has been added'
            }
            return jsonify(response), 201



if __name__ == '__main__':
    mynode=node()
    mynode.start(argument, number_of_nodes)
