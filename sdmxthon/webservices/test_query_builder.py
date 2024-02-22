import pytest
from pytest import mark

from query_builder import QueryBuilder, SdmxWs1, SdmxWs2p0


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


params_structure_queries_SdmxWs1 = [
    ('get_dsds', '/datastructure/all/all/latest'),
    ('get_mdsds', '/metadatastructure/all/all/latest'),
    ('get_data_flows', '/dataflow/all/all/latest'),
    ('get_meta_data_flows', '/metadataflow/all/all/latest'),
    ('get_provision_agreements', '/provisionagreement/all/all/latest'),
    ('get_structure_sets', '/structureset/all/all/latest'),
    ('get_process', '/process/all/all/latest'),
    ('get_categorisation', '/categorisation/all/all/latest'),
    ('get_content_constraint', '/contentconstraint/all/all/latest'),
    ('get_actual_constraint', '/actualconstraint/all/all/latest'),
    ('get_allowed_constraint', '/allowedconstraint/all/all/latest'),
    ('get_attachment_constraint', '/attachmentconstraint/all/all/latest'),
    ('get_structure', '/structure/all/all/latest'),
    ('get_concept_scheme', '/conceptscheme/all/all/latest'),
    ('get_code_list', '/codelist/all/all/latest'),
    ('get_category_scheme', '/categoryscheme/all/all/latest'),
    ('get_hierarchical_codelist', '/hierarchicalcodelist/all/all/latest'),
    ('get_organisation_scheme', '/organisationscheme/all/all/latest'),
    ('get_agency_scheme', '/agencyscheme/all/all/latest'),
    ('get_data_provider_scheme', '/dataproviderscheme/all/all/latest'),
    ('get_data_consumer_scheme', '/dataconsumerscheme/all/all/latest'),
    ('get_organisation_unit_scheme', '/organisationunitscheme/all/all/latest'),
    ('get_transformation_scheme', '/transformationscheme/all/all/latest'),
    ('get_ruleset_scheme', '/rulesetscheme/all/all/latest'),
    ('get_user_defined_operator_scheme',
     '/userdefinedoperatorscheme/all/all/latest'),
    ('get_custom_type_scheme', '/customtypescheme/all/all/latest'),
    ('get_name_personalisation_scheme',
     '/namepersonalisationscheme/all/all/latest'),
    ('get_name_alias_scheme', '/namealiasscheme/all/all/latest'),
    ('get_schemas_datastructure', '/schema/datastructure/all/all/latest'),
    ('get_schemas_meta_datastructure',
     '/schema/metadatastructure/all/all/latest'),
    ('get_schemas_dataflow', '/schema/dataflow/all/all/latest'),
    ('get_schemas_meta_dataflow', '/schema/metadataflow/all/all/latest'),
    ('get_schemas_provision_agreement',
     '/schema/provisionagreement/all/all/latest')
]

params_item_queries_SdmxWs1 = [
    ('get_concepts', '/conceptscheme/all/all/latest/all'),
    ('get_codes', '/codelist/all/all/latest/all'),
    ('get_categories', '/categoryscheme/all/all/latest/all'),
    ('get_hierarchies', '/hierarchicalcodelist/all/all/latest/all'),
    ('get_organisations', '/organisationscheme/all/all/latest/all'),
    ('get_agencies', '/agencyscheme/all/all/latest/all'),
    ('get_data_providers', '/dataproviderscheme/all/all/latest/all'),
    ('get_data_consumers', '/dataconsumerscheme/all/all/latest/all'),
    ('get_organisation_unit_schemes',
     '/organisationunitscheme/all/all/latest/all'),
    ('get_transformation_schemes', '/transformationscheme/all/all/latest/all'),
    ('get_ruleset_schemes', '/rulesetscheme/all/all/latest/all'),
    ('get_user_defined_operator_schemes',
     '/userdefinedoperatorscheme/all/all/latest/all'),
    ('get_custom_type_schemes', '/customtypescheme/all/all/latest/all'),
    ('get_name_personalisation_schemes',
     '/namepersonalisationscheme/all/all/latest/all'),
    ('get_name_alias_schemes', '/namealiasscheme/all/all/latest/all')
]

