from web3core.helpers.validation import is_valid_block_identifier


def test_is_valid_block_identifier() -> None:
    """Return True if the given block identifier is valid, False otherwise"""
    # Predefined block identifiers
    assert is_valid_block_identifier("latest")
    assert is_valid_block_identifier("pending")
    assert is_valid_block_identifier("earliest")
    assert is_valid_block_identifier("safe")
    assert is_valid_block_identifier("finalized")
    # Integers
    assert is_valid_block_identifier(0)
    assert is_valid_block_identifier(16505875)
    assert is_valid_block_identifier("0x0")  # integer in hex form
    assert is_valid_block_identifier(
        "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcde"
    )
    # SHA256 hashes
    assert is_valid_block_identifier(
        "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
    )
    assert not is_valid_block_identifier(
        "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdefg"
    )
