# Flashcards CLI - WIP

[![Unit Tests](https://github.com/ebisu-flashcards/flashcards-cli/actions/workflows/tests.yml/badge.svg)](https://github.com/ebisu-flashcards/flashcards-cli/actions/workflows/tests.yml)  [![Coverage Status](https://coveralls.io/repos/github/ebisu-flashcards/flashcards-cli/badge.svg)](https://coveralls.io/github/ebisu-flashcards/flashcards-cli)  [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)   <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

Flashcards application CLI interface.

**NOTE**: This is a work-in-progress, not running application. 
Do not expect it to just download it and be able to run it if you're not
familiar with Python.

## Install

```bash
> python3 -m venv venv
> source venv/bin/activate
> pip install .
> flashcards
```

# Contribute

```bash
> python3 -m venv venv
> source venv/bin/activate
> pip install -e .
> pre-commit install

... do some changes ...

> pytest
```
The pre-commit hook runs Black and Flake8 with fairly standard setups. Do not send a PR if these checks, or the tests, are failing.
