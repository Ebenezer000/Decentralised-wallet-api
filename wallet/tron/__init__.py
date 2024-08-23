from tronpy import Tron
from tronpy.keys import PrivateKey
from tronpy.keys import to_base58check_address
from tronpy.providers import HTTPProvider
from wallet.multichain_wallet.helpers.chain_paths import SERVICE_FEE_ADDRESS
from decimal import Decimal

def phrase_to_tron_account(seed: str):
    tron_w3 = Tron(HTTPProvider('https://api.trongrid.io'))
    tron_account = tron_w3.generate_address_from_mnemonic(mnemonic=seed)
    account = {
        "address": tron_account['base58check_address'],
        "private_key": tron_account['private_key']
    }

    return account

def transfer_trx(client: Tron, account: dict, to_address: str, amount_trx: float) -> str:
    """
    Transfer TRX from one account to another.

    Args:
        client (Tron): Tronpy client instance.
        account (dict): Account dictionary with 'address' and 'key'.
        to_address (str): Address to send TRX to.
        amount_trx (float): Amount of TRX to send.

    Returns:
        str: Transaction ID.
    """
    sender = PrivateKey(bytes.fromhex(account["key"]))
    txn = (
        client.trx.transfer(account["address"], to_address, int(amount_trx * 1_000_000))
        .memo("TRX Transfer")
        .build()
        .sign(sender)
    )
    tx_id = relay_tron_transaction(client, txn, account['key'])

    return tx_id

def relay_tron_transaction(client, tx_data, private_key):
    SERVICE_FEE_PERCENT = Decimal('0.001')
    client = Tron()
    transaction = client.get_transaction_from_raw(tx_data)
    
    # Calculate service fee
    amount = Decimal(transaction.amount) / Decimal(1e6)
    service_fee = amount * SERVICE_FEE_PERCENT
    adjusted_amount = amount - service_fee

    # Adjust the transaction value
    transaction.amount = int(adjusted_amount * Decimal(1e6))

    # Sign and send the transaction
    signed_tx = client.trx.sign(transaction, private_key)
    tx_hash = client.trx.broadcast(signed_tx).wait()

    # Service fee transaction
    service_fee_tx = client.trx.transfer(transaction['owner_address'], SERVICE_FEE_ADDRESS['tron'], int(service_fee * Decimal(1e6)))
    signed_service_fee_tx = client.trx.sign(service_fee_tx, private_key)
    client.trx.broadcast(signed_service_fee_tx)

    return  tx_hash['txid']

def import_tron_token(chain_provider, token_address, owner_address):
    """
    Function to retrieve details of a TRC20 token (Tron)
    Args:
        chain_provider [str]: RPC URL or API endpoint of the Tron network
        token_address [str]: Address of the TRC20 token
        owner_address [str]: Address of the token owner
    Returns:
        dict: details of token
    """
    client = Tron(chain_provider)

    token_contract = client.get_contract(token_address)
    token_name = token_contract.functions.name()
    token_symbol = token_contract.functions.symbol()
    token_decimals = token_contract.functions.decimals()
    user_balance = token_contract.functions.balanceOf(to_base58check_address(owner_address))

    token_details = {
        "name": token_name,
        "symbol": token_symbol,
        "decimal": token_decimals,
        "balance": user_balance
    }

    return token_details

def transfer_token(client: Tron, account: dict, token_id: int, to_address: str, amount: int) -> str:
    """
    Transfer TRC-20 tokens from one account to another.

    Args:
        client (Tron): Tronpy client instance.
        account (dict): Account dictionary with 'address' and 'key'.
        token_id (int): Token ID of the TRC-20 token.
        to_address (str): Address to send tokens to.
        amount (int): Amount of tokens to send.

    Returns:
        str: Transaction ID.
    """
    sender = PrivateKey(bytes.fromhex(account["key"]))
    contract = client.get_contract(token_id)
    txn = (
        contract.functions.transfer(to_address, amount)
        .with_owner(sender.address)
        .fee_limit(1_000_000)
        .build()
        .sign(sender)
    )
    tx_id = txn.broadcast().wait().txid
    return tx_id

def sign_message(account: dict, message: str) -> bytes:
    """
    Sign a message with the account's private key.

    Args:
        account (dict): Account dictionary with 'address' and 'key'.
        message (str): Message to sign.

    Returns:
        bytes: Signed message.
    """
    private_key = PrivateKey(bytes.fromhex(account['key']))
    return private_key.sign_msg(message.encode())