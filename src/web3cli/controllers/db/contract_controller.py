from cement import ex
from web3cli.controllers.controller import Controller
from web3cli.core.helpers.os import read_json
from web3cli.core.models.contract import Contract
from web3cli.core.exceptions import Web3CliError
from web3cli.helpers.render import render_table
from playhouse.shortcuts import model_to_dict


class ContractController(Controller):
    """Handler of the `w3 db contract` commands"""

    class Meta:
        label = "contract"
        help = "add, list or delete contracts"
        stacked_type = "nested"
        stacked_on = "db"

    @ex(help="list contracts")
    def list(self) -> None:
        render_table(
            self.app,
            data=[
                [c.name, c.chain, c.address] for c in Contract.get_all(Contract.name)
            ],
            headers=["NAME", "CHAIN", "ADDRESS"],
            wrap=42,
        )

    @ex(
        help="show details of the given contract",
        arguments=[
            (["name"], {"help": "name of the contract"}),
        ],
    )
    def get(self) -> None:
        contract = Contract.get_by_name_or_raise(self.app.pargs.name)
        self.app.render(model_to_dict(contract), indent=4, handler="json")

    @ex(
        help="add a new contract to the database",
        arguments=[
            (["name"], {"help": "name of the contract, for reference"}),
            (
                ["address"],
                {"help": "address of the contract on the blockchain (0x...)"},
            ),
            (["-d", "--desc"], {"action": "store"}),
            (
                ["-u", "--update"],
                {
                    "help": "if a contract with the same name is present, overwrite it",
                    "action": "store_true",
                },
            ),
            (
                ["--abi"],
                {
                    "help": "json file containing the contract's ABI",
                },
            ),
        ],
    )
    def add(self) -> None:

        # Parse ABI file
        abi = None
        if self.app.pargs.abi:
            try:
                abi = read_json(self.app.pargs.abi)
            except:
                raise Web3CliError(f"Could not read ABI from file {self.app.pargs.abi}")

        # Add or update contract
        contract = Contract.get_by_name(self.app.pargs.name)
        if not contract or self.app.pargs.update:
            Contract.upsert(
                {
                    "name": self.app.pargs.name,
                    "desc": self.app.pargs.desc,
                    "address": self.app.pargs.address,
                    "chain": self.app.chain_name,
                    "abi": abi,
                },
                logger=self.app.log.info,
            )
        else:
            raise Web3CliError(
                f"Contract '{self.app.pargs.name}' already exists. Use `--update` or `-u` to update it."
            )

    @ex(
        help="delete a contract",
        arguments=[
            (["name"], {"help": "hash of the contract to delete"}),
        ],
    )
    def delete(self) -> None:
        contract = Contract.get_by_name_or_raise(self.app.pargs.name)
        contract.delete_instance()
        self.app.log.info(f"Contract '{self.app.pargs.name}' deleted correctly")
