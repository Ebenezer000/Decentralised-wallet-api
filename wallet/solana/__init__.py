from solana.rpc.api import Client
from solana.keypair import Keypair
from solana.transaction import Transaction
from solana.system_program import TransferParams, transfer
from solana.rpc.commitment import Confirmed
from solana.message import Message
from solana.publickey import PublicKey

def phrase_to_account(phrase: str) -> Keypair:
    """
    Function to turn seed phrase into a Keypair object.
    Args:
        phrase[str]: Seed phrase of account
    Returns:
        Keypair: Keypair object attached to seed phrase      
    """
    # Assuming seed phrase to secret key conversion logic
    # secret_key = mnemonic_to_secret_key(phrase)  # Replace with actual function
    # return Keypair.from_secret_key(secret_key)


def transfer_sol(client: Client, sender: Keypair, recipient_address: str, amount_sol: float) -> str:
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
    recipient_pubkey = PublicKey(recipient_address)
    amount_lamports = int(amount_sol * 1_000_000_000)  # 1 SOL = 1 billion lamports
    txn = Transaction().add(transfer(TransferParams(from_pubkey=sender.public_key, to_pubkey=recipient_pubkey, lamports=amount_lamports)))
    txn_signature = client.send_transaction(txn, sender, opts=Confirmed)
    return txn_signature["result"]


def sign_message(sender: Keypair, message: str) -> bytes:
    """
    Sign a message with the sender's private key.

    Args:
        sender (Keypair): Sender's Keypair.
        message (str): Message to sign.

    Returns:
        bytes: Signed message.
    """
    message_bytes = message.encode('utf-8')
    return sender.sign(message_bytes)

# Example usage
client = Client("https://api.mainnet-beta.solana.com")
phrase = "your seed phrase here"
sender_account = phrase_to_account(phrase)
recipient_address = "recipient_public_key"

# Transfer SOL
signature = transfer_sol(client, sender_account, recipient_address, 0.1)
print(f"SOL Transfer Signature: {signature}")

# Sign a message
message = "Hello, Solana!"
signed_message = sign_message(sender_account, message)
print(f"Signed Message: {signed_message.hex()}")
