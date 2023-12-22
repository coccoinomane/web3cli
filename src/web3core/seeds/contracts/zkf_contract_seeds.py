from web3core.models.types import ContractFields

wusdc: ContractFields = {
    "name": "wusdc",
    "desc": "Wrapped USDC",
    "type": "erc20",
    "address": "0xD33Db7EC50A98164cC865dfaa64666906d79319C",
    "chain": "zkf",
}

zkf: ContractFields = {
    "name": "zkf",
    "desc": "ZKFair token",
    "type": "erc20",
    "address": "0x1cd3e2a23c45a690a18ed93fd1412543f464158f",
    "chain": "zkf",
}

eth: ContractFields = {
    "name": "eth",
    "desc": "Ether",
    "type": "erc20",
    "address": "0x4b21b980d0Dc7D3C0C6175b0A412694F3A1c7c6b",
    "chain": "zkf",
}

usdt: ContractFields = {
    "name": "usdt",
    "desc": "USDT Tether token",
    "type": "erc20",
    "address": "0x3f97bf3cd76b5ca9d4a4e9cd8a73c24e32d6c193",
    "chain": "zkf",
}

dai: ContractFields = {
    "name": "dai",
    "desc": "DAI Maker stablecoin",
    "type": "erc20",
    "address": "0xa9f4eeb30dc48d4ef77310a2108816c80457cf6f",
    "chain": "zkf",
}


wbtc: ContractFields = {
    "name": "wbtc",
    "desc": "Wrapped BTC token",
    "type": "erc20",
    "address": "0x813bcb548f99bc081e5efeeaa65e3018befb92ae",
    "chain": "zkf",
}

all = [wusdc, zkf, eth, usdt, dai, wbtc]
