from web3core.models.types import ContractFields

usdc: ContractFields = {
    "name": "usdc",
    "desc": "USDC Circle token",
    "type": "erc20",
    "address": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
    "chain": "eth",
}

usdt: ContractFields = {
    "name": "usdt",
    "desc": "Tether USD",
    "type": "erc20",
    "address": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
    "chain": "eth",
}

weth: ContractFields = {
    "name": "weth",
    "desc": "Wrapped Ether",
    "type": "erc20",
    "address": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
    "chain": "eth",
}

uniswap_v2: ContractFields = {
    "name": "uniswap_v2",
    "desc": "Uniswap V2: Router 2",
    "type": "uniswap_v2",
    "address": "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D",
    "chain": "eth",
}

uniswap_v2_factory: ContractFields = {
    "name": "uniswap_v2_factory",
    "desc": "Uniswap V2: Factory",
    "type": "uniswap_v2_factory",
    "address": "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f",
    "chain": "eth",
}

uniswap_v2_usdc_usdt: ContractFields = {
    "name": "uniswap_v2_usdc_usdt",
    "desc": "Uniswap V2: Pool USDC/USDT",
    "type": "uniswap_v2_pool",
    "address": "0x3041cbd36888becc7bbcbc0045e3b1f144466f5f",
    "chain": "eth",
}

uniswap_v3: ContractFields = {
    "name": "uniswap_v3",
    "desc": "Uniswap V3: SwapRouter",
    "type": "uniswap_v3",
    "address": "0xE592427A0AEce92De3Edee1F18E0157C05861564",
    "chain": "eth",
}


all = [
    usdc,
    weth,
    usdt,
    uniswap_v2,
    uniswap_v2_factory,
    uniswap_v2_usdc_usdt,
    uniswap_v3,
]
