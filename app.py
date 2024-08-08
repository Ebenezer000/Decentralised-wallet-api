import json
import requests
from flask import Response, Flask, request
from zpywallet import wallet
from wallet.multichain_wallet import MultiChainWallet
from wallet.multichain_wallet.chain import chains
from wallet.evm import get_evm_balance, transfer_eth, phrase_to_account, transfer_token, import_token
from wallet.bitcoin import transfer_btc, transfer_altcoin
from wallet.solana import transfer_sol
from wallet.tron import transfer_trx, phrase_to_tron_account
from wallet.multichain_wallet.helpers import extract_wallets_and_values
from wallet.multichain_wallet.helpers.chain_paths import headers, chain_paths

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

    try:
        bitcoin = multi_wallet.get_bitcoin_account()
        eth = multi_wallet.get_eth_account()
        tron = multi_wallet.get_tron_account()
        solana = multi_wallet.get_solana_account()
        
        wallet = {
            'seed': seed,
            'bitcoin': bitcoin,
            'ethereum': eth,
            'tron': tron,
            'solana': solana
        }

        wallet_json = json.dumps(wallet, indent=4)
        return Response(wallet_json, 200, mimetype="application/json")
    except Exception as e:
        return Response(json.dumps(str(e)), 500, mimetype="application/json")

@app.route('/fetch_wallet', methods=['POST'])
def fetch_wallet():
    body: tuple = request.json
    seed: str = body["mnemonic"]
    chain: str = body["chain"]

    multi_wallet = MultiChainWallet(seed)
    try: 
        wallet = multi_wallet.get_altcoin_account(chain)
        
        wallet = {
            'seed': seed,
            'wallet': wallet
        }

        wallet_json = json.dumps(wallet, indent=4)
        return Response(wallet_json, 200, mimetype="application/json")
    except Exception as e:
        return Response(json.dumps(str(e)), 500, mimetype="application/json")

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
            'Bitcoin': f"${data['bitcoin']['usd']}",
            'Eth': f"${data['ethereum']['usd']}",
            'Tron': f"${data['tron']['usd']}",
            'Solana': f"${data['solana']['usd']}"
        }
        if prices:
            return prices
        else:
            return "Failed"

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

###
# EVM API CALS
###

@app.route('/transfer_evm', methods=['POST'])
def transfer_evm():
    body: tuple = request.json
    seed: str = body["seed"]
    recipient: str = body["recipient"]
    amount: str = body["amount"]
    rpc_provider: str = body["rpc_provider"]
    explorer_url: str = body["explorer_url"]

    try:
        account = phrase_to_account(rpc_provider, seed)
        transaction_details = transfer_eth(rpc_provider, explorer_url, account, recipient, amount)

        # transaction_details = {
        #     "transaction_state": "COMPLETED",
        #     "transaction_hash": tx_hash,
        #     "transaction_link": explore_link
        # }

        return transaction_details
    
    except Exception as e:
        return Response(json.dumps(str(e)), 500, mimetype="application/json")

@app.route('/import_chain', methods=['POST'])
def import_chain():
    body: tuple = request.json
    seed: str = body["seed"]
    rpc_provider: str = body['rpc_provider']

    try: 
        account = phrase_to_account(rpc_provider, seed)
        balance = get_evm_balance(rpc_provider, account["address"])

        wallet = {
            'seed': seed,
            'address': account['address'],
            'private_key': account['key'],
            'balance': balance
        }

        return wallet
    except Exception as e:
        return Response(json.dumps(str(e)), 500, mimetype="application/json")

@app.route('/transfer_token_evm', methods=['POST'])
def transfer_token_evm():
    body: tuple = request.json
    seed: str = body["seed"]
    recipient: str = body["recipient"]
    amount: str = body["amount"]
    token_address: str = body['token_address']
    rpc_provider: str = body["rpc_provider"]
    explorer_url: str = body["explorer_url"]

    try: 
        account = phrase_to_account(rpc_provider, seed)
        transaction_details = transfer_token(rpc_provider, explorer_url, account, recipient, token_address, amount)

        # transaction_details = {
        #     "transaction_state": "COMPLETED",
        #     "transaction_hash": tx_hash,
        #     "transaction_link": explore_link
        # }

        return transaction_details
    
    except Exception as e:
        return Response(json.dumps(str(e)), 500, mimetype="application/json")

@app.route('/import_token_evm', methods=['POST'])
def fetch_evm_token():
    body: tuple = request.json
    rpc_provider: str = body['rpc_provider']
    user_address: str = body['user_address']
    token_address: str = body['token_address']

    try: 
        token_details = import_token(rpc_provider, token_address, user_address)

        return token_details
    
    except Exception as e:
        return Response(json.dumps(str(e)), 500, mimetype="application/json")

