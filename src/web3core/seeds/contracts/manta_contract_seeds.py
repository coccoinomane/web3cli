from web3core.models.types import ContractFields

weth: ContractFields = {
    "name": "weth",
    "desc": "Wrapped ETH",
    "type": "weth",
    "address": "0x0Dc808adcE2099A9F62AA87D9670745AbA741746",
    "chain": "manta",
}

manta: ContractFields = {
    "name": "manta",
    "desc": "Manta token",
    "type": "erc20",
    "address": "0x95CeF13441Be50d20cA4558CC0a27B601aC544E5",
    "chain": "manta",
}

usdc: ContractFields = {
    "name": "usdc",
    "desc": "USDC Circle token",
    "type": "erc20",
    "address": "0xb73603C5d87fA094B7314C74ACE2e64D165016fb",
    "chain": "manta",
}

usdt: ContractFields = {
    "name": "usdt",
    "desc": "USDT Tether token",
    "type": "erc20",
    "address": "0xf417F5A458eC102B90352F697D6e2Ac3A3d2851f",
    "chain": "manta",
}

dai: ContractFields = {
    "name": "dai",
    "desc": "DAI Maker stablecoin",
    "type": "erc20",
    "address": "0x1c466b9371f8aBA0D7c458bE10a62192Fcb8Aa71",
    "chain": "manta",
}

wbtc: ContractFields = {
    "name": "wbtc",
    "desc": "Wrapped BTC token",
    "type": "erc20",
    "address": "0x305E88d809c9DC03179554BFbf85Ac05Ce8F18d6",
    "chain": "manta",
}

stone: ContractFields = {
    "name": "stone",
    "desc": "STONE token Manta",
    "type": "erc20",
    "address": "0xEc901DA9c68E90798BbBb74c11406A32A70652C3",
    "chain": "manta",
}


all = [weth, manta, usdc, usdt, dai, wbtc, stone]
