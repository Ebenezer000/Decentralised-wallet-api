import blockcypher
from tronpy import Tron
from web3 import Web3
from solana.rpc.api import Client
from tronpy.providers import HTTPProvider

def get_crypto_balance(address: str, coin_symbol: str = "btc") -> float:
    """
    Fetch the balance of a cryptocurrency address.

    Args:
        address (str): The cryptocurrency address to check.
        coin_symbol (str): The symbol of the cryptocurrency (e.g., "btc", "ltc", "dash", "doge").

    Returns:
        float: The balance in the corresponding cryptocurrency units.
    """
    try:
        # Define BlockCypher coin symbols
        coin_symbols = {
            "btc": "btc",    # Bitcoin
            "ltc": "ltc",    # Litecoin
            "dash": "dash",  # Dash
            "doge": "doge"   # Dogecoin
        }

        # Fetch the address details from BlockCypher for the specified coin
        if coin_symbol in coin_symbols:
            address_details = blockcypher.get_address_details(
                address, coin_symbol=coin_symbols[coin_symbol], api_key="15bd83fc27cf437db9fcb8c1358f8cfe"
            )
            balance_satoshis = address_details.get('balance', 0)
            balance = balance_satoshis / 1e8  # Convert satoshis to the main unit
            return balance
        else:
            print(f"Unsupported coin symbol: {coin_symbol}")
            return 0.0
    except Exception as e:
        print(f"Error fetching balance: {e}")
        return 0.0

       
def get_alt_crypto_balance(chain, address):
    """
    Function to retieve base balance of address
    Args:
        chain[str]: Name of current chain
        address[str]: Address of user
    Returns:
        str: balance of user     
    """
    balance = ""
    if chain == "ETHEREUM":
        w3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/073d45dbb7714609b5980055d74875dd"))
        balance = w3.eth.get_balance(address)
    
    elif chain == "TRON":
        w3 = Tron(HTTPProvider('https://api.trongrid.io'))
        balance = w3.get_account_balance(address)

    elif chain == "SOLANA":
        rpc_url: str = "https://api.mainnet-beta.solana.com"
        client = Client(rpc_url)
        response = client.get_balance(address)

        if response.get("result"):
            lamports = response["result"]["value"]
            sol = lamports / 1e9  # Convert lamports to SOL
            return sol
        else:
            print(f"Error fetching balance: {response.get('error')}")
            balance = "0"

    return balance 
