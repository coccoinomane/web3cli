from typing import List
from web3cli.core.seeds.types import ChainSeed

# Ethereum
ethereum: ChainSeed = {
    "name": "ethereum",
    "chain_id": 1,
    "coin": "ETH",
    "tx_type": 2,
    "middlewares": [""],
    "rpcs": [
        "https://cloudflare-eth.com",
        "https://mainnet.infura.io/v3/98c23dcc2c3947cbacc2a0c7e1b1757a",
    ],
}

# BNB Chain
binance: ChainSeed = {
    "name": "binance",
    "chain_id": 56,
    "coin": "BNB",
    "tx_type": 1,
    "middlewares": ["geth_poa_middleware"],
    "rpcs": [
        "https://bsc-dataseed.binance.org/",
    ],
}

# Avalanche C Chian
avalanche: ChainSeed = {
    "name": "avalanche",
    "chain_id": 43114,
    "coin": "AVAX",
    "tx_type": 2,
    "middlewares": ["geth_poa_middleware"],
    "rpcs": [
        "https://api.avax.network/ext/bc/C/rpc",
    ],
}

# Local chain (e.g. ganache or hardhat network)
local_chain: ChainSeed = {
    "name": "local_chain",
    "chain_id": 1,
    "coin": "ETH",
    "tx_type": 1,
    "middlewares": [],
    "rpcs": [
        "http://127.0.0.1:8545",
    ],
}

chain_seeds: List[ChainSeed] = [ethereum, binance, avalanche, local_chain]
