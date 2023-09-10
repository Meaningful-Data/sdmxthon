"""
Module implementing the builder pattern for SDMX
Web-Service queries.
"""
from abc import ABC, abstractmethod


class SdmxWebservice(ABC):
    """
    Interface specifying the methods for creating the queries
    """
    REFERENCES_OPTIONS = []
    STRUCTURE_DETAIL_OPTIONS = []
    DATA_DETAIL_OPTIONS = []

    @abstractmethod
    def get_data_flows(self, agency_id, resources, 
                       version, references=None, detail=None) -> str:
        """
        Returns query to retrieve data flows
        """

    @abstractmethod
    def get_data(self, flow, key=None, provider=None, start_period=None,
                 end_period=None, updated_after=None, first_n_observations=None,
                 last_n_observations=None, dimension_at_observation=None,
                 detail=None, include_history=None):
        """
        Returns query to retrieve data
        """

    def validate_references(self, reference:str):
        """
        Validates that the refernce is one of the allowed values
        """

        if reference not in self.REFERENCES_OPTIONS:
            raise ValueError(f"refernce must be one of the following values: {self.REFERENCES_OPTIONS}")

    def validate_structural_detail(self, detail:str):
        """
        Validates that the detail is one of the allowed values
        """
        if detail not in self.STRUCTURE_DETAIL_OPTIONS:
            raise ValueError(f"detail must be one of the following values: {self.STRUCTURE_DETAIL_OPTIONS}")

    def validate_data_detail(self, detail:str):
        """
        Validates that the detail is one of the allwoed values
        """
        if detail not in self.DATA_DETAIL_OPTIONS:
            raise ValueError(f"detail must be one of the following values: {self.STRUCTURE_DETAIL_OPTIONS}")

class SdmxWs2_0(SdmxWebservice):
    """
    SDMX Web Service 2.0 specification
    """

    REFERENCES_OPTIONS = ['none', 'parents', 'parentsandsiblings',
                          'children', 'descendants', 'all']

    STRUCTURE_DETAIL_OPTIONS = ['allstubs', 'referencestubs', 'referencepartial',
                      'allcompletestubs', 'referencecompletestubs',
                      'full']

    def get_data_flows(self, agency_id, resources=None,
                       version=None, references=None, detail=None) -> str:

        resources = resources if resources else "all"
        version = version if version else "latest"

        base_query = f"dataflow/{agency_id}/{resources}/{version}"
        references_query = f"?references={references}" if references else ""
        detail_query = f"?detail={detail}" if detail else ""

        return base_query + references_query +detail_query


    def get_data(self, flow, key=None, provider=None, start_period=None,
                 end_period=None, updated_after=None, first_n_observations=None,
                 last_n_observations=None, dimension_at_observation=None,
                 detail=None, include_history=None):

        key = key if key else 'all'
        provider = provider if provider else 'all'

        base_query = f"data/{flow}/{key}/{provider}"
        start_period_query = f"?startPeriod={start_period}" if start_period else ""
        end_period_query = f"?endPeriod={end_period}" if end_period else ""
        updated_after_query = f"?updatedAfter={updated_after}" if updated_after else ""
        first_n_observations_query = f"?firstNObservations={first_n_observations}" if first_n_observations else ""
        last_n_observations_query = f"?lastNObservations={last_n_observations}" if last_n_observations else ""
        dimension_at_observation_query = f"?dimensionAtObservation={dimension_at_observation}" if dimension_at_observation else ""
        detail_query = f"?detail={detail}" if detail else ""
        include_history_query = f"?includeHistory={include_history}" if include_history else ""

        return base_query + start_period_query + end_period_query + \
            updated_after_query + first_n_observations_query + \
            last_n_observations_query + dimension_at_observation_query +\
            detail_query + include_history_query


