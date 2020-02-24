# py_client: a python client for Braincube

## Description

The python package `py_client` provides a tool for datascientists to access their data on Braincube directly from python.

## Installation

Clone the [git repository]()

And install the dependencies with [poetry](https://python-poetry.org/):

```bash
cd py_client
poetry install
```

## Usage

```python
from py_client.client import Client

client = Client(config_file="pathto/config.json")
```

**Note:** If the parameter config_file is not provided, the client tests whether one of the two files `./config.json`  or `~/.braincube/config.json` exist.

## Configuration

In order to connect to the web service, the client needs a Oauth2 token saved in a configuration file. For simplicity it is recommended to use a helper [script](https://gitlab.ipleanware.com/braincube/core/python/braincube_token_getter) to get the token and to setup the configuration file as follows:

`config.json`

```json
{
    "client_id": "app id",
    "client_secret": "app key",
    "domain": "mybraincube.com",
    "verify": true,
    "oauth2_token": "token value"
}
```
The `token-getter` script saves the configuration in the `~/.braincube/config.json` file by default.
