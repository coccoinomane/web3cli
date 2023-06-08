from typing import List

from web3core.models.types import ChainFields

eth: ChainFields = {
    "name": "eth",
    "desc": "Ethereum Mainnet",
    "chain_id": 1,
    "coin": "ETH",
    "tx_type": 2,
    "middlewares": "",
    "rpcs": [
        {
            "url": "https://cloudflare-eth.com",
        },
    ],
}

bnb: ChainFields = {
    "name": "bnb",
    "desc": "Binance Smart Chain Mainnet",
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

avax: ChainFields = {
    "name": "avax",
    "desc": "Avalanche C-Chain",
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

matic: ChainFields = {
    "name": "matic",
    "desc": "Polygon Mainnet",
    "chain_id": 137,
    "coin": "MATIC",
    "tx_type": 1,
    "middlewares": "geth_poa_middleware",
    "rpcs": [
        {
            "url": "https://polygon-rpc.com/",
        }
    ],
}

cro: ChainFields = {
    "name": "cro",
    "desc": "Cronos Mainnet Beta",
    "chain_id": 25,
    "coin": "CRO",
    "tx_type": 2,
    "middlewares": "",
    "rpcs": [
        {
            "url": "https://evm.cronos.org",
        }
    ],
}

arb: ChainFields = {
    "name": "arb",
    "desc": "Arbitrum One",
    "chain_id": 42161,
    "coin": "ETH",
    "tx_type": 2,
    "middlewares": "",
    "rpcs": [
        {
            "url": "https://arb1.arbitrum.io/rpc",
        },
    ],
}

era: ChainFields = {
    "name": "era",
    "desc": "zkSync Era",
    "chain_id": 324,
    "coin": "ETH",
    "tx_type": 2,
    "middlewares": "",
    "rpcs": [
        {
            "url": "https://mainnet.era.zksync.io",
        },
    ],
}

erat: ChainFields = {
    "name": "erat",
    "desc": "zkSync Era Testnet",
    "chain_id": 280,
    "coin": "ETH",
    "tx_type": 2,
    "middlewares": "",
    "rpcs": [
        {
            "url": "https://testnet.era.zksync.dev",
        },
    ],
}


gno: ChainFields = {
    "name": "gno",
    "desc": "Gnosis",
    "chain_id": 100,
    "coin": "xDAI",
    "tx_type": 2,
    "middlewares": "",
    "rpcs": [
        {
            "url": "https://rpc.gnosischain.com/",
        },
        {
            "url": "https://rpc.gnosis.gateway.fm",
        },
        {
            "url": "https://rpc.ankr.com/gnosis",
        },
    ],
}


ganache: ChainFields = {
    "name": "ganache",
    "desc": "Ganache local chain",
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

anvil: ChainFields = {
    "name": "anvil",
    "desc": "Anvil local chain",
    "chain_id": 31337,
    "coin": "ETH",
    "tx_type": 2,
    "middlewares": "",
    "rpcs": [
        {
            "url": "http://127.0.0.1:8545",
        }
    ],
}

all: List[ChainFields] = [
    eth,
    bnb,
    avax,
    matic,
    cro,
    arb,
    era,
    erat,
    gno,
    ganache,
    anvil,
]
