# -*- coding: utf-8 -*-

"""A set of constants available for the package."""

import os

DEFAULT_CONFIG = "config.json"
DEFAULT_HOME_CONFIG = os.path.join(os.path.expanduser("~"), ".braincube", DEFAULT_CONFIG)
NO_CONFIG_MSG = "The client needs a configuration file."
DEFAULT_PAGE_SIZE = 150
DEFAULT_PARSE_DATE = False
API_KEY = "api_key"
PAT_KEY = "X-api-key"
DOMAIN_KEY = "domain"
OAUTH2_KEY = "oauth2_token"
SSO_TOKEN_KEY = "IPLSSOTOKEN"  # noqa: S105
VERIFY_CERT = "verify"
