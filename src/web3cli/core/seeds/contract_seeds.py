from typing import List

from web3cli.core.models.types import ContractFields
from web3cli.core.seeds import (
    avax_contract_seeds,
    bnb_contract_seeds,
    eth_contract_seeds,
)

all: List[ContractFields] = (
    eth_contract_seeds.all + bnb_contract_seeds.all + avax_contract_seeds.all
)
