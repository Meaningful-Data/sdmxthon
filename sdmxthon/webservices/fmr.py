import json
from time import time, sleep

from requests import post, get
from requests.exceptions import ConnectionError

from sdmxthon.model.error import SDMXError
from sdmxthon.model.utils import (generate_basic_auth_token,
                                  METADATA_ENDPOINT, STATUS_ERRORS,
                                  STATUS_IN_PROCESS)


def check_host_availability(host_url):
    """
    Checks if the host is available
    :param host_url: URL to check
    :return: True if the host is available, False otherwise
    :exception: Exception if the host is not available
    """
    response = get(host_url)
    # Check if the response status code is 200 (OK)
    if not response.status_code == 200:
        raise Exception(f"Could not find an FMR instance at {host_url}")
    return True


def handle_status(response_status):
    if response_status.json()['Status'] == 'Complete':
        if response_status.json()['Datasets'][0]['Errors']:
            return response_status.json()['Datasets'][0]['ValidationReport']
        else:
            return []
    if response_status.json()['Status'] in STATUS_ERRORS:
        raise Exception(response_status.json()['Error'])


def validation_status_request(status_url: str,
                              uid: str,
                              headers: dict,
                              max_retries: int = 10,
                              interval_time: float = 0.5):
    start_global = time()
    start = time()
    interval_counter = 0
    current = time()
    timeout = max_retries * interval_time
    while current - start_global < timeout:
        current = time()
        # The time interval from now to the beginning
        interval_start = current - start_global
        interval = current - start
        if interval_start <= interval_time:
            continue
        # Perform the get request to the server to check the load status
        response_status = get(url=status_url,
                              params={'uid': uid},
                              headers=headers)
        if 'Status' not in response_status.json():
            raise Exception("Error: Status not found in response")
        if response_status.json()['Status'] in STATUS_IN_PROCESS:
            if interval > interval_time:
                interval_counter += 1
                start = time()
            if interval_counter == max_retries:
                raise Exception(
                    f"Error: Max retries exceeded ({interval_counter})")
        return handle_status(response_status)

    raise Exception(f"Timeout {timeout} exceeded on status request.")


def get_validation_status(status_url: str,
                          uid: str,
                          max_retries: int = 10,
                          interval_time: float = 0.5
                          ):
    # The list of load status in which we are going
    # to wait those time intervals

    sleep(interval_time)

    response_status = get(url=status_url,
                          params={'uid': uid})

    if response_status.json()['Status'] in STATUS_IN_PROCESS:
        return validation_status_request(status_url=status_url,
                                         uid=uid,
                                         max_retries=max_retries,
                                         interval_time=interval_time)
    return handle_status(response_status)


def validate_sdmx_csv_fmr(csv_text: str,
                          host: str = 'localhost',
                          port: int = 8080,
                          use_https: bool = False,
                          delimiter: str = 'comma',
                          max_retries: int = 10,
                          interval_time: float = 0.5
                          ):
    base_url = f'http{"s" if use_https else ""}://{host}:{port}'
    upload_url = base_url + '/ws/public/data/load'
    if delimiter not in ('comma', 'semicolon', 'tab', 'space'):
        raise ValueError('Delimiter must be comma, semicolon, tab or space')

    # The headers we want to add in the request
    headers = {'Data-Format': f'csv;delimiter={delimiter}'}
    # Perform the POST request to the server with the CSV data as an attachment
    response = post(upload_url,
                    files={'uploadFile': csv_text},
                    headers=headers)

    # Check the response from the server
    if not response.status_code == 200:
        raise Exception(response.text, response.status_code)
    status_url = base_url + '/ws/public/data/loadStatus'
    # Get the uid from the request response
    uid = response.json()['uid']
    return get_validation_status(status_url=status_url,
                                 uid=uid,
                                 max_retries=max_retries,
                                 interval_time=interval_time)


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
    from sdmxthon.parsers.read import read_xml
    result = read_xml(response.text, validate=False)
    if isinstance(result, SDMXError):
        raise Exception('Error uploading to FMR', result.code, result.text)

    response_text = json.dumps(result, default=lambda x: x.__dict__(),
                               indent=4)
    print(f'Upload to FMR successful: {response_text}')
