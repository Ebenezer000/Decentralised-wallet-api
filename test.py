import requests
from wallet.multichain_wallet.helpers import extract_wallets_and_values
from wallet.multichain_wallet.helpers.chain_paths import headers, chain_paths

if __name__ == "__main__":
    explorer_url = "https://etherscan.io"
    address = "0xa434e3c499288391104b39a3660f3ef7eec81984"
    url = f"{explorer_url}/txs?a={address}&ps=25"

    response = requests.post(url, headers=headers)
    responseHTML = response.text

    transaction_history = extract_wallets_and_values(responseHTML, explorer_url)
    print(transaction_history)
