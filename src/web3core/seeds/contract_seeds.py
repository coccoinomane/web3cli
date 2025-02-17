from typing import List

from web3core.models.types import ContractFields
from web3core.seeds.contracts import (
    arb_contract_seeds,
    avax_contract_seeds,
    base_contract_seeds,
    bnb_contract_seeds,
    era_contract_seeds,
    erat_contract_seeds,
    eth_contract_seeds,
    fantom_contract_seeds,
    gno_contract_seeds,
    manta_contract_seeds,
    op_contract_seeds,
    scroll_contract_seeds,
    sonic_contract_seeds,
    zkf_contract_seeds,
)

all: List[ContractFields] = (
    eth_contract_seeds.all
    + bnb_contract_seeds.all
    + avax_contract_seeds.all
    + arb_contract_seeds.all
    + era_contract_seeds.all
    + erat_contract_seeds.all
    + gno_contract_seeds.all
    + fantom_contract_seeds.all
    + op_contract_seeds.all
    + scroll_contract_seeds.all
    + base_contract_seeds.all
    + zkf_contract_seeds.all
    + manta_contract_seeds.all
    + sonic_contract_seeds.all
)
