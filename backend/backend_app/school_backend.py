from flask import Flask, request, jsonify
from web3 import Web3
import json
import os
app = Flask(__name__)

# Connect to Ganache or Ethereum node

# Connect to the Ethereum network
w3 = Web3(Web3.HTTPProvider('https://eth-sepolia.g.alchemy.com/v2/3LAfFWhjVk6bCEvhaSN-QK14ifGQclgp'))

# Load the contract ABI and address
abi_path = os.path.join(os.path.dirname(__file__), '../smart_contract/zkac_storage_abi.json')
with open(abi_path) as f:
    contract_abi = json.load(f)
contract_address = "0xeeccb8dc5c0f0a1d4aefc7aab5cb6dda4c73fbe6"
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# School address
manager_address = "0xb3ff7fa3992e9325cf47d2af0aca4ba1155b35c7"
private_key = "3b7041f06f948636c3ccc48dcae30b9fd60ac509d5bb71d5386a7448a86122ab"

@app.route('/invalidate_public_key', methods=['POST'])
def invalidate_public_key():
    data = request.json
    public_key = data['public_key']
    invalidation_id = data['invalidation_id']
    
    # Check if public key is valid
    is_valid = contract.functions.isPublicKeyValid(public_key).call()
    if not is_valid:
        return jsonify({"status": "public_key_invalid"}), 400

    # Invalidate the public key on blockchain
    txn = contract.functions.invalidatePublicKey(public_key).buildTransaction({
        'from': manager_address,
        'nonce': w3.eth.get_transaction_count(manager_address),
        'gas': 2000000,
        'gasPrice': w3.toWei('20', 'gwei')
    })
    signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)
    txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

    return jsonify({
        "status": "public_key_invalidated",
        "txn_hash": txn_hash.hex(),
        "public_key": public_key,
        "invalidation_id": invalidation_id
    })

@app.route('/update_public_key', methods=['POST'])
def update_public_key():
    data = request.json
    new_public_key = data['new_public_key']
    old_public_key = data['old_public_key']
    invalidation_id = data['invalidation_id']
    signature = data['signature']

    # Verify the signature with the old public key
    # (Assume we have a function to verify signature)

    # Update public key on the blockchain
    txn = contract.functions.updatePublicKey(new_public_key).buildTransaction({
        'from': manager_address,
        'nonce': w3.eth.get_transaction_count(manager_address),
        'gas': 2000000,
        'gasPrice': w3.toWei('20', 'gwei')
    })
    signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)
    txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

    return jsonify({
        "status": "public_key_updated",
        "txn_hash": txn_hash.hex(),
        "new_public_key": new_public_key
    })

if __name__ == '__main__':
    app.run(port=5001)
