# TODO

### Top priority

- Test get_signer() switch function
- Refactor code to use get_signer() switch function
- Do we really need both app.chain_name and app.chain?
- Define function that parses chain and signer args, creates objects, extends app object.  Call this function in each command, rather than in args.py, and make it replace all the calls to chain_ready_or_raise and signer_ready_or_rise

### Commands 

- Tests: test add liq + swap
- Swap: refactor in web3core + test
- Token: test approve
- Get tokens balance
- w3 ls to see ETH balances of all signers
- Token: Approve and allowance commands
- Add support for uniswap v3 (https://docs.traderjoexyz.com/, https://snowtrace.io/address/0xe3ffc583dc176575eea7fd9df2a7c65f7e23f4c3#code)
- Command to swap tokens via Defi LLama token aggregator (https://twitter.com/DefiLlama/status/1609989799653285888)
- Command to import chains from https://chainid.network/chains.json
- Command to import tokens from ethereum-lists
- Command to import contracts from ethPM or etherscan ([like brownie](https://eth-brownie.readthedocs.io/en/latest/core-contracts.html#fetching-from-a-remote-source))
- Command: init wizard with `w3 init` (can use [`cement generate` approach](https://docs.builtoncement.com/getting-started/developer-tools#creating-your-first-project-built-on-cement-tm), see also [cement.shell](https://docs.builtoncement.com/utilities/shell))

### Docs

- README badges: web3.py, ape, PDM, cement

### Address book

- ENS support
- Resolve address should look also in signer names? Unique constraint on name?
- Resolve address should look also in contract names? Unique constraint on name?
- Address book: helper method to un-resolve address (from 0x to name, if it exists), useful for `w3 tx list`

### UX

- resolve_contract: return a contract from ethPM or etherscan
- Swap should support native coins too
- Transact: Warn before sending tx if gas price is too high
- Handle decimal output (e.g. w3 balance)
- Group contract and ABI functions: contract add, contract list, contract call,
  contract abi...
- Add trailing newline to json output
- Harmonize JSON/YAML CLI output
- Hide stack trace from errors unless --debug is passed
- Retry transactions until gas fee goes below x gwei
- Autocomplete commands
- Autocomplete addresses, signers and contracts
- Swap: retry until slippage is met
- Option to wait for receipt
- Dry-run: Print tx instead of sending it, via global argument/setting

### Misc

- Support multi-hop swaps
- Use pipx to install web3cli (https://pypa.github.io/pipx/)
- Should be able to run `config get` and `config set` without a database
- Make web3cli extensible
- Use memory DB for dev environment
- Test ABI controller
- Make contract.type a foreign key to ContractType?
- Launch local block explorer after tests
- Enforce lowercase for all model names (at the DB level?)
- Reset local chain between tests
- Fix setting boolean variables via env, e.g. `WEB3CLI_POPULATE_DB=0 w3 chain list` or `WEB3CLI_POPULATE_DB=false w3 chain list` should work as intended
- Define command shortcuts using argparse aliases, e.g. `w3 add-chain` instead of `w3 chain add`
- Tests: use london hardfork instead of istanbul?
- Config: non-string support in `config set`
- Record all transactions in Txs table
- Fix usage message (still refers to `web3cli`)
- Make alphabetical order case insensitive for `w3 contract list`
