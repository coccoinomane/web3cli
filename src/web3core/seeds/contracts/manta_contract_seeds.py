import json

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

tia: ContractFields = {
    "name": "tia",
    "desc": "Celestia Token",
    "type": "erc20",
    "address": "0x6Fae4D9935E2fcb11fC79a64e917fb2BF14DaFaa",
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

wusdm: ContractFields = {
    "name": "usdm",
    "desc": "Mountain Protocol USD (Wrapped)",
    "type": "erc20",
    "address": "0xbdAd407F77f44F7Da6684B416b1951ECa461FB07",
    "chain": "manta",
}

usdm: ContractFields = {  # alias for wusdm
    "name": "wusdm",
    "desc": "Mountain Protocol USD (Wrapped)",
    "type": "erc20",
    "address": "0xbdAd407F77f44F7Da6684B416b1951ECa461FB07",
    "chain": "manta",
}

labm: ContractFields = {
    "name": "labm",
    "desc": "LayerBank Token",
    "type": "erc20",
    "address": "0x20a512dbdc0d006f46e6ca11329034eb3d18c997",
    "chain": "manta",
}

gai: ContractFields = {
    "name": "gai",
    "desc": "GAI Stablecoin",
    "type": "erc20",
    "address": "0xcd91716ef98798a85e79048b78287b13ae6b99b2",
    "chain": "manta",
}

gok: ContractFields = {
    "name": "gok",
    "desc": "GOK Goku Money",
    "type": "erc20",
    "address": "0x387660BC95682587efC12C543c987ABf0fB9778f",
    "chain": "manta",
}

maticx: ContractFields = {
    "name": "maticx",
    "desc": "Stader Liquid Staking Matic",
    "type": "erc20",
    "address": "0x01D27580C464d5B3B26F78Bee12E684901dbC02a",
    "chain": "manta",
}

asm: ContractFields = {
    "name": "asm",
    "desc": "As Match token",
    "type": "erc20",
    "address": "0xcd5d6de3fdbce1895f0dac13a065673599ed6806",
    "chain": "manta",
}

wsteth: ContractFields = {
    "name": "wsteth",
    "desc": "Wrapped liquid staked Ether 2.0",
    "type": "erc20",
    "address": "0x2FE3AD97a60EB7c79A976FC18Bb5fFD07Dd94BA5",
    "chain": "manta",
}

firefly_v3_factory = {
    "name": "firefly_v3_factory",
    "desc": "Firefly V3 Factory",
    "address": "0x8666EF9DC0cA5336147f1B11f2C4fC2ecA809B95",
    "chain": "manta",
    "abi": json.loads(
        '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint24","name":"fee","type":"uint24"},{"indexed":true,"internalType":"int24","name":"tickSpacing","type":"int24"}],"name":"FeeAmountEnabled","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"oldOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnerChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"token0","type":"address"},{"indexed":true,"internalType":"address","name":"token1","type":"address"},{"indexed":true,"internalType":"uint24","name":"fee","type":"uint24"},{"indexed":false,"internalType":"int24","name":"tickSpacing","type":"int24"},{"indexed":false,"internalType":"address","name":"pool","type":"address"}],"name":"PoolCreated","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"tokenA","type":"address"},{"indexed":false,"internalType":"address","name":"tokenB","type":"address"},{"indexed":false,"internalType":"uint24","name":"fee","type":"uint24"}],"name":"WhitelistPair","type":"event"},{"inputs":[],"name":"INIT_CODE_PAIR_HASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint24","name":"fee","type":"uint24"}],"name":"createPool","outputs":[{"internalType":"address","name":"pool","type":"address"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint24","name":"fee","type":"uint24"},{"internalType":"int24","name":"tickSpacing","type":"int24"}],"name":"enableFeeAmount","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint24","name":"","type":"uint24"}],"name":"feeAmountTickSpacing","outputs":[{"internalType":"int24","name":"","type":"int24"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"}],"name":"getPairWhitelist","outputs":[{"internalType":"uint24","name":"fee","type":"uint24"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"},{"internalType":"uint24","name":"","type":"uint24"}],"name":"getPool","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"parameters","outputs":[{"internalType":"address","name":"factory","type":"address"},{"internalType":"address","name":"token0","type":"address"},{"internalType":"address","name":"token1","type":"address"},{"internalType":"uint24","name":"fee","type":"uint24"},{"internalType":"int24","name":"tickSpacing","type":"int24"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_owner","type":"address"}],"name":"setOwner","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint24","name":"fee","type":"uint24"}],"name":"whitelistPair","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
    ),
}

all = [
    weth,
    manta,
    usdc,
    usdt,
    tia,
    dai,
    wbtc,
    stone,
    wusdm,
    usdm,
    labm,
    gai,
    gok,
    maticx,
    asm,
    wsteth,
    firefly_v3_factory,
]
