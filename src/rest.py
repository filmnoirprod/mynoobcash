import sys
import requests
import json
from flask import Flask, jsonify, request, render_template
#from uuid import uuid4
#from flask_cors import CORS

import node
import block
import blockchain
import wallet
import transaction


### JUST A BASIC EXAMPLE OF A REST API WITH FLASK

app = Flask(__name__)
#CORS(app)
# Generate a globally unique address for this node
# node_identifier = str(uuid4()).replace('-', '')

mynode=node.node(sys.argv[1], int(sys.argv[2]), sys.argv[3])

#.......................................................................................



# get all transactions in the blockchain


@app.route('/transactions/get', methods=['GET'])
def get_transactions():
    transactions = myblockchain.transactions

    response = {'transactions': transactions}
    return jsonify(response), 200

@app.route('/mine', methods=['GET'])
def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = myblockchain.last_block
    proof = myblockchain.proof_of_work(last_block)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    myblockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # Forge the new Block by adding it to the chain
    previous_hash = myblockchain.hash(last_block)
    block = myblockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    data = request.get_json()
    sender = data['sender_adress']
    receiver = data['receiver']
    value = data['value']
    myid = data['myid']
    in_list = data['inputs']
    out_list = data['outputs']
    sign = data['sign']
    
    # add 

    mynode.receive_trans(sender,receiver,value,myid,in_list,out_list,sign)
    
    response = {'message': 'ok'}
    return jsonify(response), 200


@app.route('/nodes/mined_block', methods=['POST'])
def node_found():
    values = request.get_json()
    blockchain = values['blockchain']
    print(blockchain)
    mynode.chain.e.set()

    # blockchain from JSON to list of blocks
    # compare with mynode.chain and resolve

    # check if better
    response = {
        'message': 'JOB DONE'
    }
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': mynode.chain.output()
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    #values = request.get_json(force=True)
    address = request.form['address']
    key = request.form['public_key']
    print(address)
    #address = values['address']
    if address is None:
        return "Error: Please supply a valid address", 400

    mynode.register_node(address, key)

    response = {
        'message': 'New node has been added to the ring'
    }
    return jsonify(response), 201

@app.route('/nodes/register_ack', methods=['POST'])
def register_ack():
    data = request.get_json()
    node_id = data['node_id']
    print (node_id)
    ring = data['ring']
    print (ring)
    genesis = data['genesis']
    print(genesis)
    public_key_list = data['public_key_list']
    if node_id is None:
        return "Error: Please supply a valid node id", 400
    if ring is None:
        return "Error: Please supply a valid ring", 400

    mynode.receive_init_info(node_id, ring, public_key_list, genesis )

    response = {
        'message': 'JOB DONE'
    }
    return jsonify(response), 201

@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = myblockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': myblockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': myblockchain.chain
        }

    return jsonify(response), 200


# run it once for every node

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(sys.argv[3]))

'''
if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)
'''
