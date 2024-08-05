
from wallet.multichain_wallet import MultiChainWallet

if __name__ == "__main__":
    seed = "million crush leave asthma slush margin okay tornado spawn intact ranch often"

    wallet = MultiChainWallet(seed)
    wallet.get_bitcoin_account()

