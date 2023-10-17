import requests
from sdmxthon.webservices import query_builder
from sdmxthon.webservices.query_builder import SdmxWs1
from sdmxthon.api.api import read_sdmx
import csv
import random


# Initialize the SDMX web service
def initialize_sdmx():
    ws_implementation = SdmxWs1()
    qb = query_builder.QueryBuilder(ws_implementation)
    return qb


# Make an HTTP request to the specified URL and log the results
def make_request(url, agency_name, query, csv_data):
    try:
        response = requests.get(url)
        status_code = response.status_code

        if status_code == 200:
            print(f"XML data fetched successfully for '{query}' in '{agency_name}': {status_code}")
        else:
            print(f"Error fetching data for '{query}' in '{agency_name}': {status_code}")

        agency_info = [agency_name, entry_points[agency_name], query, status_code]
        csv_data.append(agency_info)

    except Exception as e:
        error_message = str(e)
        print(f"Error fetching data for '{query}' in '{agency_name}': {error_message}")
        agency_info = [agency_name, entry_points[agency_name], query, error_message]
        csv_data.append(agency_info)


# Convert the dataflow format for a given dataflow
def convert_dataflow_format(dataflow):
    parts = dataflow.split(":")
    if len(parts) == 2:
        agency, rest = parts
        version = rest.replace("(", ",").replace(")", "")  # Replace parentheses with commas
        return f"{agency},{version}"
    else:
        return dataflow


# Fetch data flows for a specific agency
def fetch_data_flows(agency_name, csv_data):
    qb = initialize_sdmx()
    data_flows_query = qb.get_data_flows()
    data_flows_url = entry_points[agency_name] + data_flows_query
    print(f"URL for 'dataflows' in '{agency_name}': {data_flows_url}")
    make_request(data_flows_url, agency_name, data_flows_query, csv_data)


# Fetch data for a specific agency
def fetch_data(agency_name, csv_data, dataflow):
    qb = initialize_sdmx()
    dataflow_query = qb.get_data(flow=convert_dataflow_format(dataflow))
    data_url = entry_points[agency_name] + dataflow_query
    print(f"URL for 'data' in '{agency_name}': {data_url}")
    make_request(data_url, agency_name, dataflow_query, csv_data)


# Fetch Data Structure Definitions (DSDs) for a specific agency
def fetch_dsds(agency_name, csv_data):
    qb = initialize_sdmx()
    dsds_query = qb.get_dsds()
    dsds_url = entry_points[agency_name] + dsds_query
    print(f"URL for 'dsds' in '{agency_name}': {dsds_url}")
    make_request(dsds_url, agency_name, dsds_query, csv_data)


# Fetch constraints for a specific agency
def fetch_constraints(agency_name, csv_data, dataflow):
    qb = initialize_sdmx()
    constraints_query = qb.get_constraints(flow=convert_dataflow_format(dataflow))
    constraints_url = entry_points[agency_name] + constraints_query
    print(f"URL for 'constraints' in '{agency_name}': {constraints_url}")
    make_request(constraints_url, agency_name, constraints_query, csv_data)


if __name__ == '__main__':
    # Define entry points for various agencies
    entry_points = {
        "ABS": "https://api.data.abs.gov.au",
        "BBK": "https://api.statistiken.bundesbank.de",
        "BIS": "https://stats.bis.org/api/v1",
        "EC_COMP": "https://webgate.ec.europa.eu/comp/redisstat/api/dissemination/sdmx/2.1",
        "EC_EMPL": "https://webgate.ec.europa.eu/empl/redisstat/api/dissemination/sdmx/2.1",
        "EC_GROW": "https://webgate.ec.europa.eu/grow/redisstat/api/dissemination/sdmx/2.1",
        "ECB": "https://data-api.ecb.europa.eu/service",
        "ESTAT": "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1",
        "ESTAT_COMEX": "https://ec.europa.eu/eurostat/api/comext/dissemination/sdmx/2.1",
        "ILO": "https://www.ilo.org/sdmx/rest",
        "IMF": "http://dataservices.imf.org/REST/SDMX_XML.svc",
        "ISTAT": "http://sdmx.istat.it/WS_CENSPOP/rest",
        "NB": "https://data.norges-bank.no/api",
        "OECD:": "http://stats.oecd.org/restsdmx/sdmx.ashx",
        "SGR": "https://registry.sdmx.org/sdmx/v2",
        "SPC:": "http://stats-nsi-stable.pacificdata.org/rest",
        "UNICEF": "https://sdmx.data.unicef.org/ws/public/sdmxapi/rest",
        "UNSD:": "http://data.un.org/ws/rest",
        "WITS": "http://wits.worldbank.org/API/V1/SDMX/V21/rest"
        # Add other agencies as needed
    }

    # Create a CSV data structure
    csv_data = [["Agency", "EntryPoint", "Query", "ResponseCode"]]

    # Iterate through agencies and fetch data
    for agency_name in entry_points:
        # Fetch data flows and dsds
        fetch_data_flows(agency_name, csv_data)
        fetch_dsds(agency_name, csv_data)

        # Get a random dataflow for the agency
        response = requests.get(entry_points[agency_name] + initialize_sdmx().get_data_flows())

        if response.status_code == 200:
            sdmx_data_message = read_sdmx(response.text)
            dataflows = sdmx_data_message.content.get('Dataflows')
            if dataflows:
                random_dataflow = random.choice(list(dataflows.keys()))
                fetch_data(agency_name, csv_data, random_dataflow)
                fetch_constraints(agency_name, csv_data, random_dataflow)
            else:
                print(f"No dataflows found for '{agency_name}'")

    # Save the CSV data to a file
    csv_filename = "shared_data.csv"
    with open(csv_filename, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(csv_data)

    print(f"CSV data saved to '{csv_filename}'")
