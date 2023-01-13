from web3core.models.types import ContractFields

avax_usdc: ContractFields = {
    "name": "usdc",
    "desc": "USDC Circle token",
    "type": "erc20",
    "address": "0xb97ef9ef8734c71904d8002f8b6bc66dd9c48a6e",
    "chain": "avax",
}

avax_traderjoe_router: ContractFields = {
    "name": "traderjoe_router",
    "desc": "Trader Joe: Router",
    "type": "uniswap_router_v2",
    "address": "0x60aE616a2155Ee3d9A68541Ba4544862310933d4",
    "chain": "avax",
}

all = [avax_usdc, avax_traderjoe_router]
