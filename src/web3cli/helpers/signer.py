import json
from typing import Any

from web3cli.exceptions import SignerNotResolved
from web3cli.framework.app import App
from web3cli.helpers.crypto import decrypt_keyfile_dict
from web3core.models.signer import Signer


def get_signer_from_keyfile_dict(
    app: App, name: str, keyfile_dict: dict[str, Any]
) -> Signer:
    """Instantiate a Signer object from a keyfile; the user will be asked for
    the keyfile password"""
    key = decrypt_keyfile_dict(keyfile_dict)
    return Signer.instantiate_encrypt(name, key, app.app_key)


def get_signer(app: App, signer_identifier: str) -> Signer:
    """Return a Signer object from the given identifier (name, address,
    private key or path to keyfile).

    In case of a keyfile, the user will be asked for the password."""

    # Case 1: signer_identifier is the name of a registered signer
    try:
        signer = Signer.get_by_name_or_raise(signer_identifier)
        app.log.debug(f"Using '{signer.name}' signer with address {signer.address}")
        return signer
    except:
        pass
    # Case 2: signer_identifier is the address of a registered signer
    if signer_identifier.startswith("0x"):
        try:
            signer = Signer.get(Signer.address == signer_identifier)
            app.log.debug(
                f"Using '{signer.name}' signer with address {signer_identifier}"
            )
            return signer
        except:
            pass
    # Case 3: signer_identifier is the path to a keyfile
    try:
        with open(signer_identifier) as f:
            keyfile_dict = json.load(f)
        signer = get_signer_from_keyfile_dict(app, "temp", keyfile_dict)
        app.log.debug(f"Using keyfile signer with address {signer.address}")
        return signer
    except:
        pass
    # Case 4: signer_identifier is the private key of a signer
    try:
        signer = Signer.instantiate_encrypt("temp", signer_identifier, app.app_key)
        app.log.debug(f"Using private key signer with address {signer.address}")
        return signer
    except:
        pass

    raise SignerNotResolved(
        f"Could not find signer with name, address, private key or keyfile '{signer_identifier}'"
    )
