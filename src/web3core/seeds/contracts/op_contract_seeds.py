from web3core.models.types import ContractFields

weth: ContractFields = {
    "name": "weth",
    "desc": "Wrapped Ether",
    "type": "erc20",
    "address": "0x4200000000000000000000000000000000000006",
    "chain": "op",
}

usdc: ContractFields = {
    "name": "usdc",
    "desc": "USDC Circle token",
    "type": "erc20",
    "address": "0x7f5c764cbc14f9669b88837ca1490cca17c31607",
    "chain": "op",
}

usdt: ContractFields = {
    "name": "usdt",
    "desc": "USDT Tether token",
    "type": "erc20",
    "address": "0x94b008aa00579c1307b0ef2c499ad98a8ce58e58",
    "chain": "op",
}


wbtc: ContractFields = {
    "name": "wbtc",
    "desc": "Wrapped BTC token",
    "type": "erc20",
    "address": "0x68f180fcce6836688e9084f035309e29bf0a2095",
    "chain": "op",
}

all = [weth, usdc, usdt, wbtc]
