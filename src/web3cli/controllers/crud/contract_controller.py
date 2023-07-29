from cement import ex
from eth_utils import encode_hex, function_abi_to_4byte_selector
from playhouse.shortcuts import model_to_dict
from web3._utils.abi import abi_to_signature

from web3cli.exceptions import Web3CliError
from web3cli.framework.controller import Controller
from web3cli.helpers import args
from web3cli.helpers.render import render, render_table
from web3core.helpers.client_factory import make_web3_contract
from web3core.helpers.seed import seed_contracts
from web3core.models.contract import Contract
from web3core.seeds import contract_seeds


class ContractController(Controller):
    """Handler of the `w3 contract` CRUD commands"""

    class Meta:
        label = "contract"
        help = "add, list or delete contracts"
        stacked_type = "nested"
        stacked_on = "base"

    @ex(
        help="list contracts on the current chain",
        arguments=[
            (
                ["type"],
                {
                    "help": "optionally restrict to a certain type of contract, e.g. uniswap_v2, erc20, etc.",
                    "default": None,
                    "nargs": "?",
                },
            ),
            args.chain(),
        ],
    )
    def list(self) -> None:
        render_table(
            self.app,
            data=[
                [c.name, c.chain, c.type, "Yes" if bool(c.abi) else "No", c.address]
                for c in Contract.get_all(Contract.name)
                if c.chain == self.app.chain.name
                and (self.app.pargs.type is None or self.app.pargs.type == c.type)
            ],
            headers=["NAME", "CHAIN", "TYPE", "ABI", "ADDRESS"],
            wrap=42,
        )

    @ex(
        help="show details of contract by name and optionally chain",
        arguments=[
            (["name"], {"help": "name of the contract"}),
            args.chain(),
        ],
    )
    def get(self) -> None:
        contract = Contract.get_by_name_and_chain_or_raise(
            self.app.pargs.name, self.app.chain.name
        )
        render(self.app, model_to_dict(contract))

    @ex(
        help="add a new contract to the database",
        arguments=[
            (["name"], {"help": "name of the contract, for reference"}),
            (["-d", "--desc"], {"action": "store"}),
            (
                ["-t", "--type"],
                {
                    "help": "type of the contract, e.g. erc20 or uniswap_v2. The type will be used to infer the contract's ABI."
                },
            ),
            (
                ["address"],
                {"help": "address of the contract on the blockchain (0x...)"},
            ),
            (
                ["-u", "--update"],
                {
                    "help": "if a contract with the same name is present, overwrite it",
                    "action": "store_true",
                },
            ),
            args.contract_abi(
                help="Contract's ABI, as a string or file. Required, unless --type is provided.",
            ),
            args.chain(),
        ],
    )
    def add(self) -> None:
        # Parse ABI file
        abi = None
        if self.app.pargs.abi:
            abi = args.parse_contract_abi(self.app)

        # Throw if no ABI and no type
        if not self.app.pargs.update and not abi and not self.app.pargs.type:
            raise Web3CliError("Either --type or --abi must be provided")

        # Add or update contract
        contract = Contract.get_by_name_and_chain(
            self.app.pargs.name, self.app.chain.name
        )
        if not contract or self.app.pargs.update:
            Contract.upsert(
                {
                    "name": self.app.pargs.name,
                    "desc": self.app.pargs.desc,
                    "type": self.app.pargs.type,
                    "address": self.app.pargs.address,
                    "chain": self.app.chain.name,
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
            (["name"], {"help": "name of the contract to delete"}),
            args.chain(),
        ],
    )
    def delete(self) -> None:
        contract = Contract.get_by_name_and_chain_or_raise(
            self.app.pargs.name, self.app.chain.name
        )
        contract.delete_instance()
        self.app.log.info(
            f"Contract '{self.app.pargs.name}' on chain '{self.app.chain.name}' deleted correctly"
        )

    @ex(help="preload a few contracts and their chains")
    def seed(self) -> None:
        seed_contracts(contract_seeds.all)
        self.app.log.info(
            f"Imported {len(contract_seeds.all)} contracts, run `w3 contract list` to show them"
        )

    @ex(
        help="Given input data for a contract call, return the signature of the function and its decoded arguments",
        arguments=[
            (["contract"], {"help": "Name of the contract"}),
            (
                ["data"],
                {"help": "Input data"},
            ),
            (
                ["--function", "--fn"],
                {
                    "help": "Provide the function name if you did not include the function selector in the data"
                },
            ),
            args.chain(),
        ],
    )
    def decode_function_data(self) -> None:
        web3_contract = make_web3_contract(self.app.pargs.contract, self.app.chain)
        # Prepend selector if --function is specified
        if self.app.pargs.function:
            func_obj = web3_contract.get_function_by_name(self.app.pargs.function)
            selector = encode_hex(function_abi_to_4byte_selector(func_obj.abi))
            if not self.app.pargs.data.startswith(selector):
                self.app.pargs.data = selector + self.app.pargs.data
        # Decode the function params
        func_obj, func_params = web3_contract.decode_function_input(self.app.pargs.data)
        func_params["__function_signature"] = abi_to_signature(func_obj.abi)
        render(self.app, func_params)
