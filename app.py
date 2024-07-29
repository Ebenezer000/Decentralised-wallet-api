import json
from flask import Response, Flask, request
from zpywallet import wallet
from zpywallet.utils.bip32 import HDWallet

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello Welcome to Leeway Wallet"


@app.route('/create_wallet', methods=['POST'])
def create_wallet():
    # body: tuple = request.json
    # phone: str = body["user_id"]
    w = wallet.generate_mnemonic()
    wallet_tuple = HDWallet.from_mnemonic(w)
    print(w)
    return w

@app.route('/transfer_btc', methods=['POST'])
def transfer_btc():
    body: tuple = request.json
    phone: str = body["user_id"]

@app.route('/transfer_eth', methods=['POST'])
def transfer_eth():
    body: tuple = request.json
    phone: str = body["user_id"]

@app.route('/transfer_solana', methods=['POST'])
def transfer_solana():
    body: tuple = request.json
    phone: str = body["user_id"]

@app.route('/transfer_tron', methods=['POST'])
def transfer_tron():
    body: tuple = request.json
    phone: str = body["user_id"]
