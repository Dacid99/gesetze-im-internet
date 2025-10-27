# Development Quickstart

## Setup

Your global python version should be at least *3.9*.

If necessary you can install it via [the deadsnakes ppa](https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa).

Make sure to also install the **python-dev** version!

Then to install the python dependencies start a new virtual environment and activate it:

[Poetry](https://python-poetry.org/docs/) is used to manage the python dependencies of this project.

```bash
pip install poetry
```

You can then add the tab completions for it by:

```bash
poetry completions bash >> ~/.bash_completion
```

Then install all the dependencies to a virtual environment:

```bash
poetry install --with dev --no-root
```

Finally you can activate the venv with

```bash
eval $(poetry env activate)
```

## Testing

The projects tests are in the test/ directory. You can run them from the project root with

```bash
pytest tests
```

## Validation and Linting

You can use the tools in tools/ to lint and check your changes.

The code is formatted using ruffs formatter and imports are sorted with ruffs isort implementation.

There are preconfigured githooks in tools/githooks that format, check and lint the code before every commit.
Set them for your local repository via

```bash
git config core.hooksPath tools/githooks/
```

## Workspace Recommendations

### VSCodium / VSCode

#### Settings

- Trim final newlines

```json
    "files.trimFinalNewlines": true,
```

- Trim trailing whitespace

```json
    "files.trimTrailingWhitespace": true,
```

- Insert final newline

```json
    "files.insertFinalNewline": true,
```

#### Extensions

- everything for python
- python test, with config

```json
    "python.testing.cwd": "/path/to/repo/test/"
```

- ruff, with config

```json
    "ruff.configuration": "tools/ruff.toml")
```

- python poetry
