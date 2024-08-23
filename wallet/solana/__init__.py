from solana.rpc.api import Client
from solders.keypair import Keypair
from solana.transaction import Transaction
from solders.system_program import TransferParams, transfer
from solana.rpc.commitment import Confirmed
from solders.pubkey import Pubkey
from decimal import Decimal
from solana.rpc.async_api import AsyncClient
from spl.token.constants import TOKEN_PROGRAM_ID
from spl.token.client import Token
from spl.token.instructions import transfer_checked, get_associated_token_address, create_associated_token_account
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
    client.send_transaction(service_fee_txn, sender)

    return main_txn_signature["result"]


async def import_solana_token(chain_provider, token_address, owner_address):
    """
    Function to retrieve details of an SPL token (Solana)
    Args:
        chain_provider [str]: RPC URL of the Solana cluster
        token_address [str]: Address of the SPL token
        owner_address [str]: Address of the token owner
    Returns:
        dict: details of token
    """
    async with AsyncClient(chain_provider) as client:
        token_pubkey = Pubkey(token_address)
        owner_pubkey = Pubkey(owner_address)

        token = Token(client, token_pubkey, TOKEN_PROGRAM_ID, owner_pubkey)
        token_info = await client.get_token_accounts_by_owner(owner_pubkey, token_pubkey)
        
        token_name = "N/A"  # Solana tokens don't have a standard name field
        token_symbol = "N/A"  # Solana tokens don't have a standard symbol field
        token_decimals = await token.get_decimals()
        user_balance = await token.get_balance(owner_pubkey)

        token_details = {
            "name": token_name,
            "symbol": token_symbol,
            "decimal": token_decimals,
            "balance": user_balance['result']['value']['amount']
        }

    return token_details

async def transfer_solana_token(chain_provider, sender_private_key, token_address, recipient_address, amount, sender_token_account=None):
    """
    Function to transfer SPL tokens on Solana.
    Args:
        chain_provider [str]: RPC URL of the Solana cluster
        sender_private_key [str]: Base58 encoded private key of the sender
        token_address [str]: Address of the SPL token
        recipient_address [str]: Address of the recipient
        amount [int]: Amount of tokens to transfer (in smallest units, not decimals)
        sender_token_account [str]: Optional. The sender's token account address. If not provided, it will be derived.
    Returns:
        str: Transaction signature of the transfer
    """
    # Connect to Solana RPC
    async with AsyncClient(chain_provider) as client:
        sender_keypair = Keypair.from_secret_key(bytes(sender_private_key))
        sender_pubkey = sender_keypair.public_key

        token_pubkey = Pubkey(token_address)
        recipient_pubkey = Pubkey(recipient_address)

        # Derive sender token account if not provided
        if sender_token_account is None:
            sender_token_account = get_associated_token_address(sender_pubkey, token_pubkey)

        # Derive recipient token account
        recipient_token_account = get_associated_token_address(recipient_pubkey, token_pubkey)

        # Ensure the recipient token account exists
        account_info = await client.get_account_info(recipient_token_account)
        if account_info['result']['value'] is None:
            # Create associated token account if it does not exist
            transaction = Transaction()
            transaction.add(
                create_associated_token_account(sender_pubkey, recipient_pubkey, token_pubkey)
            )
            await client.send_transaction(transaction, sender_keypair)

        # Create the transfer transaction
        transaction = Transaction()
        transaction.add(
            transfer_checked(
                source=sender_token_account,
                destination=recipient_token_account,
                owner=sender_pubkey,
                amount=amount,
                decimals=await client.get_token_decimals(token_pubkey),
                program_id=TOKEN_PROGRAM_ID
            )
        )

        # Send the transaction
        response = await client.send_transaction(transaction, sender_keypair)

    return response['result']


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
