# TODO

### Top priority

- Document contract in README with examples
- Make web3cli extensible
- Test on Windows

### Extra commands 

- Get tokens balance
- Command to swap tokens via Defi LLama token aggregator (https://twitter.com/DefiLlama/status/1609989799653285888)
- Command to import chains from https://chainid.network/chains.json
- Command to import tokens from ethereum-lists
- Command to import contracts from ethPM or etherscan ([like brownie](https://eth-brownie.readthedocs.io/en/latest/core-contracts.html#fetching-from-a-remote-source))
- Command: init wizard with `w3 init` (can use [`cement generate` approach](https://docs.builtoncement.com/getting-started/developer-tools#creating-your-first-project-built-on-cement-tm), see also [cement.shell](https://docs.builtoncement.com/utilities/shell))

### Docs

- README badges: web3.py, brownie, PDM, cement

### Address book

- ENS support
- Resolve address should look also in signer names? Unique constraint on name?
- Resolve address should look also in contract names? Unique constraint on name?
- Address book: helper method to un-resolve address (from 0x to name, if it exists), useful for `w3 tx list`

### UX

- Retry transactions until gas fee goes below x gwei
- Autocomplete commands
- Autocomplete addresses, signers and contracts
- Swap: retry until slippage is met
- Option to wait for receipt
- Dry-run: Print tx instead of sending it, via global argument/setting

### Misc

- Use memory db for dev environment
- Make contract.type a foreign key to ContractType?
- Launch local block explorer after tests
- Enforce lowercase for all model names (at the db level?)
- Reset local chain between tests
- Add trailing newline to json output
- Fix setting boolean variables via env, e.g. `WEB3CLI_POPULATE_DB=0 w3 db chain list` or `WEB3CLI_POPULATE_DB=false w3 db chain list` should work as intended
- Define command shortcuts using argparse aliases, e.g. `w3 add-chain` instead of `w3 db chain add`
- Tests: use london hardfork instead of istanbul?
- Config: non-string support in `config set`
- Record all transactions in Txs table
- Fix usage message (still refers to `web3cli`)
- Make alphabetical order case insensitive for `w3 db contract list`
