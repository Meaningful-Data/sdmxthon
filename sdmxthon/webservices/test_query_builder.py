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


def test_get_data_flows_with_references(query_builder):
    query = query_builder.get_data_flows(agency_id="ABS", resources="all", version="latest", references="parents")
    assert query == "/dataflow/ABS/all/latest?references=parents"


def test_get_data_flows_with_detail(query_builder):
    query = query_builder.get_data_flows(agency_id="ABS", resources="all", version="latest", detail="allstubs")
    assert query == "/dataflow/ABS/all/latest?detail=allstubs"


def test_get_data_with_start_and_end_period(query_builder):
    query = query_builder.get_data(flow="example_flow", start_period="20220101", end_period="20221231")
    assert query == "/data/example_flow/all/all?startPeriod=20220101&endPeriod=20221231"


def test_get_data_with_updated_after(query_builder):
    query = query_builder.get_data(flow="example_flow", updated_after="20220101")
    assert query == "/data/example_flow/all/all?updatedAfter=20220101"


def test_get_data_with_multiple_parameters(query_builder):
    query = query_builder.get_data(flow="example_flow", key="example_key", provider="example_provider",
                                   start_period="20220101", end_period="20221231", updated_after="20220101",
                                   first_n_observations=100, detail="full", include_history="true")
    assert query == ("/data/example_flow/example_key/example_provider?startPeriod=20220101&endPeriod=20221231"
                     "&updatedAfter=20220101&firstNObservations=100&detail=full&includeHistory=true")


def test_get_data_with_detail_parameter(query_builder):
    query = query_builder.get_data(flow="example_flow", key="all", provider="all", detail="full")
    assert query == "/data/example_flow/all/all?detail=full"


def test_get_dsds_with_references_and_detail(query_builder):
    query = query_builder.get_dsds(agency_id="all", resources="all", version="latest", references="all", detail="full")
    assert query == "/datastructure/all/all/latest?references=all&detail=full"


def test_get_constraints_with_mode(query_builder):
    query = query_builder.get_constraints(flow="example_flow", key="all", provider="all", component_id="all",
                                          mode="available")
    assert query == "/availableconstraint/example_flow/all/all/all?mode=available"


def test_get_constraints_with_references(query_builder):
    query = query_builder.get_constraints(flow="example_flow", references="all")
    assert query == "/availableconstraint/example_flow/all/all/all?references=all"


def test_get_constraints_with_start_and_end_period(query_builder):
    query = query_builder.get_constraints(flow="example_flow", start_period="20220101", end_period="20221231")
    assert query == "/availableconstraint/example_flow/all/all/all?startPeriod=20220101&endPeriod=20221231"


def test_get_constraints_with_multiple_parameters(query_builder):
    query = query_builder.get_constraints(flow="example_flow", key="example_key", provider="example_provider",
                                          component_id="example_component", mode="available", references="none",
                                          start_period="20220101", end_period="20221231", updated_after="20220101")
    assert query == ("/availableconstraint/example_flow/example_key/example_provider/example_component?mode=available"
                     "&references=none&startPeriod=20220101&endPeriod=20221231&updatedAfter=20220101")


def test_get_mdsds_with_references_and_detail(query_builder):
    query = query_builder.get_mdsds(agency_id="BIS", resources="all", version="latest", references="all", detail="full")
    assert query == "/metadatastructure/BIS/all/latest?references=all&detail=full"


if __name__ == '__main__':
    pytest.main()
