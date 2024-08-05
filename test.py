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

if __name__ == "__main__":
    seed = "million crush leave asthma slush margin okay tornado spawn intact ranch often"

    bip44_wallet = Bip44.FromSeed(seed, Bip44Coins.BITCOIN)
    account = bip44_wallet.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
    private_key = account.PrivateKey().Raw().ToHex()
    public_key = account.PublicKey().ToAddress()  # Bitcoin address

    print(public_key)

