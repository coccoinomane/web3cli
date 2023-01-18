<!-- https://shields.io/ --> 
<p align="right">
    <a href="https://www.alchemy.com/dapps/web3cli"><img src="https://img.shields.io/badge/featured%20on-alchemy-005493.svg"/></a>
    <a href="https://github.com/coccoinomane/web3cli/pulse" alt="Activity"><img src="https://img.shields.io/github/commit-activity/m/badges/shields?color=009051"/></a>
    <img src="https://img.shields.io/github/last-commit/coccoinomane/web3cli?color=009051"/>
</p>

Interact with blockchains and smart contracts using the command line: no coding needed!

# Features

- Interact with Ethereum and EVM-compatible chains via your terminal
- Bypass sluggish and potentially compromised frontends
- No configuration needed
- Label addresses, tokens and contracts for ease of use
- Use as many signers as you wish
- Concatenate commands to build powerful scripts
- Transfer tokens via their ticker
- Thoroughly tested using [*brownie*](https://github.com/eth-brownie/brownie/)'s testing framework

Soon:

- Swap with Uniswap, TraderJoe, PancakeSwap, etc
- Claim and reinvest yield from DeFi protocols
- Automatically buy when slippage is low enough
- Get notified on Telegram when a pair is liquid enough, or unbalanced
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

- Send native coins to any address and in any unit:
   ```
   w3 send unicef 1 ETH              # send 1 ETH, ask for confirmation
   w3 send unicef 1 ETH gwei         # send 1 gwei, ask for confirmation
   w3 send unicef 1 ETH gwei --force # send 1 gwei straight away
   ```

- Send tokens as well:
   ```
   w3 send unicef 1 USDC           # send 1 USDC
   w3 send unicef 1 USDC smallest  # send 1 decimal unit of USDC (10^-6)
   ```

- Fetch blocks from the blockchain, in easy-to-read JSON format:
   ```bash
   w3 block latest
   w3 block finalized
   w3 block 6094305
   w3 block 0x54c891931a2d1195e668e77391b14b9fa43a4d68bc2f60b14d90fef0c63e9c4c
   ```

- Fetch transactions & receipts from the blockchain:
   ```bash
   w3 tx get 0x3bbdcc2c7721521f7c767b7873ccb857f0816ac94e9f32c5601f4b15c87d1ef1
   w3 tx rc 0x3bbdcc2c7721521f7c767b7873ccb857f0816ac94e9f32c5601f4b15c87d1ef1
   ```

- Extract single fields from blocks or transactions, using `jq` (more details [in the Wiki](https://github.com/coccoinomane/web3cli/wiki/%E2%86%AA%EF%B8%8F-Output-processing)):
   ```bash
   w3 block latest | jq -r '.baseFeePerGas'
   ```

- Sign messages:
   ```bash
   w3 sign "Hello world!"
   ```

# Smart Contract support

`web3cli` comes with a database of common contracts, including ERC20 tokens and
Uniswap clones.

See the available contracts with `w3 db contract list`:

```
w3 db contract list              # contracts on Ethereum
w3 --chain bnb db contract list  # contracts on BNB chain
```

You can also add custom contracts with `w3 db contract add`:

```
w3 db contract add weth 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2 --type erc20
```

See available functions on a contract with `w3 abi functions`:

```
w3 abi functions weth
```

Call a function on the contract with `w3 call`:

```
w3 call weth totalSupply
```

Function arguments are parsed automatically, so you can call `balanceOf` with:

```
w3 call weth balanceOf 0xA59B29d7dbC9794d1e7f45123C48b2b8d0a34636
```

You can also do more complex stuff like:

```bash
# get the amount of USDT you get for 100 USDC
w3 call uniswap_router_v2 getAmountsOut 100e6 usdc,usdt | jq -r '.[1]' 
```

# Multichain support

`web3cli` comes with out-of-the-box support for [many chains](https://github.com/coccoinomane/web3cli/wiki/%E2%9B%93-Supported-chains), including Binance Chain, Avalanche and Polygon.

Pass the chain name as an optional argument:

```
w3 --chain bnb balance 0x8894e0a0c962cb723c1976a4421c95949be2d4e3  # bnb chain
w3 --chain avax balance 0x8894e0a0c962cb723c1976a4421c95949be2d4e3 # avax chain
```

or use one of the provided aliases:

```
w3bnb balance 0x8894e0a0c962cb723c1976a4421c95949be2d4e3  # bnb chain
w3avax balance 0x8894e0a0c962cb723c1976a4421c95949be2d4e3 # avax chain
```

If you are focussing on a specific chain, set it as the default:

```
w3 config set default_chain bnb
w3 balance 0x8894e0a0c962cb723c1976a4421c95949be2d4e3             # bnb chain
w3 --chain eth balance 0x8894e0a0c962cb723c1976a4421c95949be2d4e3 # eth chain
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

# Documentation

Check the [project's wiki on Github](https://github.com/coccoinomane/web3cli/wiki/). In particular:

- [🫡 List of commands](https://github.com/coccoinomane/web3cli/wiki/%F0%9F%AB%A1-List-of-commands)
- [⛓ Supported chains](https://github.com/coccoinomane/web3cli/wiki/%E2%9B%93-Supported-chains)
- [📝 Configuration](https://github.com/coccoinomane/web3cli/wiki/%F0%9F%93%9D-Configuration)
- [↪️ Output processing](https://github.com/coccoinomane/web3cli/wiki/%E2%86%AA%EF%B8%8F-Output-processing)


# Acknowledgements

Thank you very much to the communities behind [web3.py](https://github.com/ethereum/web3.py) and [`brownie`](https://github.com/eth-brownie/brownie): `web3cli` would not exist without your efforts!
