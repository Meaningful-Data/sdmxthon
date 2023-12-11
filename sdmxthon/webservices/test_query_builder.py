import pytest
from query_builder import SdmxWs1, SdmxWs2p0, QueryBuilder


@pytest.fixture
def sdmx_ws1():
    return SdmxWs1()


@pytest.fixture
def sdmx_ws2():
    return SdmxWs2p0()


@pytest.fixture
def query_builder(sdmx_ws1):
    return QueryBuilder(sdmx_ws1)


@pytest.fixture
def query_builder_ws2(sdmx_ws2):
    return QueryBuilder(sdmx_ws2)


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


def test_get_data_flows_ws2(query_builder_ws2):
    query = query_builder_ws2.get_data_flows(agency_id="all", resources="all", version="latest")
    assert query == "/structure/dataflow/all/all/latest"


def test_get_dsds_ws2(query_builder_ws2):
    query = query_builder_ws2.get_dsds(agency_id="all", resources="all", version="latest")
    assert query == "/structure/datastructure/all/all/latest"


def test_get_mdsds_ws2(query_builder_ws2):
    query = query_builder_ws2.get_mdsds(agency_id="all", resources="all", version="latest")
    assert query == "/structure/metadatastructure/all/all/latest"


def test_get_meta_data_flows_ws2(query_builder_ws2):
    query = query_builder_ws2.get_meta_data_flows(agency_id="all", resources="all", version="latest")
    assert query == "/structure/metadataflow/all/all/latest"


def test_get_provision_agreements_ws2(query_builder_ws2):
    query = query_builder_ws2.get_provision_agreements(agency_id="all", resources="all", version="latest")
    assert query == "/structure/provisionagreement/all/all/latest"


def test_get_structure_sets_ws2(query_builder_ws2):
    query = query_builder_ws2.get_structure_sets(agency_id="all", resources="all", version="latest")
    assert query == "/structure/structureset/all/all/latest"


def test_get_process_ws2(query_builder_ws2):
    query = query_builder_ws2.get_process(agency_id="all", resources="all", version="latest")
    assert query == "/structure/process/all/all/latest"


def test_get_categorisation_ws2(query_builder_ws2):
    query = query_builder_ws2.get_categorisation(agency_id="all", resources="all", version="latest")
    assert query == "/structure/categorisation/all/all/latest"


def test_get_data_constraint_ws2(query_builder_ws2):
    query = query_builder_ws2.get_data_constraint(agency_id="all", resources="all", version="latest")
    assert query == "/structure/dataconstraint/all/all/latest"


def test_get_metadata_constraint_ws2(query_builder_ws2):
    query = query_builder_ws2.get_metadata_constraint(agency_id="all", resources="all", version="latest")
    assert query == "/structure/metadataconstraint/all/all/latest"


def test_get_concept_scheme_ws2(query_builder_ws2):
    query = query_builder_ws2.get_concept_scheme(agency_id="all", resources="all", version="latest")
    assert query == "/structure/conceptscheme/all/all/latest"


def test_get_code_list_ws2(query_builder_ws2):
    query = query_builder_ws2.get_code_list(agency_id="all", resources="all", version="latest")
    assert query == "/structure/codelist/all/all/latest"


def test_get_category_scheme_ws2(query_builder_ws2):
    query = query_builder_ws2.get_category_scheme(agency_id="all", resources="all", version="latest")
    assert query == "/structure/categoryscheme/all/all/latest"


def test_get_hierarchy_ws2(query_builder_ws2):
    query = query_builder_ws2.get_hierarchy(agency_id="all", resources="all", version="latest")
    assert query == "/structure/hierarchy/all/all/latest"


def test_get_hierarchy_association_ws2(query_builder_ws2):
    query = query_builder_ws2.get_hierarchy_association(agency_id="all", resources="all", version="latest")
    assert query == "/structure/hierarchyassociation/all/all/latest"


def test_get_agency_scheme_ws2(query_builder_ws2):
    query = query_builder_ws2.get_agency_scheme(agency_id="all", resources="all", version="latest")
    assert query == "/structure/agencyscheme/all/all/latest"


