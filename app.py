# Flask python app
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from web3 import Web3
from eth_account import Account
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialise Flask App
app = Flask(__name__)
CORS(app)

# Connect to Flare RPC (Change to Coston testnet)
FLARE_RPC_URL = os.getenv("FLARE_RPC_URL", "https://coston-api.flare.network/ext/bc/C/rpc")
web3 = Web3(Web3.HTTPProvider(FLARE_RPC_URL))

# Check if connected
if web3.is_connected():
    print("Connected to Flare RPC :-)")
else:
    print("Failed to connect to Flare RPC")

# Load wallet from private key
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
if not PRIVATE_KEY:
    raise ValueError("PRIVATE_KEY is missing! Check your .env file!")
try:
    ACCOUNT = Account.from_key(PRIVATE_KEY)
    wallet_address = ACCOUNT.address
except ValueError as e:
    raise ValueError("Invalid PRIVATE_KEY format! Ensure it's 64 characters long & a hex string") from e

# Initialise JWT authentication
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET", "supersecretkey")
jwt = JWTManager(app)


@app.route("/balance", methods=["GET"])
def get_balance():
    # Fetch the balance of the Wallet on Flare
    balance_wei = web3.eth.get_balance(wallet_address)
    balance_flr = web3.from_wei(balance_wei, "ether")
    return jsonify({"address": wallet_address, "balance": str(balance_flr) + " FLR"})

@app.route("/send_transaction", methods=["POST"])
def send_transaction():
    try:
        # Send FLR from Flask to another wallet.
        data = request.json
        to_address = data.get("to")
        amount = web3.to_wei(float(data.get("amount")), "ether")

        # Build transaction
        txn = {
            "from": wallet_address,
            "to": to_address,
            "value": amount,
            "gas": 21000,
            "gasPrice": web3.eth.gas_price,
            "nonce": web3.eth.get_transaction_count(wallet_address),
            "chainId": web3.eth.chain_id
        }
        
        # Sign and send transaction
        signed_txn = web3.eth.account.sign_transaction(txn, PRIVATE_KEY)
        txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

        return jsonify({"transaction_hash": txn_hash.hex()})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)