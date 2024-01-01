from web3core.models.types import ContractFields

wusdc: ContractFields = {
    "name": "wusdc",
    "desc": "Wrapped USDC",
    "type": "weth",
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

sideswap: ContractFields = {
    "name": "sideswap",
    "desc": "SideSwap: Router",
    "type": "uniswap_v2",
    "address": "0x72E25Dd6a6E75fC8f7820bA2eDEc3F89bB61f7A4",
    "chain": "zkf",
}

sideswap_factory: ContractFields = {
    "name": "sideswap_factory",
    "desc": "Sideswap: Factory",
    "type": "uniswap_v2_factory",
    "address": "0x3F5a6e62cccD2C9AAF3dE431e127D65BC457000a",
    "chain": "zkf",
}

sideswap_eth_usdc: ContractFields = {
    "name": "sideswap_eth_usdc",
    "desc": "SideSwap: Pool ETH/USDC",
    "type": "uniswap_v2_pool",
    "address": "0xe0dd622547525b81a53Cc788a88a7f085ea634FE",
    "chain": "zkf",
}

sideswap_usdt_usdc: ContractFields = {
    "name": "sideswap_usdt_usdc",
    "desc": "SideSwap: Pool USDT/USDC",
    "type": "uniswap_v2_pool",
    "address": "0x79cAABe653D37e56246d13895b26676cC57cc463",
    "chain": "zkf",
}

izumi: ContractFields = {
    "name": "izumi",
    "desc": "Izumi: Swap router",
    "type": "izumi",
    "address": "0x02F55D53DcE23B4AA962CC68b0f685f26143Bdb2",
    "chain": "zkf",
}


all = [
    wusdc,
    zkf,
    eth,
    usdt,
    dai,
    wbtc,
    sideswap,
    sideswap_factory,
    sideswap_eth_usdc,
    sideswap_usdt_usdc,
    izumi,
]
