import pytest
from query_builder import SdmxWs1, QueryBuilder


@pytest.fixture
def sdmx_ws1():
    return SdmxWs1()


@pytest.fixture
def query_builder(sdmx_ws1):
    return QueryBuilder(sdmx_ws1)


def test_get_data_flows(query_builder):
    query = query_builder.get_data_flows(agency_id="all", resources="all", version="latest")
    assert query == "/dataflow/all/all/latest"


def test_get_data(query_builder):
    query = query_builder.get_data(flow="example_flow", key="all", provider="all")
    assert query == "/data/example_flow/all/all"


def test_get_dsds(query_builder):
    query = query_builder.get_dsds(agency_id="all", resources="all", version="latest")
    assert query == "/datastructure/all/all/latest"


def test_get_constraints(query_builder):
    query = query_builder.get_constraints(flow="example_flow", key="all", provider="all", component_id="all")
    assert query == "/availableconstraint/example_flow/all/all/all"


def test_get_mdsds(query_builder):
    query = query_builder.get_mdsds(agency_id="all", resources="all", version="latest")
    assert query == "/metadatastructure/all/all/latest"


def test_get_meta_data_flows(query_builder):
    query = query_builder.get_meta_data_flows(agency_id="all", resources="all", version="latest")
    assert query == "/metadataflow/all/all/latest"


def test_get_provision_agreements(query_builder):
    query = query_builder.get_provision_agreements(agency_id="all", resources="all", version="latest")
    assert query == "/provisionagreement/all/all/latest"


def test_get_structure_sets(query_builder):
    query = query_builder.get_structure_sets(agency_id="all", resources="all", version="latest")
    assert query == "/structureset/all/all/latest"


def test_get_process(query_builder):
    query = query_builder.get_process(agency_id="all", resources="all", version="latest")
    assert query == "/process/all/all/latest"


def test_get_categorisation(query_builder):
    query = query_builder.get_categorisation(agency_id="all", resources="all", version="latest")
    assert query == "/categorisation/all/all/latest"


def test_get_content_constraint(query_builder):
    query = query_builder.get_content_constraint(agency_id="all", resources="all", version="latest")
    assert query == "/contentconstraint/all/all/latest"


def test_get_actual_constraint(query_builder):
    query = query_builder.get_actual_constraint(agency_id="all", resources="all", version="latest")
    assert query == "/actualconstraint/all/all/latest"


def test_get_allowed_constraint(query_builder):
    query = query_builder.get_allowed_constraint(agency_id="all", resources="all", version="latest")
    assert query == "/allowedconstraint/all/all/latest"


def test_get_attachment_constraint(query_builder):
    query = query_builder.get_attachment_constraint(agency_id="all", resources="all", version="latest")
    assert query == "/attachmentconstraint/all/all/latest"


def test_get_structure(query_builder):
    query = query_builder.get_structure(agency_id="all", resources="all", version="latest")
    assert query == "/structure/all/all/latest"


def test_get_concept_scheme(query_builder):
    query = query_builder.get_concept_scheme(agency_id="all", resources="all", version="latest")
    assert query == "/conceptscheme/all/all/latest"


def test_get_code_list(query_builder):
    query = query_builder.get_code_list(agency_id="all", resources="all", version="latest")
    assert query == "/codelist/all/all/latest"


def test_get_category_scheme(query_builder):
    query = query_builder.get_category_scheme(agency_id="all", resources="all", version="latest")
    assert query == "/categoryscheme/all/all/latest"


def test_get_hierarchical_codelist(query_builder):
    query = query_builder.get_hierarchical_codelist(agency_id="all", resources="all", version="latest")
    assert query == "/hierarchicalcodelist/all/all/latest"


def test_get_organisation_scheme(query_builder):
    query = query_builder.get_organisation_scheme(agency_id="all", resources="all", version="latest")
    assert query == "/organisationscheme/all/all/latest"


def test_get_agency_scheme(query_builder):
    query = query_builder.get_agency_scheme(agency_id="all", resources="all", version="latest")
    assert query == "/agencyscheme/all/all/latest"


def test_get_data_provider_scheme(query_builder):
    query = query_builder.get_data_provider_scheme(agency_id="all", resources="all", version="latest")
    assert query == "/dataproviderscheme/all/all/latest"


def test_get_data_consumer_scheme(query_builder):
    query = query_builder.get_data_consumer_scheme(agency_id="all", resources="all", version="latest")
    assert query == "/dataconsumerscheme/all/all/latest"


def test_get_organisation_unit_scheme(query_builder):
    query = query_builder.get_organisation_unit_scheme(agency_id="all", resources="all", version="latest")
    assert query == "/organisationunitscheme/all/all/latest"


def test_get_transformation_scheme(query_builder):
    query = query_builder.get_transformation_scheme(agency_id="all", resources="all", version="latest")
    assert query == "/transformationscheme/all/all/latest"


def test_get_ruleset_scheme(query_builder):
    query = query_builder.get_ruleset_scheme(agency_id="all", resources="all", version="latest")
    assert query == "/rulesetscheme/all/all/latest"


def test_get_user_defined_operator_scheme(query_builder):
    query = query_builder.get_user_defined_operator_scheme(agency_id="all", resources="all", version="latest")
    assert query == "/userdefinedoperatorscheme/all/all/latest"


def test_get_custom_type_scheme(query_builder):
    query = query_builder.get_custom_type_scheme(agency_id="all", resources="all", version="latest")
    assert query == "/customtypescheme/all/all/latest"


