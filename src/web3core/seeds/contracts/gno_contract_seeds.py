from web3core.models.types import ContractFields

wxdai: ContractFields = {
    "name": "wxdai",
    "desc": "Wrapped xDAI token",
    "type": "erc20",
    "address": "0xe91d153e0b41518a2ce8dd3d7944fa863463a97d",
    "chain": "gno",
}

gno: ContractFields = {
    "name": "gno",
    "desc": "Gnosis token",
    "type": "erc20",
    "address": "0x9c58bacc331c9aa871afd802db6379a98e80cedb",
    "chain": "gno",
}

usdc: ContractFields = {
    "name": "usdc",
    "desc": "USDC Circle token",
    "type": "erc20",
    "address": "0xddafbb505ad214d7b80b1f830fccc89b60fb7a83",
    "chain": "gno",
}

usdt: ContractFields = {
    "name": "usdt",
    "desc": "USDT Tether token",
    "type": "erc20",
    "address": "0x4ecaba5870353805a9f068101a40e0f32ed605c6",
    "chain": "gno",
}

weth: ContractFields = {
    "name": "weth",
    "desc": "Wrapped Ether",
    "type": "erc20",
    "address": "0x6a023ccd1ff6f2045c3309768ead9e68f978f6e1",
    "chain": "gno",
}

wbtc: ContractFields = {
    "name": "wbtc",
    "desc": "Wrapped BTC token",
    "type": "erc20",
    "address": "0x8e5bbbb09ed1ebde8674cda39a0c169401db4252",
    "chain": "gno",
}

all = [wxdai, gno, usdc, usdt, weth, wbtc]
