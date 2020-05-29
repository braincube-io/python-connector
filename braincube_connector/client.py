# -*- coding: utf-8 -*-

"""This module manages the user identity and to perform the requests to the API web services."""

from typing import Dict, Tuple, Any

from braincube_connector import tools
from braincube_connector.bases import base
from braincube_connector import instances

import requests

INSTANCE_KEY = "client"


class Client(base.Base):
    """A Client handles html requests."""

    def __init__(self, config_file: str = "", timeout: int = 60, verify_cert: bool = True) -> None:
        """Initialize Client.

        Args:
            config_file: Path of the configuration file.
            timeout: Combined connect and read timeout for HTTP requests, in seconds.
            verify_cert: Verify SSL certificate.
        """
        if instances.get_instance(INSTANCE_KEY) is not None:
            raise Exception("A client has already been inialized.")
        else:
            config_file = tools.check_config_file(config_file)
            config = tools.read_config(config_file)
            self._domain = tools.strip_domain(config["domain"])
            self._verify = verify_cert
            self._oauth2_token = config["oauth2_token"]
            token, available_braincube_infos = self._request_access()
            self._sso_token = token
            self._braincube_infos = available_braincube_infos
            self._timeout = timeout
            self._headers = tools.generate_header(sso_token=self._sso_token)

    def __str__(self) -> str:
        """Produce informal representation of the Client object.

        Returns:
            An informal representation of the Client object.
        """
        return self._get_str({"domain": self._domain})

    def request_ws(
        self,
        path: str,
        headers: Dict[str, Any] = None,
        body_data: Any = None,
        rtype: str = "GET",
        api: bool = True,
    ) -> Dict[str, Any]:
        """Make a request at a given path on the client's domain.

        Args:
            path: Path on the domain.
            headers: Headers of the request.
            body_data: Data to associate to the request.
            rtype: Request type (GET, POST).
            api: Requests the API server on the domain.

        Returns:
            The request's json output.
        """
        domain = self._domain
        if api:
            domain = "api.{dom}".format(dom=domain)
        url = tools.generate_url(domain, path)

        if not headers:
            headers = self._headers
        request_result = getattr(requests, rtype.lower())(
            url, headers=headers, data=body_data, verify=self._verify
        )
        request_result.raise_for_status()
        return request_result.json()

    def get_braincube_infos(self) -> Dict[str, Any]:
        """Get the information about the braincubes available to the client.

        Returns:
            Return the dictionary of braincubes available to the client.
        """
        return self._braincube_infos

    def _request_access(self) -> Tuple[str, Dict[str, Any]]:
        """Request a sso token access and a list of available braincubes.

        Returns:
            a sso token and a list of available braincubes.
        """
        headers = {"Authorization": "Bearer {oauth2}".format(oauth2=self._oauth2_token)}
        access_data = self.request_ws(
            "sso-server/rest/session/openWithToken", headers=headers, api=False
        )
        braincube_instance_infos = {
            bc["product"]["name"]: _extract_braincube_param(bc) for bc in access_data["accessList"]
        }
        return access_data["token"], braincube_instance_infos


def _extract_braincube_param(metadata: Dict[str, Any]) -> "Tuple[str, str, Dict[str, str]]":
    """Extract the data needed by Braincube.__init__ from a json.

    Args:
        metadata: A braincube metadata.

    Returns:
        A braincube id, a braincube name, and a braincube metadata.
    """
    return (metadata["product"]["productId"], metadata["product"]["name"], metadata)


def get_instance(config_file: str = "") -> Client:
    """Static method to get the client.

    Args:
        config_file: Path of the configuration file.

    Returns:
        A client object.
    """
    if instances.get_instance(INSTANCE_KEY) is None:
        instances.add_instance(INSTANCE_KEY, Client(config_file))
    return instances.get_instance(INSTANCE_KEY)


def request_ws(
    path: str,
    headers: Dict[str, Any] = None,
    body_data: Any = None,
    rtype: str = "GET",
    api: bool = True,
) -> Dict[str, Any]:
    """Make a request at a given path on the client's domain.

    Args:
        path: Path on the domain.
        headers: Headers of the request.
        body_data: Data to associate to the request.
        rtype: Request type (GET, POST).
        api: Requests the API server on the domain.

    Returns:
        The request's json output.
    """
    cli = get_instance()
    return cli.request_ws(path, headers, body_data, rtype, api)
