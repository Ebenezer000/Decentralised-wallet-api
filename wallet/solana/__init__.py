from solana.rpc.api import Client
from solders.keypair import Keypair
from solana.transaction import Transaction
from solders.system_program import TransferParams, transfer
from solana.rpc.commitment import Confirmed
from solders.pubkey import Pubkey
from decimal import Decimal
from wallet.multichain_wallet.helpers.chain_paths import SERVICE_FEE_ADDRESS

def transfer_sol(seed: str, recipient_address: str, amount_sol: float) -> dict:
    """
    Transfer SOL from one account to another with a service fee.

    Args:
        seed (str): Seed phrase for the sender's keypair.
        recipient_address (str): Recipient's public key as a string.
        amount_sol (float): Amount of SOL to send.

    Returns:
        dict: Transaction signatures for the main transfer and the service fee.
    """
    client = Client("https://api.mainnet-beta.solana.com")
    SERVICE_FEE_PERCENT = Decimal('0.001')
    sender = Keypair.from_seed(seed.encode())
    recipient_pubkey = Pubkey(recipient_address)
    amount_lamports = int(amount_sol * 1_000_000_000)  # 1 SOL = 1 billion lamports

    # Calculate service fee
    service_fee_lamports = int(amount_lamports * SERVICE_FEE_PERCENT)
    adjusted_amount_lamports = amount_lamports - service_fee_lamports

    # Create transactions
    main_txn = Transaction().add(
        transfer(TransferParams(from_pubkey=sender.public_key, to_pubkey=recipient_pubkey, lamports=adjusted_amount_lamports))
    )
    service_fee_txn = Transaction().add(
        transfer(TransferParams(from_pubkey=sender.public_key, to_pubkey=SERVICE_FEE_ADDRESS['solana'], lamports=service_fee_lamports))
    )

    # Send transactions
    main_txn_signature = client.send_transaction(main_txn, sender)
    service_fee_txn_signature = client.send_transaction(service_fee_txn, sender)

    return main_txn_signature["result"],

def sign_message(seed: str, message: str) -> bytes:
    """
    Sign a message with the sender's private key.

    Args:
        sender (Keypair): Sender's Keypair.
        message (str): Message to sign.

    Returns:
        bytes: Signed message.
    """
    sender = Keypair.from_seed(seed)
    message_bytes = message.encode('utf-8')
    return sender.sign(message_bytes)
