# -*- coding: utf-8 -*-

"""client manages the user identity and to perform the requests to the API web services."""

import os
from typing import Dict, Any

from py_client import tools

import requests

DEFAULT_CONFIG = "config.json"
DEFAULT_HOME_CONFIG = os.path.join(os.path.expanduser("~"), ".braincube", DEFAULT_CONFIG)
NO_CONFIG_MSG = "The client needs a configuration file."


class Client(object):
    """Handles html request errors."""

    def __init__(self, config_file: str = "", timeout: int = 60, verify_cert: bool = True) -> None:
        """Initialize Client.

        Args:
            config_file: Path of the configuration file.
            timeout: Combined connect and read timeout for HTTP requests, in seconds.
            verify_cert: Verify SSL certificate.
        """
        if config_file == "":
            if os.path.exists(DEFAULT_CONFIG):
                config_file = DEFAULT_CONFIG
            elif os.path.exists(DEFAULT_HOME_CONFIG):
                config_file = DEFAULT_HOME_CONFIG
            else:
                raise FileNotFoundError(NO_CONFIG_MSG)

        config = tools.read_config(config_file)

        self._domain = tools.strip_domain(config["domain"])
        self._oauth2_token = config["oauth2_token"]
        self._sso_token = self._request_sso_token()
        self._timeout = timeout
        self._headers = tools.generate_header(sso_token=self._sso_token)
        self._verify = verify_cert

    def request_ws(
        self,
        path: str,
        headers: Dict[str, Any] = None,
        body_data: Dict[str, Any] = None,
        rtype: str = "GET",
    ) -> Dict[str, Any]:
        """Make a request at a given path on the client's domain.

        Args:
            path: Path on the domain.
            headers: Headers of the request.
            body_data: Data to associate to the request.
            rtype: Request type (GET, POST).

        Returns:
            The request's json output.
        """
        url = self._generate_url(path)
        if not headers:
            headers = self._headers
        request_result = getattr(requests, rtype.lower())(
            url, headers=headers, data=body_data, verify=self._verify
        )
        request_result.raise_for_status()
        return request_result.json()

    def _generate_url(self, path: str) -> str:
        """Appends a path to the client domain to generate a valid url.

        Args:
            path: Path on the domain.

        Returns:
            A complete url on the configured domain.
        """
        path = tools.strip_path(path)
        return "https://{domain}/{path}".format(domain=self._domain, path=path)

    def _request_sso_token(self) -> str:
        """Use a OAuth2 token to request a sso token to the sso server.

        Returns:
            a sso token.
        """
        headers = {"Authorization": "Bearer {oauth2}".format(oauth2=self._oauth2_token)}
        return self.request_ws("sso-server/rest/session/openWithToken", headers=headers)["token"]
