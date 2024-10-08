from web3 import Web3
from hexbytes import HexBytes
from wallet.evm.abi import TOKEN_ABI
from wallet.multichain_wallet.helpers.chain_paths import SERVICE_FEE_ADDRESS

def phrase_to_account(chain_provider, phrase) -> dict:
    """
    Function to turn seed phrase into account dictionary
    Args:
        chain[str]: Name of current chain
        phrase[str]: Seed phrase of account
    Returns:
        dict: account attached to seed phrase      
    """
    w3 = Web3(Web3.HTTPProvider(f'{chain_provider}'))
    account = ""

    w3.eth.account.enable_unaudited_hdwallet_features()
    acc = w3.eth.account.from_mnemonic(phrase)
    account = {
        "address": str(acc.address),
        "key": HexBytes.hex(acc.key),
    }
    return account

def get_evm_balance(chain_rpc, address):
    """
    Function to retieve base balance of address
    Args:
        chain_rpc[str]: RPC provider of chain
        address[str]: Address of user
    Returns:
        str: balance of user     
    """
    balance = ""
    w3 = Web3(Web3.HTTPProvider(chain_rpc))
    balance = w3.eth.get_balance(address)
    return balance

def transfer_eth(chain_provider, explorer, account, to_address, amount_ether, gas=21000, gas_price=None):
    """
    Transfer Ether from one account to another.
    
    Args:
        w3 (Web3): Web3 instance.
        account (dict): Account dictionary with 'address' and 'key'.
        to_address (str): Address to send Ether to.
        amount_ether (float): Amount of Ether to send.
        gas (int): Gas limit for the transaction (default: 21000).
        gas_price (int): Gas price in Wei (optional).
    
    Returns:
        str: Transaction hash.
    """
    w3 = Web3(Web3.HTTPProvider(f'{chain_provider}'))
    nonce = w3.eth.get_transaction_count(account["address"])
    gas_price = gas_price or w3.eth.gas_price
    transaction = {
        'to': to_address,
        'value': w3.to_wei(amount_ether, 'ether'),
        'gas': gas,
        'gasPrice': gas_price,
        'nonce': nonce
    }
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=account['key'])
    tx_hash = relay_transaction(signed_txn, w3, account['key'])
    explore_link = f"{explorer}/tx/{tx_hash}"
    complete_transaction = {
        "transaction_state": "COMPLETED",
        "transaction_hash": tx_hash,
        "transaction_link": explore_link
    }
    return complete_transaction

def relay_transaction(signed_tx , web3, private_key):
    SERVICE_FEE_ADDRESS_ETH = SERVICE_FEE_ADDRESS['ethereum']
    SERVICE_FEE_PERCENT = 0.001
    tx = web3.eth.account.decode_transaction(signed_tx)
    sender = tx['from']
    tx_value = tx['value']

    # Calculate service fee
    service_fee = int(tx_value * SERVICE_FEE_PERCENT)
    
    # Adjust transaction value
    adjusted_value = tx_value - service_fee

    # Rebuild the transaction with adjusted value
    tx['value'] = adjusted_value
    tx['nonce'] = web3.eth.get_transaction_count(sender)
    
    # Sign the adjusted transaction
    signed_tx = web3.eth.account.sign_transaction(tx, private_key)
    
    # Send the main transaction
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    
    # Send service fee transaction
    service_fee_tx = {
        'from': sender,
        'to': SERVICE_FEE_ADDRESS_ETH,
        'value': service_fee,
        'gas': 21000,
        'gasPrice': web3.eth.gas_price,
        'nonce': web3.eth.get_transaction_count(sender) + 1
    }
    signed_service_fee_tx = web3.eth.account.sign_transaction(service_fee_tx, private_key)
    web3.eth.send_raw_transaction(signed_service_fee_tx.rawTransaction)
    
    return  tx_hash.hex()

