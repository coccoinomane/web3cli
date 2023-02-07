Pull requests are welcome ❤️

To start working on web3cli, please follow these steps:

1. Install and configure [PDM](https://github.com/pdm-project/pdm/); it's a packag manager like Poetry, but better. You can install it via script:
   ```bash
   curl -sSL https://raw.githubusercontent.com/pdm-project/pdm/main/install-pdm.py | python3 -
   ```
   If you are on Windows, you may be better of using [pipx](https://pypa.github.io/pipx/):
   ```bash
   pipx install pdm
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

To run tests:

1. Install [ganache](https://www.npmjs.com/package/ganache), using `node >= 18`.
2. Run `pdm test`.
