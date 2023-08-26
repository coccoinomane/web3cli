<!-- https://shields.io/ --> 
<p align="center">
    <a href="https://github.com/coccoinomane/web3cli/pulse" alt="Activity"><img src="https://img.shields.io/github/commit-activity/m/badges/shields?color=009051"/></a>
    <img src="https://img.shields.io/github/last-commit/coccoinomane/web3cli?color=009051"/>
</p>
<p align="center">
        <a href="https://www.alchemy.com/dapps/web3cli"><img style="width:150px;height:33px" src="https://static.alchemyapi.io/images/marketing/badge.png"/></a>
</p>

Interact with blockchains and smart contracts using the command line: no coding needed!

# Table of contents

- [Features](#features)
- [Install](#install)
- [Simple examples](#simple-examples)
- [Advanced examples](#advanced-examples)
- [Smart Contract support](#smart-contract-support)
    + [Read from a smart contract](#read-from-a-smart-contract)
    + [Send a transaction to a smart contract](#send-a-transaction-to-a-smart-contract)
- [Multi-chain support](#multi-chain-support)
- [Use custom RPC](#use-custom-rpc)
- [Add custom chains](#add-custom-chains)
- [Address book](#address-book)
- [Wallet management](#wallet-management)
    + [Default signer](#default-signer)
    + [Create new private keys](#create-new-private-keys)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [Acknowledgements](#acknowledgements)

# Features

- Interact with Ethereum and EVM-compatible chains via your terminal
- Bypass sluggish and potentially compromised frontends
- No configuration needed
- Label addresses, tokens and contracts for ease of use
- Swap with Uniswap, TraderJoe, PancakeSwap, etc
- Support for the Compound V2 lending protocol and its forks (e.g. Eralend)
- Transfer tokens via their ticker
- Set Telegram alerts based on pending transactions, new blocks and contract events
- Replay transactions just with the tx hash
- Concatenate commands to build powerful scripts
- Import signers via private key or keyfile
- Thoroughly tested using the [Ape Framework](https://github.com/ApeWorX/ape)'s testing framework
- [Windows compatible](https://github.com/coccoinomane/web3cli/wiki/%F0%9F%AA%9F-Run-web3cli-on-Windows)

Soon:

- React to pending transactions, new blocks and contract events
- Set up scheduled buys and sells (DCA)
- Automatically buy when slippage is low enough
- Get notified on Telegram when a pair is liquid enough, or unbalanced
- Analyze on-chain data for tax or sleuthing purposes
- Claim and reinvest yield from DeFi protocols


# Install

Make sure you have at least Python 3.9 installed, then run:

```bash
pip3 install -U web3cli
```

The same command will also upgrade web3cli to the latest version.

*Windows user?* [Here's a tutorial for you](https://github.com/coccoinomane/web3cli/wiki/%F0%9F%AA%9F-Run-web3cli-on-Windows)!

## Install via pipx

Fan of isolated environments?  Install web3cli via [pipx](https://pypa.github.io/pipx/):

```bash
pipx install web3cli
```

To upgrade web3cli, run `pipx upgrade web3cli`.

# Simple examples

- Get the ETH balance of any address:
   ```
   w3 balance 0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae
   ```

- Save addresses with easy-to-rember tags:
   ```
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
   w3 sign 'Hello world!'
   ```

- Get Keccak256 hashes starting from a text or a hex-string:
   ```bash
   w3 keccak-text 'Hello world!'
   w3 keccak-hex 'b495b1154ef1b2'
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

- Stream blocks, transactions and contract events as they happen in realtime:
   ```
   w3 subscribe blocks   # stream blocks as they are mined
   w3 subscribe pending  # stream pending transactions
   w3 subscribe events   # stream all contract events
   ```
  Streaming requires a websocket connection: specify one with the `--rpc wss://...` flag.

- Set a Telegram alert for when a specific event is emitted:
   ```bash
   # Get notified on Telegram when USDC is transferred
   transfer=0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef
   w3 subscribe events --telegram --contracts usdc --topics $transfer
   # Send a post notification when USDC is transferred
   w3 subscribe events --post https://www.example.com/ --contracts usdc --topics $transfer
   ```
  Telegram alerts require setting up a Telegram bot, please find instructions [in the Wiki](https://github.com/coccoinomane/web3cli/wiki/%F0%9F%93%AD-Telegram-alerts).

- Replay a given transactions on the blockchain:
   ```bash
   tx=`w3 send unicef 1 USDC --force` # send 1 USDC to Unicef
   w3 replay $tx                      # re-send 1 USDC to Unicef
   ```

# Smart Contract support

web3cli comes preloaded with some popular smart contracts, including ERC20 tokens and Uniswap clones.

See the available contracts with `w3 contract list`:

```
w3 contract list               # contracts on Ethereum
w3 contract list --chain bnb   # contracts on BNB chain
w3 contract list --type erc20  # tokens on Ethereum
```

You can also add custom contracts with `w3 contract add`:

```
w3 contract add weth 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2 --type erc20
w3 contract add sushi 0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F --type uniswap_v2
```

To add or list new tokens, you can use the `w3 token` shorthand:

```
w3 token add weth 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2
w3 token list
w3 token delete weth
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

### Send a transaction to a smart contract

To write to the blockchain, use `w3 transact`. For example, to transfer 1 ETH to 
address, run:

```
w3 transact weth transfer <address> 1e18
```

To swap 1 USDC for USDT on Uniswap, accepting no less than 0.9 USDT in return, run:

```
w3 transact usdc approve uniswap_v2 1e6
w3 transact uniswap_v2 swapExactTokensForTokens 1e6 0.9e6 usdc,usdt <receiver address> 9e9
```

# Multi-chain support

web3cli comes with out-of-the-box support for many chains.  To see the list of available chains, [visit the Wiki](https://github.com/coccoinomane/web3cli/wiki/%E2%9B%93-Supported-chains) or run the command `w3 chain list`.

Pass the chain name using the flag `--chain` or the shorthand `-c`:

```
w3 balance 0x8894e0a0c962cb723c1976a4421c95949be2d4e3 --chain bnb  # bnb chain
w3 balance 0x8894e0a0c962cb723c1976a4421c95949be2d4e3 --chain avax # avax chain
```

You can also use one of the provided aliases, like `w3bnb`, `w3avax`, or `w3arb`:

```
w3bnb balance 0x8894e0a0c962cb723c1976a4421c95949be2d4e3  # bnb chain
w3avax balance 0x8894e0a0c962cb723c1976a4421c95949be2d4e3 # avax chain
```

If you are focussing on a specific chain, set it as the default:

```
w3 config set default_chain bnb
w3 balance 0x8894e0a0c962cb723c1976a4421c95949be2d4e3             # bnb chain
w3 balance 0x8894e0a0c962cb723c1976a4421c95949be2d4e3 --chain eth # eth chain
```

# Use custom RPC

By default, web3cli will connect to the blockchain using a pre-configured public node.  You can see the list of such nodes with the command `w3 rpc list`.

To use a custom mode, please specify the `--rpc` flag.  For example, to use Ankr's node to Ethereum:

```bash
w3 block latest --rpc https://rpc.ankr.com/eth
```

Using a custom node is most useful in the following situations:

1. You want to use a node from a node provider, e.g. Infura:
   ```bash
   w3 block --rpc https://eth-mainnet.g.alchemy.com/v2/{YOUR-API-KEY}
   ```
2. You want to use a private node:
   ```bash
   w3 block --rpc http://127.0.0.1:8545
   w3 block --rpc ws://127.0.0.1:8546
   ```
3. You want to use a testnet chain:
   ```bash
   w3eth block --rpc https://rpc.ankr.com/eth_goerli
   w3bnb block --rpc https://data-seed-prebsc-1-s1.binance.org:8545/
   ```


# Add custom chains

Add new chains with `w3 chain add`:

```
w3 chain add cronos 25 CRO --tx-type 2 --rpc https://evm.cronos.org
```

Use the custom chain with `--chain`:

```
w3 balance 0x7de9ab1e6a60ac7a70ce96d1d95a0dfcecf7bfb7 --chain cronos
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
w3 balance binance_hot_wallet --chain bnb
```

To see the list of saved addresses, run `w3 address list`, to delete an address use `w3 address delete`.

# Wallet management

Commands such as `w3 send` and `w3 swap` require that you specify who is going to sign the transactions.  You can specify the signer with the `--signer` or `-s` flag:

```bash
w3 <command> --signer my-signer
```

Here, `my_signer` can be any of these things:

- The name or the address of a signer that you previously registered with `w3 signer add my_signer`.  Signers created in this way are encrypted with the app key and stored in the database.  At any time, you can see the list of registered users by running `w3 signer list`.
- The path to a file that you previously created with `w3 keyfile create`.  A keyfile is a simple JSON file that contains your private key in password-encrypted form.  Feel free to use keyfiles generated by other tools, like geth, parity, brownie, etc.
- The actual private key of the signer that you want to use.  This is unsafe, use it at your own risk!

Please note that when the `--signer` flag is not provided, and there is only one registered signer, then this will be used.


### Default signer

If you plan to use the same signer for a while, make it the **default signer** with the command:

```bash
w3 config set default_signer my_signer
```

In this way, you will not have to specify the `--signer` flag anymore.


### Create new private keys

You can also create a brand new wallet on the go, without the need to provide a key, by using the `--create` flag:

```bash
w3 signer add my_wallet --create
```

The resulting private key will be printed to screen.

# Documentation

Check the [project's wiki on Github](https://github.com/coccoinomane/web3cli/wiki/). In particular:

- [🫡 List of commands](https://github.com/coccoinomane/web3cli/wiki/%F0%9F%AB%A1-List-of-commands)
- [⛓ All supported chains](https://github.com/coccoinomane/web3cli/wiki/%E2%9B%93-Supported-chains)
- [📝 Configuration](https://github.com/coccoinomane/web3cli/wiki/%F0%9F%93%9D-Configuration)
- [🪟 Run web3cli on Windows](https://github.com/coccoinomane/web3cli/wiki/%F0%9F%AA%9F-Run-web3cli-on-Windows)
- [↪️ Output processing](https://github.com/coccoinomane/web3cli/wiki/%E2%86%AA%EF%B8%8F-Output-processing)

# Contributing

All contributions are welcome! To start improving web3cli, please refer to our [__contribution guide__](./CONTRIBUTING.md).

# Acknowledgements

Thank you very much to the communities behind [web3.py](https://github.com/ethereum/web3.py) and the [Ape Framework](https://github.com/ApeWorX/ape): web3cli would not exist without your efforts!
