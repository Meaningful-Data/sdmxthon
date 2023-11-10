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


def fetch_mdsds(agency_name, csv_data):
    qb = initialize_sdmx()
    mdsds_query = qb.get_mdsds()
    mdsds_url = entry_points[agency_name] + mdsds_query
    print(f"URL for 'mdsds' in '{agency_name}': {mdsds_url}")
    make_request(mdsds_url, agency_name, mdsds_query, csv_data)


def fetch_meta_data_flows(agency_name, csv_data):
    qb = initialize_sdmx()
    meta_data_flows_query = qb.get_meta_data_flows()
    meta_data_flows_url = entry_points[agency_name] + meta_data_flows_query
    print(f"URL for 'metadataflows' in '{agency_name}': {meta_data_flows_url}")
    make_request(meta_data_flows_url, agency_name, meta_data_flows_query, csv_data)


def fetch_provision_agreements(agency_name, csv_data):
    qb = initialize_sdmx()
    provision_agreements_query = qb.get_provision_agreements()
    provision_agreements_url = entry_points[agency_name] + provision_agreements_query
    print(f"URL for 'provision agreements' in '{agency_name}': {provision_agreements_url}")
    make_request(provision_agreements_url, agency_name, provision_agreements_query, csv_data)


def fetch_structure_sets(agency_name, csv_data):
    qb = initialize_sdmx()
    structure_sets_query = qb.get_structure_sets()
    structure_sets_url = entry_points[agency_name] + structure_sets_query
    print(f"URL for 'structure sets' in '{agency_name}': {structure_sets_url}")
    make_request(structure_sets_url, agency_name, structure_sets_query, csv_data)


def fetch_process(agency_name, csv_data):
    qb = initialize_sdmx()
    process_query = qb.get_process()
    process_url = entry_points[agency_name] + process_query
    print(f"URL for 'processes' in '{agency_name}': {process_url}")
    make_request(process_url, agency_name, process_query, csv_data)


def fetch_categorisation(agency_name, csv_data):
    qb = initialize_sdmx()
    categorisation_query = qb.get_categorisation()
    categorisation_url = entry_points[agency_name] + categorisation_query
    print(f"URL for 'categorisations' in '{agency_name}': {categorisation_url}")
    make_request(categorisation_url, agency_name, categorisation_query, csv_data)


def fetch_content_constraint(agency_name, csv_data):
    qb = initialize_sdmx()
    content_constraint_query = qb.get_content_constraint()
    content_constraint_url = entry_points[agency_name] + content_constraint_query
    print(f"URL for 'content constraints' in '{agency_name}': {content_constraint_url}")
    make_request(content_constraint_url, agency_name, content_constraint_query, csv_data)


def fetch_actual_constraint(agency_name, csv_data):
    qb = initialize_sdmx()
    actual_constraint_query = qb.get_actual_constraint()
    actual_constraint_url = entry_points[agency_name] + actual_constraint_query
    print(f"URL for 'actual constraints' in '{agency_name}': {actual_constraint_url}")
    make_request(actual_constraint_url, agency_name, actual_constraint_query, csv_data)


def fetch_allowed_constraint(agency_name, csv_data):
    qb = initialize_sdmx()
    allowed_constraint_query = qb.get_allowed_constraint()
    allowed_constraint_url = entry_points[agency_name] + allowed_constraint_query
    print(f"URL for 'allowed constraints' in '{agency_name}': {allowed_constraint_url}")
    make_request(allowed_constraint_url, agency_name, allowed_constraint_query, csv_data)


def fetch_attachment_constraint(agency_name, csv_data):
    qb = initialize_sdmx()
    attachment_constraint_query = qb.get_attachment_constraint()
    attachment_constraint_url = entry_points[agency_name] + attachment_constraint_query
    print(f"URL for 'attachment constraints' in '{agency_name}': {attachment_constraint_url}")
    make_request(attachment_constraint_url, agency_name, attachment_constraint_query, csv_data)


def fetch_structure(agency_name, csv_data):
    qb = initialize_sdmx()
    structure_query = qb.get_structure()
    structure_url = entry_points[agency_name] + structure_query
    print(f"URL for 'structure' in '{agency_name}': {structure_url}")
    make_request(structure_url, agency_name, structure_query, csv_data)


