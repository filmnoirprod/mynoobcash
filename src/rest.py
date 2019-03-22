import requests
from flask import Flask, jsonify, request, render_template
import sys
import json

import block
import node
import blockchain
import wallet
import transaction
import wallet

app = Flask(__name__)
start = node.node(sys.argv[1], int(sys.argv[2]),sys.argv[3])
blockchain = blockchain.Blockchain()
#.......................................................................................

@app.route('/show_balance', methods=['GET'])
def get_bal():
    bal = start.wallet.mybalance()
    response = {
        'Balance': bal
    }
    return jsonify(response), 200

@app.route('/view_transactions', methods=['GET'])
def get_trans():

    last_transactions = start.chain.list[-1].listOfTransactions
    # edo kati einai lathos
    response = {
        'reply': last_transactions,
        'List of transactions in the last verified block': last_transactions
    }
    return jsonify(response), 200

@app.route('/create_transaction', methods=['POST'])
def create():
    data = request.get_json()
    addr = data['addr']
    amount = data['amount']
    bal = start.wallet.mybalance()
    if (not addr.isnumeric() or int(addr) < 0 or int(addr) > start.nei):
        response = {
            'message': "Please provide a number between 0 and " + str(start.nei) + " as address."
        }
    elif (int(addr) == start.id):
        response = {
            'message': "You cannot make a transaction with yourself..."
        }
    elif (not amount.isnumeric() or int(amount) <= 0):
        response = {
            'message': "Please provide a positive number as amount."
        }
    elif int(amount) > bal:
        response = {
            #'message': "Ena pitsiriki, einai mpatiraki...",
            'CLICK HERE': "https://www.youtube.com/watch?v=TeT0vNbjs5w"
        }
    else:
        # stall transaction till mining is done
        if not node.no_mine.isSet():
            node.no_mine.wait()

        sender = start.public_key_list[start.id]
        receiver =  start.public_key_list[int(addr)]
        start.create_transaction(sender,receiver,int(amount))

        response = {
            'message': "Create transaction works !"
        }
    return jsonify(response), 200

@app.route('/nodes/mined_block', methods = ['POST'])
def node_found():
    values = request.get_json()
    last_block = values['last_block']   # isos to pairnei lathoss
    print("Last block of miner", last_block)
    if start.verify_and_add_block(last_block):
        node.no_mine.set()
        response = {
            'message' : 'BLOCK ADDED TO BLOCKCHAIN'
        }
        return jsonify(response), 201
    else:
        response = {
            'message' : 'BLOCK VERIFICATION FAILED'
        }
        return jsonify(response), 400

@app.route('/nodes/register', methods = ['POST'])
def register():
    data = request.get_json()
    myid = data['id']
    ring = data['ring']
    keys = data['public_key_list']
    genesis = data['genesis']
    if myid is None:
        return "Error:No valid myid",400
    if ring is None:
        return "Error:No valid ring",400
    if keys is None:
        return "Error:No valid public keys",400
    start.recieve(myid, ring,keys,genesis)
    response = {'message': 'ok'}
    return jsonify(response), 200

@app.route('/nodes/reg_dad', methods = ['POST'])
def reg():
    a = request.form['address']
    mykey = request.form['public_key']
    if a is None:
        return "Error:No valid address",400
    start.reg_a_node(a,mykey)
    response = {'message': 'ok'}
    return jsonify(response), 200

@app.route('/transactions/new', methods = ['POST'])
def new_tran():
    data = request.get_json()
    sender = data['sender']
    receiver = data['receiver']
    value = data['value']
    myid = data['myid']
    in_list = data['inputs']
    out_list = data['outputs']
    sign =data['sign']

    # NOT SURE IF NEEDED
    if not node.no_mine.isSet():
        node.no_mine.wait()

    start.receive_trans(sender,receiver,value,myid,in_list,out_list,sign)

    print("BALANCE",start.wallet.mybalance())
    response = {'message': 'ok'}
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host= sys.argv[5], port = int(sys.argv[3]))

