import json
from flask import Response, Flask, request
from zpywallet import wallet
from wallet.multichain_wallet import MultiChainWallet


app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello Welcome to Leeway Wallet"

@app.route('/create_mnemonic', methods=['POST'])
def create_mnemonic():
    # body: tuple = request.json
    # phone: str = body["user_id"]
    seed = wallet.generate_mnemonic()
    
    return seed

@app.route('/create_wallet', methods=['POST'])
def create_wallet():
    body: tuple = request.json
    seed: str = body["mnemonic"]
    multi_wallet = MultiChainWallet(seed)

    bitcoin = multi_wallet.get_bitcoin_account()
    eth = multi_wallet.get_eth_account()
    tron = multi_wallet.get_tron_account()
    solana = multi_wallet.get_solana_account()
    
    wallet_json = {
        'seed': seed,
        'bitcoin account': bitcoin,
        'eth account': eth,
        'tron account': tron,
        'solana account': solana
    }

    print(wallet_json)
    return Response(json.dumps(wallet_json), 200, mimetype="application/json")

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
