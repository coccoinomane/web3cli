# from cement import ex
# from web3cli.controllers.controller import Controller
# import secrets

# class Signer(Controller):
#     """Handler of the `web3 key` commands"""

#     class Meta:
#         label = "key"
#         help = "handle application keys"
#         stacked_type = "nested"
#         stacked_on = "base"

#     @ex(
#         help="generate an app key, replacing the current one",
#     )
#     def add(self) -> None:
#         key = secrets.token_bytes(32)

#         key = getpass.getpass("Private key: ")
#         try:
#             address = Account.from_key(key).address
#         except:
#             raise KeyIsInvalid(
#                 "Invalid private key. Please note that private key is different from mnemonic password."
#             )
#         Model.create(
#             label=self.app.pargs.label,
#             key=key,
#             address=address,
#         )
#         self.app.log.info(f"Signer '{self.app.pargs.label}' added correctly")

#     # @ex(
#     #     help="delete an address",
#     #     arguments=[
#     #         (["label"], {"help": "label of the address to delete", "action": "store"}),
#     #     ],
#     # )
#     # def delete(self) -> None:
#     #     address = Model.get_by_label(self.app.pargs.label)
#     #     if not address:
#     #         raise AddressNotFound(
#     #             f"Address '{self.app.pargs.label}' does not exist, can't delete it"
#     #         )
#     #     address.delete_instance()
#     #     self.app.log.info(f"Address '{self.app.pargs.label}' deleted correctly")

#     @ex(help="get current signer")
#     def get(self) -> None:
#         self.app.print(self.app.signer)
