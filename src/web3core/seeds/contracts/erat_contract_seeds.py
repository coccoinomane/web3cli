from web3core.models.types import ContractFields

usdc: ContractFields = {
    "name": "usdc",
    "desc": "USDC Circle token",
    "type": "erc20",
    "address": "0x0faf6df7054946141266420b43783387a78d82a9",
    "chain": "erat",
}

usdt: ContractFields = {
    "name": "usdt",
    "desc": "USDT Tether token",
    "type": "erc20",
    "address": "0xfced12debc831d3a84931c63687c395837d42c2b",
    "chain": "erat",
}

test: ContractFields = {
    "name": "test",
    "desc": "Testnet token",
    "type": "erc20",
    "address": "0x26c78bd5901f57da8aa5cf060ab2116d26906b5e",
    "chain": "erat",
}

wbtc: ContractFields = {
    "name": "wbtc",
    "desc": "Wrapped Bitcoin",
    "type": "erc20",
    "address": "0x0bfce1d53451b4a8175dd94e6e029f7d8a701e9c",
    "chain": "erat",
}

weth: ContractFields = {
    "name": "weth",
    "desc": "Wrapped Ether",
    "type": "erc20",
    "address": "0x33f1fbe337a19bebca41a3dcba896752729286ea",
    "chain": "erat",
}

all = [usdc, usdt, test, wbtc, weth]
