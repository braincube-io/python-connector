# Python client to Braincube

## Description

The python package *braincube_connect* provides a tool for datascientist to access their data on Braincube directly from python.

## Installation

To use braincube_connect, you need an Oauth2 token that can be requested using the following [script](https://gitlab.ipleanware.com/braincube/core/python/braincube_token_getter).

Next Clone the [git repository]()

And install the dependencies with *pipenv*:

```bash
cd braincube_connect
pipenv install
```

## Usage

```bash
import braincube_connector as BC

client = BC.Client()
```