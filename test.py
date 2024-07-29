from zpywallet import wallet
from wallet.multichain_wallet import MultiChainWallet

if __name__ == '__main__':
    # body: tuple = request.json
    # seed: str = body["mnemonic"]
    seed = wallet.generate_mnemonic()
    multi_wallet = MultiChainWallet(seed)

    bitcoin = multi_wallet.get_bitcoin_account()
    eth = multi_wallet.get_eth_account()
    tron = multi_wallet.get_tron_account()
    solana = multi_wallet.get_solana_account()
    
    wallet_json = {
        'seed': seed,
        'bitcoin account': bitcoin,
        'eth account': eth,
        'tron account': tron,
        'solana account': solana
    }

    print(wallet_json)