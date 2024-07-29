from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes
from solders.keypair import Keypair
from tronpy import Tron
from tronpy.keys import PrivateKey, PublicKey
from eth_account import Account

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
        return {"address": public_key, "private_key": private_key}


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
        private_key = account.PrivateKey().Raw().ToHex()
        full_key = Account.from_key(private_key)  # Bitcoin address
        return {"address": full_key.address, "private_key": full_key.key}
    

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
        return {"address": public_key, "private_key": private_key}

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
        return {"address": keypair_total.pubkey(), "private_key": keypair_total.secret()}

    def get_altcoin_account(self, coin: Bip44Coins, account_index: int = 0) -> dict:
        """
        Get altcoin account details.

        Args:
            coin (Bip44Coins): Coin type for the altcoin.
            account_index (int): Account index for derivation.

        Returns:
            dict: Altcoin account with address and private key.
        """
        bip44_wallet = Bip44.FromSeed(self.seed, coin)
        account = bip44_wallet.Purpose().Coin().Account(account_index).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
        private_key = account.PrivateKey().Raw().ToHex()
        address = account.PublicKey().ToAddress()
        return {"address": address, "private_key": private_key}
