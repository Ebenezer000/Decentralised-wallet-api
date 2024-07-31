import json
import requests
from flask import Response, Flask, request
from zpywallet import wallet
from wallet.multichain_wallet import MultiChainWallet
from wallet.multichain_wallet.chain import chains
from bip_utils import Bip44Coins


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
    
    wallet = {
        'seed': seed,
        'bitcoin account': bitcoin,
        'eth account': eth,
        'tron account': tron,
        'solana account': solana
    }

    wallet_json = json.dumps(wallet, indent=4)
    return Response(wallet_json, 200, mimetype="application/json")

@app.route('/fetch_wallet', methods=['POST'])
def fetch_wallet():
    body: tuple = request.json
    seed: str = body["mnemonic"]
    chain: str = body["chain"]

    multi_wallet = MultiChainWallet(seed)
    coin_type = chains[chain]['coin']
    wallet = multi_wallet.get_altcoin_account(coin_type)
    
    wallet = {
        'seed': seed,
        'wallet': wallet
    }

    wallet_json = json.dumps(wallet, indent=4)
    return Response(wallet_json, 200, mimetype="application/json")

@app.route('/fetch_price', methods=['POST'])
def fetch_price():

    # Define the cryptocurrencies and their CoinGecko IDs
    cryptos = {
        'bitcoin': 'bitcoin',
        'eth': 'ethereum',
        'tron': 'tron',
        'solana': 'solana'
    }

    # Base URL for CoinGecko API
    base_url = "https://api.coingecko.com/api/v3/simple/price"

    # Prepare the query parameters
    ids = ",".join(cryptos.values())
    params = {
        'ids': ids,
        'vs_currencies': 'usd'
    }

    try:
        # Send a GET request to the API
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an error if the request failed
        data = response.json()

        # Extract prices and store in the prices dictionary with the desired format
        prices = {
            'Bitcoin': f"$ {data['bitcoin']['usd']}",
            'Eth': f"$ {data['ethereum']['usd']}",
            'Tron': f"$ {data['tron']['usd']}",
            'Solana': f"$ {data['solana']['usd']}"
        }
        
        return Response(prices, 200, mimetype="application/json")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")


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
