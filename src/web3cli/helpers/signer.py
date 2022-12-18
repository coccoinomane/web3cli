from cement import App

from web3cli.core.exceptions import SignerNotFound, Web3CliError
from web3cli.core.models.signer import Signer


def signer_ready_or_raise(app: App) -> None:
    """Check whether the signer is ready to write on the blockchain"""
    if not app.signer:
        raise Web3CliError(
            "No signer given. Specify one with the `w3 --signer` flag or, if you don't have any yet, add one with `w3 db signer add`."
        )
    Signer.get_by_name_or_raise(app.signer)
