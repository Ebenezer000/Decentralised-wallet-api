from solders.pubkey import Pubkey
from solana.rpc.api import Client

def get_solana_balance(address):
    rpc_url = "https://api.mainnet-beta.solana.com"
    client = Client(rpc_url)

    try:
        response = client.get_balance(address)
        lamports = response.value
        sol = lamports / 1e9  # Convert lamports to SOL
        print(sol)
        return sol
    except Exception as e:
        print(f"Error fetching balance: {e}")
        return 0

if __name__ == "__main__":
    address_str = "DJPzoxSqMqU5euccLSthowpt83KwjPeoMifX86UNaVje"
    address = Pubkey.from_string(address_str)
    balance = get_solana_balance(address)
    print(f"SOL Balance: {balance}")