params_data_queries_SdmxWs2p0 = [
    ('get_data_datastructures', '/data/datastructure/all/all/latest/all'),
    ('get_data_dataflows', '/data/dataflow/all/all/latest/all'),
    ('get_data_provision_agreements',
     '/data/provisionagreement/all/all/latest/all'),
    ('get_data_all_contexts', '/data/all/all/all/latest/all')
]

params_data_constraints_queries_SdmxWs2p0 = [
    ('get_constraint_datastructures',
     '/availability/datastructure/all/all/latest/all/all'),
    ('get_constraint_dataflows',
     '/availability/dataflow/all/all/latest/all/all'),
    ('get_constraint_provision_agreements',
     '/availability/provisionagreement/all/all/latest/all/all'),
    ('get_constraint_all_contexts', '/availability/all/all/all/latest/all/all')
]

params_structure_schema_queries_SdmxWs2p0 = [
    ('get_dsds', '/structure/datastructure/all/all/latest'),
    ('get_mdsds', '/structure/metadatastructure/all/all/latest'),
    ('get_data_flows', '/structure/dataflow/all/all/latest'),
    ('get_meta_data_flows', '/structure/metadataflow/all/all/latest'),
    (
        'get_provision_agreements',
        '/structure/provisionagreement/all/all/latest'),
    ('get_structure_sets', '/structure/structureset/all/all/latest'),
    ('get_process', '/structure/process/all/all/latest'),
    ('get_categorisation', '/structure/categorisation/all/all/latest'),
    ('get_data_constraint', '/structure/dataconstraint/all/all/latest'),
    ('get_metadata_constraint', '/structure/metadataconstraint/all/all/latest'),
    ('get_concept_scheme', '/structure/conceptscheme/all/all/latest'),
    ('get_code_list', '/structure/codelist/all/all/latest'),
    ('get_category_scheme', '/structure/categoryscheme/all/all/latest'),
    ('get_hierarchy', '/structure/hierarchy/all/all/latest'),
    ('get_hierarchy_association',
     '/structure/hierarchyassociation/all/all/latest'),
    ('get_agency_scheme', '/structure/agencyscheme/all/all/latest'),
    (
        'get_data_provider_scheme',
        '/structure/dataproviderscheme/all/all/latest'),
    (
        'get_data_consumer_scheme',
        '/structure/dataconsumerscheme/all/all/latest'),
    ('get_organisation_unit_scheme',
     '/structure/organisationunitscheme/all/all/latest'),
    ('get_transformation_scheme',
     '/structure/transformationscheme/all/all/latest'),
    ('get_ruleset_scheme', '/structure/rulesetscheme/all/all/latest'),
    ('get_user_defined_operator_scheme',
     '/structure/userdefinedoperatorscheme/all/all/latest'),
    ('get_custom_type_scheme', '/structure/customtypescheme/all/all/latest'),
    ('get_name_personalisation_scheme',
     '/structure/namepersonalisationscheme/all/all/latest'),
    ('get_vtl_mapping_scheme', '/structure/vtlmappingscheme/all/all/latest'),
    ('get_value_list', '/structure/valuelist/all/all/latest'),
    ('get_structure_map', '/structure/structuremap/all/all/latest'),
    ('get_representation_map', '/structure/representationmap/all/all/latest'),
    ('get_concept_scheme_map', '/structure/conceptschememap/all/all/latest'),
    ('get_category_scheme_map', '/structure/categoryschememap/all/all/latest'),
    ('get_organisation_scheme_map',
     '/structure/organisationschememap/all/all/latest'),
    ('get_reporting_taxonomy_map',
     '/structure/reportingtaxonomymap/all/all/latest'),
    ('get_metadata_dsds', '/metadata/structure/datastructure/all/all/latest'),
    ('get_metadata_mdsds',
     '/metadata/structure/metadatastructure/all/all/latest'),
    ('get_metadata_dataflows', '/metadata/structure/dataflow/all/all/latest'),
    ('get_metadata_metadata_flows',
     '/metadata/structure/metadataflow/all/all/latest'),
    ('get_metadata_provision_agreements',
     '/metadata/structure/provisionagreement/all/all/latest'),
    ('get_metadata_structure_sets',
     '/metadata/structure/structureset/all/all/latest'),
    ('get_metadata_processes', '/metadata/structure/process/all/all/latest'),
    ('get_metadata_categorisations',
     '/metadata/structure/categorisation/all/all/latest'),
    ('get_metadata_data_constraints',
     '/metadata/structure/dataconstraint/all/all/latest'),
    ('get_metadata_metadata_constraints',
     '/metadata/structure/metadataconstraint/all/all/latest'),
    ('get_metadata_concept_schemes',
     '/metadata/structure/conceptscheme/all/all/latest'),
    ('get_metadata_code_lists', '/metadata/structure/codelist/all/all/latest'),
    ('get_metadata_category_schemes',
     '/metadata/structure/categoryscheme/all/all/latest'),
    (
        'get_metadata_hierarchies',
        '/metadata/structure/hierarchy/all/all/latest'),
    ('get_metadata_hierarchy_associations',
     '/metadata/structure/hierarchyassociation/all/all/latest'),
    ('get_metadata_agency_schemes',
     '/metadata/structure/agencyscheme/all/all/latest'),
    ('get_metadata_data_provider_schemes',
     '/metadata/structure/dataproviderscheme/all/all/latest'),
    ('get_metadata_data_consumer_schemes',
     '/metadata/structure/dataconsumerscheme/all/all/latest'),
    ('get_metadata_organisation_unit_schemes',
     '/metadata/structure/organisationunitscheme/all/all/latest'),
    ('get_metadata_transformation_schemes',
     '/metadata/structure/transformationscheme/all/all/latest'),
    ('get_metadata_ruleset_schemes',
     '/metadata/structure/rulesetscheme/all/all/latest'),
    ('get_metadata_user_defined_operator_schemes',
     '/metadata/structure/userdefinedoperatorscheme/all/all/latest'),
    ('get_metadata_custom_type_schemes',
     '/metadata/structure/customtypescheme/all/all/latest'),
    ('get_metadata_name_personalisation_schemes',
     '/metadata/structure/namepersonalisationscheme/all/all/latest'),
    ('get_metadata_vtl_mapping_schemes',
     '/metadata/structure/vtlmappingscheme/all/all/latest'),
    (
        'get_metadata_value_lists',
        '/metadata/structure/valuelist/all/all/latest'),
    ('get_metadata_structure_maps',
     '/metadata/structure/structuremap/all/all/latest'),
    ('get_metadata_representation_maps',
     '/metadata/structure/representationmap/all/all/latest'),
    ('get_metadata_concept_scheme_maps',
     '/metadata/structure/conceptschememap/all/all/latest'),
    ('get_metadata_category_scheme_maps',
     '/metadata/structure/categoryschememap/all/all/latest'),
    ('get_metadata_organisation_scheme_maps',
     '/metadata/structure/organisationschememap/all/all/latest'),
    ('get_metadata_reporting_taxonomy_maps',
     '/metadata/structure/reportingtaxonomymap/all/all/latest'),
    ('get_schema_datastructures', '/schema/datastructure/all/all/latest'),
    ('get_schema_meta_datastructures',
     '/schema/metadatastructure/all/all/latest'),
    ('get_schema_dataflows', '/schema/dataflow/all/all/latest'),
    ('get_schema_meta_dataflows', '/schema/metadataflow/all/all/latest'),
    ('get_schema_provision_agreements',
     '/schema/provisionagreement/all/all/latest')
]