class SdmxWs1_5(SdmxWebservice):
    """
    SDMX Web Service 1.5 specification
    """

    REFERENCES_OPTIONS = ['none', 'parents', 'parentsandsiblings',
                          'children', 'descendants', 'all']

    STRUCTURE_DETAIL_OPTIONS = ['allstubs', 'referencestubs', 'referencepartial',
                      'allcompletestubs', 'referencecompletestubs',
                      'full']

    def get_data_flows(self, agency_id, resources=None,
                       version=None, references=None, detail=None) -> str:

        resources = resources if resources else "all"
        version = version if version else "latest"

        base_query = f"dataflow/{agency_id}/{resources}/{version}"
        references_query = f"?references={references}" if references else ""
        detail_query = f"?detail={detail}" if detail else ""

        return base_query + references_query +detail_query


    def get_data(self, flow, key=None, provider=None, start_period=None,
                 end_period=None, updated_after=None, first_n_observations=None,
                 last_n_observations=None, dimension_at_observation=None,
                 detail=None, include_history=None):
        pass


class SdmxWs1_4(SdmxWebservice):
    """
    SDMX Web Service 1.4 specification
    """

    REFERENCES_OPTIONS = ['none', 'parents', 'parentsandsiblings',
                          'children', 'descendants', 'all']

    STRUCTURE_DETAIL_OPTIONS = ['allstubs', 'referencestubs', 'referencepartial',
                      'allcompletestubs', 'referencecompletestubs',
                      'full']

    def get_data_flows(self, agency_id, resources=None,
                       version=None, references=None, detail=None) -> str:

        resources = resources if resources else "all"
        version = version if version else "latest"

        base_query = f"dataflow/{agency_id}/{resources}/{version}"
        references_query = f"?references={references}" if references else ""
        detail_query = f"?detail={detail}" if detail else ""

        return base_query + references_query +detail_query


    def get_data(self, flow, key=None, provider=None, start_period=None,
                 end_period=None, updated_after=None, first_n_observations=None,
                 last_n_observations=None, dimension_at_observation=None,
                 detail=None, include_history=None):
        pass

class QueryBuilder:
    """
    Class implementing the director in the builder pattern
    """

    def __init__(self, ws_implementation):
        if not isinstance(ws_implementation, SdmxWebservice):
            raise TypeError("QueryBuilder requies an SdmxWebservice object")
        self._ws_implementation = ws_implementation


    def id_builder(self, ids=None) -> str:
        "returns the string for the list of resources ids"
        if isinstance(ids, str):
            return ids
        if isinstance(ids, list):
            return "+".join(ids)
        if not ids:
            return "all"
        raise TypeError("Ids has to be string, list or None")


    def get_data_flows(self, agency_id, resources=None, 
                       version=None, references=None, detail=None) -> str:
        "Returns the get data flows query for the WS Implementation"
        resources = self.id_builder(resources)

        if references:
            self._ws_implementation.validate_references(references)
        if detail:
            self._ws_implementation.validate_structural_detail(detail)

        return self._ws_implementation.get_data_flows(
            agency_id, resources, version,
            references, detail)

    def get_data(self, flow, key=None, provider=None, start_period=None,
                 end_period=None, updated_after=None, first_n_observations=None,
                 last_n_observations=None, dimension_at_observation=None,
                 detail=None, include_history=None):
        "Returns the data query for the WS Implementation"

        provider = self.id_builder(provider)
        if detail:
            self._ws_implementation.validate_data_detail(detail)

        return self._ws_implementation.get_data(flow, key,provider,
            start_period,end_period, updated_after, first_n_observations, 
            last_n_observations, dimension_at_observation, detail, include_history)

if __name__ == "__main__":
    query_builder = QueryBuilder(SdmxWs2_0())
    print(query_builder.get_data_flows('ECB'))
    print(query_builder.get_data_flows('ECB', 'DF1'))
    print(query_builder.get_data_flows('ECB', ['DF1', 'DF2']))

    print(query_builder.get_data_flows('ECB', ['DF1', 'DF2'], references = 'descendants'))
    print(query_builder.get_data_flows('ECB', ['DF1', 'DF2'], references = 'descendants', detail='full'))
    print(query_builder.get_data('flow1'))

    # print(query_builder.get_data_flows('ECB', ['DF1', 'DF2'], references = 'abc'))