def fetch_concept_scheme(agency_name, csv_data):
    qb = initialize_sdmx()
    concept_scheme_query = qb.get_concept_scheme()
    concept_scheme_url = entry_points[agency_name] + concept_scheme_query
    print(f"URL for 'concept schemes' in '{agency_name}': {concept_scheme_url}")
    make_request(concept_scheme_url, agency_name, concept_scheme_query, csv_data)


def fetch_code_list(agency_name, csv_data):
    qb = initialize_sdmx()
    code_list_query = qb.get_code_list()
    code_list_url = entry_points[agency_name] + code_list_query
    print(f"URL for 'codelists' in '{agency_name}': {code_list_url}")
    make_request(code_list_url, agency_name, code_list_query, csv_data)


def fetch_category_scheme(agency_name, csv_data):
    qb = initialize_sdmx()
    category_scheme_query = qb.get_category_scheme()
    category_scheme_url = entry_points[agency_name] + category_scheme_query
    print(f"URL for 'category schemes' in '{agency_name}': {category_scheme_url}")
    make_request(category_scheme_url, agency_name, category_scheme_query, csv_data)


def fetch_hierarchical_codelist(agency_name, csv_data):
    qb = initialize_sdmx()
    hierarchical_codelist_query = qb.get_hierarchical_codelist()
    hierarchical_codelist_url = entry_points[agency_name] + hierarchical_codelist_query
    print(f"URL for 'hierarchical codelists' in '{agency_name}': {hierarchical_codelist_url}")
    make_request(hierarchical_codelist_url, agency_name, hierarchical_codelist_query, csv_data)


def fetch_organisation_scheme(agency_name, csv_data):
    qb = initialize_sdmx()
    organisation_scheme_query = qb.get_organisation_scheme()
    organisation_scheme_url = entry_points[agency_name] + organisation_scheme_query
    print(f"URL for 'organisation schemes' in '{agency_name}': {organisation_scheme_url}")
    make_request(organisation_scheme_url, agency_name, organisation_scheme_query, csv_data)


def fetch_agency_scheme(agency_name, csv_data):
    qb = initialize_sdmx()
    agency_scheme_query = qb.get_agency_scheme()
    agency_scheme_url = entry_points[agency_name] + agency_scheme_query
    print(f"URL for 'agency schemes' in '{agency_name}': {agency_scheme_url}")
    make_request(agency_scheme_url, agency_name, agency_scheme_query, csv_data)


def fetch_data_provider_scheme(agency_name, csv_data):
    qb = initialize_sdmx()
    data_provider_scheme_query = qb.get_data_provider_scheme()
    data_provider_scheme_url = entry_points[agency_name] + data_provider_scheme_query
    print(f"URL for 'data provider schemes' in '{agency_name}': {data_provider_scheme_url}")
    make_request(data_provider_scheme_url, agency_name, data_provider_scheme_query, csv_data)


def fetch_data_consumer_scheme(agency_name, csv_data):
    qb = initialize_sdmx()
    data_consumer_scheme_query = qb.get_data_consumer_scheme()
    data_consumer_scheme_url = entry_points[agency_name] + data_consumer_scheme_query
    print(f"URL for 'data consumer schemes' in '{agency_name}': {data_consumer_scheme_url}")
    make_request(data_consumer_scheme_url, agency_name, data_consumer_scheme_query, csv_data)


def fetch_organisation_unit_scheme(agency_name, csv_data):
    qb = initialize_sdmx()
    organisation_unit_scheme_query = qb.get_organisation_unit_scheme()
    organisation_unit_scheme_url = entry_points[agency_name] + organisation_unit_scheme_query
    print(f"URL for 'organisation unit schemes' in '{agency_name}': {organisation_unit_scheme_url}")
    make_request(organisation_unit_scheme_url, agency_name, organisation_unit_scheme_query, csv_data)


def fetch_transformation_scheme(agency_name, csv_data):
    qb = initialize_sdmx()
    transformation_scheme_query = qb.get_transformation_scheme()
    transformation_scheme_url = entry_points[agency_name] + transformation_scheme_query
    print(f"URL for 'transformation schemes' in '{agency_name}': {transformation_scheme_url}")
    make_request(transformation_scheme_url, agency_name, transformation_scheme_query, csv_data)


def fetch_ruleset_scheme(agency_name, csv_data):
    qb = initialize_sdmx()
    ruleset_scheme_query = qb.get_ruleset_scheme()
    ruleset_scheme_url = entry_points[agency_name] + ruleset_scheme_query
    print(f"URL for 'ruleset schemes' in '{agency_name}': {ruleset_scheme_url}")
    make_request(ruleset_scheme_url, agency_name, ruleset_scheme_query, csv_data)