def test_get_name_personalisation_scheme(query_builder):
    query = query_builder.get_name_personalisation_scheme(agency_id="all", resources="all", version="latest")
    assert query == "/namepersonalisationscheme/all/all/latest"


def test_get_name_alias_scheme(query_builder):
    query = query_builder.get_name_alias_scheme(agency_id="all", resources="all", version="latest")
    assert query == "/namealiasscheme/all/all/latest"


def test_get_concepts(query_builder):
    query = query_builder.get_concepts(agency_id="all", resources="all", version="latest", item_id="all")
    assert query == "/conceptscheme/all/all/latest/all"


def test_get_codes(query_builder):
    query = query_builder.get_codes(agency_id="all", resources="all", version="latest", item_id="all")
    assert query == "/codelist/all/all/latest/all"


def test_get_categories(query_builder):
    query = query_builder.get_categories(agency_id="all", resources="all", version="latest", item_id="all")
    assert query == "/categoryscheme/all/all/latest/all"


def test_get_hierarchies(query_builder):
    query = query_builder.get_hierarchies(agency_id="all", resources="all", version="latest", item_id="all")
    assert query == "/hierarchicalcodelist/all/all/latest/all"


def test_get_organisations(query_builder):
    query = query_builder.get_organisations(agency_id="all", resources="all", version="latest", item_id="all")
    assert query == "/organisationscheme/all/all/latest/all"


def test_get_agencies(query_builder):
    query = query_builder.get_agencies(agency_id="all", resources="all", version="latest", item_id="all")
    assert query == "/agencyscheme/all/all/latest/all"


def test_get_data_providers(query_builder):
    query = query_builder.get_data_providers(agency_id="all", resources="all", version="latest", item_id="all")
    assert query == "/dataproviderscheme/all/all/latest/all"


def test_get_data_consumers(query_builder):
    query = query_builder.get_data_consumers(agency_id="all", resources="all", version="latest", item_id="all")
    assert query == "/dataconsumerscheme/all/all/latest/all"


def test_get_organisation_unit_schemes(query_builder):
    query = query_builder.get_organisation_unit_schemes(agency_id="all", resources="all", version="latest",
                                                        item_id="all")
    assert query == "/organisationunitscheme/all/all/latest/all"


def test_get_transformation_schemes(query_builder):
    query = query_builder.get_transformation_schemes(agency_id="all", resources="all", version="latest",
                                                     item_id="all")
    assert query == "/transformationscheme/all/all/latest/all"


def test_get_get_ruleset_schemes(query_builder):
    query = query_builder.get_ruleset_schemes(agency_id="all", resources="all", version="latest", item_id="all")
    assert query == "/rulesetscheme/all/all/latest/all"


def test_get_user_defined_operator_schemes(query_builder):
    query = query_builder.get_user_defined_operator_schemes(agency_id="all", resources="all", version="latest",
                                                            item_id="all")
    assert query == "/userdefinedoperatorscheme/all/all/latest/all"


def test_get_custom_type_schemes(query_builder):
    query = query_builder.get_custom_type_schemes(agency_id="all", resources="all", version="latest", item_id="all")
    assert query == "/customtypescheme/all/all/latest/all"


def test_get_name_personalisation_schemes(query_builder):
    query = query_builder.get_name_personalisation_schemes(agency_id="all", resources="all", version="latest",
                                                           item_id="all")
    assert query == "/namepersonalisationscheme/all/all/latest/all"


def test_get_name_alias_schemes(query_builder):
    query = query_builder.get_name_alias_schemes(agency_id="all", resources="all", version="latest", item_id="all")
    assert query == "/namealiasscheme/all/all/latest/all"


def test_get_data_flows_with_multiple_params(query_builder):
    query = query_builder.get_data_flows(agency_id="all", resources="all", version="latest", references="descendants",
                                         detail="referencecompletestubs")
    assert query == "/dataflow/all/all/latest?references=descendants&detail=referencecompletestubs"


def test_get_concepts_with_multiple_params(query_builder):
    query = query_builder.get_concepts(agency_id="all", resources="all", version="latest", item_id="all",
                                       references="parents", detail="allstubs")
    assert query == "/conceptscheme/all/all/latest/all?references=parents&detail=allstubs"


def test_get_data_with_multiple_parameters(query_builder):
    query = query_builder.get_data(flow="example_flow", key="all", provider="all",
                                   start_period="2022-01-01", end_period="2022-12-31", updated_after="2022-01-01",
                                   first_n_observations=10, dimension_at_observation="TIME_PERIOD",
                                   detail="serieskeysonly", include_history="true")
    assert query == ("/data/example_flow/all/all?startPeriod=2022-01-01&endPeriod=2022-12-31"
                     "&updatedAfter=2022-01-01&firstNObservations=10&dimensionAtObservation=TIME_PERIOD&"
                     "detail=serieskeysonly&includeHistory=true")


def test_get_constraints_with_multiple_params(query_builder):
    query = query_builder.get_constraints(flow="example_flow", mode="available", references="dataproviderscheme",
                                          start_period="2020-01-01", end_period="2020-12-31",
                                          updated_after="2020-01-01")
    assert query == ("/availableconstraint/example_flow/all/all/all?mode=available&references=dataproviderscheme&"
                     "startPeriod=2020-01-01&endPeriod=2020-12-31&updatedAfter=2020-01-01")


if __name__ == '__main__':
    pytest.main()
