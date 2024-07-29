from tronpy import Tron
from tronpy.keys import PrivateKey
from tronpy.providers import HTTPProvider

def phrase_to_account(phrase: str) -> dict:
    """
    Function to turn seed phrase into account dictionary.

    Args:
        phrase[str]: Seed phrase of account

    Returns:
        dict: Account attached to seed phrase      
    """
    # Assuming seed phrase to private key conversion logic
    private_key_hex = mnemonic_to_private_key(phrase)  # Replace with actual function
    private_key = PrivateKey(bytes.fromhex(private_key_hex))
    account = {
        "address": private_key.address,
        "key": private_key_hex,
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
    tx_id = txn.broadcast().wait().txid
    return tx_id

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

# Example usage
client = Tron(HTTPProvider("https://api.trongrid.io"))
phrase = "your seed phrase here"
account = phrase_to_account(phrase)

# Transfer TRX
to_address = "recipient_address"
trx_amount = 10
tx_id = transfer_trx(client, account, to_address, trx_amount)
print(f"TRX Transfer TxID: {tx_id}")

# Transfer Token
token_id = 1002000  # Example token ID
token_amount = 1000
tx_id = transfer_token(client, account, token_id, to_address, token_amount)
print(f"Token Transfer TxID: {tx_id}")

# Sign a message
message = "Hello, Tron!"
signed_message = sign_message(account, message)
print(f"Signed Message: {signed_message.hex()}")
