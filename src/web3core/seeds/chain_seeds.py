from typing import List

from web3core.models.types import ChainFields

"""
  _      _      ___   _             _
 | |    / |    / __| | |_    __ _  (_)  _ _    ___
 | |__  | |   | (__  | ' \  / _` | | | | ' \  (_-<
 |____| |_|    \___| |_||_| \__,_| |_| |_||_| /__/

"""

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


"""
  _      ___     ___   _             _
 | |    |_  )   / __| | |_    __ _  (_)  _ _    ___
 | |__   / /   | (__  | ' \  / _` | | | | ' \  (_-<
 |____| /___|   \___| |_||_| \__,_| |_| |_||_| /__/

"""


matic: ChainFields = {
    "name": "matic",
    "desc": "Polygon POS Mainnet",
    "chain_id": 137,
    "coin": "MATIC",
    "tx_type": 1,
    "middlewares": "geth_poa_middleware",
    "rpcs": [
        {
            "url": "https://polygon-rpc.com",
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

op: ChainFields = {
    "name": "op",
    "desc": "Optimism OP Mainnet",
    "chain_id": 10,
    "coin": "ETH",
    "tx_type": 2,
    "middlewares": "",
    "rpcs": [
        {
            "url": "https://mainnet.optimism.io",
        },
        {
            "url": "https://rpc.ankr.com/optimism",
        },
        {
            "url": "https://rpc.ankr.com/gnosis",
        },
    ],
}

scroll: ChainFields = {
    "name": "scroll",
    "desc": "Scroll Mainnet",
    "chain_id": 534352,
    "coin": "ETH",
    "tx_type": 2,
    "middlewares": "geth_poa_middleware",
    "rpcs": [
        {
            "url": "https://mainnet-rpc.scroll.io",
        },
        {
            "url": "https://rpc.ankr.com/scroll",
        },
    ],
}

"""
  _                        _         _             _
 | |     ___   __   __ _  | |   __  | |_    __ _  (_)  _ _    ___
 | |__  / _ \ / _| / _` | | |  / _| | ' \  / _` | | | | ' \  (_-<
 |____| \___/ \__| \__,_| |_|  \__| |_||_| \__,_| |_| |_||_| /__/

"""

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
    # L1s
    eth,
    bnb,
    avax,
    cro,
    gno,
    # L2s
    matic,
    arb,
    era,
    erat,
    op,
    scroll,
    # Local
    ganache,
    anvil,
]