def transfer_token(chain_provider, explorer, account, to_address, token_contract_address, amount, gas=60000, gas_price=None):
    """
    Transfer ERC-20 tokens from one account to another.
    
    Args:
        w3 (Web3): Web3 instance.
        account (dict): Account dictionary with 'address' and 'key'.
        to_address (str): Address to send tokens to.
        token_contract_address (str): ERC-20 token contract address.
        amount (int): Amount of tokens to send.
        gas (int): Gas limit for the transaction (default: 60000).
        gas_price (int): Gas price in Wei (optional).
    
    Returns:
        str: Transaction hash.
    """
    w3 = Web3(Web3.HTTPProvider(f'{chain_provider}'))
    token_contract = w3.eth.contract(address=token_contract_address, abi=TOKEN_ABI)
    nonce = w3.eth.get_transaction_count(account["address"])
    gas_price = gas_price or w3.eth.gas_price
    transaction = token_contract.functions.transfer(to_address, amount).build_transaction({
        'gas': gas,
        'gasPrice': gas_price,
        'nonce': nonce
    })
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=account['key'])
    raw_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_hash = raw_hash.hex()
    explore_link = f"{explorer}/tx/{tx_hash}"
    complete_transaction = {
        "transaction_state": "COMPLETED",
        "transaction_hash": tx_hash,
        "transaction_link": explore_link
    }
    return complete_transaction

def import_token(chain_provider, token_address, owner_address ):
    """
    Function to retieve details of erc20 token
    Args:
        chain[str]: Name of current chain
        token[str]: Address of current token
    Returns:
        dict: details of token       
    """
    w3 =  Web3(Web3.HTTPProvider(chain_provider))
    token_contract = w3.eth.contract(Web3.to_checksum_address(token_address), abi= TOKEN_ABI)
    token_name = token_contract.caller.name()
    token_symbol = token_contract.caller.symbol()
    token_decimal = token_contract.caller.decimals()
    user_balance = token_contract.caller.balanceOf(owner_address)
    token = {
        "name": token_name,
        "symbol": token_symbol,
        "decimal": token_decimal,
        "balance": user_balance
    }

    return token

def interact_contract(chain_provider, account, contract_address, contract_abi, function_name, *args, gas=200000, gas_price=None):
    """
    Interact with a smart contract by calling a function.
    
    Args:
        w3 (Web3): Web3 instance.
        account (dict): Account dictionary with 'address' and 'key'.
        contract_address (str): Smart contract address.
        contract_abi (list): ABI of the smart contract.
        function_name (str): Name of the function to call.
        args: Arguments to pass to the function.
        gas (int): Gas limit for the transaction (default: 200000).
        gas_price (int): Gas price in Wei (optional).
    
    Returns:
        str: Transaction hash or function return value.
    """

    w3 = Web3(Web3.HTTPProvider(f'{chain_provider}'))
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)
    function = contract.functions[function_name](*args)
    nonce = w3.eth.get_transaction_count(account["address"])
    gas_price = gas_price or w3.eth.gas_price

    transaction = function.build_transaction({
        'gas': gas,
        'gasPrice': gas_price,
        'nonce': nonce
    })

    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=account['key'])
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return tx_hash.hex()

def sign_message(chain_provider, account, message):
    """
    Sign a message with the account's private key.
    
    Args:
        w3 (Web3): Web3 instance.
        account (dict): Account dictionary with 'address' and 'key'.
        message (str): Message to sign.
    
    Returns:
        dict: Signed message object.
    """
    w3 = Web3(Web3.HTTPProvider(f'{chain_provider}'))
    signed_message = w3.eth.account.sign_message(
        w3.eth.account.messages.encode_defunct(text=message),
        private_key=account['key']
    )
    return {
        'message': message,
        'messageHash': signed_message.messageHash.hex(),
        'r': signed_message.r,
        's': signed_message.s,
        'v': signed_message.v,
        'signature': signed_message.signature.hex()
    }