params_item_queries_SdmxWs2p0 = [
    ('get_concept_scheme_item', '/structure/conceptscheme/all/all/latest/all'),
    ('get_codelist_item', '/structure/codelist/all/all/latest/all'),
    (
        'get_category_scheme_item',
        '/structure/categoryscheme/all/all/latest/all'),
    ('get_agency_scheme_item', '/structure/agencyscheme/all/all/latest/all'),
    ('get_data_provider_scheme_item',
     '/structure/dataproviderscheme/all/all/latest/all'),
    ('get_data_consumer_scheme_item',
     '/structure/dataconsumerscheme/all/all/latest/all'),
    ('get_organisation_unit_scheme_item',
     '/structure/organisationunitscheme/all/all/latest/all'),
    ('get_transformation_scheme_item',
     '/structure/transformationscheme/all/all/latest/all'),
    ('get_ruleset_scheme_item', '/structure/rulesetscheme/all/all/latest/all'),
    ('get_user_defined_operator_scheme_item',
     '/structure/userdefinedoperatorscheme/all/all/latest/all'),
    ('get_custom_type_scheme_item',
     '/structure/customtypescheme/all/all/latest/all'),
    ('get_name_personalisation_scheme_item',
     '/structure/namepersonalisationscheme/all/all/latest/all'),
    ('get_vtl_mapping_scheme_item',
     '/structure/vtlmappingscheme/all/all/latest/all'),
    ('get_value_list_item', '/structure/valuelist/all/all/latest/all')
]


