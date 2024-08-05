## Postman Documentation for Leeway Wallet API
# Base URL
    ```
    https://leeway-wallet-api.onrender.com/

    ```
## URLs

1. GET /
    Description: Welcome message.

    Request:

    Method: GET 
    URL: /
    Response:

    ```
    Body: "Hello Welcome to Leeway Wallet"
    ```

2. POST /create_mnemonic
    Description: Generate a new mnemonic seed phrase.

    Request:

    Method: POST
    URL: /create_mnemonic
    Response:

    Body:
    ```json
        {
        "mnemonic": "seed phrase"
        }
    ```

3. POST /create_wallet
    Description: Create wallets for Bitcoin, Ethereum, Tron, and Solana using a mnemonic seed phrase.

    Request:

    Method: POST
    URL: /create_wallet
    Body:
    ```json
        {
        "mnemonic": "your mnemonic phrase here"
        }
    ```
    Response:
    Body:
    ```json
    {
        "seed": "your mnemonic phrase",
        "bitcoin account": {
            "address": "bitcoin address",
            "private_key": "bitcoin private key"
        },
        "eth account": {
            "address": "ethereum address",
            "private_key": "ethereum private key"
        },
        "tron account": {
            "address": "tron address",
            "private_key": "tron private key"
        },
        "solana account": {
            "address": "solana address",
            "public_key": "solana public key",
            "private_key": "solana private key"
        }
    }
    ```

4. POST /fetch_wallet
    Description: Fetch a wallet for a specific chain using the mnemonic seed phrase.

    Request:

    Method: POST
    URL: /fetch_wallet
    Body:
    ```json
        {
        "mnemonic": "your mnemonic phrase here",
        "chain": "chain name (e.g., BITCOIN, ETHEREUM, etc.)"
        }
    ```

    Response:
    Body:
    ```json
    
    {
        "seed": "your mnemonic phrase",
        "wallet": {
            "address": "wallet address",
            "private_key": "wallet private key"
        }
    }
    ```

5. POST /fetch_price
    Description: Fetch current prices of supported cryptocurrencies.

    Request:
    Method: POST
    URL: /fetch_price
    Response:

    Body:
    ```json
    {
        "bitcoin": "current price in USD",
        "eth": "current price in USD",
        "tron": "current price in USD",
        "solana": "current price in USD"
    }
    ```
6. Transfer EVM
    Description: Transfer EVM Coins.

    URL: /transfer_evm
    Method: POST

    Request Body:

    ```json
    
    {
        "seed": "string",              // The seed phrase to derive the account.
        "recipient": "string",         // The recipient's address.
        "amount": "string",            // The amount to transfer.
        "rpc_provider": "string",      // The RPC provider URL.
        "explorer_url": "string"       // The blockchain explorer URL.
    }
    ```

    Response:

    ```json
    
    {
        "transaction_state": "string", // Transaction state (e.g., "COMPLETED").
        "transaction_hash": "string",  // Transaction hash.
        "transaction_link": "string"   // Link to the transaction on the explorer.
    }

    ```

7. Transfer Token EVM

    Description: Transfer EVM Tokens.
    URL: /transfer_token_evm
    Method: POST

    Request Body:

    ```json
    
    {
        "seed": "string",              // The seed phrase to derive the account.
        "recipient": "string",         // The recipient's address.
        "amount": "string",            // The amount of tokens to transfer.
        "token_address": "string",     // The address of the token contract.
        "rpc_provider": "string",      // The RPC provider URL.
        "explorer_url": "string"       // The blockchain explorer URL.
    }
    ```

    Response:

    ```json
    
    {
        "transaction_state": "string", // Transaction state (e.g., "COMPLETED").
        "transaction_hash": "string",  // Transaction hash.
        "transaction_link": "string"   // Link to the transaction on the explorer.
    }
    ```

8. Import Token EVM
    Description: Import and get EVM token details.
    URL: /import_token_evm
    Method: POST

    Request Body:

    ```json

    {
        "rpc_provider": "string",      // The RPC provider URL.
        "user_address": "string",      // The user's address.
        "token_address": "string"      // The address of the token contract.
    }
    ```
    
    Response:

    ```json

    {
        "name": "string",              // Token name.
        "symbol": "string",            // Token symbol.
        "decimals": "integer",         // Token decimals.
        "balance": "string"            // Total Token Balance of User
    }
    ```

9. Transfer BTC Altcoins

    Description: Transfer coins on BTC and adjacent chains
    URL: /transfer_btc_alts
    Method: POST

    Request Body:

    ```json

    {
        "seed": "string",              // The seed phrase to derive the account.
        "chain": "string",             // The blockchain name (e.g., "BITCOIN", "LITECOIN").
        "recipient": "string",         // The recipient's address.
        "amount": "string"             // The amount to transfer.
    }
    ```

    Response:
    ```json

    {
        "transaction_state": "string", // Transaction state (e.g., "COMPLETED").
        "transaction_hash": "string"   // Transaction hash.
    }
    ```

