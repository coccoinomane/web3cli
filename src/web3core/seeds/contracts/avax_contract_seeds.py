from web3core.models.types import ContractFields

wavax: ContractFields = {
    "name": "wavax",
    "desc": "Wrapped AVAX",
    "type": "erc20",
    "address": "0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7",
    "chain": "avax",
}

usdc: ContractFields = {
    "name": "usdc",
    "desc": "USDC Circle token",
    "type": "erc20",
    "address": "0xb97ef9ef8734c71904d8002f8b6bc66dd9c48a6e",
    "chain": "avax",
}

usdt_e: ContractFields = {
    "name": "usdt.e",
    "desc": "Tether USD",
    "type": "erc20",
    "address": "0xc7198437980c041c805A1EDcbA50c1Ce5db95118",
    "chain": "avax",
}

btc_b: ContractFields = {
    "name": "btc.b",
    "desc": "Wrapped Bitcoin (Avalabs)",
    "type": "erc20",
    "address": "0x152b9d0FdC40C096757F570A51E494bd4b943E50",
    "chain": "avax",
}

wbtc_e: ContractFields = {
    "name": "wbtc.e",
    "desc": "Wrapped Bitcoin",
    "type": "erc20",
    "address": "0x50b7545627a5162F82A992c33b87aDc75187B218",
    "chain": "avax",
}

yeti: ContractFields = {
    "name": "yeti",
    "desc": "YETI Token",
    "type": "erc20",
    "address": "0x77777777777d4554c39223C354A05825b2E8Faa3",
    "chain": "avax",
}

traderjoe: ContractFields = {
    "name": "traderjoe",
    "desc": "Trader Joe: Router",
    "type": "uniswap_v2",
    "address": "0x60aE616a2155Ee3d9A68541Ba4544862310933d4",
    "chain": "avax",
}

traderjoe_v2: ContractFields = {
    "name": "traderjoe_v2",
    "desc": "Trader Joe: LBRouter",
    "type": "traderjoe_v2",
    "address": "0xE3Ffc583dC176575eEA7FD9dF2A7c65F7E23f4C3",
    "chain": "avax",
}

pangolin: ContractFields = {
    "name": "pangolin",
    "desc": "Pangolin Router",
    "type": "uniswap_v2",
    "address": "0xE54Ca86531e17Ef3616d22Ca28b0D458b6C89106",
    "chain": "avax",
}

all = [
    usdc,
    usdt_e,
    btc_b,
    wbtc_e,
    wavax,
    yeti,
    traderjoe,
    traderjoe_v2,
    pangolin,
]
