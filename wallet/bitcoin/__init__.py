from bit import Key, PrivateKeyTestnet
# from bit.network import NetworkAPI
from blockcypher import simple_spend

def transfer_btc(private_key: str, recipient_address: str, amount_btc: float, testnet: bool = False) -> str:
    """
    Transfer BTC from one account to another.

    Args:
        private_key (str): Private key of the sender.
        recipient_address (str): Recipient's public address.
        amount_btc (float): Amount of BTC to send.
        testnet (bool): If True, use Bitcoin testnet.

    Returns:
        str: Transaction ID.
    """
    # Choose Key class based on mainnet or testnet
    key_class = PrivateKeyTestnet if testnet else Key
    sender = key_class(private_key)
    tx_hash = sender.send([(recipient_address, amount_btc, 'btc')])
    return tx_hash


def transfer_altcoin(private_key: str, recipient_address: str, amount: float, coin: str) -> str:
    """
    Transfer ALTCOINS (LTC, DOGE, DASH ) from one account to another.

    Args:
        private_key (str): Private key of the sender.
        recipient_address (str): Recipient's public address.
        amount (float): Amount of currency to send.

    Returns:
        str: Transaction hash.
    """
    # Convert amount from LTC to satoshis
    amount_satoshis = int(amount * 1e8)
    # sender_address = get_address_details(private_key, coin_symbol='ltc')['address']

    # Create transaction and broadcast it
    tx_hash = simple_spend(from_privkey=private_key, to_address=recipient_address, to_satoshis=amount_satoshis, coin_symbol=coin)
    return tx_hash