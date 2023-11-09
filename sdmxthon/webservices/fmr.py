import json

from requests import post
from requests.exceptions import ConnectionError

from sdmxthon.model.error import SDMXError
from sdmxthon.model.utils import generate_basic_auth_token, METADATA_ENDPOINT
from sdmxthon.parsers.read import read_xml


def submit_structures_to_fmr(sdmx_text: str,
                             host: str = 'localhost',
                             port: int = 8080,
                             user: str = 'root',
                             password: str = 'password',
                             use_https: bool = False):
    """
    Uploads the metadata to the FMR
    :param sdmx_text: SDMX metadata as string
    :param host: FMR instance host
    :param port: FMR instance port
    :param user: User for Basic Auth (Admin or Agency privileges)
    :param password: Password for Basic Auth
    :param use_https: Flag to use or not https
    :return:
    """
    # Argument handling
    if port < 1 or port > 65535:
        raise ValueError('Port must be between 1 and 65535')
    # Header definition for request
    headers = {'Authorization': generate_basic_auth_token(user, password)}
    # Generation of base URL
    base_url = f'http{"s" if use_https else ""}://{host}:{port}'
    # Endpoint on FMR
    url = base_url + METADATA_ENDPOINT
    try:
        response = post(url, headers=headers, files={'uploadFile': sdmx_text})
    except ConnectionError:
        raise ConnectionError(f'Unable to connect to FMR at {base_url}')
    result = read_xml(response.text, validate=False)
    if isinstance(result, SDMXError):
        raise Exception(f'Error uploading to FMR', result.code, result.text)

    response_text = json.dumps(result, default=lambda x: x.__dict__(), indent=4)
    print(f'Upload to FMR successful: {response_text}')
