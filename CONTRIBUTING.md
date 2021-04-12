# Contributing

To contribute to the `braincube_connector` project, please make use of the following tools.

Contribute to :
- [The project](#Project-Contribution)
- [The development](#Development-Contribution)

## Project Contribution:

### Table of Contents
- [Code of conduct](#Code-of-conduct)
- [Opening Issues](#Opening-Issues)
- [Update Version](#update-version)

### Code of conduct

All contributors are expecting to abide by our [Code of Conduct](./CODE_OF_CONDUCT.md).

### Opening Issues

- Search existing [issues](https://github.com/braincube-io/python-connector/issues) for your problem.
- [Update](#update-version) your Braincube-Connector.
- Fill out the provided issue template.
- Describe your problem, not your solution.
- Explain how to reproduce the issue.

Finally, if you are up to date, supported, have collected information about the problem, and have the best reproduction instructions you can give, you are ready to [open an issue](https://github.com/braincube-io/python-connector/issues/new/choose).

### Update Version

Update braincube_connector with pip:

```bash
pip install braincube_connector -U
```

## Development Contribution:

### Table of Contents
- [Install](#Install)
- [Style](#Style)
	- [Docstring style](#docstring-style)
	- [Type hint](#Type-hint)
- [Test](#Test)
- [Continuous integration (CI)](#continuous-integration-ci)

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

### Continuous integration (CI)

At every push on the project the  CI executes a set of action defined in the `.github/workflows/ci.yml` script.

- Setup project environment (with `poetry`)
- Check the type hint consistency (with `mypy`)
- Fix the code style (with `black`)
- Check the style (with `flake8`)
- Run the test suite (with `pytest`)
