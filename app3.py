import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from web3 import Web3
from eth_account import Account
from dotenv import load_dotenv
import json
import requests

#import my own miniapps
from testGoogleAPIrequest import *

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

# Google API Key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Predefined courts and coaches
tennis_courts = [
    {"id": 1, "name": "Central Tennis Club", "address": "WC2N 5DU"},
    {"id": 2, "name": "East Side Badminton", "address": "EC1A 4HD"},
    {"id": 3, "name": "West Squash Center", "address": "W1B 2AB"}
]

coaches = [
    {"id": 101, "name": "John Doe", "address": "WC1A 1AA", "blockchain": "0xA1B2C3D4E5F6G7H8I9J0"},
    {"id": 102, "name": "Sarah Smith", "address": "EC1V 9AE", "blockchain": "0xB1C2D3E4F5G6H7I8J9K0"},
    {"id": 103, "name": "David Brown", "address": "W2 3PH", "blockchain": "0xC1D2E3F4G5H6I7J8K9L0"}
]

# Google API Integration
def get_coordinates(address):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={GOOGLE_API_KEY}"
    response = requests.get(url).json()
    if response["status"] == "OK":
        return response["results"][0]["geometry"]["location"]
    return None

def get_distances(origins, destinations):
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origins}&destinations={destinations}&units=imperial&key={GOOGLE_API_KEY}"
    response = requests.get(url).json()
    return response["rows"][0]["elements"]

@app.route("/courts", methods=["GET"])
def get_nearby_courts():
    user_address = request.args.get("postcode")
    user_coords = get_coordinates(user_address)
    if not user_coords:
        return jsonify({"error": "Invalid postcode"}), 400
    destinations = "|".join([court["address"] for court in tennis_courts])
    distances = get_distances(user_address, destinations)
    sorted_courts = sorted(
        [{"name": tennis_courts[i]["name"], "distance": distances[i]["distance"]["text"]} for i in range(len(tennis_courts))],
        key=lambda x: float(x["distance"].split()[0])
    )
    return jsonify(sorted_courts)

@app.route("/coaches", methods=["GET"])
def get_nearby_coaches():
    court_address = request.args.get("court")
    court_coords = get_coordinates(court_address)
    if not court_coords:
        return jsonify({"error": "Invalid court address"}), 400
    destinations = "|".join([coach["address"] for coach in coaches])
    distances = get_distances(court_address, destinations)
    sorted_coaches = sorted(
        [{"name": coaches[i]["name"], "distance": distances[i]["distance"]["text"], "blockchain": coaches[i]["blockchain"]}
         for i in range(len(coaches))],
        key=lambda x: float(x["distance"].split()[0])
    )
    return jsonify(sorted_coaches)

# Booking a court FUNCTIONALITY :-)
@app.route("/book_court", methods=["POST"])
def book_courts():
    court_address = request.args.get("court")
    court_coords = get_coordinates(court_address)
    if not court_coords:
        return jsonify({"error": "Invalid court address"}), 400
    # Book court


# Booking a coach FUNCTIONALITY :-)
@app.route("/book_coach", methods=["POST"])
def book_coach():
    pass

# SPECIAL REQUEST W/ GOOGLE API for postcode suggestions
@app.route("/postcode-check", methods=["GET"])
def postcode_check():
    # use imported function
    pc_origin = request.args.get("origin")
    pc_destination = request.args.get("destination")
    out1, out2 = distance_time_between_postcodes(pc_origin, pc_destination)
    return jsonify({"distance (miles)": out1, "duration (time)": out2})

@app.route("/")
def index():
    return render_template("main.html")

if __name__ == "__main__":
    app.run(debug=True)
