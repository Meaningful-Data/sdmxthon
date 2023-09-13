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
                 end_period=None, updated_after=None,
                 first_n_observations=None, last_n_observations=None,
                 dimension_at_observation=None,
                 detail=None, include_history=None):
        """
        Returns query to retrieve data
        """

    @abstractmethod
    def get_dsds(self, resources, agency_id, version,
                 references=None, detail=None):
        """
        Returns query to get dsd
        """

    def validate_references(self, reference: str):
        """
        Validates that the refernce is one of the allowed values
        """

        if reference not in self.REFERENCES_OPTIONS:
            raise ValueError(f"refernce must be one of the following values: "
                             f"{self.REFERENCES_OPTIONS}")

    def validate_structural_detail(self, detail: str):
        """
        Validates that the detail is one of the allowed values
        """
        if detail not in self.STRUCTURE_DETAIL_OPTIONS:
            raise ValueError(f"detail must be one of the following values: "
                             f"{self.STRUCTURE_DETAIL_OPTIONS}")

    def validate_data_detail(self, detail: str):
        """
        Validates that the detail is one of the allwoed values
        """
        if detail not in self.DATA_DETAIL_OPTIONS:
            raise ValueError(f"detail must be one of the following values: "
                             f"{self.STRUCTURE_DETAIL_OPTIONS}")


class SdmxWs2p0(SdmxWebservice):
    """
    SDMX Web Service 2.0 specification
    """

    REFERENCES_OPTIONS = ['none', 'parents', 'parentsandsiblings',
                          'children', 'descendants', 'all']

    STRUCTURE_DETAIL_OPTIONS = ['allstubs', 'referencestubs',
                                'referencepartial',
                                'allcompletestubs', 'referencecompletestubs',
                                'full']

    def get_data_flows(self, agency_id, resources=None,
                       version=None, references=None, detail=None) -> str:
        resources = resources if resources else "all"
        version = version if version else "latest"

        base_query = f"dataflow/{agency_id}/{resources}/{version}"
        references_query = f"?references={references}" if references else ""
        detail_query = f"?detail={detail}" if detail else ""

        return base_query + references_query + detail_query

    def get_data(self, flow, key=None, provider=None, start_period=None,
                 end_period=None, updated_after=None,
                 first_n_observations=None, last_n_observations=None,
                 dimension_at_observation=None,
                 detail=None, include_history=None):
        raise NotImplementedError("get_data not implemented for SDMX 2.0")


class SdmxWs1(SdmxWebservice):
    """
    Generic Sdmx Ws 1 implementation for queries that do not change
    """

    REFERENCES_OPTIONS = ['none', 'parents', 'parentsandsiblings',
                          'children', 'descendants', 'all']

    STRUCTURE_DETAIL_OPTIONS = ['allstubs', 'referencestubs',
                                'referencepartial',
                                'allcompletestubs', 'referencecompletestubs',
                                'full']

    def get_data_flows(self, agency_id=None, resources=None,
                       version=None, references=None, detail=None) -> str:
        resources = resources if resources else "all"
        version = version if version else "latest"
        agency_id = agency_id if agency_id else "all"

        base_query = f"/dataflow/{agency_id}/{resources}/{version}"
        params = ""
        if references:
            params += f"?references={references}"
        if detail:
            params += f"?detail={detail}"

        return base_query + params

    def get_data(self, flow, key=None, provider=None, start_period=None,
                 end_period=None, updated_after=None,
                 first_n_observations=None, last_n_observations=None,
                 dimension_at_observation=None,
                 detail=None, include_history=None) -> str:
        key = key if key else 'all'
        provider = provider if provider else 'all'

        base_query = f"/data/{flow}/{key}/{provider}"

        params = ""
        if start_period:
            params += f"?startPeriod={start_period}"
        if end_period:
            params += f"?endPeriod={end_period}"
        if updated_after:
            params += f"?updatedAfter={updated_after}"
        if first_n_observations:
            params += f"?firstNObservations={first_n_observations}"
        if last_n_observations:
            params += f"?lastNObservations={last_n_observations}"
        if dimension_at_observation:
            params += f"?dimensionAtObservation={dimension_at_observation}"
        if detail:
            params += f"?detail={detail}"
        if include_history:
            params += f"?includeHistory={include_history}"

        return base_query + params

    def get_dsds(self, resources=None, agency_id=None, version=None,
                 references=None, detail=None):
        resources = resources if resources else "all"
        version = version if version else "latest"
        agency_id = agency_id if agency_id else "all"

        base_query = f"/datastructure/{agency_id}/{resources}/{version}"
        params = ""
        if references:
            params += f"?references={references}"
        if detail:
            params += f"?detail={detail}"

        return base_query + params


class SdmxWs1p5(SdmxWs1):
    """
    SDMX Web Service 1.5 specification
    """


class SdmxWs1p4(SdmxWs1):
    """
    SDMX Web Service 1.4 specification
    """


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

    def get_data_flows(self, agency_id=None, resources=None,
                       version=None, references=None, detail=None) -> str:
        "Returns the get data flows query for the WS Implementation"
        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"

        if references:
            self._ws_implementation.validate_references(references)
        if detail:
            self._ws_implementation.validate_structural_detail(detail)

        return self._ws_implementation.get_data_flows(
            agency_id, resources, version,
            references, detail)

    def get_dsds(self, agency_id=None, resources=None,
                 version=None, references=None, detail=None) -> str:
        "Returns the get data structures query for the WS Implementation"
        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"

        if references:
            self._ws_implementation.validate_references(references)
        if detail:
            self._ws_implementation.validate_structural_detail(detail)

        return self._ws_implementation.get_dsds(
            agency_id, resources, version,
            references, detail)

    def get_data(self, flow, key=None, provider=None, start_period=None,
                 end_period=None, updated_after=None,
                 first_n_observations=None, last_n_observations=None,
                 dimension_at_observation=None,
                 detail=None, include_history=None):
        "Returns the data query for the WS Implementation"

        provider = self.id_builder(provider)
        if detail:
            self._ws_implementation.validate_data_detail(detail)

        return self._ws_implementation.get_data(flow, key, provider,
                                                start_period, end_period,
                                                updated_after,
                                                first_n_observations,
                                                last_n_observations,
                                                dimension_at_observation,
                                                detail, include_history)
