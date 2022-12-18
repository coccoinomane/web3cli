Interact with blockchains and smart contracts using the command line: no coding needed!

# Features

- Interact with Ethereum-compatible chains via your terminal
- Bypass sluggish and potentially compromised frontends
- No configuration needed
- Label addresses, tokens and contracts for ease of use
- Use as many signers as you wish
- Concatenate commands to build powerful scripts
- Thoroughly tested using [*brownie*](https://github.com/eth-brownie/brownie/)'s testing framework

Soon:

- Transfer tokens via their ticker
- Swap with Uniswap, TraderJoe, PancakeSwap, etc
- Claim and reinvest yield from DeFi protocols
- Set up scheduled buys and sells (DCA)
- Analys on-chain data for tax or sleuthing purposes


# Install

```bash
pip3 install -U web3cli
```

# Simple examples

- Get the ETH balance of any address:
   ```
   w3 balance 0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae
   ```

- Save addresses with easy-to-rember tags:
   ```
   w3 db address add unicef 0xa59b29d7dbc9794d1e7f45123c48b2b8d0a34636
   ```
   then use the tag in any command:
   ```
   w3 balance unicef
   ```

- Send native coins to any address:
   ```
   w3 send unicef 1 ETH
   ```
   and in any unit:
   ```
   w3 send unicef 1 ETH gwei
   ```

- Sign messages:
   ```bash
   w3 sign "Hello world!"
   ```

# Multichain support

`web3cli` comes with out-of-the-box support for Ethereum, Binance Chain and Avalanche. Select which chain to use with the `--chain` option:

```
w3 --chain bnb balance 0x8894e0a0c962cb723c1976a4421c95949be2d4e3
w3 --chain avax balance 0x8894e0a0c962cb723c1976a4421c95949be2d4e3
```

Set a default chain to avoid typing `--chain` for every command:

```
w3 config set default_chain bnb
w3 balance 0x8894e0a0c962cb723c1976a4421c95949be2d4e3 # bnb chain
w3 --chain eth balance 0x8894e0a0c962cb723c1976a4421c95949be2d4e3 # eth chain
```

Alternatively, use the aliases `web3eth`, `web3bnb` and `web3avax`:

```
w3eth balance 0x8894e0a0c962cb723c1976a4421c95949be2d4e3 # eth chain
w3bnb balance 0x8894e0a0c962cb723c1976a4421c95949be2d4e3 # bnb chain
w3avax balance 0x8894e0a0c962cb723c1976a4421c95949be2d4e3 # avalanche chain
```

# Add custom RPCs

Add custom RPCs to any existing chain with `w3 db rpc add`:

```
w3 db rpc add eth https://eth-mainnet.g.alchemy.com/v2/{YOUR API KEY}
```

List existing RPCs with `w3 db rpc list`, and delete them with `w3 db rpc delete`.

# Add custom chains

Add new chains with `w3 db chain add`:

```
w3 db chain add cronos 25 CRO --tx-type 2 --rpc https://evm.cronos.org
```

Use the custom chain with `--chain`:

```
w3 --chain cronos balance 0x7de9ab1e6a60ac7a70ce96d1d95a0dfcecf7bfb7
```

List existing chains with `w3 db chain list`, and delete them with `w3 db chain delete`.


# Address book

`w3` can store tags just like you would do on etherscan.io or bscscan.com:

```bash
w3 db address add ethereum_foundation 0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae
w3 db address add binance_hot_wallet 0x8894e0a0c962cb723c1976a4421c95949be2d4e3
```

You can use these tags instead of the actual addresses:

```bash
w3 balance ethereum_foundation
w3 --chain bnb balance binance_hot_wallet
```

To see the list of saved addresses, run `w3 db address list`, to delete an address use `w3 db address delete`.

# Wallet management

Commands such as `w3 send` and `w3 sign` require that you add a signer first:

```bash
w3 db signer add my_signer
```

You will be prompted to insert a private key, which will be encrypted and stored in the database.

You can also create a brand new wallet on the go, without the need to provide a key:

```
w3 db signer add my-wallet --create
```

### Multiple signers

Add more signers with `w3 db signer add` and select which one to use with the `--signer` flag:

```bash
w3 --signer my_signer <command>
```

If you plan to use the same signer for a while, make it the **default signer** with the command:

```
w3 config set default_signer my_signer
```

# Settings

Settings are read from the configuration file `~/.web3cli/config/web3cli.yaml`, or from environment variables. (The symbol `~` refers to the home folder of your user.)
See the [example configuration file](./web3cli.example.yml) for a list of available settings.

### Environment variables

All settings can be overridden via environment variables.
For example, the settings `web3cli.default_chain` can be overridden by setting the env variable `WEB3CLI_DEFAULT_CHAIN`:

```bash
WEB3CLI_DEFAULT_CHAIN=avax w3 db chain get

output> avax
```

### Folder-specific settings

To have settings that apply only to the current folder, create a `web3cli.yaml` file in that folder and execute `w3` from that folder.

Settings specified in `web3cli.yaml` will override those in your home folder. Environment variables will still get the precedence.

### Edit configuration via the CLI

You can edit the configuration files using `w3 config`. For example:

- Show the value of a single setting:
   ```bash
   pdm w3 config get default_chain
   ```
- Show all settings:
   ```bash
   pdm w3 config get
   ```
- Edit a setting value at the global level (`~/.web3cli/database/web3cli.sqlite`):
   ```bash
   pdm w3 config set default_chain avax
   ```
- Edit a setting value at the local level (`web3cli.yml`):
   ```bash
   pdm w3 config set default_chain avax --no-global
   ```

# Contribute ❤️

Pull requests are welcome!

1. Install and configure [PDM](https://github.com/pdm-project/pdm/):
   ```bash
   curl -sSL https://raw.githubusercontent.com/pdm-project/pdm/main/install-pdm.py | python3 -
   ```
2. Install dependencies: 
   ```bash
   pdm install
   ```
3. To run the CLI against your changes: 
   ```bash
   pdm w3 <command>
   ```


### Tests

To run tests, first install [`ganache`](https://www.npmjs.com/package/ganache) on at least `node` 18, then run:

```bash
pdm test
```

# Acknowledgements

Thank you very much to the [web3.py](https://github.com/ethereum/web3.py) and [`brownie`](https://github.com/eth-brownie/brownie) teams: `web3` would not exist without your efforts!


# TODO
- ENS support
- Contract: Controller tests
- Fix setting boolean variables via env, e.g. `WEB3CLI_POPULATE_DB=0 w3 db chain list` or `WEB3CLI_POPULATE_DB=false w3 db chain list` should work as intended
- Define command shortcuts using argparse aliases, e.g. `w3 add-chain` instead of `w3 db chain add`
- Use different db file for dev environment
- README: Explain json output + trick `| python3 -mjson.tool`
- Implement `w3 block`
- Implement `w3 tx fetch`
- Move tests/seeder to core (in models?)
- Tests: use london hardfork instead of istanbul?
- Send command: option to wait for receipt
- Retry transactions until gas fee goes below x gwei
- README badges: web3.py, brownie, PDM, cement
- Resolve address should look also in signature names (make signer & address names unique?)
- Address book: helper method to un-resolve address (from 0x to name, if it exists), useful for `w3 tx list`
- Rpc: check that chain's chain_id in DB corresponds to chain_id of RPC
- Chain: Preload chains from https://chainid.network/chains.json
- Command: `w3 init` to import chain + add signer
- Windows: test on a Windows machine
- Do not mess with DB unless needed by the command
- Do not mess with signers unless needed by the command
- Autocomplete commands
- Tests: should we change evm_version in ganache for non-ethereum chains? (see CLI_FLAGS brownie/network/rpc/ganache.py)
- Autocomplete addresses and signers
- Config: non-string support in `config set`
- Gas: Upper limit on basefee via global argument/setting
- Dry-run: Print tx instead of sending it, via global argument/setting
- Use chains and tokens from other sources (e.g. ethereum-lists)
- ethPM registry / etherscan to pull smart contract interfaces? E.g. https://eth-brownie.readthedocs.io/en/latest/core-contracts.html#fetching-from-a-remote-source
- Record transaction in Txs table
- Fix usage message (still refers to `web3cli`)
