Interact with blockchains and smart contracts using the command line.

Built on [web3client](https://github.com/coccoinomane/web3client), the Swiss-army knife of the blockchain.

# Install

```bash
pip3 install -U web3cli
```

# Examples

- Get the ETH balance of the Ethereum foundation:
   ```bash
   web3 balance 0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae
   ```

- Get the BNB balance of the Binance hot wallet on BNB chain:
   ```bash
   web3 -n binance balance 0x8894e0a0c962cb723c1976a4421c95949be2d4e3
   ```

- List all supported networks (blockchains):
   ```bash
   web3 network list
   ```

# Address book

`web3` can store tags just like you would do on etherscan.io or bscscan.com:

```bash
web3 address add "Ethereum foundation" 0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae
web3 address add "Binance hot wallet" 0x8894e0a0c962cb723c1976a4421c95949be2d4e3
```

You can use these tags instead of the actual addresses:

```bash
web3 balance "Ethereum foundation"
web3 -n binance balance "Binance hot wallet"
```

You can see the list of saved addresses. Running

```bash
web3 address list
```

will produce the following output:

```
| LABEL               | ADDRESS                                    |
|---------------------+--------------------------------------------|
| Binance hot wallet  | 0x8894e0a0c962cb723c1976a4421c95949be2d4e3 |
| Ethereum foundation | 0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae |
```

To see all the actions that can be done with addresses, run `web3 address`.


# Settings

Settings are read from the configuration file `~/.web3cli/config/web3cli.yaml`, or from environment variables. (The symbol `~` refers to the home folder of your user.)
See the [example configuration file](./web3cli.example.yml) for a list of available settings.

### Environment variables

All settings can be overridden via environment variables.
For example, the settings `web3cli.default_network` can be overridden by setting the env variable `WEB3CLI_DEFAULT_NETWORK`:

```bash
WEB3CLI_DEFAULT_NETWORK=avalanche web3 network get

output> avalanche
```

### Folder-specific settings

To have settings that apply only to the current folder, create a `web3cli.yaml` file in that folder and execute `web3` from that folder.
Settings specified in `web3cli.yaml` will override those in your home folder.
Environment variables will still get the precedence.

### Edit configuration via the CLI

You can edit the configuration files using `web3 config`. For example:

- Show the value of a single setting:
   ```bash
   pdm web3 config get default_network
   ```
- Show all settings:
   ```bash
   pdm web3 config get
   ```
- Edit a setting value at the local leval (`web3cli.yml`):
   ```bash
   pdm web3 config set default_network avalanche
   ```
- Edit a setting value at the global level (`~/.web3cli/database/web3cli.sqlite`):
   ```bash
   pdm web3 config set default_network avalanche --global
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
   pdm web3 ...
   ```
4. To run tests:
   ```bash
   pdm test
   ```

# TODO
- Signer: Wallet authentication
- Signer: store key in DB as blob
- Windows: test on a Windows machine
- Key: test controller
- Config: test controller (requires web3cli_test.yml)
- Signer: Make app_key non-overridable (https://docs.builtoncement.com/core-foundation/configuration-settings#configuration-settings-vs.-meta-options)
- Signer: test controller
- Signer: resolve signers
- Signer: update + delete signer
- Signer: readme documentation
- Transfer ETH command
- Do not mess with DB unless needed by the command
- Do not mess with signers unless needed by the command
- Autocomplete
- Command structure
- Config: non-string support in `config set`
- Interactive vs non-interactive mode
- Allow to add custom networks?
- Use chains and tokens from ethereum-lists
- Model methods should return class instance, not BaseModel (python 3.11?)