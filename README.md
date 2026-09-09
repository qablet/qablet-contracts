# qablet_contracts

[![CI](https://github.com/qablet/qablet-contracts/actions/workflows/main.yml/badge.svg)](https://github.com/qablet/qablet-contracts/actions/workflows/main.yml)


**Qablet Contracts documentation is at [qablet.github.io/qablet-contracts](https://qablet.github.io/qablet-contracts/).**

A Qablet timetable defines a financial product using a sequence of payments, choices and conditions. A valuation model implemented with a Qablet parser can value any contract, as long as the contract can be described using a Qablet Timetable. 

This repository contains code to create qablet timetables.
It does not contain models that price qablet timetables. Such models will be available in other independent projects.  


## Install it from PyPI

```bash
pip install qablet_contracts
```

## Development

**Prerequisites:** Python 3.12

### Create a virtual environment

**Linux / macOS**

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e .[test]
```

**Windows**

```
py -3.12 -m venv .venv
.venv\Scripts\activate
pip install -e .[test]
```

### Run tests

```bash
pytest tests/
```

On Linux/macOS you can also use the Makefile, which runs linters before tests and generates a coverage report:

```bash
make test
```
