import json
import os.path
from time import time
from pathlib import Path
import random
import pandas as pd
import requests
from requests import RequestException
from sdmxthon.api.api import read_sdmx
from sdmxthon.model.dataset import Dataset


# Function to check the availability of a host by sending a GET request
def check_host_availability(host_url):
    response = requests.get(host_url)
    if not response.status_code == 200:  # Check if the response status code is 200 (OK)
        raise Exception(f"Could not find an FMR instance at {host_url}")


def main():
    # Define file paths
    base_path = Path("sdmxthon/testSuite/readingValidation/data")
    data_path = base_path / "data_sample"
    metadata_path = base_path / "metadata"
    metadata_filename = "metadata.xml"
    data_filename = "dataflow.xml"

    # Read the data from an SDMX file and store it in a DataFrame
    message = read_sdmx(os.path.join(data_path, data_filename), validate=True)
    dataset = message.payload['BIS:WEBSTATS_DER_DATAFLOW(1.0)']
    df: pd.DataFrame = dataset.data

    for k, v in dataset.attached_attributes.items():
        df[k] = v

    # Read metadata from another SDMX file and assign the structure and data to the data set
    message1 = read_sdmx(os.path.join(metadata_path, metadata_filename))
    dataset.structure = message1.payload['DataStructures']['BIS:BIS_DER(1.0)']
    dataset.data = df

    # Assign the url of the desired host
    host_url = "http://localhost:8080"

    # Check if the host is available with the function previously created
    if not check_host_availability(host_url):
        raise Exception("Host is Unavailable or it is not a")
    # Insert two columns at the beginning of the data set
    df.insert(0, 'STRUCTURE', 'datastructure')
    df.insert(1, 'STRUCTURE_ID', 'BIS:BIS_DER(1.0)')

    # Convert the dataset into a csv file
    csv_text = df.to_csv(index=False, header=True)

    # Define the endpoint URL for the POST request
    end_point_url = "http://localhost:8080/ws/public/data/load"

    # Perform the POST request to the server with the CSV data as an attachment
    response = requests.post(end_point_url, files={'uploadFile': csv_text})

    # Check the response from the server
    if response.status_code == 200:
        print("Solicitud exitosa. Los datos se enviaron correctamente.")
    else:
        print("Error en la solicitud HTTP. Código de estado:", response.status_code)

    # Get the uid from the request response
    uid = response.json()['uid']

    # Define the endpoint URL for the request
    url_load_status = "http://localhost:8080/ws/public/data/loadStatus"

    # Assign the time interval we want to wait before starting the process
    interval_time = random.uniform(0, 0.5)

    # Assign the number of intervals we are going to wait before giving up the process
    number_of_intervals_before_error = 10
    # Assign the time of those intervals
    time_interval_request = 0.5

    start_global = time()
    start = time()
    interval_counter = 0

    # The headers we want to add in the request
    headers = {'Data-Format': 'csv;delimiter=comma'}

    # The list of load status in which we are going to wait those time intervals
    load_status_in_process = ['Initialising', 'Analysing', 'Validating', 'Consolidating']

    # The list of load status which means is an error
    load_status_error = ['IncorrectDSD', 'InvalidRef', 'MissingDSD', 'Error']
    while time() >= 0:
        end = time()
        interval_start = end - start_global  # The time interval from now to the beginning
        interval = end - start
        if interval_start <= interval_time:
            continue
        # Perform the get request to the server to check the load status
        response_status = requests.get(url_load_status, params={'uid': uid}, headers=headers)
        if 'Status' in response_status.json():
            if response_status.json()['Status'] == 'Complete':
                if response_status.json()['Datasets'][0]['Errors']:
                    return response_status.json()['Datasets'][0]['ValidationReport']
                else:
                    return []
            elif response_status.json()['Status'] in load_status_in_process:
                if interval > time_interval_request:
                    interval_counter += 1
                    start = time()
                if interval_counter == number_of_intervals_before_error:
                    raise Exception(f"Error: Max retries exceeded ({interval_counter})")
            elif response_status.json()['Status'] in load_status_error:
                raise Exception(response_status.json()['Error'])


if __name__ == "__main__":
    main()