10. Transfer Solana

    Description: Transfer Solana SOL
    URL: /transfer_solana
    Method: POST

    Request Body:

    ```json

    {
        "seed": "string",              // The seed phrase to derive the account.
        "recipient": "string",         // The recipient's address.
        "amount": "string"             // The amount of SOL to transfer.
    }
    ```

    Response:

    ```json

    {
        "transaction_state": "string", // Transaction state (e.g., "COMPLETED").
        "transaction_hash": "string",  // Transaction hash.
        "transaction_link": "string"   // Link to the transaction on the explorer.
    }

11. Transfer TRON

    Description: Transfer TRON TRX
    URL: /transfer_tron
    Method: POST

    Request Body:

    ```json

    {
    "seed": "string",              // The seed phrase to derive the account.
    "recipient": "string",         // The recipient's address.
    "amount": "string"             // The amount of TRX to transfer.
    }
    ```

    Response:

    ```json
    {
    "transaction_state": "string", // Transaction state (e.g., "COMPLETED").
    "transaction_hash": "string",  // Transaction hash.
    "transaction_link": "string"   // Link to the transaction on the explorer.
    }
    ```

    ## Supported Chains

The library supports the following blockchains:

- ALGORAND (Bip44Coins.ALGORAND)
- AVALANCHE_C_CHAIN (Bip44Coins.AVALANCHE_C_CHAIN)
- AVALANCHE_X_CHAIN (Bip44Coins.AVALANCHE_X_CHAIN)
- BINANCE_CHAIN (Bip44Coins.BINANCE_CHAIN)
- BITCOIN (Bip44Coins.BITCOIN)
- BITCOIN_CASH (Bip44Coins.BITCOIN_CASH)
- BITCOIN_SV (Bip44Coins.BITCOIN_SV)
- BITCOIN_TESTNET (Bip44Coins.BITCOIN_TESTNET)
- CARDANO_ICARUS (Bip44Coins.CARDANO_ICARUS)
- CARDANO_LEDGER (Bip44Coins.CARDANO_LEDGER)
- CHAINLINK (Bip44Coins.CHAINLINK)
- COSMOS (Bip44Coins.COSMOS)
- DASH (Bip44Coins.DASH)
- DOGECOIN (Bip44Coins.DOGECOIN)
- ELROND (Bip44Coins.ELROND)
- ETHEREUM (Bip44Coins.ETHEREUM)
- ETHEREUM_CLASSIC (Bip44Coins.ETHEREUM_CLASSIC)
- ETHEREUM_TESTNET (Bip44Coins.ETHEREUM_TESTNET)
    - Ethereum (ETH)
    - Binance Smart Chain (BSC)
    - Avalanche C-Chain
    - Polygon (Matic)
    - Fantom (FTM)
    - Arbitrum
    - Optimism
    - Moonbeam (on Polkadot)
    - Cronos (Crypto.com Chain)
    - Kovan Testnet
    - Ropsten Testnet
    - Rinkeby Testnet
    - Goerli Testnet
    - Celo
    - Harmony One
    - xDAI (Gnosis Chain)
    - Huobi ECO Chain (HECO)
    - OKExChain
    - Klaytn
    - TomoChain
    - Velas
    - IoTeX
    - Aurora (on NEAR)
    - Milkomeda (on Cardano)

- FILECOIN (Bip44Coins.FILECOIN)
- HARMONY_ONE (Bip44Coins.HARMONY_ONE)
- HORIZEN (Bip44Coins.HORIZEN)
- KUSAMA (Bip44Coins.KUSAMA)
- LITECOIN (Bip44Coins.LITECOIN)
- MONERO (Bip44Coins.MONERO)
- NANO (Bip44Coins.NANO)
- NEO (Bip44Coins.NEO)
- NEO3 (Bip44Coins.NEO3)
- NULS (Bip44Coins.NULS)
- NULS2 (Bip44Coins.NULS2)
- POLKADOT (Bip44Coins.POLKADOT)
- RIPPLE (Bip44Coins.RIPPLE)
- SOLANA (Bip44Coins.SOLANA)
- STELLAR (Bip44Coins.STELLAR)
- TERRA (Bip44Coins.TERRA)
- TERRA_CLASSIC (Bip44Coins.TERRA_CLASSIC)
- TEZOS (Bip44Coins.TEZOS)
- THETA (Bip44Coins.THETA)
- TRON (Bip44Coins.TRON)
- VECHAIN (Bip44Coins.VECHAIN)
- ZCASH (Bip44Coins.ZCASH)
- ZILLIQA (Bip44Coins.ZILLIQA)

Security

- Private Key Management: Keep your private keys secure and do not expose them publicly.
- Seed Phrase: Your mnemonic phrase should be stored securely and never shared.
- Testing: Use testnets for testing purposes to avoid potential losses.


Acknowledgments

AUTHOR
Ebenezer Akpas

- zpywallet for secure phrase generation
- bip_utils for BIP44 implementations
- solana for Solana-specific functionalities
- tronpy for Tron blockchain support
- eth-account for Ethereum account management
- bit for Bitcoin transactions
- blockcypher for Litecoin and Dogecoin transactions