def test_get_data_provider_scheme_ws2(query_builder_ws2):
    query = query_builder_ws2.get_data_provider_scheme(agency_id="all", resources="all", version="latest")
    assert query == "/structure/dataproviderscheme/all/all/latest"


def test_get_data_consumer_scheme_ws2(query_builder_ws2):
    query = query_builder_ws2.get_data_consumer_scheme(agency_id="all", resources="all", version="latest")
    assert query == "/structure/dataconsumerscheme/all/all/latest"


def test_get_organisation_unit_scheme_ws2(query_builder_ws2):
    query = query_builder_ws2.get_organisation_unit_scheme(agency_id="all", resources="all", version="latest")
    assert query == "/structure/organisationunitscheme/all/all/latest"


def test_get_transformation_scheme_ws2(query_builder_ws2):
    query = query_builder_ws2.get_transformation_scheme(agency_id="all", resources="all", version="latest")
    assert query == "/structure/transformationscheme/all/all/latest"


def test_get_ruleset_scheme_ws2(query_builder_ws2):
    query = query_builder_ws2.get_ruleset_scheme(agency_id="all", resources="all", version="latest")
    assert query == "/structure/rulesetscheme/all/all/latest"


def test_get_user_defined_operator_scheme_ws2(query_builder_ws2):
    query = query_builder_ws2.get_user_defined_operator_scheme(agency_id="all", resources="all", version="latest")
    assert query == "/structure/userdefinedoperatorscheme/all/all/latest"


def test_get_custom_type_scheme_ws2(query_builder_ws2):
    query = query_builder_ws2.get_custom_type_scheme(agency_id="all", resources="all", version="latest")
    assert query == "/structure/customtypescheme/all/all/latest"


def test_get_name_personalisation_scheme_ws2(query_builder_ws2):
    query = query_builder_ws2.get_name_personalisation_scheme(agency_id="all", resources="all", version="latest")
    assert query == "/structure/namepersonalisationscheme/all/all/latest"


def test_get_vtl_mapping_scheme_ws2(query_builder_ws2):
    query = query_builder_ws2.get_vtl_mapping_scheme(agency_id="all", resources="all", version="latest")
    assert query == "/structure/vtlmappingscheme/all/all/latest"


def test_get_value_list_ws2(query_builder_ws2):
    query = query_builder_ws2.get_value_list(agency_id="all", resources="all", version="latest")
    assert query == "/structure/valuelist/all/all/latest"


def test_get_structure_map_ws2(query_builder_ws2):
    query = query_builder_ws2.get_structure_map(agency_id="all", resources="all", version="latest")
    assert query == "/structure/structuremap/all/all/latest"


def test_get_representation_map_ws2(query_builder_ws2):
    query = query_builder_ws2.get_representation_map(agency_id="all", resources="all", version="latest")
    assert query == "/structure/representationmap/all/all/latest"


def test_get_concept_scheme_map_ws2(query_builder_ws2):
    query = query_builder_ws2.get_concept_scheme_map(agency_id="all", resources="all", version="latest")
    assert query == "/structure/conceptschememap/all/all/latest"


def test_get_category_scheme_map_ws2(query_builder_ws2):
    query = query_builder_ws2.get_category_scheme_map(agency_id="all", resources="all", version="latest")
    assert query == "/structure/categoryschememap/all/all/latest"


def test_get_organisation_scheme_map_ws2(query_builder_ws2):
    query = query_builder_ws2.get_organisation_scheme_map(agency_id="all", resources="all", version="latest")
    assert query == "/structure/organisationschememap/all/all/latest"


def test_get_reporting_taxonomy_map_ws2(query_builder_ws2):
    query = query_builder_ws2.get_reporting_taxonomy_map(agency_id="all", resources="all", version="latest")
    assert query == "/structure/reportingtaxonomymap/all/all/latest"


def test_get_data_flows_with_multiple_params_ws2(query_builder_ws2):
    query = query_builder_ws2.get_data_flows(agency_id="all", resources="all", version="latest",
                                             references="descendants",
                                             detail="referencecompletestubs")
    assert query == "/structure/dataflow/all/all/latest?references=descendants&detail=referencecompletestubs"


if __name__ == '__main__':
    pytest.main()