def fetch_user_defined_operator_scheme(agency_name, csv_data):
    qb = initialize_sdmx()
    user_defined_operator_scheme_query = qb.get_user_defined_operator_scheme()
    user_defined_operator_scheme_url = entry_points[agency_name] + user_defined_operator_scheme_query
    print(f"URL for 'user defined operator schemes' in '{agency_name}': {user_defined_operator_scheme_url}")
    make_request(user_defined_operator_scheme_url, agency_name, user_defined_operator_scheme_query, csv_data)


def fetch_custom_type_scheme(agency_name, csv_data):
    qb = initialize_sdmx()
    custom_type_scheme_query = qb.get_custom_type_scheme()
    custom_type_scheme_url = entry_points[agency_name] + custom_type_scheme_query
    print(f"URL for 'custom type schemes' in '{agency_name}': {custom_type_scheme_url}")
    make_request(custom_type_scheme_url, agency_name, custom_type_scheme_query, csv_data)


def fetch_name_personalisation_scheme(agency_name, csv_data):
    qb = initialize_sdmx()
    name_personalisation_scheme_query = qb.get_name_personalisation_scheme()
    name_personalisation_scheme_url = entry_points[agency_name] + name_personalisation_scheme_query
    print(f"URL for 'name personalisation schemes' in '{agency_name}': {name_personalisation_scheme_url}")
    make_request(name_personalisation_scheme_url, agency_name, name_personalisation_scheme_query, csv_data)


def fetch_name_alias_scheme(agency_name, csv_data):
    qb = initialize_sdmx()
    name_alias_scheme_query = qb.get_name_alias_scheme()
    name_alias_scheme_url = entry_points[agency_name] + name_alias_scheme_query
    print(f"URL for 'name personalisation schemes' in '{agency_name}': {name_alias_scheme_url}")
    make_request(name_alias_scheme_url, agency_name, name_alias_scheme_query, csv_data)


def fetch_concepts(agency_name, csv_data):
    qb = initialize_sdmx()
    concepts_query = qb.get_concepts()
    concepts_url = entry_points[agency_name] + concepts_query
    print(f"URL for 'concepts' in '{agency_name}': {concepts_url}")
    make_request(concepts_url, agency_name, concepts_query, csv_data)


def fetch_codes(agency_name, csv_data):
    qb = initialize_sdmx()
    codes_query = qb.get_codes()
    codes_url = entry_points[agency_name] + codes_query
    print(f"URL for 'codes' in '{agency_name}': {codes_url}")
    make_request(codes_url, agency_name, codes_query, csv_data)


def fetch_categories(agency_name, csv_data):
    qb = initialize_sdmx()
    categories_query = qb.get_categories()
    categories_url = entry_points[agency_name] + categories_query
    print(f"URL for 'codes' in '{agency_name}': {categories_url}")
    make_request(categories_url, agency_name, categories_query, csv_data)


def fetch_hierarchies(agency_name, csv_data):
    qb = initialize_sdmx()
    hierarchies_query = qb.get_hierarchies()
    hierarchies_url = entry_points[agency_name] + hierarchies_query
    print(f"URL for 'hierarchies' in '{agency_name}': {hierarchies_url}")
    make_request(hierarchies_url, agency_name, hierarchies_query, csv_data)


def fetch_organisations(agency_name, csv_data):
    qb = initialize_sdmx()
    organisations_query = qb.get_organisations()
    organisations_url = entry_points[agency_name] + organisations_query
    print(f"URL for 'organisations' in '{agency_name}': {organisations_url}")
    make_request(organisations_url, agency_name, organisations_query, csv_data)


def fetch_agencies(agency_name, csv_data):
    qb = initialize_sdmx()
    agencies_query = qb.get_agencies()
    agencies_url = entry_points[agency_name] + agencies_query
    print(f"URL for 'agencies' in '{agency_name}': {agencies_url}")
    make_request(agencies_url, agency_name, agencies_query, csv_data)


def fetch_data_providers(agency_name, csv_data):
    qb = initialize_sdmx()
    data_providers_query = qb.get_data_providers()
    data_providers_url = entry_points[agency_name] + data_providers_query
    print(f"URL for 'data providers' in '{agency_name}': {data_providers_url}")
    make_request(data_providers_url, agency_name, data_providers_query, csv_data)


