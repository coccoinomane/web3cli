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
