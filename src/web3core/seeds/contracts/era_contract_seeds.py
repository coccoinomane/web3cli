from web3core.models.types import ContractFields

usdc: ContractFields = {
    "name": "usdc",
    "desc": "USDC Circle token",
    "type": "erc20",
    "address": "0x3355df6D4c9C3035724Fd0e3914dE96A5a83aaf4",
    "chain": "era",
}

vc: ContractFields = {
    "name": "vc",
    "desc": "Velocore token",
    "type": "erc20",
    "address": "0x85D84c774CF8e9fF85342684b0E795Df72A24908",
    "chain": "era",
}

weth: ContractFields = {
    "name": "weth",
    "desc": "Wrapped Ether",
    "type": "erc20",
    "address": "0x5AEa5775959fBC2557Cc8789bC1bf90A239D9a91",
    "chain": "era",
}

nusdc: ContractFields = {
    "name": "nusdc",
    "desc": "Eralend nUSDC pool",
    "type": "compound_v2_pool",
    "address": "0x1181D7BE04D80A8aE096641Ee1A87f7D557c6aeb",
    "chain": "era",
}


all = [usdc, vc, weth, nusdc]
