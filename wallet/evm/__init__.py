from web3 import Web3
from hexbytes import HexBytes
from web3.middleware import construct_sign_and_send_raw_middleware


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

