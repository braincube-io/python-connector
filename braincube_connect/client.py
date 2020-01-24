"""
client contains the functionalities to handle the user identity and to permorm the request
to the API web services.
"""
import os
import requests
import braincube_connect.errors as errors
import json

HOME = os.path.expanduser("~")
TOKEN_FILE = "OAuth2AccessToken"
DOMAIN = 'mybraincube.com'


def read_oauth_token(path):
    """Read the token from a file

    :param path: Path of the token file.
    :type path: string
    :return: A OAuth2 token.
    :rtype: string
    """
    token_path = os.path.join(path, TOKEN_FILE)
    try:
        with open(token_path) as ftoken:
            token = ftoken.readline()
    except FileNotFoundError:
        raise FileNotFoundError("Token file {} not found".format(token_path))
    return token


def handle_request_status(status_code):
    """Make sure the requests worked properly and return a custom error if the
    returned status is not a success.
    """
    if status_code >= 400:
        raise errors.RequestError(status_code)


class Client():
    """ Formulates requests to the braincube API webservices."""
    def __init__(self,
                 OAuth2Token="",
                 config_dir="",
                 timeout=60,
                 domain='mybraincube.com',
                 verify_cert=True):
        """
        :param OAuth2Token: OAuth2 key to connect throught the sso. Required.
        :type OAuth2Token: string
        :param timeout: Combined connect and read timeout for HTTP requests, in seconds.
        :type timeout: int
        :param verify_cert: Verify SSL certificate
        :type verify_cert: bool
        """
        if OAuth2Token and config_dir:
            raise ValueError(
                "Specify either a OAuth2Token or a configuration directory")

        if not OAuth2Token:
            if not config_dir:
                config_dir = os.path.join(HOME, ".braincube")
            try:
                OAuth2Token = read_oauth_token(config_dir)
            except FileNotFoundError:
                raise ValueError(
                    "OAuth2Token not found: provide a OAuth2Token parameter\
 or create a configuration file")
        self._domain = domain
        self._oauth2_token = OAuth2Token
        self._sso_token = self.request_sso_token(self._oauth2_token)
        self._timeout = timeout
        self._headers = {
            'Content-Type': 'application/json',
            'Accept': "application/json",
            'IPLSSOTOKEN': self._sso_token
        }
        self._verify = verify_cert

    def request_sso_token(self, oauth2):
        """Use a OAuth2 token to request a sso token to the sso server
        
        :param OAuth2: A OAuth2 token.
        :type OAuth2: string
        :return: A sso token.
        :rtype: string
        """
        headers = {'Authorization': 'Bearer {oauth2}'.format(oauth2=oauth2)}
        url = "https://{}/sso-server/rest/session/openWithToken".format(
            self._domain)
        result = requests.get(url, headers=headers)
        handle_request_status(result.status_code)
        return json.loads(result.text)["token"]
