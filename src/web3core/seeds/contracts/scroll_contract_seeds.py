from web3core.models.types import ContractFields

weth: ContractFields = {
    "name": "weth",
    "desc": "Wrapped Ether",
    "type": "erc20",
    "address": "0x5300000000000000000000000000000000000004",
    "chain": "scroll",
}

usdc: ContractFields = {
    "name": "usdc",
    "desc": "USDC Circle token",
    "type": "erc20",
    "address": "0x06efdbff2a14a7c8e15944d1f4a48f9f95f663a4",
    "chain": "scroll",
}

usdt: ContractFields = {
    "name": "usdt",
    "desc": "USDT Tether token",
    "type": "erc20",
    "address": "0xf55BEC9cafDbE8730f096Aa55dad6D22d44099Df",
    "chain": "scroll",
}


wbtc: ContractFields = {
    "name": "wbtc",
    "desc": "Wrapped BTC token",
    "type": "erc20",
    "address": "0x3C1BCa5a656e69edCD0D4E36BEbb3FcDAcA60Cf1",
    "chain": "scroll",
}

all = [weth, usdc, usdt, wbtc]
