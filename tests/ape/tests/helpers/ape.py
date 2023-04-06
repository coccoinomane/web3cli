import ape


def get_contract_container(contract_name: str) -> ape.contracts.ContractContainer:
    """Get a contract container from the ape project, that can be used
    to deploy a contract instance."""
    try:
        return getattr(ape.project, contract_name)
    except AttributeError:
        raise ValueError(f"Contract {contract_name} not found in ape project")
