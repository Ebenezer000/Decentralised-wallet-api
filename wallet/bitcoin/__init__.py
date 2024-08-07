from bit import Key, PrivateKeyTestnet
from blockcypher import simple_spend
from wallet.multichain_wallet.helpers.chain_paths import SERVICE_FEE_ADDRESS
from decimal import Decimal

def transfer_altcoin(private_key: str, recipient_address: str, amount: float, coin: str) -> dict:
    """
    Transfer ALTCOINS (LTC, DOGE, DASH ) from one account to another with a service fee.

    Args:
        private_key (str): Private key of the sender.
        recipient_address (str): Recipient's public address.
        amount (float): Amount of currency to send.
        coin (str): Symbol of the altcoin ('ltc', 'doge', 'dash').

    Returns:
        dict: Transaction hashes for the main transfer and the service fee.
    """
    # Calculate service fee
    SERVICE_FEE_PERCENT = Decimal('0.001')
    service_fee = amount * SERVICE_FEE_PERCENT
    adjusted_amount = amount - service_fee

    # Convert amounts to satoshis
    adjusted_amount_satoshis = int(adjusted_amount * 1e8)
    service_fee_satoshis = int(service_fee * 1e8)

    # Create transactions
    tx_hash_recipient = simple_spend(from_privkey=private_key, to_address=recipient_address, to_satoshis=adjusted_amount_satoshis, coin_symbol=coin)
    simple_spend(from_privkey=private_key, to_address=SERVICE_FEE_ADDRESS, to_satoshis=service_fee_satoshis, coin_symbol=coin)

    return tx_hash_recipient

def transfer_btc(private_key: str, recipient_address: str, amount_btc: float, testnet: bool = False) -> str:
    """
    Transfer BTC from one account to another with a service fee.

    Args:
        private_key (str): Private key of the sender.
        recipient_address (str): Recipient's public address.
        amount_btc (float): Amount of BTC to send.
        testnet (bool): If True, use Bitcoin testnet.

    Returns:
        str: Transaction ID.
    """
    # Choose Key class based on mainnet or testnet
    SERVICE_FEE_PERCENT = Decimal('0.001')
    key_class = PrivateKeyTestnet if testnet else Key
    sender = key_class(private_key)
    
    # Calculate service fee
    service_fee_btc = amount_btc * SERVICE_FEE_PERCENT
    adjusted_amount_btc = amount_btc - service_fee_btc
    
    # Create transactions
    tx_hash_recipient = sender.send([(recipient_address, adjusted_amount_btc, 'btc')])
    sender.send([(SERVICE_FEE_ADDRESS['bitcoin'], service_fee_btc, 'btc')])
    
    return tx_hash_recipient
