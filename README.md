Interact with blockchains and smart contracts using the command line.

# Features

- Easily interact with EVM-compatible chains using your terminal
- Works with the most popular chains: Ethereum, Binance, Avalanche and more to come
- Save addresses you use often and access them with their tag
- Send transactions from multiple signers
- Concatenate commands to build powerful scripts
- [To be implemented]: Transfer tokens, using the token name (USDC, UNI, WETH, etc) instead of its address.
- [To be implemented]: DeFi support: sell Curve's rewards on Uniswap, setup a DCA plan on TraderJoe, etc.


# Install

```bash
pip3 install -U web3cli
```

# Simple examples

- Add chains before using them:
   ```
   w3 db chain add ethereum 1 ETH --tx-type 2 --rpc https://cloudflare-eth.com 
   w3 db chain add binance 56 BNB --rpc https://bsc-dataseed.binance.org/
   w3 db chain add avalanche 43114 --rpc https://api.avax.network/ext/bc/C/rpc
   ```
   ... or import them in one go:
   ```
   w3 db chain seed
   ```

- Get the ETH balance of the Ethereum foundation:
   ```
   w3 --chain ethereum balance 0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae
   ```
   ... or the BNB balance of a Binance hot wallet on BNB chain:
   ```
   w3 --chain binance balance 0x8894e0a0c962cb723c1976a4421c95949be2d4e3
   ```

- Tired of using the `--chain` argument? Set a default chain:
   ```
   w3 config set default_chain ethereum
   w3 balance 0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae
   ```

- Tired of pasting addresses around? Save them with an easy to remember name:
   ```
   w3 db address add ethereum-foundation 0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae
   w3 balance ethereum-foundation
   ```

- Want to send transactions? Add a signer:
   ```
   w3 db signer add my-wallet
   ```
   You will be asked for a private key, which will be saved on disk in encrypted form.


- Once you have a signer, you can send 1 ETH to the Ethereum foundation:
   ```bash
   w3 send ethereum-foundation 1 ETH
   ```
   or maybe it's better to send just 1 gwei:
   ```
   w3 send ethereum-foundation 1 ETH gwei
   ```

- Need to sign a message? This will print the whole signed message:
   ```bash
   w3 sign "Hello world!"
   ```

# Address book

`w3` can store tags just like you would do on etherscan.io or bscscan.com:

```bash
w3 db address add "Ethereum foundation" 0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae
w3 db address add "Binance hot wallet" 0x8894e0a0c962cb723c1976a4421c95949be2d4e3
```

You can use these tags instead of the actual addresses:

```bash
w3 balance "Ethereum foundation"
w3 --chain binance balance "Binance hot wallet"
```

To see the list of saved addresses, run:

```bash
w3 db address list
```

which will produce the following output:

```
| LABEL               | ADDRESS                                    |
|---------------------+--------------------------------------------|
| Binance hot wallet  | 0x8894e0a0c962cb723c1976a4421c95949be2d4e3 |
| Ethereum foundation | 0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae |
```

To see all the actions that can be done with addresses, run `w3 db address`.

# Sign & send

You can use `web3cli` to send transactions to the blockchain or to sign messages. To do so, you first need to define a signer:

```bash
w3 db signer add my_signer
```

You will be prompted to insert a private key, which will be encrypted and stored in the database. Feel free to do so with this test private key: `d94e4166f0b3c85ffebed3e0eaa7f7680ae296cf8a7229d637472b7452c8602c`.

You can also create a brand new wallet on the go, without the need to provide a key:

```
w3 db signer add my-wallet --create
```

### Examples

Once you have added a signer, you can use any of the commands that need a private key, as shown in the following examples.

**Sign a message**:

```bash
w3 sign "Hello world!"
```

Output:

```python
{'messageHash': HexBytes('0x8144a6fa26be252b86456491fbcd43c1de7e022241845ffea1c3df066f7cfede'),
 'r': 29064792366355323740950985371105895961858398238980883773193501881276705228481,
 's': 35017827091540952858431223849020104301448914783999277111090808754042212439431,
 'signature': HexBytes('0x404216ea232b5289610a7483de746fed3c94b6e6c2b8bf62ce5286850ff346c14d6b63445107a9d9e342720e88e82a3ff794dd6bd255931b552dedf2e243d5871c'),
 'v': 28}
```

**Send ETH, BNB, AVAX, etc**:

This is to be implemented yet, but the idea is to send funds with the following command:

```bash
w3 send <address> 0.001 ETH
```

where `address` is either an address from the address book, or a `0x..` hex string.

### Multiple signers

Add more signers with `w3 db signer add` and select which one to use with the `--signer` flag:

```bash
w3 --signer my_signer <command>
w3 -s my_signer <command> # short version
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
WEB3CLI_DEFAULT_CHAIN=avalanche w3 db chain get

output> avalanche
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
   pdm w3 config set default_chain avalanche
   ```
- Edit a setting value at the local level (`web3cli.yml`):
   ```bash
   pdm w3 config set default_chain avalanche --no-global
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

To run tests, first install [`ganache`](https://www.npmjs.com/package/ganache) on at least node 18, then run:

```bash
pdm test
```

# Acknowledgements

Thank you very much to the [web3.py](https://github.com/ethereum/web3.py) and [`brownie`](https://github.com/eth-brownie/brownie) teams: `web3` would not exist without your efforts!


# TODO
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
