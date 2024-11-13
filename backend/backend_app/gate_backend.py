from flask import Flask, request, jsonify
from web3 import Web3
import json
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

app = Flask(__name__)

# Connect to School Backend
SCHOOL_BACKEND_URL = "http://localhost:5001"

# Connect to local Ethereum blockchain (e.g., Ganache)
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

# Load the contract ABI and address
with open("ZKACStorageABI.json") as f:
    contract_abi = json.load(f)
contract_address = "YOUR_CONTRACT_ADDRESS"
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Gate’s private key for decrypting user data
gate_private_key = RSA.import_key(open("gate_private_key.pem").read())

def verify_proof(a, s, y, p, g):
    # Generate the challenge
    e = int(SHA256.new((str(a) + str(y)).encode()).hexdigest(), 16)
    # Check if g^s % p == a * y^e % p
    return pow(g, s, p) == (a * pow(y, e, p)) % p

@app.route('/process_user_entry', methods=['POST'])
def process_user_entry():
    data = request.json
    encrypted_data = bytes.fromhex(data['encrypted_data'])
    
    # Decrypt data using the gate's private key
    cipher = PKCS1_OAEP.new(gate_private_key)
    decrypted_data = cipher.decrypt(encrypted_data).decode().split(',')
    a, s, y, ID_inv = map(int, decrypted_data)

    # Verify the proof
    g, p = 2, 23  # Example values for generator and prime
    if verify_proof(a, s, y, p, g):
        # Call school backend to validate and invalidate public key
        response = requests.post(f"{SCHOOL_BACKEND_URL}/invalidate_public_key", json={
            "public_key": y,
            "invalidation_id": ID_inv
        })
        return response.json()
    else:
        return jsonify({"status": "proof_invalid"}), 400

if __name__ == '__main__':
    app.run(port=5002)
