import requests

def get_crypto_prices():
    # Define the cryptocurrencies and their CoinGecko IDs
    cryptos = {
        'bitcoin': 'bitcoin',
        'eth': 'ethereum',
        'tron': 'tron',
        'solana': 'solana'
    }

    # Base URL for CoinGecko API
    base_url = "https://api.coingecko.com/api/v3/simple/price"

    # Prepare the query parameters
    ids = ",".join(cryptos.values())
    params = {
        'ids': ids,
        'vs_currencies': 'usd'
    }

    try:
        # Send a GET request to the API
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an error if the request failed
        data = response.json()

        # Extract prices and store in the prices dictionary with the desired format
        prices = {
            'Bitcoin': f"$ {data['bitcoin']['usd']}",
            'Eth': f"$ {data['ethereum']['usd']}",
            'Tron': f"$ {data['tron']['usd']}",
            'Solana': f"$ {data['solana']['usd']}"
        }
        return prices

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

    return None

# Example usage
if __name__ == "__main__":
    prices = get_crypto_prices()
    if prices:
        print("Current cryptocurrency prices (in USD):")
        print(prices)
        print("GOT THIS FROM THE RIGHT FOLDER")
    else:
        print("Failed to retrieve prices.")
