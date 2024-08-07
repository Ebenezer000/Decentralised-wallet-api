from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes
from solders.keypair import Keypair
from tronpy.keys import PrivateKey, PublicKey
from eth_account import Account
from wallet.multichain_wallet.chain import chains
from wallet.multichain_wallet.helpers import get_crypto_balance, get_alt_crypto_balance

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
        balance = get_crypto_balance(address = str(public_key), coin_symbol =  "btc")
        return {"address": public_key, "private_key": private_key, "balance": balance}

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

        balance = get_alt_crypto_balance("ETHEREUM", full_key.address)
            
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
        balance = get_alt_crypto_balance("TRON", public_key)
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

        balance = get_alt_crypto_balance("SOLANA", str(keypair_total.pubkey()))
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
            balance = get_crypto_balance(address = address, coin_symbol = coin_symbols[coin])
            
            return {"address": address, "private_key": private_key, "balance": balance}
        
        elif coin in ["ETHEREUM", "TRON", "SOLANA"]:

            balance = get_alt_crypto_balance(address, coin)
            
            return {"address": address, "private_key": private_key, "balance": balance }
        
        else:
            return {"address": address, "private_key": private_key}
        