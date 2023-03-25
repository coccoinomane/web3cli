<!-- https://shields.io/ --> 
<p align="right">
    <a href="https://www.alchemy.com/dapps/web3cli"><img src="https://img.shields.io/badge/featured%20on-alchemy-005493.svg"/></a>
    <a href="https://github.com/coccoinomane/web3cli/pulse" alt="Activity"><img src="https://img.shields.io/github/commit-activity/m/badges/shields?color=009051"/></a>
    <img src="https://img.shields.io/github/last-commit/coccoinomane/web3cli?color=009051"/>
</p>

Interact with blockchains and smart contracts using the command line: no coding needed!

# Table of contents

- [Features](#features)
- [Install](#install)
- [Simple examples](#simple-examples)
- [Advanced examples](#advanced-examples)
- [Smart Contract support](#smart-contract-support)
    + [Read from a smart contract](#read-from-a-smart-contract)
    + [Write to a smart contract](#write-to-a-smart-contract)
- [Multichain support](#multichain-support)
- [Add custom RPCs](#add-custom-rpcs)
- [Add custom chains](#add-custom-chains)
- [Address book](#address-book)
- [Wallet management](#wallet-management)
    + [Multiple signers](#multiple-signers)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [Acknowledgements](#acknowledgements)

# Features

- Interact with Ethereum and EVM-compatible chains via your terminal
- Bypass sluggish and potentially compromised frontends
- No configuration needed
- Label addresses, tokens and contracts for ease of use
- Swap with Uniswap, TraderJoe, PancakeSwap, etc
- Transfer tokens via their ticker
- Concatenate commands to build powerful scripts
- Use as many signers as you wish
- Thoroughly tested using [*brownie*](https://github.com/eth-brownie/brownie/)'s testing framework
- [Windows compatible](https://github.com/coccoinomane/web3cli/wiki/%F0%9F%AA%9F-Run-web3cli-on-Windows)

Soon:

- Set up scheduled buys and sells (DCA)
- Automatically buy when slippage is low enough
- Get notified on Telegram when a pair is liquid enough, or unbalanced
- Analyze on-chain data for tax or sleuthing purposes
- Claim and reinvest yield from DeFi protocols


# Install

Make sure you have at least Python 3.7 installed, then run:

```bash
pip3 install -U web3cli
```

Windows user? [Here's a tutorial for you](https://github.com/coccoinomane/web3cli/wiki/%F0%9F%AA%9F-Run-web3cli-on-Windows)!

# Simple examples

- Get the ETH balance of any address:
   ```
   w3 balance 0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae
   ```

- Save addresses with easy-to-rember tags:
   ```
   w3 address add unicef 0xa59b29d7dbc9794d1e7f45123c48b2b8d0a34636
   w3 address add unicef 0xa59b29d7dbc9794d1e7f45123c48b2b8d0a34636
   ```
   then use the tag in any command:
   ```
   w3 balance unicef
   ```

- Fetch blocks from the blockchain, in easy-to-read JSON format:
   ```bash
   w3 block latest
   w3 block finalized
   w3 block 6094305
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

# Advanced examples

- Send coins or tokens to any address:
   ```
   w3 send unicef 1 ETH      # send 1 ETH, ask for confirmation
   w3 send unicef 1 ETH gwei # send 1 gwei, ask for confirmation
   w3 send unicef 1 usdc     # send 1 USDC
   ```

- Swap tokens on a DEX:
   ```
   w3 swap uniswap_v2 1 usdc usdt     # swap 1 USDC for USDT on Uniswap
   w3avax swap traderjoe 1 usdc wavax # swap 1 USDC for WAVAX on TraderJoe
   ```

# Smart Contract support

`web3cli` comes preloaded with some popular smart contracts, including ERC20 tokens and Uniswap clones.

See the available contracts with `w3 contract list`:
See the available contracts with `w3 contract list`:

```
w3 contract list              # contracts on Ethereum
w3 contract list              # contracts on Ethereum
w3 --chain bnb contract list  # contracts on BNB chain
w3 --chain bnb contract list  # contracts on BNB chain
```

You can also add custom contracts with `w3 contract add`:
You can also add custom contracts with `w3 contract add`:

```
w3 contract add weth 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2 --type erc20
w3 contract add weth 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2 --type erc20
```

See available functions and events on a contract with `w3 abi functions` and `w3 abi events`:

```
w3 abi fns weth           # functions on WETH token
w3 abi evs uniswap_v2     # events on Uniswap V2
w3 abi fns --abi abi.json # functions of an arbitrary ABI
```

### Read from a smart contract

To read from a smart contract, use `w3 call`. For example, to get the total
supply of the WETH token, run:

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
w3 call uniswap_v2 getAmountsOut 100e6 usdc,usdt | jq -r '.[1]' 
```

### Write to a smart contract

To write to the blockchain, use `w3 transact`. For example, to transfer 1 ETH to 
address, run:

```
w3 transact weth transfer <address> 1e18
```

To swap 1 USDC for USDT on Uniswap, accepting no less than 0.9 USDT in return, run:

```
w3 transact usdc approve uniswap_v2_usdc_usdt 1e6
w3 transact uniswap_v2 swapExactTokensForTokens 1e6 0.9e6 usdc,usdt <receiver address> 9e9
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

Add custom RPCs to any existing chain with `w3 rpc add`:
Add custom RPCs to any existing chain with `w3 rpc add`:

```
w3 rpc add eth https://eth-mainnet.g.alchemy.com/v2/{YOUR API KEY}
w3 rpc add eth https://eth-mainnet.g.alchemy.com/v2/{YOUR API KEY}
```

List existing RPCs with `w3 rpc list`, and delete them with `w3 rpc delete`.
List existing RPCs with `w3 rpc list`, and delete them with `w3 rpc delete`.
List existing RPCs with `w3 rpc list`, and delete them with `w3 rpc delete`.

# Add custom chains

Add new chains with `w3 chain add`:

```
w3 chain add cronos 25 CRO --tx-type 2 --rpc https://evm.cronos.org
```

Use the custom chain with `--chain`:

```
w3 --chain cronos balance 0x7de9ab1e6a60ac7a70ce96d1d95a0dfcecf7bfb7
```

List existing chains with `w3 chain list`, and delete them with `w3 chain delete`.


# Address book

`w3` can store tags just like you would do on etherscan.io or bscscan.com:

```bash
w3 address add ethereum_foundation 0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae
w3 address add binance_hot_wallet 0x8894e0a0c962cb723c1976a4421c95949be2d4e3
```

You can use these tags instead of the actual addresses:

```bash
w3 balance ethereum_foundation
w3 --chain bnb balance binance_hot_wallet
```

To see the list of saved addresses, run `w3 address list`, to delete an address use `w3 address delete`.

# Wallet management

Commands such as `w3 send` and `w3 sign` require that you add a signer first:

```bash
w3 signer add my_signer
```

You will be prompted to insert a private key, which will be encrypted and stored in the database.

You can also create a brand new wallet on the go, without the need to provide a key:

```
w3 signer add my-wallet --create
```

### Multiple signers

Add more signers with `w3 signer add` and select which one to use with the `--signer` flag:

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
- [🪟 Run web3cli on Windows](https://github.com/coccoinomane/web3cli/wiki/%F0%9F%AA%9F-Run-web3cli-on-Windows)
- [↪️ Output processing](https://github.com/coccoinomane/web3cli/wiki/%E2%86%AA%EF%B8%8F-Output-processing)

# Contributing

All contributions are welcome! To start improving `web3cli`, please refer to our [__contribution guide__](./CONTRIBUTING.md).

# Acknowledgements

Thank you very much to the communities behind [web3.py](https://github.com/ethereum/web3.py) and [`brownie`](https://github.com/eth-brownie/brownie): `web3cli` would not exist without your efforts!
