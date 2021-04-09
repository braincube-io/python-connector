# Contributing

To contribute to the `braincube_connector` project, please make use of the following tools.

Contribute to :
- [The project](#Project-Contribution)
- [The development](#Development-Contribution)

## Project Contribution:

### Table of Contents
- [Code of conduct](#Code-of-conduct)
- [Opening Issues](#Opening-Issues)

### Code of conduct

All contributors are expecting to abide by our [Code of Conduct](./CODE_OF_CONDUCT.md).

### Opening Issues

- Search existing [issues](https://github.com/braincube-io/python-connector/issues) for your problem.
- [Update](#Update) your Braincube-Connector.
- Fill out the provided issue template.
- Describe your problem, not your solution.
- Explain how to reproduce the issue.

Finally, if you are up to date, supported, have collected information about the problem, and have the best reproduction instructions you can give, you are ready to [open an issue](https://github.com/braincube-io/python-connector/issues/new/choose).

### Update Version


## Development Contribution:

### Table of Contents
- [Install](#Install)
- [Style](#Style)
	- [Docstring style](#docstring-style)
	- [Type hint](#Type-hint)
- [Test](#Test)
	- [Coverage](#coverage)
- [Build documentation](#Build-documentation)
- [Continuous integration (CI)](#Continuous-integration-(CI))

### Install

The project uses [poetry](https://github.com/python-poetry/poetry) to manage the configuration and the package building.

To install `braincube_connector` run

```bash
poetry install
```

This will install all the project dependencies.  To run a command within the project virtual environment run

```text
$ poetry run <command>
# or
$ poetry shell
(.venv) $ <command>
```

Next it is recommended to install the git hooks so that several tests are run before each commit:

```
poetry run pre-commit install
```

**Note:** pre-commit behavior is configured within the `.pre-commit-config.yaml`

### Style

The code style is fixed with the [black](https://github.com/psf/black) library:

```bash
black braincube_connector
```

The overall quality is checked with the `flake8` and several extensions provided by the [`wemake-python-styleguide`](https://wemake-python-stylegui.de/en/latest/pages/usage/violations/index.html#external-plugins) package.  

```bash
flake8 braincube_connector
```

`flake8` has a few parameters set: `max-line-length = 100`, `inline-quotes = "`

A few violations could not be fixed and were ignored in the `.flake8` file:  

- [`I001` isort found an import in the wrong position](https://pypi.org/project/flake8-isort/)
  → Incompatible with `WPS318`, `WPS319`, and `black`.
- [`I002`: no configuration found (.isort.cfg or [isort] in configs)](https://github.com/gforcada/flake8-isort#error-codes)
- [`DAR401`: Missing exception(s) in Raises section: -r KeyError](https://github.com/terrencepreilly/darglint#error-codes)
- [`WPS326`: Found implicit string concatenation](https://wemake-python-stylegui.de/en/latest/pages/usage/violations/consistency.html#wemake_python_styleguide.violations.consistency.ImplicitStringConcatenationViolation)
  → Incompatible with `black`
- [`C812`, `815`: missing trailing comma](https://github.com/PyCQA/flake8-commas/#errors)
  → Incompatible with `black`
- [`D100`: Missing docstring in public module](http://www.pydocstyle.org/en/5.0.2/error_codes.html#grouping)
- [`RST`: Ignore rst format related warnings.](https://github.com/peterjc/flake8-rst-docstrings)
  → Incompatible with `**kwargs` gets confused with `**title` in rst format. Removing this warning has no effect since we are using markdown.

#### docstring style

The `braincube_connector` project uses the google docstring styles:

```python
def function(val: int) -> int:
	""" Description of the functions.

	Args:
		val: val parameter.

	Return:
		a multiplication of val.
	"""
    return 2*val
```

#### Type hint

Since python 3.5, there is the possibility to use the type hints on the function definitions. It should help detect an important number errors and enforce better practice so we decided to incorporate it in the project.

The consistence of the type hints is checked with  [mypy](http://mypy-lang.org/):

```
mypy braincube_connector/
```

### Test

The test suite rely on the to libraries [pytest](https://docs.pytest.org/en/latest/) and  [pytest_mock](https://github.com/pytest-dev/pytest-mock).

To run the tests, simply run the following command:

```bash
poetry run pytest tests/*
```

#### coverage

To test the test suite coverage, use the [coverage](https://github.com/nedbat/coveragepy/blob/coverage-5.0.3/doc/index.rst) package.

```bash
poetry run coverage run --source=braincube_connector -m pytest tests/*
```
Then generate the report:

```bash
poetry run coverage html # for an html report
poetry run coverage report # for a report in the shell
```

### Build documentation

The documentation is built with [mkdocs](https://www.mkdocs.org/) using the [material](https://squidfunk.github.io/mkdocs-material/) theme, modified to match braincube's commons.

To get the braincube modification on the style, run the following commands:

```bash
git clone https://gitlab.ipleanware.com/braincube/misc/gitlabci-commons.git
cp -r gitlabci-commons/braincube-pages/docs/* docs/
cp -r gitlabci-commons/braincube-pages/custom_theme .
```

**Note:**  `cp -r gitlabci-commons/braincube-pages/docs/* docs/ ` overwrites the `index.md` so it is best to leave unchanged.

Additional files can be added to the doc by creating a markdown file within the `docs/` directory and creating referencing to it under the *nav* section in the `mkdocs.yml` file.

*mkdocs* uses `mkdocstrings` to parse the docstrings with a module. This is done automatically when the symbole `::: modulename` is found in one of the markdown source files.

Finally compile the documentation with mkdocs:

```bash
bash docs/build_doc.sh build
```
The site is stored in the `site` directory.  

or to run a server:
```bash
bash docs/build_doc.sh serve
```



**Note:** The local building of the documentation is useful for test purposes but otherwise it is handled by the CI

### Continuous integration (CI)

At every push on the project the  CI executes a set of action defined in the `.github/workflows/ci.yml` script.

|!| A modifier

- Setup project environment (with `poetry`)
- Check the type hint consistency (with `mypy`)
- Check the style (with `flake8`)

- Run the test suite (with `pytest`)
- Evaluate the test coverage (with `coverage`)