@app.route('/fetch_token_image', methods =['POST'])
def get_token_image_url() -> str:
    """
    Retrieves the URL of a token image from the Trust Wallet GitHub repository.

    Args:
        chain (str): The blockchain name (e.g., "ethereum", "binance", "polygon").
        contract_address (str): The token's contract address.

    Returns:
        str: The URL of the token image.
    """
    # Map the blockchain to the corresponding GitHub path

    body: tuple = request.json
    chain: str = body["chain"]
    contract_address: str = body["contract_address"]

    chain_path = chain_paths[chain.lower()]
    if not chain_path:
        raise ValueError(f"Unsupported chain: {chain}")

    # Construct the URL for the token image
    base_url = "https://raw.githubusercontent.com/trustwallet/assets/master/blockchains"
    image_url = f"{base_url}/{chain_path}/assets/{contract_address}/logo.png"

    # Check if the image exists
    response = requests.get(image_url)
    if response.status_code == 200:
        return image_url
    else:
        return Response(json.dumps("Token image not found"), 500, mimetype="application/json")


###
# END EVM API CALS
###


###
# BTC ALTCOINS API CALS
###

@app.route('/transfer_btc_alts', methods=['POST'])
def transfer_btc_alts():
    body: tuple = request.json
    seed: str = body['seed']
    coin: str = body["chain"]
    recipient: str = body['recipient']
    amount: str = body['amount']
    transaction_hash = ""

    transaction_details = {
        "transaction_state" : "COMPLETED",
        "transaction_hash" : transaction_hash
    }

    multi_wallet = MultiChainWallet(seed)

    try:
        if coin in ['LITECOIN', 'DOGECOIN', 'DASH']:
            coin_symbol = (
                "doge" if coin == "DOGECOIN" 
                else "ltc" if coin == "LITECOIN" 
                else "dash"
            )
            coin_type = chains[coin]['coin']
            wallet_keys = multi_wallet.get_altcoin_account(coin_type)

            transaction_hash = transfer_altcoin(wallet_keys['private_key'], recipient, float(amount), coin_symbol)

        elif coin == "BITCOIN":
            coin_symbol = "btc"

            coin_type = chains[coin]['coin']
            wallet_keys = multi_wallet.get_altcoin_account(coin_type)

            transaction_hash = transfer_btc(wallet_keys['private_key'], recipient, float(amount), coin_symbol)

        return transaction_details
    
    except Exception as e:
        return Response(json.dumps(str(e)), 500, mimetype="application/json")
###
# END BTC ALTCOINS API CALS
###

@app.route('/transfer_solana', methods=['POST'])
def transfer_solana():
    body: tuple = request.json
    seed: str = body["seed"]
    recipient: str = body["recipient"]
    amount: str = body["amount"]
    try:
        tx_hash = transfer_sol(seed, recipient, amount)
        transaction_details = {
            "transaction_state": "COMPLETED",
            "transaction_hash": tx_hash,
            "transaction_link": f"https://solscan.io/tx/{tx_hash}"
        }

        return transaction_details
    except Exception as e:
        return Response(json.dumps(str(e)), 500, mimetype="application/json")
    
@app.route('/transfer_tron', methods=['POST'])
def transfer_tron():
    body: tuple = request.json
    seed: str = body["seed"]
    recipient: str = body["recipient"]
    amount: str = body["amount"]
    try:

        account = phrase_to_tron_account(seed)
        tx_hash = transfer_trx("mainnet", account, recipient, amount)

        transaction_details = {
            "transaction_state": "COMPLETED",
            "transaction_hash": tx_hash,
            "transaction_link": f"https://solscan.io/tx/{tx_hash}"
        }

        return transaction_details
    except Exception as e:
        return Response(json.dumps(str(e)), 500, mimetype="application/json")


@app.route('/fetch_history_evm', methods=['POST'])
def fetch_history_evm():
    body: tuple = request.json
    address: str = body["address"]
    explorer_url: str = body["explorer"]
    url = f"{explorer_url}/txs?a={address}&ps=25"

    try:
        response = requests.post(url, headers=headers)
        responseHTML = response.text

        transaction_history = extract_wallets_and_values(responseHTML, explorer_url)
        return Response(json.dumps(str(transaction_history)), 200, mimetype="application/json")
    except Exception as e:
        return Response(json.dumps(str(e)), 500, mimetype="application/json")


    