def fetch_data_consumers(agency_name, csv_data):
    qb = initialize_sdmx()
    data_consumers_query = qb.get_data_consumers()
    data_consumers_url = entry_points[agency_name] + data_consumers_query
    print(f"URL for 'data consumers' in '{agency_name}': {data_consumers_url}")
    make_request(data_consumers_url, agency_name, data_consumers_query, csv_data)


def fetch_organisation_unit_schemes(agency_name, csv_data):
    qb = initialize_sdmx()
    organisation_unit_schemes_query = qb.get_organisation_unit_schemes()
    organisation_unit_schemes_url = entry_points[agency_name] + organisation_unit_schemes_query
    print(f"URL for 'organisation unit schemes' in '{agency_name}': {organisation_unit_schemes_url}")
    make_request(organisation_unit_schemes_url, agency_name, organisation_unit_schemes_query, csv_data)


def fetch_transformation_schemes(agency_name, csv_data):
    qb = initialize_sdmx()
    transformation_schemes_query = qb.get_transformation_schemes()
    transformation_schemes_url = entry_points[agency_name] + transformation_schemes_query
    print(f"URL for 'transformation schemes' in '{agency_name}': {transformation_schemes_url}")
    make_request(transformation_schemes_url, agency_name, transformation_schemes_query, csv_data)


def fetch_ruleset_schemes(agency_name, csv_data):
    qb = initialize_sdmx()
    ruleset_schemes_query = qb.get_ruleset_schemes()
    ruleset_schemes_url = entry_points[agency_name] + ruleset_schemes_query
    print(f"URL for 'ruleset schemes' in '{agency_name}': {ruleset_schemes_url}")
    make_request(ruleset_schemes_url, agency_name, ruleset_schemes_query, csv_data)


def fetch_user_defined_operator_schemes(agency_name, csv_data):
    qb = initialize_sdmx()
    user_defined_operator_schemes_query = qb.get_user_defined_operator_schemes()
    user_defined_operator_schemes_url = entry_points[agency_name] + user_defined_operator_schemes_query
    print(f"URL for 'user defined operator schemes' in '{agency_name}': {user_defined_operator_schemes_url}")
    make_request(user_defined_operator_schemes_url, agency_name, user_defined_operator_schemes_query, csv_data)


def fetch_custom_type_schemes(agency_name, csv_data):
    qb = initialize_sdmx()
    custom_type_schemes_query = qb.get_custom_type_schemes()
    custom_type_schemes_url = entry_points[agency_name] + custom_type_schemes_query
    print(f"URL for 'custom type schemes' in '{agency_name}': {custom_type_schemes_url}")
    make_request(custom_type_schemes_url, agency_name, custom_type_schemes_query, csv_data)


def fetch_name_personalisation_schemes(agency_name, csv_data):
    qb = initialize_sdmx()
    name_personalisation_schemes_query = qb.get_name_personalisation_schemes()
    name_personalisation_schemes_url = entry_points[agency_name] + name_personalisation_schemes_query
    print(f"URL for 'name personalisation schemes' in '{agency_name}': {name_personalisation_schemes_url}")
    make_request(name_personalisation_schemes_url, agency_name, name_personalisation_schemes_query, csv_data)


def fetch_name_alias_schemes(agency_name, csv_data):
    qb = initialize_sdmx()
    name_alias_schemes_query = qb.get_name_alias_schemes()
    name_alias_schemes_url = entry_points[agency_name] + name_alias_schemes_query
    print(f"URL for 'name alias schemes' in '{agency_name}': {name_alias_schemes_url}")
    make_request(name_alias_schemes_url, agency_name, name_alias_schemes_query, csv_data)


