Pull requests are welcome ❤️ To start working on web3cli, please follow these steps.

# 1. Clone the repo

This is simple:

```bash
git clone https://github.com/coccoinomane/web3cli.git
```

# 2. Install dependencies

`web3cli` uses [PDM](https://github.com/pdm-project/pdm/) to manage dependencies. You can install it via script:

```bash
curl -sSL https://raw.githubusercontent.com/pdm-project/pdm/main/install-pdm.py | python3 -
```

Or, if you are on Windows, you may be better off using [pipx](https://pypa.github.io/pipx/):

```bash
pipx install pdm
```

Then, to install `web3cli` and its dependencies, just run:

```bash
pdm install
```

All packages, including `web3cli` will be installed in a newly created virtual environment in the `.venv` folder.

## Pre-commit

One last step before you start coding: please run `pre-commit install`.

This will instruct git to run some checks before every commit, to ensure that your code does not have obvious bugs. It is all automatic, don't worry!

**PS**: If the install command fails, try instead with `.venv/bin/pre-commit install` or, if you are on Windows, `.\.venv\Scripts\pre-commit install`.


# 3. Code!

`web3cli` consists of two main parts:

- The CLI, in the [`src/web3cli/`](./src/web3cli/) folder. Here goes everything related to CLI commands: controllers, hooks, CLI-aware helper functions, templates. The CLI makes ample use of the library.
- The library, in the [`src/web3core/`](src/web3core/) folder. The library contains the models and various general-purpose helpers. The library does not know that the CLI exists, and can therefore be used for other projects, e.g. a web interface.

For example, if you want to add a new command, you should create a new
controller in the [`src/web3cli/controllers/`](./src/web3cli/controllers/) folder, and add it
to the `handlers` list in [`src/web3cli/main.py`](./src/web3cli/main.py) file.

When you are done with your changes, please make sure to run `pdm test` to make
sure that your code does not break anything (see section 5).

# 4. Run your code

To run a command against your modifications, use `pdm w3` instead of just `w3`:

```bash
pdm w3 <command>
```

The rule is simple: `pdm w3` runs against your working `web3cli` folder, while `w3` runs against the system-installed `w3` (if any).

## Custom database

If you want to have a separate DB for your working `web3cli` folder, run:

```bash
pdm w3 config set db_file newdb --no-global
```

This will create a `newdb` file in the current folder, which will be used by `web3cli` instead of the global one.

# 5. Run tests

Plese run `pdm test` before every commit, to make sure your edits did not mess with the pre-existing code.

Some tests require a local blockchain, so make sure to install [ganache](https://www.npmjs.com/package/ganache) the first time you run `pdm test`!

To create a new test, feel free to copy and customize an existing one: all tests are in the [`tests`](./tests) folder.


