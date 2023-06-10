from web3core.models.types import ContractFields

busd: ContractFields = {
    "name": "busd",
    "desc": "Binance-Peg BUSD Token",
    "type": "erc20",
    "address": "0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56",
    "chain": "bnb",
}

usdt: ContractFields = {
    "name": "usdt",
    "desc": "Binance-Peg USDT Token",
    "type": "erc20",
    "address": "0x55d398326f99059ff775485246999027b3197955",
    "chain": "bnb",
}

btcb: ContractFields = {
    "name": "btcb",
    "desc": "Binance-Peg BTC Token",
    "type": "erc20",
    "address": "0x7130d2a12b9bcbfae4f2634d864a1ee1ce3ead9c",
    "chain": "bnb",
}

pancakeswap_v2: ContractFields = {
    "name": "pancakeswap_v2",
    "desc": "PancakeSwap: Router v2",
    "type": "uniswap_v2",
    "address": "0x10ED43C718714eb63d5aA57B78B54704E256024E",
    "chain": "bnb",
}

all = [busd, usdt, btcb, pancakeswap_v2]
