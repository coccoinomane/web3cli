from typing import List
from web3cli.core.seeds.types import ChainSeed


seed_chains: List[ChainSeed] = [
    # Ethereum
    {
        "name": "ethereum",
        "chain_id": 1,
        "coin": "ETH",
        "tx_type": 2,
        "middlewares": [""],
        "rpcs": [
            "https://mainnet.infura.io/v3/98c23dcc2c3947cbacc2a0c7e1b1757a",
            "https://ethereum-mainnet--rpc.datahub.figment.io/apikey/cfd6d301706d81d97fd78bced8211f27",
        ],
    },
    # BNB chain
    {
        "name": "binance",
        "chain_id": 56,
        "coin": "BNB",
        "tx_type": 1,
        "middlewares": ["geth_poa_middleware"],
        "rpcs": [
            "https://bsc-dataseed.binance.org/",
            "https://bsc--mainnet--rpc.datahub.figment.io/apikey/1e03acdcb04656b9412009ac14b1a201",
        ],
    },
    # Avalanche C Chain
    {
        "name": "avalanche",
        "chain_id": 43114,
        "coin": "AVAX",
        "tx_type": 2,
        "middlewares": ["geth_poa_middleware"],
        "middlewares": [""],
        "rpcs": [
            "https://api.avax.network/ext/bc/C/rpc",
            "https://avalanche-mainnet.infura.io/v3/98c23dcc2c3947cbacc2a0c7e1b1757a",
            "https://avalanche--mainnet--rpc.datahub.figment.io/apikey/cfd6d301706d81d97fd78bced8211f27/ext/bc/C/rpc",
        ],
    },
]
