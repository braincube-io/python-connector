# -*- coding: utf-8 -*-

"""This module manages the user identity and to perform the requests to the API web services."""

from typing import Any, Dict, Tuple

import requests

from braincube_connector import instances, tools, constants
from braincube_connector.bases import base

INSTANCE_KEY = "client"


class Client(base.Base):
    """A Client handles html requests."""

    def __init__(
        self, config_file: str = None, config_dict: Dict[str, str] = None, timeout: int = 60,
    ) -> None:
        """Initialize Client.

        Args:
            config_file: A path to a configuration file.
            config_dict: A configuration dictionary.
            timeout: Combined connect and read timeout for HTTP requests, in seconds.
        """
        if instances.get_instance(INSTANCE_KEY) is not None:
            raise Exception("A client has already been inialized.")
        else:
            self._config_dict = tools.check_config(config_dict=config_dict, config_file=config_file)
            self._sso_url = tools.get_sso_base_url(self._config_dict)
            self._braincube_base_url = tools.get_braincube_base_url(self._config_dict)
            self._verify = self._config_dict.get(constants.VERIFY_CERT, True)  # noqa: WPS425
            self._authentication = self._build_authentication(self._config_dict)
            available_braincube_infos = self._request_braincubes()
            self._braincube_infos = available_braincube_infos
            self._timeout = timeout
            self._headers = tools.generate_header(authentication=self._authentication)

    def __str__(self) -> str:
        """Produce informal representation of the Client object.

        Returns:
            An informal representation of the Client object.
        """
        return self._get_str({"domain": self._sso_url})

    def request_ws(
        self,
        path: str,
        headers: Dict[str, Any] = None,
        body_data: Any = None,
        rtype: str = "GET",
        api: bool = True,
        response_as_json: bool = True,
        braincube_name: str = "",
    ) -> Dict[str, Any]:
        """Make a request at a given path on the client's domain.

        Args:
            path: Path on the domain.
            headers: Headers of the request.
            body_data: Data to associate to the request.
            rtype: Request type (GET, POST).
            api: Requests the API server on the domain.
            response_as_json: parse a json output to a python dictionary.
            braincube_name: name of the Braincube you want to use to do this request.
                            Usefull when you have {braincube-name} in your base URL

        Returns:
            The request's json output or the full response.
        """
        base_url = self._sso_url
        if api:
            base_url = self._braincube_base_url

        url = tools.build_url(base_url, path, braincube_name)

        if not headers:
            headers = self._headers
        request_result = getattr(requests, rtype.lower())(
            url, headers=headers, data=body_data, verify=self._verify
        )
        request_result.raise_for_status()
        if response_as_json:
            return request_result.json()
        return request_result

    def get_braincube_infos(self) -> Dict[str, Any]:
        """Get the information about the braincubes available to the client.

        Returns:
            Return the dictionary of braincubes available to the client.
        """
        return self._braincube_infos

    def has_placeholder_in_braincube_url(self):
        """Indicates whether or not braincube_base_url contains a placeholder.

        The placeholder format is given by constants.BRAINCUBE_NAME_PLACEHOLDER.

        Returns:
            Returns a boolean indicating whether or not braincube_base_url contains a placeholder
        """
        return constants.BRAINCUBE_NAME_PLACEHOLDER in self._braincube_base_url

    def _request_braincubes(self) -> Dict[str, Any]:
        """Request the accessible braincube to the sso server.

        Returns:
            a list of available braincubes.
        """
        headers = self._authentication
        access_data = self.request_ws("sso-server/ws/user/me", headers=headers, api=False)
        return {
            bc["product"]["name"]: _extract_braincube_param(bc) for bc in access_data["accessList"]
        }

    def _build_authentication(self, config_dict: Dict[str, str]):
        """Automatically identify the authentication method and build the authentication header.

        Args:
            config_dict: a configuration dictionary.

        Returns:
            a dictionary containing an authentication header.
        """
        if constants.API_KEY in config_dict:
            return {constants.PAT_KEY: config_dict.get(constants.API_KEY)}
        elif constants.OAUTH2_KEY in config_dict:
            headers = {
                "Authorization": "Bearer {oauth2}".format(
                    oauth2=config_dict.get(constants.OAUTH2_KEY)
                )
            }
            access_data = self.request_ws(
                "sso-server/ws/oauth2/session", headers=headers, api=False
            )
            return {constants.SSO_TOKEN_KEY: access_data["token"]}
        raise KeyError(
            "The configuration file needs a {0}  or a {1} token.".format(
                constants.OAUTH2_KEY, constants.PAT_KEY
            )
        )


def _extract_braincube_param(metadata: Dict[str, Any]) -> "Tuple[str, str, Dict[str, str]]":
    """Extract the data needed by Braincube.__init__ from a json.

    Args:
        metadata: A braincube metadata.

    Returns:
        A braincube id, a braincube name, and a braincube metadata.
    """
    return (metadata["product"]["productId"], metadata["product"]["name"], metadata)


def get_instance(config_file: str = None, config_dict: Dict[str, str] = None) -> Client:
    """Static method to get the client.

    Args:
        config_file: A path to a configuration file.
        config_dict: A configuration dictionary.

    Returns:
        A client object.
    """
    if instances.get_instance(INSTANCE_KEY) is None:
        instances.add_instance(
            INSTANCE_KEY, Client(config_file=config_file, config_dict=config_dict)
        )
    return instances.get_instance(INSTANCE_KEY)


def request_ws(
    path: str,
    headers: Dict[str, Any] = None,
    body_data: Any = None,
    rtype: str = "GET",
    api: bool = True,
    response_as_json: bool = True,
    braincube_name: str = "",
) -> Dict[str, Any]:
    """Make a request at a given path on the client's domain.

    Args:
        path: Path on the domain.
        headers: Headers of the request.
        body_data: Data to associate to the request.
        rtype: Request type (GET, POST).
        api: Requests the API server on the domain.
        response_as_json: parse a json output to a python dictionary.
        braincube_name: name of the braincube on which is made the request,
                        useful if you use a placeholder in your config

    Returns:
        The request's json output or the full response.
    """
    cli = get_instance()
    return cli.request_ws(path, headers, body_data, rtype, api, response_as_json, braincube_name)
