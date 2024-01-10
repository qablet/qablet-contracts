# About this repo

This is a summary of this repo for those who want to borrow code for qablet applications, and for potential contributors.

## Structure

Lets take a look at the structure of this repo:

```text
├── Containerfile            # The file to build a container using buildah or docker
├── docs                     # Documentation site
│   └── index.md             # The index page for the docs site
├── .github                  # Github metadata for repository
│   ├── release_message.sh   # A script to generate a release message
│   └── workflows            # The CI pipeline for Github Actions
├── .gitignore               # A list of files to ignore when pushing to Github
├── HISTORY.md               # Auto generated list of changes to the project
├── LICENSE                  # The license for the project
├── Makefile                 # A collection of utilities to manage the project
├── MANIFEST.in              # A list of files to include in a package
├── mkdocs.yml               # Configuration for documentation site
├── qablet_contracts         # The main python package for the project
│   ├── base.py              # The base module for the project
│   ├── __init__.py          # This tells Python that this is a package
│   ├── __main__.py          # The entry point for the project
│   └── VERSION              # The version for the project is kept in a static file
├── README.md                # The main readme for the project
├── setup.py                 # The setup.py file for installing and packaging the project
├── requirements.txt         # An empty file to hold the requirements for the project
├── requirements-test.txt    # List of requirements for testing and devlopment
├── setup.py                 # The setup.py file for installing and packaging the project
└── tests                    # Unit tests for the project (add mote tests files here)
    ├── conftest.py          # Configuration, hooks and fixtures for pytest
    ├── __init__.py          # This tells Python that this is a test package
    └── test_base.py         # The base test case for the project
```


## The Makefile

All the utilities for the template and project are on the Makefile

```bash
❯ make
Usage: make <target>

Targets:
help:             ## Show the help.
install:          ## Install the project in dev mode.
fmt:              ## Format code using black & isort.
lint:             ## Run pep8, black, mypy linters.
test: lint        ## Run tests and generate coverage report.
watch:            ## Run tests on every change.
clean:            ## Clean unused files.
virtualenv:       ## Create a virtual environment.
release:          ## Create a new tag for release.
docs:             ## Build the documentation.
switch-to-poetry: ## Switch to poetry package manager.
```
