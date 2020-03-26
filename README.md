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

## Client

A client can be inialized manually from a custom configuration file.

```python
from py_client import client

client.get_instance(config_file="pathto/config.json")
```

**Note:** If the client is not initialized manually, the package creates a client instance from one of these two files `./config.json`  or `~/.braincube/config.json` (in this priority order) if they exist.


### Braincube

To obtain a list of all the available `Braincubes` entities with a client:
```python
from py_client import braincube

braincube.get_braincube_list()
```

Or to select a specific `Braincube` entity from its name:
```python
bc = braincube.get_braincube("demo")
```

### MemoryBase

The list of all the memory bases available within a `Braincube` is obtained with

```python
mb_list = bc.get_memory_base_list()
```

**Note: ** The number of memory bases in a braincube can be numerous,  hence `get_memory_base_list` allows paginated requests `bc.get_memory_base_list(page=0)`

To select a unique memory base, go with its bcId:

```python
mb_list = bc.get_memory_base(20)
```


### VariableDescriptions

The variable description are linked to a memory base.

```python
var_desc = mb.get_variable("2000034")
```

For multiple variable descriptions:

```python
mb.get_variable_list(page=0)
```

**Note:** Similarly to memory bases, providing no argument to `get_variable_list` retrieves all variable descriptions available in the memory base.

The type of variable is obtained with the function `get_type`

```python
var_desc.get_type()
```


### JobDescription

The job desciption are also linked to a memory base.

```python
job_desc = mb.get_job("573")
```

For multiple job descriptions:

```python
mb.get_job_list(page=0)
```
**Note:** Similarly to `get_variable_list`, providing no argument to `get_job_list` retrieves all job descriptions available in the memory base.

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