if __name__ == '__main__':
    # Define entry points for various agencies
    entry_points = {
        "ABS": "https://api.data.abs.gov.au",
        # "BBK": "https://api.statistiken.bundesbank.de",
        "BIS": "https://stats.bis.org/api/v1", #
        # "EC_COMP": "https://webgate.ec.europa.eu/comp/redisstat/api/dissemination/sdmx/2.1",
        # "EC_EMPL": "https://webgate.ec.europa.eu/empl/redisstat/api/dissemination/sdmx/2.1",
        # "EC_GROW": "https://webgate.ec.europa.eu/grow/redisstat/api/dissemination/sdmx/2.1",
        "ECB": "https://data-api.ecb.europa.eu/service",
        "ESTAT": "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1",
        # "ESTAT_COMEX": "https://ec.europa.eu/eurostat/api/comext/dissemination/sdmx/2.1",
        "ILO": "https://www.ilo.org/sdmx/rest",
        "IMF": "http://dataservices.imf.org/REST/SDMX_XML.svc",
        # "INSEE": "https://bdm.insee.fr/series/sdmx",
        "ISTAT": "http://sdmx.istat.it/WS_CENSPOP/rest",
        # "NB": "https://data.norges-bank.no/api",
        "OECD:": "http://stats.oecd.org/restsdmx/sdmx.ashx",
        # "SGR": "https://registry.sdmx.org/sdmx/v2",
        # "SPC:": "http://stats-nsi-stable.pacificdata.org/rest",
        "UNICEF": "https://sdmx.data.unicef.org/ws/public/sdmxapi/rest",
        "UNSD:": "http://data.un.org/ws/rest",
        "WITS": "http://wits.worldbank.org/API/V1/SDMX/V21/rest"
        # Add other agencies as needed
    }

    # Create a CSV data structure
    csv_data = [["Agency", "EntryPoint", "Query", "ResponseCode"]]

    # Iterate through agencies and fetch data
    for agency_name in entry_points:
        fetch_data_flows(agency_name, csv_data)
        fetch_dsds(agency_name, csv_data)
        fetch_mdsds(agency_name, csv_data)
        fetch_meta_data_flows(agency_name, csv_data)
        fetch_provision_agreements(agency_name, csv_data)
        fetch_structure_sets(agency_name, csv_data)
        fetch_process(agency_name, csv_data)
        fetch_categorisation(agency_name, csv_data)
        fetch_content_constraint(agency_name, csv_data)
        fetch_actual_constraint(agency_name, csv_data)
        fetch_allowed_constraint(agency_name, csv_data)
        fetch_attachment_constraint(agency_name, csv_data)
        fetch_structure(agency_name, csv_data)
        fetch_concept_scheme(agency_name, csv_data)
        fetch_code_list(agency_name, csv_data)
        fetch_category_scheme(agency_name, csv_data)
        fetch_hierarchical_codelist(agency_name, csv_data)
        fetch_organisation_scheme(agency_name, csv_data)
        fetch_agency_scheme(agency_name, csv_data)
        fetch_data_provider_scheme(agency_name, csv_data)
        fetch_data_consumer_scheme(agency_name, csv_data)
        fetch_organisation_unit_scheme(agency_name, csv_data)
        fetch_transformation_scheme(agency_name, csv_data)
        fetch_ruleset_scheme(agency_name, csv_data)
        fetch_user_defined_operator_scheme(agency_name, csv_data)
        fetch_custom_type_scheme(agency_name, csv_data)
        fetch_name_personalisation_scheme(agency_name, csv_data)
        fetch_name_alias_scheme(agency_name, csv_data)
        fetch_concepts(agency_name, csv_data)
        fetch_codes(agency_name, csv_data)
        fetch_categories(agency_name, csv_data)
        fetch_hierarchies(agency_name, csv_data)
        fetch_organisations(agency_name, csv_data)
        fetch_agencies(agency_name, csv_data)
        fetch_data_providers(agency_name, csv_data)
        fetch_data_consumers(agency_name, csv_data)
        fetch_organisation_unit_schemes(agency_name, csv_data)
        fetch_transformation_schemes(agency_name, csv_data)
        fetch_ruleset_schemes(agency_name, csv_data)
        fetch_user_defined_operator_schemes(agency_name, csv_data)
        fetch_custom_type_schemes(agency_name, csv_data)
        fetch_name_personalisation_schemes(agency_name, csv_data)
        fetch_name_alias_schemes(agency_name, csv_data)

        # Get a random dataflow for the agency
        response = requests.get(entry_points[agency_name] + initialize_sdmx().get_data_flows())

        if response.status_code == 200:
            sdmx_data_message = read_sdmx(response.text)
            dataflows = sdmx_data_message.content.get('Dataflows')
            if dataflows:
                random_dataflow = random.choice(list(dataflows.keys()))
                fetch_data(agency_name, csv_data, random_dataflow)
                fetch_constraints(agency_name, csv_data, random_dataflow)  #
            else:
                print(f"No dataflows found for '{agency_name}'")

    # Save the CSV data to a file
    csv_filename = "shared_data.csv"
    with open(csv_filename, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(csv_data)

    print(f"CSV data saved to '{csv_filename}'")
