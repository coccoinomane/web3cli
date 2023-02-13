from web3core.models.types import ContractFields

avax_usdc: ContractFields = {
    "name": "usdc",
    "desc": "USDC Circle token",
    "type": "erc20",
    "address": "0xb97ef9ef8734c71904d8002f8b6bc66dd9c48a6e",
    "chain": "avax",
}

avax_usdt_e: ContractFields = {
    "name": "usdt.e",
    "desc": "Tether USD",
    "type": "erc20",
    "address": "0xc7198437980c041c805A1EDcbA50c1Ce5db95118",
    "chain": "avax",
}

avax_wavax: ContractFields = {
    "name": "wavax",
    "desc": "Wrapped AVAX",
    "type": "erc20",
    "address": "0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7",
    "chain": "avax",
}

avax_traderjoe_v2: ContractFields = {
    "name": "traderjoe_v2",
    "desc": "Trader Joe: Router V2",
    "type": "uniswap_v2",
    "address": "0x60aE616a2155Ee3d9A68541Ba4544862310933d4",
    "chain": "avax",
}

all = [avax_usdc, avax_usdt_e, avax_wavax, avax_traderjoe_v2]
