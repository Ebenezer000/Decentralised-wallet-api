import json
from flask import Response, Flask, request
from flask_cors import CORS
from zpywallet import wallet
from zpywallet.utils.bip32 import Wallet

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return "Hello Welcome to Leeway Wallet"


@app.route('/create_wallet', methods=['POST'])
def create_wallet():
    # body: tuple = request.json
    # phone: str = body["user_id"]
    w = wallet.generate_mnemonic()
    wallet_tuple = Wallet.from_mnemonic(w)

    return wallet_tuple['seed']

@app.route('/transfer_btc', methods=['POST'])
def transfer_btc():
    body: tuple = request.json
    phone: str = body["user_id"]

@app.route('/transfer_eth', methods=['POST'])
def transfer_btc():
    body: tuple = request.json
    phone: str = body["user_id"]

@app.route('/transfer_solana', methods=['POST'])
def transfer_btc():
    body: tuple = request.json
    phone: str = body["user_id"]

@app.route('/transfer_tron', methods=['POST'])
def transfer_btc():
    body: tuple = request.json
    phone: str = body["user_id"]
