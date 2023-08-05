### Top priority

- Make web3cli extensible

### To do

- Tests: subscribe controller
- Tests: compound-v2 controller
- Tests: test get_signer() switch function
- Ignore case in contract names, including tokens

### Backlog

- Subscribe: immediate exit on ctrl-c
- Fix usage message (still refers to `web3cli`)
- Config: non-string support via env, e.g. `WEB3CLI_POPULATE_DB=0 w3 chain list`
- Config: non-string support in `config set`, e.g. `w3 config set populate_db false`
- Tests: approve helper
- Command to import/resolve tokens from ethereum-lists
- Tests: compound-v2 commands
- Subscribe: cache tx for logs subscription (and possibly use it in callback)
- Tests: test add liq + swap
- Swap: refactor in web3core + tests
- w3 ls to see ETH balances of all signers
- Swap: Support for Uniswap v3 (https://docs.traderjoexyz.com/, https://snowtrace.io/address/0xe3ffc583dc176575eea7fd9df2a7c65f7e23f4c3#code)
- Swap: Defi LLama token aggregator command
- Command to import/resolve chains from https://chainid.network/chains.json
- Command to import/resolve contracts from ethPM or etherscan ([like brownie](https://eth-brownie.readthedocs.io/en/latest/core-contracts.html#fetching-from-a-remote-source))
- Address book: ENS support
- Swap should support native coins too
- Autocomplete commands
- Autocomplete addresses, signers and contracts
- Swap: retry until slippage is met
- Should be able to run `config get` and `config set` without a database
- Record all transactions in history table
