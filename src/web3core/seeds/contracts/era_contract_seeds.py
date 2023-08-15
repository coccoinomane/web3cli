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

neth: ContractFields = {
    "name": "neth",
    "desc": "Eralend: ETH market",
    "type": "compound_v2_eth",
    "address": "0x1BbD33384869b30A323e15868Ce46013C82B86FB",
    "chain": "era",
}

nusdc: ContractFields = {
    "name": "nusdc",
    "desc": "Eralend: USDC market",
    "type": "compound_v2_erc20",
    "address": "0x1181D7BE04D80A8aE096641Ee1A87f7D557c6aeb",
    "chain": "era",
}

rfeth: ContractFields = {
    "name": "rfeth",
    "desc": "ReactorFusion: ETH market",
    "type": "compound_v2_eth",
    "address": "0xC5db68F30D21cBe0C9Eac7BE5eA83468d69297e6",
    "chain": "era",
}

rfusdc: ContractFields = {
    "name": "rfusdc",
    "desc": "ReactorFusion: USDC market",
    "type": "compound_v2_erc20",
    "address": "0x04e9Db37d8EA0760072e1aCE3F2A219988Fdac29",
    "chain": "era",
}


all = [usdc, vc, weth, neth, nusdc, rfeth, rfusdc]
