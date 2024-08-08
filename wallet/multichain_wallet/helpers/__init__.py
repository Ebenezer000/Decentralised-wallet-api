import re
import blockcypher
from tronpy import Tron
from web3 import Web3
from solana.rpc.api import Client
from solders.pubkey import Pubkey
from tronpy.providers import HTTPProvider
from bs4 import BeautifulSoup

def extract_wallets_and_values(html_text, address, explorer_url):
    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html_text, 'html.parser')
    
    # Find all table rows
    rows = soup.find_all('tr')
    
    # Initialize the list to store wallet details
    full_history = []

    # Loop through each row
    for row in rows:
        # Find the address and value in the row
        recipient_raw = row.find('a', href=re.compile(r"^/address/0x[0-9a-fA-F]{40}"))
        value_tag = row.find('span', {'class': 'td_showValue'})
        amount_tag = row.find('span', {'class': 'td_showAmount'})
        method = row.find('span', {'class': 'd-block badge border border-opacity-10 text-dark fw-normal text-truncate w-100 py-1.5 bg-light border-dark dark:border-white'})
        trx_date = row.find('span', {'class': 'showDate'})
        trx_age = row.find('span', {'class': 'showAge'})
        transaction_hash = row.find('a', href=re.compile(r"^/tx/0x[0-9a-fA-F]{64}$"))

        inward_class = "badge bg-success bg-opacity-10 border border-success border-opacity-25 text-success fs-70x text-uppercase w-100 py-1.5"
        Inward_trx = row.find('span', {'class': inward_class})
        
        if recipient_raw and transaction_hash:
            # Extract and clean the address
            recipient = recipient_raw['href'].replace("/address/", "").strip()

            # Extract and clean the value
            value_text = value_tag.text if value_tag else None
            amount_raw = amount_tag.text if amount_tag else None

            # Debug: Print extracted elements
            print(f"Method: {method}")
            print(f"Inward_trx: {Inward_trx}")

            method_name = method.text if method else "Unknown"

            transaction_history = {
                "transaction_type": "IN" if Inward_trx else "OUT",
                "transaction_hash": transaction_hash['href'].replace("/tx/", "").strip() if transaction_hash else None,
                "transaction_name": method_name,
                "transaction_date": trx_date.text if trx_date else None,
                "transaction_age": trx_age.text if trx_age else None,
                "recieving_address": recipient,
                "amount": amount_raw,
                "amount_in_usd": value_text,
                'transaction_url': f"{explorer_url}/tx/{transaction_hash['href'].replace('/tx/', '').strip()}" if transaction_hash else None
            }
            full_history.append(transaction_history)
    
    return full_history

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
        if balance != "":
            return int(balance)
        else:
            return 0
        
    elif chain == "TRON":
        w3 = Tron(HTTPProvider('https://api.trongrid.io'))
        try:
            balance = w3.get_account_balance(address)
            if balance != "":
                return int(balance)
            else:
                return 0
        except Exception as e:
            return 0


    elif chain == "SOLANA":
        rpc_url = "https://api.mainnet-beta.solana.com"
        client = Client(rpc_url)

        try:
            address_pubkey = Pubkey.from_string(address)
            response = client.get_balance(address_pubkey)
            lamports = response.value
            sol = lamports / 1e9  # Convert lamports to SOL
            print(sol)
            return sol
        except Exception as e:
            print(f"Error fetching balance: {e}")
            return 0
        

