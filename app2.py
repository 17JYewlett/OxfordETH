import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from web3 import Web3
from eth_account import Account
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Initialize Flask App
app = Flask(__name__)
CORS(app)

# Connect to Flare RPC
FLARE_RPC_URL = os.getenv("FLARE_RPC_URL", "https://coston-api.flare.network/ext/bc/C/rpc")
web3 = Web3(Web3.HTTPProvider(FLARE_RPC_URL))

if web3.is_connected():
    print("Connected to Flare RPC")
else:
    print("Failed to connect to Flare RPC")

# Load wallet from private key
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
if not PRIVATE_KEY:
    raise ValueError("PRIVATE_KEY is missing! Check your .env file!")

ACCOUNT = Account.from_key(PRIVATE_KEY)
wallet_address = ACCOUNT.address

# Load Contract ABI & Address
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
with open("contract_abi.json", "r") as abi_file:
    CONTRACT_ABI = json.load(abi_file)

contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

@app.route("/create_session", methods=["POST"])
def create_session():
    try:
        data = request.get_json()
        coach_address = data.get("coach")
        amount = web3.to_wei(float(data.get("amount")), "ether")

        txn = contract.functions.bookCourt(coach_address).build_transaction({
            'from': wallet_address,
            'value': amount,
            'gas': 200000,
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.get_transaction_count(wallet_address)
        })
        
        signed_txn = web3.eth.account.sign_transaction(txn, PRIVATE_KEY)
        txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        return jsonify({"transaction_hash": txn_hash.hex()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/checkin", methods=["POST"])
def checkin():
    try:
        data = request.get_json()
        session_id = int(data.get("session_id"))
        location = data.get("location")

        txn = contract.functions.checkIn(session_id, location).build_transaction({
            'from': wallet_address,
            'gas': 200000,
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.get_transaction_count(wallet_address)
        })
        
        signed_txn = web3.eth.account.sign_transaction(txn, PRIVATE_KEY)
        txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        return jsonify({"transaction_hash": txn_hash.hex()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/checkout", methods=["POST"])
def checkout():
    try:
        data = request.get_json()
        session_id = int(data.get("session_id"))
        location = data.get("location")

        txn = contract.functions.checkOut(session_id, location).build_transaction({
            'from': wallet_address,
            'gas': 200000,
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.get_transaction_count(wallet_address)
        })
        
        signed_txn = web3.eth.account.sign_transaction(txn, PRIVATE_KEY)
        txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        return jsonify({"transaction_hash": txn_hash.hex()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/session_details/<int:session_id>", methods=["GET"])
def session_details(session_id):
    try:
        result = contract.functions.getSessionDetails(session_id).call()
        session_info = {
            "user": result[0],
            "coach": result[1],
            "startLocation": result[2],
            "startTime": result[3],
            "endLocation": result[4],
            "endTime": result[5],
            "isPaid": result[6]
        }
        return jsonify(session_info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
