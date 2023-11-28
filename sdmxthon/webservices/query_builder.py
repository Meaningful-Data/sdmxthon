"""
Module implementing the builder pattern for SDMX
Web-Service queries.
"""
from abc import ABC, abstractmethod


class SdmxWebservice(ABC):
    """
    Interface specifying the methods for creating the queries

    :param REFERENCES_OPTIONS: The allowed values for the references parameter
    :type REFERENCES_OPTIONS: list[str]

    :param STRUCTURE_DETAIL_OPTIONS: The allowed values for the detail parameter
    :type STRUCTURE_DETAIL_OPTIONS: list[str]

    :param DATA_DETAIL_OPTIONS: The allowed values for the detail parameter
    :type DATA_DETAIL_OPTIONS: list[str]

    :param CONSTRAINTS_MODE_OPTIONS: The allowed values for the mode parameter
    :type CONSTRAINTS_MODE_OPTIONS: list[str]
    """
    REFERENCES_OPTIONS = []
    STRUCTURE_DETAIL_OPTIONS = []
    DATA_DETAIL_OPTIONS = []
    CONSTRAINTS_MODE_OPTIONS = []

    @abstractmethod
    def get_data_flows(self, agency_id, resources,
                       version, references=None, detail=None) -> str:
        """
        Returns URL and params to get dataflows

        :param agency_id: The agency id of the dataflows
        :type agency_id: str

        :param resources: The resources to query
        :type resources: str

        :param version: The version of the dataflows
        :type version: str

        :param references: The references parameter (all, children, descendants)
        :type references: str

        :param detail: The detail parameter (full, referencestubs,
                       referencepartial, allstubs, allcompletestubs,
                       referencecompletestubs)
        :type detail: str
        """

    @abstractmethod
    def get_data(self, flow, key=None, provider=None, start_period=None,
                 end_period=None, updated_after=None,
                 first_n_observations=None, last_n_observations=None,
                 dimension_at_observation=None,
                 detail=None, include_history=None):
        """
        Returns URL and params to get data

        :param flow: The id of the dataflow
        :type flow: str

        :param key: The key is constructed as a dot ('.')
                    separated list of dimension filtered values.
        :type key: str

        :param provider: The provider of the dataflow
        :type provider: str

        :param start_period: The start period of the dataflow
        :type start_period: str

        :param end_period: The end period of the dataflow
        :type end_period: str

        :param updated_after: Data filtered by the last update date
        :type updated_after: str

        :param first_n_observations: Number of first observations to be returned
                                     per key
        :type first_n_observations: int

        :param last_n_observations: Number of last observations to be returned
                                    per key
        :type last_n_observations: int

        :param dimension_at_observation: The dimension at observation
                                         of the dataflow
        :type dimension_at_observation: str

        :param detail: The detail parameter (full, referencestubs,
                       referencepartial, allstubs, allcompletestubs,
                       referencecompletestubs)

        :param include_history: The include history of the dataflow
                                (true, false)
        :type include_history: str


        """

    @abstractmethod
    def get_dsds(self, resources, agency_id, version,
                 references=None, detail=None):
        """
        Returns URL and params to get the Data Structure Definitions

        :param resources: The resources to query
        :type resources: str

        :param agency_id: The agency id of the dataflows
        :type agency_id: str

        :param version: The version of the dataflows
        :type version: str

        :param references: The references parameter (all, children, descendants)
        :type references: str

        :param detail: The detail parameter (full, referencestubs,
                       referencepartial, allstubs, allcompletestubs,
                       referencecompletestubs)
        :type detail: str
        """

    @abstractmethod
    def get_constraints(self, flow, key=None, provider=None, component_id=None,
                        mode=None, references=None, start_period=None,
                        end_period=None, updated_after=None):
        """
        Returns URL and params to get the constraints

        :param flow: The id of the dataflow
        :type flow: str

        :param key: The key is constructed as a dot ('.')
                    separated list of dimension filtered values.
        :type key: str

        :param provider: The provider of the dataflow
        :type provider: str

        :param component_id: The component id of the dataflow
        :type component_id: str

        :param mode: The mode parameter (exact, available)
        :type mode: str

        :param references: The references parameter (all, children, descendants)
        :type references: str

        :param start_period: The start period of the dataflow
        :type start_period: str

        :param end_period: The end period of the dataflow
        :type end_period: str

        :param updated_after: Data filtered by the last update date
        :type updated_after: str
        """

    def validate_references(self, reference: str):
        """
        Validates that the reference is one of the allowed values
        """

        if reference not in self.REFERENCES_OPTIONS:
            raise ValueError(f"Reference must be one of the following values: "
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
        Validates that the detail is one of the allowed values
        """
        if detail not in self.DATA_DETAIL_OPTIONS:
            raise ValueError(f"detail must be one of the following values: "
                             f"{self.STRUCTURE_DETAIL_OPTIONS}")

    def validate_constraints_mode(self, mode: str):
        """
        Validates that the mode is one of the allowed values
        """
        if mode not in self.CONSTRAINTS_MODE_OPTIONS:
            raise ValueError(f"mode must be one of the following values: "
                             f"{self.CONSTRAINTS_MODE_OPTIONS}")


class SdmxWs2p0(SdmxWebservice):
    """
    SDMX Web Service 2.0 specification

    :param REFERENCES_OPTIONS: The allowed values for the references parameter
                            (none, parents, parentsandsiblings, children,
                            descendants, all)
    :type REFERENCES_OPTIONS: list[str]

    :param STRUCTURE_DETAIL_OPTIONS: The allowed values for the detail parameter
                            (allstubs, referencestubs, referencepartial,
                            allcompletestubs, referencecompletestubs, full)
    :type STRUCTURE_DETAIL_OPTIONS: list[str]

    :param DATA_DETAIL_OPTIONS: The allowed values for the detail parameter
    :type DATA_DETAIL_OPTIONS: list[str]
    """

    REFERENCES_OPTIONS = ['none', 'parents', 'parentsandsiblings',
                          'children', 'descendants', 'all']

    STRUCTURE_DETAIL_OPTIONS = ['allstubs', 'referencestubs',
                                'referencepartial',
                                'allcompletestubs', 'referencecompletestubs',
                                'full']

    def get_data_flows(self, agency_id, resources=None,
                       version=None, references=None, detail=None) -> str:
        """
        Returns URL and params to get dataflows

        :param agency_id: The agency id of the dataflows
        :param resources: The resources to query
        :param version: The version of the dataflows
        :param references: The references parameter (all, children, descendants)
        :param detail: The detail parameter (full, referencestubs,
                        referencepartial, allstubs, allcompletestubs,
                        referencecompletestubs)

        :return: The URL and params formatted
        """
        resources = resources if resources else "all"
        version = version if version else "latest"
        agency_id = agency_id if agency_id else "all"

        base_query = f"/structure/dataflow/{agency_id}/{resources}/{version}"

        params = ""
        if references:
            initial = "&" if "?" in params else "?"
            params += f"{initial}references={references}"
        if detail:
            initial = "&" if "?" in params else "?"
            params += f"{initial}detail={detail}"

        return base_query + params

    def get_data(self, dataflow_id, provider=None, version=None,
                 key=None,
                 start_period=None,
                 end_period=None, updated_after=None,
                 first_n_observations=None, last_n_observations=None,
                 dimension_at_observation=None,
                 detail=None, include_history=None):
        """
        Returns URL and params to get data

        :param dataflow_id: The id of the dataflow
        :param provider: The provider of the dataflow
        :param version: The version of the dataflow
        :param key: The key is constructed as a dot ('.') separated list of
                    dimension filtered values.
        :param start_period: Start period of the dataflow
        :param end_period: End period of the dataflow
        :param updated_after: Data filtered by the last update date
        :param first_n_observations: Number of first observations to be returned
                                     per key
        :param last_n_observations: Number of last observations to be returned
                                    per key
        :param dimension_at_observation: The dimension at observation
        :param detail: The detail parameter (full, referencestubs,
                        referencepartial, allstubs, allcompletestubs,
                        referencecompletestubs)
        :param include_history: Value to include history (true, false)
        :return: The URL and params formatted
        """
        base_query = f"/data/dataflow/{provider}/{dataflow_id}"
        base_query += f"/{version}" if version else ""

        base_query += f"/{key}" if key else ""

        params = ""
        if start_period:
            initial = "&" if "?" in params else "?"
            params += f"{initial}startPeriod={start_period}"
        if end_period:
            initial = "&" if "?" in params else "?"
            params += f"{initial}endPeriod={end_period}"
        if updated_after:
            initial = "&" if "?" in params else "?"
            params += f"{initial}updatedAfter={updated_after}"
        if first_n_observations:
            initial = "&" if "?" in params else "?"
            params += f"{initial}firstNObservations={first_n_observations}"
        if last_n_observations:
            initial = "&" if "?" in params else "?"
            params += f"{initial}lastNObservations={last_n_observations}"
        if dimension_at_observation:
            initial = "&" if "?" in params else "?"
            params += (f"{initial}dimensionAtObservation="
                       f"{dimension_at_observation}")
        if detail:
            initial = "&" if "?" in params else "?"
            params += f"{initial}detail={detail}"
        if include_history:
            initial = "&" if "?" in params else "?"
            params += f"{initial}includeHistory={include_history}"

        return base_query + params

    def get_constraints(self, flow, key=None, provider=None, component_id=None,
                        mode=None, references=None, start_period=None,
                        end_period=None, updated_after=None):
        pass

    def get_dsds(self, resources, agency_id, version, references=None,
                 detail=None):
        pass


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

    CONSTRAINTS_MODE_OPTIONS = ['exact', 'available']

    def get_data_flows(self, agency_id=None, resources=None,
                       version=None, references=None, detail=None) -> str:
        """
        Returns URL and params to get dataflows

        :param agency_id: The agency id of the dataflows
        :param resources: The resources to query
        :param version: The version of the dataflows
        :param references: The references parameter (all, children, descendants,
                            parents, parentsandsiblings)
        :param detail: The detail parameter (full, referencestubs,
                        referencepartial, allstubs, allcompletestubs,
                        referencecompletestubs)
        :return: The URL and params formatted
        """
        resources = resources if resources else "all"
        version = version if version else "latest"
        agency_id = agency_id if agency_id else "all"

        base_query = f"/dataflow/{agency_id}/{resources}/{version}"
        params = ""
        if references:
            initial = "&" if "?" in params else "?"
            params += f"{initial}references={references}"
        if detail:
            initial = "&" if "?" in params else "?"
            params += f"{initial}detail={detail}"

        return base_query + params

    def get_data(self, flow, key=None, provider=None, start_period=None,
                 end_period=None, updated_after=None,
                 first_n_observations=None, last_n_observations=None,
                 dimension_at_observation=None,
                 detail=None, include_history=None) -> str:
        """
        Returns URL and params to get data

        :param flow: The id of the dataflow
        :param key: The key is constructed as a dot ('.') separated list of
                    dimension filtered values.
        :param provider: The provider of the dataflow
        :param start_period: Start period of the dataflow
        :param end_period: End period of the dataflow
        :param updated_after: Data filtered by the last update date
        :param first_n_observations: Number of first observations to be returned
                                        per key (int)
        :param last_n_observations: Number of last observations to be returned
                                        per key (int)
        :param dimension_at_observation: The dimension at observation
        :param detail: The detail parameter (full, referencestubs,
                        referencepartial, allstubs, allcompletestubs,
                        referencecompletestubs)
        :param include_history: Value to include history (true, false)
        :return: The URL and params formatted
        """
        key = key if key else 'all'
        provider = provider if provider else 'all'

        base_query = f"/data/{flow}/{key}/{provider}"

        params = ""
        if start_period:
            initial = "&" if "?" in params else "?"
            params += f"{initial}startPeriod={start_period}"
        if end_period:
            initial = "&" if "?" in params else "?"
            params += f"{initial}endPeriod={end_period}"
        if updated_after:
            initial = "&" if "?" in params else "?"
            params += f"{initial}updatedAfter={updated_after}"
        if first_n_observations:
            initial = "&" if "?" in params else "?"
            params += f"{initial}firstNObservations={first_n_observations}"
        if last_n_observations:
            initial = "&" if "?" in params else "?"
            params += f"{initial}lastNObservations={last_n_observations}"
        if dimension_at_observation:
            initial = "&" if "?" in params else "?"
            params += (f"{initial}dimensionAtObservation="
                       f"{dimension_at_observation}")
        if detail:
            initial = "&" if "?" in params else "?"
            params += f"{initial}detail={detail}"
        if include_history:
            initial = "&" if "?" in params else "?"
            params += f"{initial}includeHistory={include_history}"

        return base_query + params

    def get_dsds(self, resources=None, agency_id=None, version=None,
                 references=None, detail=None):
        """
        Returns URL and params to get the Data Structure Definitions

        :param resources: The resources to query

        :param agency_id: The agency id of the dataflows

        :param version: The version of the dataflows

        :param references: The references parameter (all, children, descendants,
                            parents, parentsandsiblings)

        :param detail: The detail parameter (full, referencestubs,
                        referencepartial, allstubs, allcompletestubs,
                        referencecompletestubs)

        :return: The URL and params formatted
        """
        resources = resources if resources else "all"
        version = version if version else "latest"
        agency_id = agency_id if agency_id else "all"

        base_query = f"/datastructure/{agency_id}/{resources}/{version}"
        params = ""
        if references:
            initial = "&" if "?" in params else "?"
            params += f"{initial}references={references}"
        if detail:
            initial = "&" if "?" in params else "?"
            params += f"{initial}detail={detail}"

        return base_query + params

    def get_constraints(self, flow, key=None, provider=None, component_id=None,
                        mode=None, references=None, start_period=None,
                        end_period=None, updated_after=None):
        """
        Returns URL and params to get the constraints
        
        :param flow: The id of the dataflow

        :param key: The key is constructed as a dot ('.') separated list of
                    dimension filtered values.

        :param provider: The provider of the dataflow

        :param component_id: The component id of the dataflow

        :param mode: The mode parameter (exact, available)

        :param references: The references parameter (all, children, descendants,
                            parents, parentsandsiblings)

        :param start_period: The start period of the dataflow

        :param end_period: The end period of the dataflow

        :param updated_after: Data filtered by the last update date

        :return: The URL and params formatted
        """
        key = key if key else 'all'
        provider = provider if provider else 'all'
        component_id = component_id if component_id else 'all'

        base_query = f"/availableconstraint/{flow}/{key}"
        base_query += f"/{provider}/{component_id}"

        params = ""
        if mode:
            initial = "&" if "?" in params else "?"
            params += f"{initial}mode={mode}"
        if references:
            initial = "&" if "?" in params else "?"
            params += f"{initial}references={references}"
        if start_period:
            initial = "&" if "?" in params else "?"
            params += f"{initial}startPeriod={start_period}"
        if end_period:
            initial = "&" if "?" in params else "?"
            params += f"{initial}endPeriod={end_period}"
        if updated_after:
            initial = "&" if "?" in params else "?"
            params += f"{initial}updatedAfter={updated_after}"

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

    def get_data(self, flow, provider=None, detail=None, **kwargs):
        """Returns the data query for the WS Implementation"""

        provider = self.id_builder(provider)
        if detail:
            self._ws_implementation.validate_data_detail(detail)

        return self._ws_implementation.get_data(flow, provider=provider,
                                                detail=detail, **kwargs)

    def get_constraints(self, flow, key=None, provider=None, component_id=None,
                        mode=None, references=None, start_period=None,
                        end_period=None, updated_after=None):
        """Returns the constraints query for the WS Implementation"""
        provider = self.id_builder(provider)
        if mode:
            self._ws_implementation.validate_constraints_mode(mode)
        if references:
            self._ws_implementation.validate_references(references)

        return self._ws_implementation.get_constraints(flow, key, provider,
                                                       component_id, mode,
                                                       references,
                                                       start_period,
                                                       end_period,
                                                       updated_after)
