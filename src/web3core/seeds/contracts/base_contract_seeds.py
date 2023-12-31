from web3core.models.types import ContractFields

weth: ContractFields = {
    "name": "weth",
    "desc": "Wrapped Ether",
    "type": "weth",
    "address": "0x4200000000000000000000000000000000000006",
    "chain": "base",
}

usdc: ContractFields = {
    "name": "usdc",
    "desc": "USDC Circle token",
    "type": "erc20",
    "address": "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913",
    "chain": "base",
}

all = [weth, usdc]
