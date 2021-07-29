# Flashcards CLI

Very basic command-line flashcards application, based on [flashcards-core](https://github.com/ebisu-flashcards/flashcards-core).

[![CodeQL](https://github.com/ebisu-flashcards/flashcards-cli/actions/workflows/codeql.yml/badge.svg)](https://github.com/ebisu-flashcards/flashcards-cli/actions/workflows/codeql.yml)   [![Unit Tests](https://github.com/ebisu-flashcards/flashcards-cli/actions/workflows/tests.yml/badge.svg)](https://github.com/ebisu-flashcards/flashcards-cli/actions/workflows/tests.yml)  [![Coverage Status](https://coveralls.io/repos/github/ebisu-flashcards/flashcards-cli/badge.svg)](https://coveralls.io/github/ebisu-flashcards/flashcards-cli)  [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)     [![Code on: GitHub](tps://img.shields.io/badge/Code on-GitHub-blueviolet)](https://github.com/ebisu-flashcards/flashcards-cli)   <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

-----------------------------------------

## Introduction

### Flashcards & SRS (Spaced Repetition Software)

Flashcards are a great way to memorize large amount of facts, for example a foreign language vocabulary, the world's flags, some trivia, bird songs, your new colleagues names, or any other long list of item pairs, be that text, images, or sounds.

What makes flashcards so powerful is the possibility to review them as soon as they start to get forgotten thanks to spaced repetition algorithms (SRS), which are designed to propose you study session of optimal lenght and timing, so that you can study the least while achieving the most. Some popular algorithms include Anki's SM2, SuperMemo's algorithms, Duolingo's algorithm, and other simpler ones. Flashcards supports also very trivial schedulers like "random order" or "last seen first", etc. If you know how to write Python, you can also write your own scheduler and send it to us to add it to the library! See the "Contribute" section below to understand how to do it.

SRS algorithms have a noticeable impact on the short term learning rate, but their greatest benefits are seen on the long term.

#### References

- Wikipedia links: [Spaced Repetition](https://en.wikipedia.org/wiki/Spaced_repetition) and [Forgetting Curve](https://www.semanticscholar.org/paper/Spaced-retrieval%3A-absolute-spacing-enhances-of-Karpicke-Bauernschmidt/23c01da059b9eb8be667930bddddc2033e719e31)
- A great summary of [pros and cons of SRS](https://www.sinosplice.com/life/archives/2021/02/07/srs-flashcards-pros-and-cons)
- Many [scientific articles on Google Scholar](https://scholar.google.com/scholar?hl=it&as_sdt=0%2C5&q=spaced+repetition&btnG=) Remember that, like anything in science, these are not absolute truths and articles with opposite findings also exist, like [this](https://www.semanticscholar.org/paper/Spaced-retrieval%3A-absolute-spacing-enhances-of-Karpicke-Bauernschmidt/23c01da059b9eb8be667930bddddc2033e719e31) and others.


-----------------------------

## Usage

Here is an example of how to create a deck, a couple of cards, and how to study them.

!(video example of a study session)[images/study-session.gif]

Note that for the time being, only a small subset of the features of `flashcards-core` is used: for example there is no way to add tags to any entity, to add context to question and answers, to use any SRS algorithm except for `random`, and no way to configure the algorithm parameters either. On the other end, this application is extremely small, so feel free to peek into the code and send a patch with the features you wish to add. Or at least open an issues for other volunteer to be aware of your interest.


## Install

Flashcards CLI can be installed from this repo as follows:

```bash
> python3 -m venv venv
> source venv/bin/activate
> pip install -e flashcards_cli @ git+https://github.com/ebisu-flashcards/flashcards-cli.git#egg=flashcards_cli
> flashcards
```

Or from PyPi (**not yet, soon!**):

```bash
> python3 -m venv venv
> source venv/bin/activate
> pip install flashcards-cli
```

### Versioning

This library is in development and might still experience radical changes from version to version. Do not assume backwards compatibility between minor versions until we hit version 1.0.

-----------------------------

# Contribute

Contributions are really welcome here! To get started, install an editable version of this package:

```bash
> git clone https://github.com/ebisu-flashcards/flashcards-cli.git
> cd flashcards-cli
> python3 -m venv venv
> source venv/bin/activate
> pip install -e .[dev]
> pre-commit install

... do some changes ...

> pytest
```

The pre-commit hook runs [Black](https://black.readthedocs.io/en/stable/) and 
[Flake8](https://flake8.pycqa.org/en/latest/) with fairly standard setups.

Do not send a PR if these checks, or the tests, are failing, but rather 
[ask for help](https://github.com/ebisu-flashcards/flashcards-cli/issues/new).

-------------------------------------

## Contacts

Soon...

## Contributors

![GitHub Contributors Image](https://contrib.rocks/image?repo=ebisu-flashcards/flashcards-cli)
