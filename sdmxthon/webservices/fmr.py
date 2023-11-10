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
                              max_retries: int = 10,
                              interval_time: float = 0.5):
    """
    Polls the FMR instance to get the validation status of an uploaded file

    :param status_url: The URL for checking the validation status
    :type status_url: str

    :param uid: the unique identifier we have to send to the request
    :type uid: str

    :param max_retries: The maximum number of retries for
                        checking validation status
    :type max_retries: int

    :param interval_time: The interval time between retries in seconds
    :type interval_time: float

    :return: The validation status if successful

    :exception: raise an exception if the validation status
                is not found in the response
    :exception: raise an exception if the current time exceeds the timeout


    """

    # Record the starting time for the entire validation process
    start_global = time()

    # Initialize variables for tracking time intervals
    start = time()
    interval_counter = 0

    # Get the current time
    current = time()

    # Calculate the total timeout based on max retries and interval time
    timeout = max_retries * interval_time

    while current - start_global < timeout:
        current = time()

        # Calculate the time interval from the start of the validation process
        interval_start = current - start_global
        interval = current - start

        # Skip the current iteration if the time interval is less than the
        # specified interval time
        if interval_start <= interval_time:
            continue

        # Perform a get request to the server to check the load status
        response_status = get(url=status_url,
                              params={'uid': uid})

        # Check if the 'Status' key is present in the response JSON
        if 'Status' not in response_status.json():
            raise Exception("Error: Status not found in response")

        # Check if the status is still in process
        if response_status.json()['Status'] in STATUS_IN_PROCESS:
            if interval > interval_time:
                interval_counter += 1
                start = time()

            # Check if the maximum number of retries is reached
            if interval_counter == max_retries:
                raise Exception(
                    f"Error: Max retries exceeded ({interval_counter})")

        # Return the handled status if the validation is still in process
        return handle_status(response_status)

    # Raise an exception if the total timeout is exceeded
    raise Exception(f"Timeout {timeout} exceeded on status request.")


def get_validation_status(status_url: str,
                          uid: str,
                          max_retries: int = 10,
                          interval_time: float = 0.5
                          ):
    """
    Gets the validation status of file uploaded using the FMR instance.

    :param status_url: The URL for checking the validation status
    :type status_url: str

    :param uid: The unique identifier of the uploaded file
    :type uid: str

    :param max_retries: The maximum number of retries for checking validation
                        status (default is 10)
    :type max_retries: int

    :param interval_time: The interval time between retries
                          in seconds (default is 0.5)
    :type interval_time: float

    :return: The validation status if successful

    """

    # Pause execution for the specified interval time
    sleep(interval_time)

    # Perform a GET request to the server to check the load status
    response_status = get(url=status_url,
                          params={'uid': uid})

    # Check if the status is still in process
    if response_status.json()['Status'] in STATUS_IN_PROCESS:
        # If in process, recursively call the function with retries
        return validation_status_request(status_url=status_url,
                                         uid=uid,
                                         max_retries=max_retries,
                                         interval_time=interval_time)
    # Return the handled status if the validation is complete
    return handle_status(response_status)


def validate_sdmx_csv_fmr(csv_text: str,
                          host: str = 'localhost',
                          port: int = 8080,
                          use_https: bool = False,
                          delimiter: str = 'comma',
                          max_retries: int = 10,
                          interval_time: float = 0.5
                          ):
    """
    Validates an SDMX CSV file by uploading it to an FMR instance
    and checking its validation status

    :param csv_text: The SDMX CSV text to be validated
    :type csv_text: str

    :param host: The FMR instance host (default is 'localhost')
    :type host: str

    :param port: The FMR instance port (default is 8080)
    :type port: int

    :param use_https: A boolean indicating whether to use HTTPS
                     (default is False)
    :type use_https: bool

    :param delimiter: The delimiter used in the CSV file
                      (options: 'comma', 'semicolon', 'tab', 'space')
    :type delimiter: str

    :param max_retries: The maximum number of retries for checking
                        validation status (default is 10)
    :type max_retries: int

    :param interval_time: The interval time between retries
                          in seconds (default is 0.5)
    :type interval_time: float

    :exception: Exception with error details if validation fails
    """

    # Constructing the base URL based on the provided parameters
    base_url = f'http{"s" if use_https else ""}://{host}:{port}'

    # Constructing the upload URL for the FMR instance
    upload_url = base_url + '/ws/public/data/load'

    # Checking if the provided delimiter is valid
    if delimiter not in ('comma', 'semicolon', 'tab', 'space'):
        raise ValueError('Delimiter must be comma, semicolon, tab or space')

    # Defining headers for the request
    headers = {'Data-Format': f'csv;delimiter={delimiter}'}

    # Perform a POST request to the server with the CSV data as an attachment
    response = post(upload_url,
                    files={'uploadFile': csv_text},
                    headers=headers)

    # Check the response from the server
    if not response.status_code == 200:
        raise Exception(response.text, response.status_code)

    # Constructing the URL for checking the validation status
    status_url = base_url + '/ws/public/data/loadStatus'

    # Getting the uid from the request response
    uid = response.json()['uid']

    # Return the validation status by calling a separate function
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

    :param sdmx_text: The SDMX text containing structures to be submitted
    :type sdmx_text: str

    :param host: FMR instance host (default is 'localhost')
    :type host: str

    :param port: FMR instance port (default is 8080)
    :type port: int

    :param user: User for Basic Auth (Admin or Agency privileges)
    :type user: str

    :param password: Password for Basic Auth
    :type password: str

    :param use_https: Flag to use or not https
    :type use_https: bool

    :exception: Exception with error details if upload fails
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
        # Perform a POST request to submit SDMX structures to FMR
        response = post(url, headers=headers, files={'uploadFile': sdmx_text})

    except ConnectionError:

        # Raise an exception if unable to connect to FMR
        raise ConnectionError(f'Unable to connect to FMR at {base_url}')

    # Parse the response using SDMX parser
    from sdmxthon.parsers.read import read_xml
    result = read_xml(response.text, validate=False)

    # Check if the result is an SDMXError
    if isinstance(result, SDMXError):
        # Raise an exception if there is an error uploading to FMR
        raise Exception('Error uploading to FMR', result.code, result.text)

    # Convert the result to JSON for display
    response_text = json.dumps(result, default=lambda x: x.__dict__(),
                               indent=4)

    # Print a success message
    print(f'Upload to FMR successful: {response_text}')
