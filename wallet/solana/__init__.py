from solana.rpc.api import Client
from solders.keypair import Keypair
from solana.transaction import Transaction
from solders.system_program import TransferParams, transfer
from solana.rpc.commitment import Confirmed
from solders.pubkey import Pubkey

def transfer_sol(seed: str, recipient_address: str, amount_sol: float) -> str:
    """
    Transfer SOL from one account to another.

    Args:
        client (Client): Solana RPC client.
        sender (Keypair): Sender's Keypair.
        recipient_address (str): Recipient's public key as a string.
        amount_sol (float): Amount of SOL to send.

    Returns:
        str: Transaction signature.
    """
    client = Client("https://api.mainnet-beta.solana.com")
    sender = Keypair.from_seed(seed)
    recipient_pubkey = Pubkey(recipient_address)
    amount_lamports = int(amount_sol * 1_000_000_000)  # 1 SOL = 1 billion lamports
    txn = Transaction().add(transfer(TransferParams(from_pubkey=sender.pubkey, to_pubkey=recipient_pubkey, lamports=amount_lamports)))
    txn_signature = client.send_transaction(txn, sender, opts=Confirmed)
    return txn_signature["result"]

# def relay_solana_transaction():
#     data = request.json
#     tx_data = data.get('tx_data')
#     private_key = data.get('private_key')
#     recipient = data.get('recipient')
#     amount = Decimal(data.get('amount'))

#     client = SolanaClient("https://api.mainnet-beta.solana.com")
    
#     # Calculate service fee
#     service_fee = amount * SERVICE_FEE_PERCENT
#     adjusted_amount = amount - service_fee

#     # Create and send transaction
#     # Note: A full implementation would need to handle message creation, signing, etc.
#     # Here, we assume a function `create_signed_transaction` exists
#     tx_hash = create_signed_transaction(private_key, recipient, adjusted_amount)
    
#     # Send service fee transaction
#     service_fee_tx_hash = create_signed_transaction(private_key, SERVICE_FEE_ADDRESS['solana'], service_fee)

#     return tx_hash

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
