import requests
from flask import Flask, jsonify, request, render_template
#from flask_cors import CORS
import sys
import json

import node
import wallet
import transaction
import wallet


### JUST A BASIC EXAMPLE OF A REST API WITH FLASK



app = Flask(__name__)
#CORS(app)
# user should provide rest api's ports
if(len(sys.argv)==1):
    print("Usage is python3 rest.py is_it_bootstrap? how_many_children? myPort ip_bootstrap myIP !")
    sys.exit(0)

if len(sys.argv) != 6:
    print("Usage is python3 rest.py is_it_bootstrap? how_many_children? myPort ip_bootstrap myIP !")
    sys.exit(0)

# orismata os exis : bootstrap? | arithmos_paidion | port pou trexeis | ip_bootstrap | ip_dikia_sou
start = node.node(sys.argv[1], int(sys.argv[2]),sys.argv[3], sys.argv[4], sys.argv[5])

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
    #print ("Address is",addr)
    amount = data['amount']
    #print("Amount is",amount)
    #current balance
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
            'message': "Not enough"
        }
    else:
        # stall transaction till mining is done
        if not node.no_mine.isSet():
            node.no_mine.wait()

        sender = start.public_key_list[start.id]
        receiver =  start.public_key_list[int(addr)]
        start.create_transaction(sender,receiver,int(amount))

        response = {
            'message': "Transaction completed successfully !"
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

    """
    myid = request.form['id']
    ring = request.form.getlist('ring')
    keys = request.form.getlist('public_key_list')
    gen_index = request.form['gen_index']
    gen_timestamp = request.form['gen_timestamp']
    gen_transactions = request.form.getlist('gen_transactions')
    gen_nonce = request.form['gen_nonce']
    gen_previousHash = request.form['gen_previous_hash']
    """
    data = request.get_json()
    myid = data['id']
    ring = data['ring']
    keys = data['public_key_list']
    genesis = data['genesis']

    #print("genesis", genesis)
    #print("myid",myid)
    #print("gen_timestamp",gen_timestamp)
    #print("gen_transactions",gen_transactions)
    #print("gen_nonce",gen_nonce)
    #print("gen_previousHash",gen_previousHash)
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
    #print(a)
    #print(mykey)
    start.reg_a_node(a,mykey)
    response = {'message': 'ok'}
    return jsonify(response), 200

@app.route('/transactions/new', methods = ['POST'])
def new_tran():
    """
    sender = request.form['sender_adress']
    receiver = request.form['receiver']
    value = request.form['value']
    myid = request.form['myid']
    in_list = request.form.getlist('inputs')
    out_list = request.form['outputs']
    sign = request.form['sign']
    """
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
    app.run(host=sys.argv[5], port = int(sys.argv[3]))
