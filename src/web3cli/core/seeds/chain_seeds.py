from typing import List

from web3cli.core.models.types import ChainFields


# Ethereum
ethereum: ChainFields = {
    "name": "ethereum",
    "chain_id": 1,
    "coin": "ETH",
    "tx_type": 2,
    "middlewares": "",
    "rpcs": [
        {
            "url": "https://cloudflare-eth.com",
        },
        {
            "url": "https://mainnet.infura.io/v3/98c23dcc2c3947cbacc2a0c7e1b1757a",
        },
    ],
}

# BNB Chain
binance: ChainFields = {
    "name": "binance",
    "chain_id": 56,
    "coin": "BNB",
    "tx_type": 1,
    "middlewares": "geth_poa_middleware",
    "rpcs": [
        {
            "url": "https://bsc-dataseed.binance.org/",
        }
    ],
}

# Avalanche C Chian
avalanche: ChainFields = {
    "name": "avalanche",
    "chain_id": 43114,
    "coin": "AVAX",
    "tx_type": 2,
    "middlewares": "geth_poa_middleware",
    "rpcs": [
        {
            "url": "https://api.avax.network/ext/bc/C/rpc",
        }
    ],
}

# Local chain (e.g. ganache or hardhat network)
local_chain: ChainFields = {
    "name": "local",
    "chain_id": 1337,
    "coin": "ETH",
    "tx_type": 1,
    "middlewares": "",
    "rpcs": [
        {
            "url": "http://127.0.0.1:8545",
        }
    ],
}

chain_seeds: List[ChainFields] = [ethereum, binance, avalanche, local_chain]
