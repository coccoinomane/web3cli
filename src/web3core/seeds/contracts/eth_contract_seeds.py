from web3core.models.types import ContractFields

eth_usdc: ContractFields = {
    "name": "usdc",
    "desc": "USDC Circle token",
    "type": "erc20",
    "address": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
    "chain": "eth",
}

eth_usdt: ContractFields = {
    "name": "usdt",
    "desc": "Tether USD",
    "type": "erc20",
    "address": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
    "chain": "eth",
}

eth_weth: ContractFields = {
    "name": "weth",
    "desc": "Wrapped Ether",
    "type": "erc20",
    "address": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
    "chain": "eth",
}

eth_uniswap_router_v2: ContractFields = {
    "name": "uniswap_router_v2",
    "desc": "Uniswap V2: Router 2",
    "type": "uniswap_router_v2",
    "address": "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D",
    "chain": "eth",
}

all = [eth_usdc, eth_weth, eth_usdt, eth_uniswap_router_v2]
