# About this repo

This is a summary of this repo for those who want to borrow code for qablet applications, and for potential contributors.

## Structure

Lets take a look at the structure of this template:

```text
├── Containerfile            # The file to build a container using buildah or docker
├── CONTRIBUTING.md          # Onboarding instructions for new contributors
├── docs                     # Documentation site (add more .md files here)
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
├── qablet_contracts             # The main python package for the project
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

## FAQ

Frequent asked questions.


### Why the template doesn't have a `pyproject.toml` file ?

It is possible to run `pip install https://github.com/name/repo/tarball/main` and
have pip to download the package direcly from Git repo.

For that to work you need to have a `setup.py` file, and `pyproject.toml` is not
supported for that kind of installation.

I think it is easier for example you want to install specific branch or tag you can
do `pip install https://github.com/name/repo/tarball/{TAG|REVISON|COMMIT}`

People automating CI for your project will be grateful for having a setup.py file


### Why `VERSION` is kept in a static plain text file?

I used to have my version inside my main module in a `__version__` variable, then
I had to do some tricks to read that version variable inside the setuptools 
`setup.py` file because that would be available only after the installation.

I decided to keep the version in a static file because it is easier to read from
wherever I want without the need to install the package.

e.g: `cat qablet_contracts/VERSION` will get the project version without harming
with module imports or anything else, it is useful for CI, logs and debugging.

### Why to include `tests`, `history` and `Containerfile` as part of the release?

The `MANIFEST.in` file is used to include the files in the release, once the 
project is released to PyPI all the files listed on MANIFEST.in will be included
even if the files are static or not related to Python.

Some build systems such as RPM, DEB, AUR for some Linux distributions, and also
internal repackaging systems tends to run the tests before the packaging is performed.

The Containerfile can be useful to provide a safer execution environment for 
the project when running on a testing environment.

I added those files to make it easier for packaging in different formats.

### Why conftest includes a go_to_tmpdir fixture?

When your project deals with file system operations, it is a good idea to use
a fixture to create a temporary directory and then remove it after the test.

Before executing each test pytest will create a temporary directory and will
change the working directory to that path and run the test.

So the test can create temporary artifacts isolated from other tests.

After the execution Pytest will remove the temporary directory.


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
init:             ## Initialize the project based on an application template.
```
