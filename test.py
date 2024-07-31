import json
from zpywallet import wallet
from wallet.multichain_wallet import MultiChainWallet
from wallet.multichain_wallet.chain import chains


if __name__ == '__main__':

    seed: str = "million crush leave asthma slush margin okay tornado spawn intact ranch often"
    chain: str = "LITECOIN"
    # "mnemonic": "million crush leave asthma slush margin okay tornado spawn intact ranch often",
    # "chain": "LITECOIN"
    multi_wallet = MultiChainWallet(seed)
    coin_type = chains[chain]['coin']
    wallet = multi_wallet.get_altcoin_account(coin_type)
    
    wallet = {
        'seed': seed,
        'wallet': wallet
    }

    wallet_json = json.dumps(wallet, indent=4)
    print(wallet_json)