def test_get_data_SdmxWs1(query_builder):
    query = query_builder.get_data(flow="example_flow", key="all",
                                   provider="all")
    assert query == "/data/example_flow/all/all"


def test_get_constraints_SdmxWs1(query_builder):
    query = query_builder.get_constraints(flow="example_flow", key="all",
                                          provider="all", component_id="all")
    assert query == "/availableconstraint/example_flow/all/all/all"


@mark.parametrize("method,expected", params_structure_queries_SdmxWs1)
def test_query_builder_structure_and_schema_queries(method, expected,
                                                    query_builder):
    query = getattr(query_builder, method)(agency_id="all", resources="all",
                                           version="latest")
    assert query == expected


@mark.parametrize("method,expected", params_item_queries_SdmxWs1)
def test_query_builder_item_queries_SdmxWs1(method, expected, query_builder):
    query = getattr(query_builder, method)(agency_id="all", resources="all",
                                           version="latest", item_id="all")
    assert query == expected


@mark.parametrize("method,expected", params_data_queries_SdmxWs2p0)
def test_query_builder_data_queries(method, expected, query_builder_ws2):
    query = getattr(query_builder_ws2, method)(agency_id="all", resources="all",
                                               version="latest", key="all")
    assert query == expected


@mark.parametrize("method,expected", params_data_constraints_queries_SdmxWs2p0)
def test_query_builder_constraints_queries(method, expected, query_builder_ws2):
    query = getattr(query_builder_ws2, method)(agency_id="all", resources="all",
                                               version="latest", key="all",
                                               component_id="all")
    assert query == expected


@mark.parametrize("method,expected",
                  params_structure_schema_queries_SdmxWs2p0)
def test_structure_schema_queries(method,
                                  expected,
                                  query_builder_ws2):
    query = getattr(query_builder_ws2, method)(agency_id="all", resources="all",
                                               version="latest")
    assert query == expected


@mark.parametrize("method,expected", params_item_queries_SdmxWs2p0)
def test_query_builder_item_queries_SdmxWs2p0(method, expected,
                                              query_builder_ws2):
    query = getattr(query_builder_ws2, method)(agency_id="all", resources="all",
                                               version="latest", item_id="all")
    assert query == expected


def test_get_metadata_metadataflow_query(query_builder_ws2):
    query = query_builder_ws2.get_metadata_metadataflow_query(agency_id="all",
                                                              resources="all",
                                                              version="latest",
                                                              provider_id="all")
    assert query == "/metadata/metadataflow/all/all/latest/all"


def test_get_metadata_metadataset_query(query_builder_ws2):
    query = query_builder_ws2.get_metadata_metadataset_query(provider_id="all",
                                                             resources="all",
                                                             version="latest", )
    assert query == "/metadata/metadataset/all/all/latest"


if __name__ == '__main__':
    pytest.main()
