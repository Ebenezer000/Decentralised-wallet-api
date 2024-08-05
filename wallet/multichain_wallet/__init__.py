from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes
from solders.keypair import Keypair
from solana.rpc.api import Client
from tronpy import Tron
from tronpy.keys import PrivateKey, PublicKey
from tronpy.providers import HTTPProvider
from eth_account import Account
import blockcypher
from web3 import Web3
from wallet.multichain_wallet.chain import chains

class MultiChainWallet:
    def __init__(self, mnemonic: str, passphrase: str = ""):
        self.mnemonic = mnemonic
        self.passphrase = passphrase
        self.seed = Bip39SeedGenerator(mnemonic).Generate(passphrase)

    def get_bitcoin_account(self, account_index: int = 0) -> dict:
        """
        Get Bitcoin account details.

        Args:
            account_index (int): Account index for derivation.

        Returns:
            dict: Bitcoin account with address and private key.
        """
        bip44_wallet = Bip44.FromSeed(self.seed, Bip44Coins.BITCOIN)
        account = bip44_wallet.Purpose().Coin().Account(account_index).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
        private_key = account.PrivateKey().Raw().ToHex()
        public_key = account.PublicKey().ToAddress()  # Bitcoin address
        
        # Fetch the balance using blockcypher
        balance = self.get_crypto_balance(address = public_key, coin_symbol =  "btc")
        return {"address": public_key, "private_key": private_key, "balance": balance}

    def get_crypto_balance(address: str, coin_symbol: str = "btc") -> float:
        """
        Fetch the balance of a cryptocurrency address.

        Args:
            address (str): The cryptocurrency address to check.
            coin_symbol (str): The symbol of the cryptocurrency (e.g., "btc", "ltc", "dash", "doge").

        Returns:
            float: The balance in the corresponding cryptocurrency units.
        """
        try:
            # Define BlockCypher coin symbols
            coin_symbols = {
                "btc": "btc",    # Bitcoin
                "ltc": "ltc",    # Litecoin
                "dash": "dash",  # Dash
                "doge": "doge"   # Dogecoin
            }

            # Fetch the address details from BlockCypher for the specified coin
            if coin_symbol in coin_symbols:
                address_details = blockcypher.get_address_details(
                    address, coin_symbol=coin_symbols[coin_symbol], api_key="15bd83fc27cf437db9fcb8c1358f8cfe"
                )
                balance_satoshis = address_details.get('balance', 0)
                balance = balance_satoshis / 1e8  # Convert satoshis to the main unit
                return balance
            else:
                print(f"Unsupported coin symbol: {coin_symbol}")
                return 0.0
        except Exception as e:
            print(f"Error fetching balance: {e}")
            return 0.0
        
    def get_alt_crypto_balance(self, chain, address):
        """
        Function to retieve base balance of address
        Args:
            chain[str]: Name of current chain
            address[str]: Address of user
        Returns:
            str: balance of user     
        """
        balance = ""
        if chain == "ETHEREUM":
            w3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/073d45dbb7714609b5980055d74875dd"))
            balance = w3.eth.get_balance(address)
        
        elif chain == "TRON":
            w3 = Tron(HTTPProvider('https://api.trongrid.io'))
            balance = w3.get_account_balance(address)

        elif chain == "SOLANA":
            rpc_url: str = "https://api.mainnet-beta.solana.com"
            client = Client(rpc_url)
            response = client.get_balance(address)

            if response.get("result"):
                lamports = response["result"]["value"]
                sol = lamports / 1e9  # Convert lamports to SOL
                return sol
            else:
                print(f"Error fetching balance: {response.get('error')}")
                balance = "0"

        return balance 

    def get_eth_account(self, account_index: int = 0) -> dict:
        """
        Get Ethereum account details.

        Args:
            account_index (int): Account index for derivation.

        Returns:
            dict: Ethereum account with address and private key.
        """
        bip44_wallet = Bip44.FromSeed(self.seed, Bip44Coins.ETHEREUM)
        account = bip44_wallet.Purpose().Coin().Account(account_index).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
        private_key = account.PrivateKey().Raw().ToBytes()
        full_key = Account.from_key(private_key)  # Bitcoin address

        balance = self.get_alt_crypto_balance(full_key.address, "ETHEREUM")
            
        return {"address": full_key.address, "private_key": full_key.key.hex(), "balance": balance}
    

    def get_tron_account(self, account_index: int = 0) -> dict:
        """
        Get Tron account details.

        Args:
            account_index (int): Account index for derivation.

        Returns:
            dict: Tron account with address and private key.
        """
        bip44_wallet = Bip44.FromSeed(self.seed, Bip44Coins.TRON)
        account = bip44_wallet.Purpose().Coin().Account(account_index).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
        private_key = account.PrivateKey().Raw().ToHex()
        tron_account = PrivateKey(bytes.fromhex(private_key))
        public_key = PublicKey.to_base58check_address(tron_account.public_key)
        balance = self.get_alt_crypto_balance(public_key, "TRON")
        return {"address": public_key, "private_key": private_key, "balance": balance}

    def get_solana_account(self, account_index: int = 0) -> Keypair:
        """
        Get Solana account details.

        Args:
            account_index (int): Account index for derivation.

        Returns:
            Keypair: Solana Keypair object.
        """
        bip44_wallet = Bip44.FromSeed(self.seed, Bip44Coins.SOLANA)
        account = bip44_wallet.Purpose().Coin().Account(account_index).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
        total_key = account.PrivateKey().Raw().ToBytes()
        keypair_total = Keypair.from_seed(total_key)

        balance = self.get_alt_crypto_balance(str(keypair_total.pubkey()), "SOLANA")
        return {"address": str(keypair_total.pubkey()), "private_key": keypair_total.secret().hex(), "balance": balance}

    def get_altcoin_account(self, coin: str, account_index: int = 0) -> dict:
        """
        Get altcoin account details.

        Args:
            coin (Bip44Coins): Coin type for the altcoin.
            account_index (int): Account index for derivation.

        Returns:
            dict: Altcoin account with address and private key.
        """
        coin_type = chains[coin]['coin']
        bip44_wallet = Bip44.FromSeed(self.seed, coin_type)
        account = bip44_wallet.Purpose().Coin().Account(account_index).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
        private_key = account.PrivateKey().Raw().ToHex()
        address = account.PublicKey().ToAddress()

        if coin in ["LITECOIN", "BITCOIN", "DASH", "DOGE"]:
            coin_symbols = {
                "BITCOIN": "btc",    # Bitcoin
                "LITECOIN": "ltc",    # Litecoin
                "DASH": "dash",  # Dash
                "DOGE": "doge"   # Dogecoin
            }
            balance = self.get_crypto_balance(address = address, coin_symbol = coin_symbols[coin])
            
            return {"address": address, "private_key": private_key, "balance": balance}
        
        elif coin in ["ETHEREUM", "TRON", "SOLANA"]:

            balance = self.get_alt_crypto_balance(address, coin)
            
            return {"address": address, "private_key": private_key, "balance": balance }
        
        else:
            return {"address": address, "private_key": private_key}
        