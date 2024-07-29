from tronpy import Tron
from tronpy.keys import PrivateKey
from tronpy.providers import HTTPProvider


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