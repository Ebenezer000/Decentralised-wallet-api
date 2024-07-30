# MultiChain Wallet Library

The MultiChain Wallet Library provides a unified interface for generating, managing, and transacting with wallets across multiple blockchains using a single mnemonic phrase. It supports popular cryptocurrencies such as Bitcoin, Ethereum, Solana, and many others.

## Features

- Generate wallets and derive private keys for multiple blockchains using a single mnemonic.
- Transfer cryptocurrency across supported blockchains.
- Sign and broadcast transactions securely.

## Installation

To use the MultiChain Wallet Library, you'll need to install the following dependencies:

pip install bip-utils solana tronpy eth-account bit blockcypher

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

License

This project is licensed under the MIT License - see the LICENSE file for details.

Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

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
