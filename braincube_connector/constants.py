# -*- coding: utf-8 -*-

"""A set of constants available for the package."""

import os

DEFAULT_CONFIG = "config.json"
DEFAULT_VARIABLE_NAME_KEY = "standard"
DEFAULT_VARIABLE_BCID_KEY = "bcId"
DEFAULT_BCID_KEY = "name"
DEFAULT_NAME_KEY = "bcId"
DEFAULT_HOME_CONFIG = os.path.join(os.path.expanduser("~"), ".braincube", DEFAULT_CONFIG)
DEFAULT_PROTOCOL = "https"
DEFAULT_API_SUBDOMAIN = "api"
NO_CONFIG_MSG = "The client needs a configuration file."
DEFAULT_PAGE_SIZE = 150
DEFAULT_PARSE_DATE = False
API_KEY = "api_key"
PAT_KEY = "X-api-key"
DOMAIN_KEY = "domain"
SSO_BASE_URL_KEY = "sso_base_url"
BRAINCUBE_BASE_URL_KEY = "braincube_base_url"
OAUTH2_KEY = "oauth2_token"
SSO_TOKEN_KEY = "IPLSSOTOKEN"  # noqa: S105
VERIFY_CERT = "verify"
BRAINCUBE_NAME_PLACEHOLDER = "{braincube-name}"
EMPTY_STRING = ""
