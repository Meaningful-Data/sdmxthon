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
    DATA_HISTORY_OPTIONS = []
    CONSTRAINTS_MODE_OPTIONS = []
    CONSTRAINTS_REFERENCES_OPTIONS = []

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

    @abstractmethod
    def get_mdsds(self, agency_id, resources, version,
                  references=None, detail=None):
        """
        Returns query to get mdsd
        """

    @abstractmethod
    def get_meta_data_flows(self, agency_id, resources,
                            version, references=None, detail=None) -> str:
        """
        Returns query to retrieve metadata flows
        """

    @abstractmethod
    def get_provision_agreements(self, agency_id, resources,
                                 version, references=None, detail=None) -> str:
        """
        Returns query to retrieve provision agreements
        """

    @abstractmethod
    def get_structure_sets(self, agency_id, resources,
                           version, references=None, detail=None) -> str:
        """
        Returns query to retrieve structure sets
        """

    @abstractmethod
    def get_process(self, agency_id, resources,
                    version, references=None, detail=None) -> str:
        """
        Returns query to retrieve processes
        """

    @abstractmethod
    def get_categorisation(self, agency_id, resources,
                           version, references=None, detail=None) -> str:
        """
        Returns query to retrieve categorisations
        """

    @abstractmethod
    def get_data_constraint(self, agency_id, resources,
                            version, references=None, detail=None) -> str:
        """
        Returns query to retrieve data constraints (V2.0.0)
        """

    @abstractmethod
    def get_metadata_constraint(self, agency_id, resources,
                                version, references=None, detail=None) -> str:
        """
        Returns query to retrieve metadata constraints (V2.0.0)
        """

    @abstractmethod
    def get_content_constraint(self, agency_id, resources,
                               version, references=None, detail=None) -> str:
        """
        Returns query to retrieve content constraints
        """

    @abstractmethod
    def get_actual_constraint(self, agency_id, resources,
                              version, references=None, detail=None) -> str:
        """
        Returns query to retrieve actual constraints
        """

    @abstractmethod
    def get_allowed_constraint(self, agency_id, resources,
                               version, references=None, detail=None) -> str:
        """
        Returns query to retrieve allowed constraints
        """

    @abstractmethod
    def get_attachment_constraint(self, agency_id, resources,
                                  version, references=None, detail=None) -> str:
        """
        Returns query to retrieve attachment constraints
        """

    @abstractmethod
    def get_structure(self, agency_id, resources,
                      version, references=None, detail=None) -> str:
        """
        Returns query to retrieve structure
        """

    @abstractmethod
    def get_concept_scheme(self, agency_id, resources,
                           version, references=None, detail=None) -> str:
        """
        Returns query to retrieve concept schemes
        """

    @abstractmethod
    def get_code_list(self, agency_id, resources,
                      version, references=None, detail=None) -> str:
        """
        Returns query to retrieve codelists
        """

    @abstractmethod
    def get_category_scheme(self, agency_id, resources,
                            version, references=None, detail=None) -> str:
        """
        Returns query to retrieve category schemes
        """

    @abstractmethod
    def get_hierarchy(self, agency_id, resources,
                      version, references=None, detail=None) -> str:
        """
        Returns query to retrieve hierarchies (V2.0.0)
        """

    @abstractmethod
    def get_hierarchy_association(self, agency_id, resources,
                                  version, references=None, detail=None) -> str:
        """
        Returns query to retrieve hierarchy associations (V2.0.0)
        """

    @abstractmethod
    def get_hierarchical_codelist(self, agency_id, resources,
                                  version, references=None, detail=None) -> str:
        """
        Returns query to retrieve hierarchical codelists
        """

    @abstractmethod
    def get_organisation_scheme(self, agency_id, resources,
                                version, references=None, detail=None) -> str:
        """
        Returns query to retrieve organisation schemes
        """

    @abstractmethod
    def get_agency_scheme(self, agency_id, resources,
                          version, references=None, detail=None) -> str:
        """
        Returns query to retrieve agency schemes
        """

    @abstractmethod
    def get_data_provider_scheme(self, agency_id, resources,
                                 version, references=None, detail=None) -> str:
        """
        Returns query to retrieve data provider schemes
        """

    @abstractmethod
    def get_data_consumer_scheme(self, agency_id, resources,
                                 version, references=None, detail=None) -> str:
        """
        Returns query to retrieve data consumer schemes
        """

    @abstractmethod
    def get_organisation_unit_scheme(self, agency_id, resources,
                                     version, references=None, detail=None) -> str:
        """
        Returns query to retrieve organisation unit schemes
        """

    @abstractmethod
    def get_transformation_scheme(self, agency_id, resources,
                                  version, references=None, detail=None) -> str:
        """
        Returns query to retrieve transformation schemes
        """

    @abstractmethod
    def get_ruleset_scheme(self, agency_id, resources,
                           version, references=None, detail=None) -> str:
        """
        Returns query to retrieve ruleset schemes
        """

    @abstractmethod
    def get_user_defined_operator_scheme(self, agency_id, resources,
                                         version, references=None, detail=None) -> str:
        """
        Returns query to retrieve user defined operator schemes
        """

    @abstractmethod
    def get_custom_type_scheme(self, agency_id, resources,
                               version, references=None, detail=None) -> str:
        """
        Returns query to retrieve custom type schemes
        """

    @abstractmethod
    def get_name_personalisation_scheme(self, agency_id, resources,
                                        version, references=None, detail=None) -> str:
        """
        Returns query to retrieve name personalisation schemes
        """

    @abstractmethod
    def get_vtl_mapping_scheme(self, agency_id, resources,
                               version, references=None, detail=None) -> str:
        """
        Returns query to retrieve vtl mapping schemes (V2.0.0)
        """

    @abstractmethod
    def get_value_list(self, agency_id, resources,
                       version, references=None, detail=None) -> str:
        """
        Returns query to retrieve value lists (V2.0.0)
        """

    @abstractmethod
    def get_structure_map(self, agency_id, resources,
                          version, references=None, detail=None) -> str:
        """
        Returns query to retrieve structure maps (V2.0.0)
        """

    @abstractmethod
    def get_representation_map(self, agency_id, resources,
                               version, references=None, detail=None) -> str:
        """
        Returns query to retrieve representation maps (V2.0.0)
        """

    @abstractmethod
    def get_concept_scheme_map(self, agency_id, resources,
                               version, references=None, detail=None) -> str:
        """
        Returns query to retrieve concept scheme maps (V2.0.0)
        """

    @abstractmethod
    def get_category_scheme_map(self, agency_id, resources,
                                version, references=None, detail=None) -> str:
        """
        Returns query to retrieve category scheme maps (V2.0.0)
        """

    @abstractmethod
    def get_organisation_scheme_map(self, agency_id, resources,
                                    version, references=None, detail=None) -> str:
        """
        Returns query to retrieve organisation scheme maps (V2.0.0)
        """

    @abstractmethod
    def get_reporting_taxonomy_map(self, agency_id, resources,
                                   version, references=None, detail=None) -> str:
        """
        Returns query to retrieve reporting taxonomy maps (V2.0.0)
        """

    @abstractmethod
    def get_name_alias_scheme(self, agency_id, resources,
                              version, references=None, detail=None) -> str:
        """
        Returns query to retrieve name alias schemes
        """

    @abstractmethod
    def get_concepts(self, agency_id, resources,
                     version, item_id, references=None, detail=None) -> str:
        """
        Returns query to retrieve concepts
        """

    @abstractmethod
    def get_codes(self, agency_id, resources,
                  version, item_id, references=None, detail=None) -> str:
        """
        Returns query to retrieve codes
        """

    @abstractmethod
    def get_categories(self, agency_id, resources,
                       version, item_id, references=None, detail=None) -> str:
        """
        Returns query to retrieve categories
        """

    @abstractmethod
    def get_hierarchies(self, agency_id, resources,
                        version, item_id, references=None, detail=None) -> str:
        """
        Returns query to retrieve hierarchies
        """

    @abstractmethod
    def get_organisations(self, agency_id, resources,
                          version, item_id, references=None, detail=None) -> str:
        """
        Returns query to retrieve organisations
        """

    @abstractmethod
    def get_agencies(self, agency_id, resources,
                     version, item_id, references=None, detail=None) -> str:
        """
        Returns query to retrieve agencies
        """

    @abstractmethod
    def get_data_providers(self, agency_id, resources,
                           version, item_id, references=None, detail=None) -> str:
        """
        Returns query to retrieve data providers
        """

    @abstractmethod
    def get_data_consumers(self, agency_id, resources,
                           version, item_id, references=None, detail=None) -> str:
        """
        Returns query to retrieve data consumers
        """

    @abstractmethod
    def get_organisation_unit_schemes(self, agency_id, resources,
                                      version, item_id, references=None, detail=None) -> str:
        """
        Returns query to retrieve get organisation unit schemes
        """

    @abstractmethod
    def get_transformation_schemes(self, agency_id, resources,
                                   version, item_id, references=None, detail=None) -> str:
        """
        Returns query to retrieve get transformation schemes
        """

    @abstractmethod
    def get_ruleset_schemes(self, agency_id, resources,
                            version, item_id, references=None, detail=None) -> str:
        """
        Returns query to retrieve get ruleset schemes
        """

    @abstractmethod
    def get_user_defined_operator_schemes(self, agency_id, resources,
                                          version, item_id, references=None, detail=None) -> str:
        """
        Returns query to retrieve get user defined operator schemes
        """

    @abstractmethod
    def get_custom_type_schemes(self, agency_id, resources,
                                version, item_id, references=None, detail=None) -> str:
        """
        Returns query to retrieve get custom type schemes
        """

    @abstractmethod
    def get_name_personalisation_schemes(self, agency_id, resources,
                                         version, item_id, references=None, detail=None) -> str:
        """
        Returns query to retrieve get name personalisation schemes
        """

    @abstractmethod
    def get_name_alias_schemes(self, agency_id, resources,
                               version, item_id, references=None, detail=None) -> str:
        """
        Returns query to retrieve get name alias schemes
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
                             f"{self.DATA_DETAIL_OPTIONS}")

    def validate_data_history(self, include_history: str):
        """
        Validates that the includeHistory is one of the allowed options
        """
        if include_history not in self.DATA_HISTORY_OPTIONS:
            raise ValueError(f"includeHistory must be one of the following options: "
                             f"{self.DATA_HISTORY_OPTIONS}")

    def validate_constraints_mode(self, mode: str):
        """
        Validates that the mode is one of the allowed values
        """
        if mode not in self.CONSTRAINTS_MODE_OPTIONS:
            raise ValueError(f"mode must be one of the following values: "
                             f"{self.CONSTRAINTS_MODE_OPTIONS}")

    def validate_constraints_references(self, references: str):
        """
        Validates that the references constraints is one of the allowed values
        """
        if references not in self.CONSTRAINTS_REFERENCES_OPTIONS:
            raise ValueError(f"references constraints must be one of the following values: "
                             f"{self.CONSTRAINTS_REFERENCES_OPTIONS}")


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

    def common_structure_queries(self, query, agency_id=None, resources=None,
                                 version=None, references=None, detail=None) -> str:
        agency_id = agency_id if agency_id else "all"
        resources = resources if resources else "all"
        version = version if version else "latest"

        base_query = f"/structure/{query}/{agency_id}/{resources}/{version}"
        params = ""
        if references:
            initial = "&" if "?" in params else "?"
            params += f"{initial}references={references}"
        if detail:
            initial = "&" if "?" in params else "?"
            params += f"{initial}detail={detail}"

        return base_query + params

    def get_data_flows(self, agency_id=None, resources=None,
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
        return self.common_structure_queries("dataflow", agency_id, resources,
                                             version, references, detail)

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

    def get_dsds(self, agency_id=None, resources=None,
                 version=None, references=None, detail=None) -> str:

        """
        Returns URL and params to get datastructure

        :param agency_id: The agency id of the data structure definitions
        :param resources: The resources to query
        :param version: The version of the data structure definitions
        :param references: The references parameter (all, children, descendants)
        :param detail: The detail parameter (full, referencestubs,
                        referencepartial, allstubs, allcompletestubs,
                        referencecompletestubs)

        :return: The URL and params formatted
        """

        return self.common_structure_queries("datastructure", agency_id, resources,
                                             version, references, detail)

    def get_mdsds(self, agency_id=None, resources=None,
                  version=None, references=None, detail=None) -> str:

        """
        Returns URL and params to get metadata structure definitions

        :param agency_id: The agency id of metadata structure definitions
        :param resources: The resources to query
        :param version: The version of the metadata structure definitions
        :param references: The references parameter (all, children, descendants)
        :param detail: The detail parameter (full, referencestubs,
                        referencepartial, allstubs, allcompletestubs,
                        referencecompletestubs)

        :return: The URL and params formatted
        """

        return self.common_structure_queries("metadatastructure", agency_id, resources,
                                             version, references, detail)

    def get_meta_data_flows(self, agency_id=None, resources=None,
                            version=None, references=None, detail=None) -> str:

        """
        Returns URL and params to get metadata_flows

        :param agency_id: The agency id of metadata_flows
        :param resources: The resources to query
        :param version: The version of the metadata_flows
        :param references: The references parameter (all, children, descendants)
        :param detail: The detail parameter (full, referencestubs,
                        referencepartial, allstubs, allcompletestubs,
                        referencecompletestubs)

        :return: The URL and params formatted
        """

        return self.common_structure_queries("metadataflow", agency_id, resources,
                                             version, references, detail)

    def get_provision_agreements(self, agency_id=None, resources=None,
                                 version=None, references=None, detail=None) -> str:

        """
        Returns URL and params to get provision agreements

        :param agency_id: The agency id of provision agreements
        :param resources: The resources to query
        :param version: The version of the provision agreements
        :param references: The references parameter (all, children, descendants)
        :param detail: The detail parameter (full, referencestubs,
                        referencepartial, allstubs, allcompletestubs,
                        referencecompletestubs)

        :return: The URL and params formatted
        """

        return self.common_structure_queries("provisionagreement", agency_id, resources,
                                             version, references, detail)

    def get_structure_sets(self, agency_id=None, resources=None,
                           version=None, references=None, detail=None) -> str:

        """
        Returns URL and params to get structure sets

        :param agency_id: The agency id of structure sets
        :param resources: The resources to query
        :param version: The version of the structure sets
        :param references: The references parameter (all, children, descendants)
        :param detail: The detail parameter (full, referencestubs,
                        referencepartial, allstubs, allcompletestubs,
                        referencecompletestubs)

        :return: The URL and params formatted
        """

        return self.common_structure_queries("structureset", agency_id, resources,
                                             version, references, detail)

    def get_process(self, agency_id=None, resources=None,
                    version=None, references=None, detail=None) -> str:

        """
        Returns URL and params to get processes

        :param agency_id: The agency id of processes
        :param resources: The resources to query
        :param version: The version of the processes
        :param references: The references parameter (all, children, descendants)
        :param detail: The detail parameter (full, referencestubs,
                        referencepartial, allstubs, allcompletestubs,
                        referencecompletestubs)

        :return: The URL and params formatted
        """

        return self.common_structure_queries("process", agency_id, resources,
                                             version, references, detail)

    def get_categorisation(self, agency_id=None, resources=None,
                           version=None, references=None, detail=None) -> str:

        """
        Returns URL and params to get categorisations

        :param agency_id: The agency id of categorisations
        :param resources: The resources to query
        :param version: The version of the categorisations
        :param references: The references parameter (all, children, descendants)
        :param detail: The detail parameter (full, referencestubs,
                        referencepartial, allstubs, allcompletestubs,
                        referencecompletestubs)

        :return: The URL and params formatted
        """

        return self.common_structure_queries("categorisation", agency_id, resources,
                                             version, references, detail)

    def get_content_constraint(self, agency_id=None, resources=None,
                               version=None, references=None, detail=None) -> str:
        pass

    def get_actual_constraint(self, agency_id=None, resources=None,
                              version=None, references=None, detail=None) -> str:
        pass

    def get_allowed_constraint(self, agency_id=None, resources=None,
                               version=None, references=None, detail=None) -> str:
        pass

    def get_attachment_constraint(self, agency_id=None, resources=None,
                                  version=None, references=None, detail=None) -> str:
        pass

    def get_data_constraint(self, agency_id=None, resources=None,
                            version=None, references=None, detail=None) -> str:

        """
        Returns URL and params to get data constraints

        :param agency_id: The agency id of data constraints
        :param resources: The resources to query
        :param version: The version of the data constraints
        :param references: The references parameter (all, children, descendants)
        :param detail: The detail parameter (full, referencestubs,
                        referencepartial, allstubs, allcompletestubs,
                        referencecompletestubs)

        :return: The URL and params formatted
        """

        return self.common_structure_queries("dataconstraint", agency_id, resources,
                                             version, references, detail)

    def get_metadata_constraint(self, agency_id=None, resources=None,
                                version=None, references=None, detail=None) -> str:

        """
        Returns URL and params to get metadata constraints

        :param agency_id: The agency id of metadata constraints
        :param resources: The resources to query
        :param version: The version of the metadata constraints
        :param references: The references parameter (all, children, descendants)
        :param detail: The detail parameter (full, referencestubs,
                        referencepartial, allstubs, allcompletestubs,
                        referencecompletestubs)

        :return: The URL and params formatted
        """

        return self.common_structure_queries("metadataconstraint", agency_id, resources,
                                             version, references, detail)

    def get_structure(self, agency_id=None, resources=None,
                      version=None, references=None, detail=None) -> str:
        pass

    def get_concept_scheme(self, agency_id=None, resources=None,
                           version=None, references=None, detail=None) -> str:

        """
        Returns URL and params to get concept schemes

        :param agency_id: The agency id of concept schemes
        :param resources: The resources to query
        :param version: The version of the concept schemes
        :param references: The references parameter (all, children, descendants)
        :param detail: The detail parameter (full, referencestubs,
                        referencepartial, allstubs, allcompletestubs,
                        referencecompletestubs)

        :return: The URL and params formatted
        """

        return self.common_structure_queries("conceptscheme", agency_id, resources,
                                             version, references, detail)

    def get_code_list(self, agency_id=None, resources=None,
                      version=None, references=None, detail=None) -> str:

        """
        Returns URL and params to get codelists

        :param agency_id: The agency id of codelists
        :param resources: The resources to query
        :param version: The version of the codelists
        :param references: The references parameter (all, children, descendants)
        :param detail: The detail parameter (full, referencestubs,
                        referencepartial, allstubs, allcompletestubs,
                        referencecompletestubs)

        :return: The URL and params formatted
        """

        return self.common_structure_queries("codelist", agency_id, resources,
                                             version, references, detail)

    def get_category_scheme(self, agency_id=None, resources=None,
                            version=None, references=None, detail=None) -> str:

        """
        Returns URL and params to get category schemes

        :param agency_id: The agency id of category schemes
        :param resources: The resources to query
        :param version: The version of the category schemes
        :param references: The references parameter (all, children, descendants)
        :param detail: The detail parameter (full, referencestubs,
                        referencepartial, allstubs, allcompletestubs,
                        referencecompletestubs)

        :return: The URL and params formatted
        """

        return self.common_structure_queries("categoryscheme", agency_id, resources,
                                             version, references, detail)

    def get_hierarchical_codelist(self, agency_id=None, resources=None,
                                  version=None, references=None, detail=None) -> str:
        pass

    def get_hierarchy(self, agency_id=None, resources=None,
                      version=None, references=None, detail=None) -> str:

        """
        Returns URL and params to get hierarchy

        :param agency_id: The agency id of hierarchy
        :param resources: The resources to query
        :param version: The version of the hierarchy
        :param references: The references parameter (all, children, descendants)
        :param detail: The detail parameter (full, referencestubs,
                        referencepartial, allstubs, allcompletestubs,
                        referencecompletestubs)

        :return: The URL and params formatted
        """

        return self.common_structure_queries("hierarchy", agency_id, resources,
                                             version, references, detail)

    def get_hierarchy_association(self, agency_id=None, resources=None,
                                  version=None, references=None, detail=None) -> str:

        """
        Returns URL and params to get hierarchy association

        :param agency_id: The agency id of hierarchy association
        :param resources: The resources to query
        :param version: The version of the hierarchy association
        :param references: The references parameter (all, children, descendants)
        :param detail: The detail parameter (full, referencestubs,
                        referencepartial, allstubs, allcompletestubs,
                        referencecompletestubs)

        :return: The URL and params formatted
        """

        return self.common_structure_queries("hierarchyassociation", agency_id, resources,
                                             version, references, detail)

    def get_organisation_scheme(self, agency_id=None, resources=None,
                                version=None, references=None, detail=None) -> str:
        pass

    def get_agency_scheme(self, agency_id=None, resources=None,
                          version=None, references=None, detail=None) -> str:

        """
        Returns URL and params to get agency schemes

        :param agency_id: The agency id of agency schemes
        :param resources: The resources to query
        :param version: The version of the agency schemes
        :param references: The references parameter (all, children, descendants)
        :param detail: The detail parameter (full, referencestubs,
                        referencepartial, allstubs, allcompletestubs,
                        referencecompletestubs)

        :return: The URL and params formatted
        """

        return self.common_structure_queries("agencyscheme", agency_id, resources,
                                             version, references, detail)

    def get_data_provider_scheme(self, agency_id=None, resources=None,
                                 version=None, references=None, detail=None) -> str:

        """
        Returns URL and params to get data provider schemes

        :param agency_id: The agency id of data provider schemes
        :param resources: The resources to query
        :param version: The version of the data provider schemes
        :param references: The references parameter (all, children, descendants)
        :param detail: The detail parameter (full, referencestubs,
                        referencepartial, allstubs, allcompletestubs,
                        referencecompletestubs)

        :return: The URL and params formatted
        """

        return self.common_structure_queries("dataproviderscheme", agency_id, resources,
                                             version, references, detail)

    def get_data_consumer_scheme(self, agency_id=None, resources=None,
                                 version=None, references=None, detail=None) -> str:

        """
        Returns URL and params to get data consumer schemes

        :param agency_id: The agency id of data consumer schemes
        :param resources: The resources to query
        :param version: The version of the data consumer schemes
        :param references: The references parameter (all, children, descendants)
        :param detail: The detail parameter (full, referencestubs,
                        referencepartial, allstubs, allcompletestubs,
                        referencecompletestubs)

        :return: The URL and params formatted
        """

        return self.common_structure_queries("dataconsumerscheme", agency_id, resources,
                                             version, references, detail)

    def get_organisation_unit_scheme(self, agency_id=None, resources=None,
                                     version=None, references=None, detail=None) -> str:

        """
        Returns URL and params to get organisation unit schemes

        :param agency_id: The agency id of organisation unit schemes
        :param resources: The resources to query
        :param version: The version of the organisation unit schemes
        :param references: The references parameter (all, children, descendants)
        :param detail: The detail parameter (full, referencestubs,
                        referencepartial, allstubs, allcompletestubs,
                        referencecompletestubs)

        :return: The URL and params formatted
        """

        return self.common_structure_queries("organisationunitscheme", agency_id, resources,
                                             version, references, detail)

    def get_transformation_scheme(self, agency_id=None, resources=None,
                                  version=None, references=None, detail=None) -> str:

        """
        Returns URL and params to get transformation schemes

        :param agency_id: The agency id of transformation schemes
        :param resources: The resources to query
        :param version: The version of the transformation schemes
        :param references: The references parameter (all, children, descendants)
        :param detail: The detail parameter (full, referencestubs,
                        referencepartial, allstubs, allcompletestubs,
                        referencecompletestubs)

        :return: The URL and params formatted
        """

        return self.common_structure_queries("transformationscheme", agency_id, resources,
                                             version, references, detail)

    def get_ruleset_scheme(self, agency_id=None, resources=None,
                           version=None, references=None, detail=None) -> str:

        """
        Returns URL and params to get ruleset schemes

        :param agency_id: The agency id of ruleset schemes
        :param resources: The resources to query
        :param version: The version of the ruleset schemes
        :param references: The references parameter (all, children, descendants)
        :param detail: The detail parameter (full, referencestubs,
                        referencepartial, allstubs, allcompletestubs,
                        referencecompletestubs)

        :return: The URL and params formatted
        """

        return self.common_structure_queries("rulesetscheme", agency_id, resources,
                                             version, references, detail)

    def get_user_defined_operator_scheme(self, agency_id=None, resources=None,
                                         version=None, references=None, detail=None) -> str:

        """
        Returns URL and params to get user defined operator schemes

        :param agency_id: The agency id of user defined operator schemes
        :param resources: The resources to query
        :param version: The version of the user defined operator schemes
        :param references: The references parameter (all, children, descendants)
        :param detail: The detail parameter (full, referencestubs,
                        referencepartial, allstubs, allcompletestubs,
                        referencecompletestubs)

        :return: The URL and params formatted
        """

        return self.common_structure_queries("userdefinedoperatorscheme", agency_id, resources,
                                             version, references, detail)

    def get_custom_type_scheme(self, agency_id=None, resources=None,
                               version=None, references=None, detail=None) -> str:

        """
        Returns URL and params to get custom type schemes

        :param agency_id: The agency id of custom type schemes
        :param resources: The resources to query
        :param version: The version of the custom type schemes
        :param references: The references parameter (all, children, descendants)
        :param detail: The detail parameter (full, referencestubs,
                        referencepartial, allstubs, allcompletestubs,
                        referencecompletestubs)

        :return: The URL and params formatted
        """

        return self.common_structure_queries("customtypescheme", agency_id, resources,
                                             version, references, detail)

    def get_name_personalisation_scheme(self, agency_id=None, resources=None,
                                        version=None, references=None, detail=None) -> str:

        """
        Returns URL and params to get name personalisation schemes

        :param agency_id: The agency id of name personalisation schemes
        :param resources: The resources to query
        :param version: The version of the name personalisation schemes
        :param references: The references parameter (all, children, descendants)
        :param detail: The detail parameter (full, referencestubs,
                        referencepartial, allstubs, allcompletestubs,
                        referencecompletestubs)

        :return: The URL and params formatted
        """

        return self.common_structure_queries("namepersonalisationscheme", agency_id, resources,
                                             version, references, detail)

    def get_vtl_mapping_scheme(self, agency_id=None, resources=None,
                               version=None, references=None, detail=None) -> str:

        """
        Returns URL and params to get vtl mapping schemes

        :param agency_id: The agency id of vtl mapping schemes
        :param resources: The resources to query
        :param version: The version of the vtl mapping schemes
        :param references: The references parameter (all, children, descendants)
        :param detail: The detail parameter (full, referencestubs,
                        referencepartial, allstubs, allcompletestubs,
                        referencecompletestubs)

        :return: The URL and params formatted
        """

        return self.common_structure_queries("vtlmappingscheme", agency_id, resources,
                                             version, references, detail)

    def get_value_list(self, agency_id=None, resources=None,
                       version=None, references=None, detail=None) -> str:

        """
        Returns URL and params to get value lists

        :param agency_id: The agency id of value lists
        :param resources: The resources to query
        :param version: The version of the value lists
        :param references: The references parameter (all, children, descendants)
        :param detail: The detail parameter (full, referencestubs,
                        referencepartial, allstubs, allcompletestubs,
                        referencecompletestubs)

        :return: The URL and params formatted
        """

        return self.common_structure_queries("valuelist", agency_id, resources,
                                             version, references, detail)

    def get_structure_map(self, agency_id=None, resources=None,
                          version=None, references=None, detail=None) -> str:

        """
        Returns URL and params to get structure maps

        :param agency_id: The agency id of structure maps
        :param resources: The resources to query
        :param version: The version of the structure maps
        :param references: The references parameter (all, children, descendants)
        :param detail: The detail parameter (full, referencestubs,
                        referencepartial, allstubs, allcompletestubs,
                        referencecompletestubs)

        :return: The URL and params formatted
        """

        return self.common_structure_queries("structuremap", agency_id, resources,
                                             version, references, detail)

    def get_representation_map(self, agency_id=None, resources=None,
                               version=None, references=None, detail=None) -> str:

        """
        Returns URL and params to get representation maps

        :param agency_id: The agency id of representation maps
        :param resources: The resources to query
        :param version: The version of the representation maps
        :param references: The references parameter (all, children, descendants)
        :param detail: The detail parameter (full, referencestubs,
                        referencepartial, allstubs, allcompletestubs,
                        referencecompletestubs)

        :return: The URL and params formatted
        """

        return self.common_structure_queries("representationmap", agency_id, resources,
                                             version, references, detail)

    def get_concept_scheme_map(self, agency_id=None, resources=None,
                               version=None, references=None, detail=None) -> str:

        """
        Returns URL and params to get concept scheme maps

        :param agency_id: The agency id of concept scheme maps
        :param resources: The resources to query
        :param version: The version of the concept scheme maps
        :param references: The references parameter (all, children, descendants)
        :param detail: The detail parameter (full, referencestubs,
                        referencepartial, allstubs, allcompletestubs,
                        referencecompletestubs)

        :return: The URL and params formatted
        """

        return self.common_structure_queries("conceptschememap", agency_id, resources,
                                             version, references, detail)

    def get_category_scheme_map(self, agency_id=None, resources=None,
                                version=None, references=None, detail=None) -> str:

        """
        Returns URL and params to get category scheme maps

        :param agency_id: The agency id of category scheme maps
        :param resources: The resources to query
        :param version: The version of the category scheme maps
        :param references: The references parameter (all, children, descendants)
        :param detail: The detail parameter (full, referencestubs,
                        referencepartial, allstubs, allcompletestubs,
                        referencecompletestubs)

        :return: The URL and params formatted
        """

        return self.common_structure_queries("categoryschememap", agency_id, resources,
                                             version, references, detail)

    def get_organisation_scheme_map(self, agency_id=None, resources=None,
                                    version=None, references=None, detail=None) -> str:

        """
        Returns URL and params to get organisation scheme maps

        :param agency_id: The agency id of organisation scheme maps
        :param resources: The resources to query
        :param version: The version of the organisation scheme maps
        :param references: The references parameter (all, children, descendants)
        :param detail: The detail parameter (full, referencestubs,
                        referencepartial, allstubs, allcompletestubs,
                        referencecompletestubs)

        :return: The URL and params formatted
        """

        return self.common_structure_queries("organisationschememap", agency_id, resources,
                                             version, references, detail)

    def get_reporting_taxonomy_map(self, agency_id=None, resources=None,
                                   version=None, references=None, detail=None) -> str:

        """
        Returns URL and params to get reporting taxonomy maps

        :param agency_id: The agency id of reporting taxonomy maps
        :param resources: The resources to query
        :param version: The version of the reporting taxonomy maps
        :param references: The references parameter (all, children, descendants)
        :param detail: The detail parameter (full, referencestubs,
                        referencepartial, allstubs, allcompletestubs,
                        referencecompletestubs)

        :return: The URL and params formatted
        """

        return self.common_structure_queries("reportingtaxonomymap", agency_id, resources,
                                             version, references, detail)

    def get_name_alias_scheme(self, agency_id=None, resources=None,
                              version=None, references=None, detail=None) -> str:
        pass

    def get_concepts(self, agency_id=None, resources=None,
                     version=None, item_id=None, references=None, detail=None) -> str:
        pass

    def get_codes(self, agency_id=None, resources=None,
                  version=None, item_id=None, references=None, detail=None) -> str:
        pass

    def get_categories(self, agency_id=None, resources=None,
                       version=None, item_id=None, references=None, detail=None) -> str:
        pass

    def get_hierarchies(self, agency_id=None, resources=None,
                        version=None, item_id=None, references=None, detail=None) -> str:
        pass

    def get_organisations(self, agency_id=None, resources=None,
                          version=None, item_id=None, references=None, detail=None) -> str:
        pass

    def get_agencies(self, agency_id=None, resources=None,
                     version=None, item_id=None, references=None, detail=None) -> str:
        pass

    def get_data_providers(self, agency_id=None, resources=None,
                           version=None, item_id=None, references=None, detail=None) -> str:
        pass

    def get_data_consumers(self, agency_id=None, resources=None,
                           version=None, item_id=None, references=None, detail=None) -> str:
        pass

    def get_organisation_unit_schemes(self, agency_id=None, resources=None,
                                      version=None, item_id=None, references=None, detail=None) -> str:
        pass

    def get_transformation_schemes(self, agency_id=None, resources=None,
                                   version=None, item_id=None, references=None, detail=None) -> str:
        pass

    def get_ruleset_schemes(self, agency_id=None, resources=None,
                            version=None, item_id=None, references=None, detail=None) -> str:
        pass

    def get_user_defined_operator_schemes(self, agency_id=None, resources=None,
                                          version=None, item_id=None, references=None, detail=None) -> str:
        pass

    def get_custom_type_schemes(self, agency_id=None, resources=None,
                                version=None, item_id=None, references=None, detail=None) -> str:
        pass

    def get_name_personalisation_schemes(self, agency_id=None, resources=None,
                                         version=None, item_id=None, references=None, detail=None) -> str:
        pass

    def get_name_alias_schemes(self, agency_id=None, resources=None,
                               version=None, item_id=None, references=None, detail=None) -> str:
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

    DATA_DETAIL_OPTIONS = ['full', 'dataonly', 'serieskeysonly', 'nodata']

    DATA_HISTORY_OPTIONS = ['true', 'false']

    CONSTRAINTS_MODE_OPTIONS = ['exact', 'available']

    CONSTRAINTS_REFERENCES_OPTIONS = ['none', 'all', 'datastructure', 'conceptscheme',
                                      'codelist', 'dataproviderscheme', 'dataflow']

    def build_query(self, query, agency_id=None, resources=None,
                    version=None, references=None, detail=None) -> str:
        agency_id = agency_id if agency_id else "all"
        resources = resources if resources else "all"
        version = version if version else "latest"

        base_query = f"/{query}/{agency_id}/{resources}/{version}"
        params = ""
        if references:
            initial = "&" if "?" in params else "?"
            params += f"{initial}references={references}"
        if detail:
            initial = "&" if "?" in params else "?"
            params += f"{initial}detail={detail}"

        return base_query + params

    def build_query_with_item(self, query, agency_id=None, resources=None,
                              version=None, item_id=None, references=None, detail=None) -> str:
        agency_id = agency_id if agency_id else "all"
        resources = resources if resources else "all"
        version = version if version else "latest"
        item_id = item_id if item_id else "all"

        base_query = f"/{query}/{agency_id}/{resources}/{version}/{item_id}"
        params = ""
        if references:
            initial = "&" if "?" in params else "?"
            params += f"{initial}references={references}"
        if detail:
            initial = "&" if "?" in params else "?"
            params += f"{initial}detail={detail}"

        return base_query + params

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
        return self.build_query("dataflow", agency_id, resources, version, references, detail)

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

    def get_dsds(self, agency_id=None, resources=None,
                 version=None, references=None, detail=None) -> str:
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
        return self.build_query("datastructure", agency_id, resources, version, references, detail)

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

    def get_mdsds(self, agency_id=None, resources=None,
                  version=None, references=None, detail=None) -> str:
        return self.build_query("metadatastructure", agency_id, resources, version, references, detail)

    def get_meta_data_flows(self, agency_id=None, resources=None,
                            version=None, references=None, detail=None) -> str:
        return self.build_query("metadataflow", agency_id, resources, version, references, detail)

    def get_provision_agreements(self, agency_id=None, resources=None,
                                 version=None, references=None, detail=None) -> str:
        return self.build_query("provisionagreement", agency_id, resources, version, references, detail)

    def get_structure_sets(self, agency_id=None, resources=None,
                           version=None, references=None, detail=None) -> str:
        return self.build_query("structureset", agency_id, resources, version, references, detail)

    def get_process(self, agency_id=None, resources=None,
                    version=None, references=None, detail=None) -> str:
        return self.build_query("process", agency_id, resources, version, references, detail)

    def get_categorisation(self, agency_id=None, resources=None,
                           version=None, references=None, detail=None) -> str:
        return self.build_query("categorisation", agency_id, resources, version, references, detail)

    def get_data_constraint(self, agency_id, resources,
                            version, references=None, detail=None) -> str:
        pass

    def get_metadata_constraint(self, agency_id, resources,
                                version, references=None, detail=None) -> str:
        pass

    def get_content_constraint(self, agency_id=None, resources=None,
                               version=None, references=None, detail=None) -> str:
        return self.build_query("contentconstraint", agency_id, resources, version, references, detail)

    def get_actual_constraint(self, agency_id=None, resources=None,
                              version=None, references=None, detail=None) -> str:
        return self.build_query("actualconstraint", agency_id, resources, version, references, detail)

    def get_allowed_constraint(self, agency_id=None, resources=None,
                               version=None, references=None, detail=None) -> str:
        return self.build_query("allowedconstraint", agency_id, resources, version, references, detail)

    def get_attachment_constraint(self, agency_id=None, resources=None,
                                  version=None, references=None, detail=None) -> str:
        return self.build_query("attachmentconstraint", agency_id, resources, version, references, detail)

    def get_structure(self, agency_id=None, resources=None,
                      version=None, references=None, detail=None) -> str:
        return self.build_query("structure", agency_id, resources, version, references, detail)

    def get_concept_scheme(self, agency_id=None, resources=None,
                           version=None, references=None, detail=None) -> str:
        return self.build_query("conceptscheme", agency_id, resources, version, references, detail)

    def get_code_list(self, agency_id=None, resources=None,
                      version=None, references=None, detail=None) -> str:
        return self.build_query("codelist", agency_id, resources, version, references, detail)

    def get_category_scheme(self, agency_id=None, resources=None,
                            version=None, references=None, detail=None) -> str:
        return self.build_query("categoryscheme", agency_id, resources, version, references, detail)

    def get_hierarchy(self, agency_id, resources,
                      version, references=None, detail=None) -> str:
        pass

    def get_hierarchy_association(self, agency_id, resources,
                                  version, references=None, detail=None) -> str:
        pass

    def get_hierarchical_codelist(self, agency_id=None, resources=None,
                                  version=None, references=None, detail=None) -> str:
        return self.build_query("hierarchicalcodelist", agency_id, resources, version, references, detail)

    def get_organisation_scheme(self, agency_id=None, resources=None,
                                version=None, references=None, detail=None) -> str:
        return self.build_query("organisationscheme", agency_id, resources, version, references, detail)

    def get_agency_scheme(self, agency_id=None, resources=None,
                          version=None, references=None, detail=None) -> str:
        return self.build_query("agencyscheme", agency_id, resources, version, references, detail)

    def get_data_provider_scheme(self, agency_id=None, resources=None,
                                 version=None, references=None, detail=None) -> str:
        return self.build_query("dataproviderscheme", agency_id, resources, version, references, detail)

    def get_data_consumer_scheme(self, agency_id=None, resources=None,
                                 version=None, references=None, detail=None) -> str:
        return self.build_query("dataconsumerscheme", agency_id, resources, version, references, detail)

    def get_organisation_unit_scheme(self, agency_id=None, resources=None,
                                     version=None, references=None, detail=None) -> str:
        return self.build_query("organisationunitscheme", agency_id, resources, version, references, detail)

    def get_transformation_scheme(self, agency_id=None, resources=None,
                                  version=None, references=None, detail=None) -> str:
        return self.build_query("transformationscheme", agency_id, resources, version, references, detail)

    def get_ruleset_scheme(self, agency_id=None, resources=None,
                           version=None, references=None, detail=None) -> str:
        return self.build_query("rulesetscheme", agency_id, resources, version, references, detail)

    def get_user_defined_operator_scheme(self, agency_id=None, resources=None,
                                         version=None, references=None, detail=None) -> str:
        return self.build_query("userdefinedoperatorscheme", agency_id, resources, version, references, detail)

    def get_custom_type_scheme(self, agency_id=None, resources=None,
                               version=None, references=None, detail=None) -> str:
        return self.build_query("customtypescheme", agency_id, resources, version, references, detail)

    def get_name_personalisation_scheme(self, agency_id=None, resources=None,
                                        version=None, references=None, detail=None) -> str:
        return self.build_query("namepersonalisationscheme", agency_id, resources, version, references, detail)

    def get_vtl_mapping_scheme(self, agency_id, resources,
                               version, references=None, detail=None) -> str:
        pass

    def get_value_list(self, agency_id, resources,
                       version, references=None, detail=None) -> str:
        pass

    def get_structure_map(self, agency_id, resources,
                          version, references=None, detail=None) -> str:
        pass

    def get_representation_map(self, agency_id, resources,
                               version, references=None, detail=None) -> str:
        pass

    def get_concept_scheme_map(self, agency_id, resources,
                               version, references=None, detail=None) -> str:
        pass

    def get_category_scheme_map(self, agency_id, resources,
                                version, references=None, detail=None) -> str:
        pass

    def get_organisation_scheme_map(self, agency_id, resources,
                                    version, references=None, detail=None) -> str:
        pass

    def get_reporting_taxonomy_map(self, agency_id, resources,
                                   version, references=None, detail=None) -> str:
        pass

    def get_name_alias_scheme(self, agency_id=None, resources=None,
                              version=None, references=None, detail=None) -> str:
        return self.build_query("namealiasscheme", agency_id, resources, version, references, detail)

    def get_concepts(self, agency_id=None, resources=None,
                     version=None, item_id=None, references=None, detail=None) -> str:
        return self.build_query_with_item("conceptscheme", agency_id, resources, version, item_id, references, detail)

    def get_codes(self, agency_id=None, resources=None,
                  version=None, item_id=None, references=None, detail=None) -> str:
        return self.build_query_with_item("codelist", agency_id, resources, version, references, detail)

    def get_categories(self, agency_id=None, resources=None,
                       version=None, item_id=None, references=None, detail=None) -> str:
        return self.build_query_with_item("categoryscheme", agency_id, resources, version, references, detail)

    def get_hierarchies(self, agency_id=None, resources=None,
                        version=None, item_id=None, references=None, detail=None) -> str:
        return self.build_query_with_item("hierarchicalcodelist", agency_id, resources, version, references, detail)

    def get_organisations(self, agency_id=None, resources=None,
                          version=None, item_id=None, references=None, detail=None) -> str:
        return self.build_query_with_item("organisationscheme", agency_id, resources, version, references, detail)

    def get_agencies(self, agency_id=None, resources=None,
                     version=None, item_id=None, references=None, detail=None) -> str:
        return self.build_query_with_item("agencyscheme", agency_id, resources, version, references, detail)

    def get_data_providers(self, agency_id=None, resources=None,
                           version=None, item_id=None, references=None, detail=None) -> str:
        return self.build_query_with_item("dataproviderscheme", agency_id, resources, version, references, detail)

    def get_data_consumers(self, agency_id=None, resources=None,
                           version=None, item_id=None, references=None, detail=None) -> str:
        return self.build_query_with_item("dataconsumerscheme", agency_id, resources, version, references, detail)

    def get_organisation_unit_schemes(self, agency_id=None, resources=None,
                                      version=None, item_id=None, references=None, detail=None) -> str:
        return self.build_query_with_item("organisationunitscheme", agency_id, resources, version, references, detail)

    def get_transformation_schemes(self, agency_id=None, resources=None,
                                   version=None, item_id=None, references=None, detail=None) -> str:
        return self.build_query_with_item("transformationscheme", agency_id, resources, version, references, detail)

    def get_ruleset_schemes(self, agency_id=None, resources=None,
                            version=None, item_id=None, references=None, detail=None) -> str:
        return self.build_query_with_item("rulesetscheme", agency_id, resources, version, references, detail)

    def get_user_defined_operator_schemes(self, agency_id=None, resources=None,
                                          version=None, item_id=None, references=None, detail=None) -> str:
        return self.build_query_with_item("userdefinedoperatorscheme", agency_id, resources, version,
                                          references, detail)

    def get_custom_type_schemes(self, agency_id=None, resources=None,
                                version=None, item_id=None, references=None, detail=None) -> str:
        return self.build_query_with_item("customtypescheme", agency_id, resources, version,
                                          references, detail)

    def get_name_personalisation_schemes(self, agency_id=None, resources=None,
                                         version=None, item_id=None, references=None, detail=None) -> str:
        return self.build_query_with_item("namepersonalisationscheme", agency_id, resources, version,
                                          references, detail)

    def get_name_alias_schemes(self, agency_id=None, resources=None,
                               version=None, item_id=None, references=None, detail=None) -> str:
        return self.build_query_with_item("namealiasscheme", agency_id, resources, version,
                                          references, detail)


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
        """returns the string for the list of resources ids"""
        if isinstance(ids, str):
            return ids
        if isinstance(ids, list):
            return "+".join(ids)
        if not ids:
            return "all"
        raise TypeError("Ids has to be string, list or None")

    def _query_builder(self, get_method, agency_id=None, resources=None,
                       version=None, item_id=None, references=None, detail=None) -> str:
        """Method for building queries"""
        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"

        if references:
            self._ws_implementation.validate_references(references)
        if detail:
            self._ws_implementation.validate_structural_detail(detail)

        if item_id is not None:
            return get_method(agency_id, resources, version, item_id, references, detail)
        else:
            return get_method(agency_id, resources, version, references, detail)

    def query_builder_common(self, get_method, agency_id=None, resources=None,
                             version=None, references=None, detail=None) -> str:
        """Common method for building queries"""
        return self._query_builder(get_method, agency_id, resources, version, None, references, detail)

    def query_builder_common_with_item(self, get_method, agency_id=None, resources=None,
                                       version=None, item_id=None, references=None, detail=None) -> str:
        """Common method for building queries with item_id"""
        return self._query_builder(get_method, agency_id, resources, version, item_id, references, detail)

    def get_data_flows(self, agency_id=None, resources=None,
                       version=None, references=None, detail=None) -> str:
        """Returns the get data flows query for the WS Implementation"""
        return self.query_builder_common(self._ws_implementation.get_data_flows,
                                         agency_id, resources, version, references, detail)

    def get_dsds(self, agency_id=None, resources=None,
                 version=None, references=None, detail=None) -> str:
        """Returns the get data structures query for the WS Implementation"""
        return self.query_builder_common(self._ws_implementation.get_dsds,
                                         agency_id, resources, version, references, detail)

    def get_data(self, flow, provider=None, detail=None, include_history=None, **kwargs):
        """Returns the data query for the WS Implementation"""

        provider = self.id_builder(provider)
        if detail:
            self._ws_implementation.validate_data_detail(detail)
        if include_history:
            self._ws_implementation.validate_data_history(include_history)

        return self._ws_implementation.get_data(flow, provider=provider, detail=detail,
                                                include_history=include_history, **kwargs)

    def get_constraints(self, flow, key=None, provider=None, component_id=None,
                        mode=None, references=None, start_period=None,
                        end_period=None, updated_after=None):
        """Returns the constraints query for the WS Implementation"""
        provider = self.id_builder(provider)
        if mode:
            self._ws_implementation.validate_constraints_mode(mode)
        if references:
            self._ws_implementation.validate_constraints_references(references)

        return self._ws_implementation.get_constraints(flow, key, provider,
                                                       component_id, mode,
                                                       references,
                                                       start_period,
                                                       end_period,
                                                       updated_after)

    def get_mdsds(self, agency_id=None, resources=None,
                  version=None, references=None, detail=None) -> str:
        """Returns the get metadata structures query for the WS Implementation"""
        return self.query_builder_common(self._ws_implementation.get_mdsds,
                                         agency_id, resources, version, references, detail)

    def get_meta_data_flows(self, agency_id=None, resources=None,
                            version=None, references=None, detail=None) -> str:
        """Returns the get metadata flows query for the WS Implementation"""
        return self.query_builder_common(self._ws_implementation.get_meta_data_flows,
                                         agency_id, resources, version, references, detail)

    def get_provision_agreements(self, agency_id=None, resources=None,
                                 version=None, references=None, detail=None) -> str:
        """Returns the get provision agreements query for the WS Implementation"""
        return self.query_builder_common(self._ws_implementation.get_provision_agreements,
                                         agency_id, resources, version, references, detail)

    def get_structure_sets(self, agency_id=None, resources=None,
                           version=None, references=None, detail=None) -> str:
        """Returns the get structure sets query for the WS Implementation"""
        return self.query_builder_common(self._ws_implementation.get_structure_sets,
                                         agency_id, resources, version, references, detail)

    def get_process(self, agency_id=None, resources=None,
                    version=None, references=None, detail=None) -> str:
        """Returns the get process query for the WS Implementation"""
        return self.query_builder_common(self._ws_implementation.get_process,
                                         agency_id, resources, version, references, detail)

    def get_categorisation(self, agency_id=None, resources=None,
                           version=None, references=None, detail=None) -> str:
        """Returns the get categorisation query for the WS Implementation"""
        return self.query_builder_common(self._ws_implementation.get_categorisation,
                                         agency_id, resources, version, references, detail)

    def get_data_constraint(self, agency_id=None, resources=None,
                            version=None, references=None, detail=None) -> str:
        """Returns the get data constraints query for the WS Implementation"""
        return self.query_builder_common(self._ws_implementation.get_data_constraint,
                                         agency_id, resources, version, references, detail)

    def get_metadata_constraint(self, agency_id=None, resources=None,
                                version=None, references=None, detail=None) -> str:
        """Returns the get metadata constraints query for the WS Implementation"""
        return self.query_builder_common(self._ws_implementation.get_metadata_constraint,
                                         agency_id, resources, version, references, detail)

    def get_content_constraint(self, agency_id=None, resources=None,
                               version=None, references=None, detail=None) -> str:
        """Returns the get content constraints query for the WS Implementation"""
        return self.query_builder_common(self._ws_implementation.get_content_constraint,
                                         agency_id, resources, version, references, detail)

    def get_actual_constraint(self, agency_id=None, resources=None,
                              version=None, references=None, detail=None) -> str:
        """Returns the get actual constraints query for the WS Implementation"""
        return self.query_builder_common(self._ws_implementation.get_actual_constraint,
                                         agency_id, resources, version, references, detail)

    def get_allowed_constraint(self, agency_id=None, resources=None,
                               version=None, references=None, detail=None) -> str:
        """Returns the get allowed constraints query for the WS Implementation"""
        return self.query_builder_common(self._ws_implementation.get_allowed_constraint,
                                         agency_id, resources, version, references, detail)

    def get_attachment_constraint(self, agency_id=None, resources=None,
                                  version=None, references=None, detail=None) -> str:
        """Returns the get attachment constraints query for the WS Implementation"""
        return self.query_builder_common(self._ws_implementation.get_attachment_constraint,
                                         agency_id, resources, version, references, detail)

    def get_structure(self, agency_id=None, resources=None,
                      version=None, references=None, detail=None) -> str:
        """Returns the get structure query for the WS Implementation"""
        return self.query_builder_common(self._ws_implementation.get_structure,
                                         agency_id, resources, version, references, detail)

    def get_concept_scheme(self, agency_id=None, resources=None,
                           version=None, references=None, detail=None) -> str:
        """Returns the get concept schemes query for the WS Implementation"""
        return self.query_builder_common(self._ws_implementation.get_concept_scheme,
                                         agency_id, resources, version, references, detail)

    def get_code_list(self, agency_id=None, resources=None,
                      version=None, references=None, detail=None) -> str:
        """Returns the get codelists query for the WS Implementation"""
        return self.query_builder_common(self._ws_implementation.get_code_list,
                                         agency_id, resources, version, references, detail)

    def get_category_scheme(self, agency_id=None, resources=None,
                            version=None, references=None, detail=None) -> str:
        """Returns the get category schemes query for the WS Implementation"""
        return self.query_builder_common(self._ws_implementation.get_category_scheme,
                                         agency_id, resources, version, references, detail)

    def get_hierarchy(self, agency_id=None, resources=None,
                      version=None, references=None, detail=None) -> str:
        """Returns the get hierarchy query for the WS Implementation"""
        return self.query_builder_common(self._ws_implementation.get_hierarchy,
                                         agency_id, resources, version, references, detail)

    def get_hierarchy_association(self, agency_id=None, resources=None,
                                  version=None, references=None, detail=None) -> str:
        """Returns the get hierarchy association query for the WS Implementation"""
        return self.query_builder_common(self._ws_implementation.get_hierarchy_association,
                                         agency_id, resources, version, references, detail)

    def get_hierarchical_codelist(self, agency_id=None, resources=None,
                                  version=None, references=None, detail=None) -> str:
        """Returns the get hierarchical codelists query for the WS Implementation"""
        return self.query_builder_common(self._ws_implementation.get_hierarchical_codelist,
                                         agency_id, resources, version, references, detail)

    def get_organisation_scheme(self, agency_id=None, resources=None,
                                version=None, references=None, detail=None) -> str:
        """Returns the get organisation schemes query for the WS Implementation"""
        return self.query_builder_common(self._ws_implementation.get_organisation_scheme,
                                         agency_id, resources, version, references, detail)

    def get_agency_scheme(self, agency_id=None, resources=None,
                          version=None, references=None, detail=None) -> str:
        """Returns the get agency schemes query for the WS Implementation"""
        return self.query_builder_common(self._ws_implementation.get_agency_scheme,
                                         agency_id, resources, version, references, detail)

    def get_data_provider_scheme(self, agency_id=None, resources=None,
                                 version=None, references=None, detail=None) -> str:
        """Returns the get data provider schemes query for the WS Implementation"""
        return self.query_builder_common(self._ws_implementation.get_data_provider_scheme,
                                         agency_id, resources, version, references, detail)

    def get_data_consumer_scheme(self, agency_id=None, resources=None,
                                 version=None, references=None, detail=None) -> str:
        """Returns the get data consumer schemes query for the WS Implementation"""
        return self.query_builder_common(self._ws_implementation.get_data_consumer_scheme,
                                         agency_id, resources, version, references, detail)

    def get_organisation_unit_scheme(self, agency_id=None, resources=None,
                                     version=None, references=None, detail=None) -> str:
        """Returns the get organisation unit schemes query for the WS Implementation"""
        return self.query_builder_common(self._ws_implementation.get_organisation_unit_scheme,
                                         agency_id, resources, version, references, detail)

    def get_transformation_scheme(self, agency_id=None, resources=None,
                                  version=None, references=None, detail=None) -> str:
        """Returns the get transformation schemes query for the WS Implementation"""
        return self.query_builder_common(self._ws_implementation.get_transformation_scheme,
                                         agency_id, resources, version, references, detail)

    def get_ruleset_scheme(self, agency_id=None, resources=None,
                           version=None, references=None, detail=None) -> str:
        """Returns the get ruleset schemes query for the WS Implementation"""
        return self.query_builder_common(self._ws_implementation.get_ruleset_scheme,
                                         agency_id, resources, version, references, detail)

    def get_user_defined_operator_scheme(self, agency_id=None, resources=None,
                                         version=None, references=None, detail=None) -> str:
        """Returns the get user defined operator schemes query for the WS Implementation"""
        return self.query_builder_common(self._ws_implementation.get_user_defined_operator_scheme,
                                         agency_id, resources, version, references, detail)

    def get_custom_type_scheme(self, agency_id=None, resources=None,
                               version=None, references=None, detail=None) -> str:
        """Returns the get custom type schemes query for the WS Implementation"""
        return self.query_builder_common(self._ws_implementation.get_custom_type_scheme,
                                         agency_id, resources, version, references, detail)

    def get_name_personalisation_scheme(self, agency_id=None, resources=None,
                                        version=None, references=None, detail=None) -> str:
        """Returns the get name personalisation schemes query for the WS Implementation"""
        return self.query_builder_common(self._ws_implementation.get_name_personalisation_scheme,
                                         agency_id, resources, version, references, detail)

    def get_vtl_mapping_scheme(self, agency_id=None, resources=None,
                               version=None, references=None, detail=None) -> str:
        """Returns the get vtl mapping schemes query for the WS Implementation"""
        return self.query_builder_common(self._ws_implementation.get_vtl_mapping_scheme,
                                         agency_id, resources, version, references, detail)

    def get_value_list(self, agency_id=None, resources=None,
                       version=None, references=None, detail=None) -> str:
        """Returns the get value lists query for the WS Implementation"""
        return self.query_builder_common(self._ws_implementation.get_value_list,
                                         agency_id, resources, version, references, detail)

    def get_structure_map(self, agency_id=None, resources=None,
                          version=None, references=None, detail=None) -> str:
        """Returns the get structure maps query for the WS Implementation"""
        return self.query_builder_common(self._ws_implementation.get_structure_map,
                                         agency_id, resources, version, references, detail)

    def get_representation_map(self, agency_id=None, resources=None,
                               version=None, references=None, detail=None) -> str:
        """Returns the get representation maps query for the WS Implementation"""
        return self.query_builder_common(self._ws_implementation.get_representation_map,
                                         agency_id, resources, version, references, detail)

    def get_concept_scheme_map(self, agency_id=None, resources=None,
                               version=None, references=None, detail=None) -> str:
        """Returns the get concept scheme maps query for the WS Implementation"""
        return self.query_builder_common(self._ws_implementation.get_concept_scheme_map,
                                         agency_id, resources, version, references, detail)

    def get_category_scheme_map(self, agency_id=None, resources=None,
                                version=None, references=None, detail=None) -> str:
        """Returns the get category scheme maps query for the WS Implementation"""
        return self.query_builder_common(self._ws_implementation.get_category_scheme_map,
                                         agency_id, resources, version, references, detail)

    def get_organisation_scheme_map(self, agency_id=None, resources=None,
                                    version=None, references=None, detail=None) -> str:
        """Returns the get organisation scheme maps query for the WS Implementation"""
        return self.query_builder_common(self._ws_implementation.get_organisation_scheme_map,
                                         agency_id, resources, version, references, detail)

    def get_reporting_taxonomy_map(self, agency_id=None, resources=None,
                                   version=None, references=None, detail=None) -> str:
        """Returns the get reporting taxonomy maps query for the WS Implementation"""
        return self.query_builder_common(self._ws_implementation.get_reporting_taxonomy_map,
                                         agency_id, resources, version, references, detail)

    def get_name_alias_scheme(self, agency_id=None, resources=None,
                              version=None, references=None, detail=None) -> str:
        """Returns the get name alias schemes query for the WS Implementation"""
        return self.query_builder_common(self._ws_implementation.get_name_alias_scheme,
                                         agency_id, resources, version, references, detail)

    def get_concepts(self, agency_id=None, resources=None,
                     version=None, item_id=None, references=None, detail=None) -> str:
        """Returns the get concepts query for the WS Implementation"""
        return self.query_builder_common_with_item(self._ws_implementation.get_concepts,
                                                   agency_id, resources, version, item_id, references, detail)

    def get_codes(self, agency_id=None, resources=None,
                  version=None, item_id=None, references=None, detail=None) -> str:
        """Returns the get codes query for the WS Implementation"""
        return self.query_builder_common_with_item(self._ws_implementation.get_codes,
                                                   agency_id, resources, version, item_id, references, detail)

    def get_categories(self, agency_id=None, resources=None,
                       version=None, item_id=None, references=None, detail=None) -> str:
        """Returns the get categories query for the WS Implementation"""
        return self.query_builder_common_with_item(self._ws_implementation.get_categories,
                                                   agency_id, resources, version, item_id, references, detail)

    def get_hierarchies(self, agency_id=None, resources=None,
                        version=None, item_id=None, references=None, detail=None) -> str:
        """Returns the get hierarchies query for the WS Implementation"""
        return self.query_builder_common_with_item(self._ws_implementation.get_hierarchies,
                                                   agency_id, resources, version, item_id, references, detail)

    def get_organisations(self, agency_id=None, resources=None,
                          version=None, item_id=None, references=None, detail=None) -> str:
        """Returns the get organisations query for the WS Implementation"""
        return self.query_builder_common_with_item(self._ws_implementation.get_organisations,
                                                   agency_id, resources, version, item_id, references, detail)

    def get_agencies(self, agency_id=None, resources=None,
                     version=None, item_id=None, references=None, detail=None) -> str:
        """Returns the get agencies query for the WS Implementation"""
        return self.query_builder_common_with_item(self._ws_implementation.get_agencies,
                                                   agency_id, resources, version, item_id, references, detail)

    def get_data_providers(self, agency_id=None, resources=None,
                           version=None, item_id=None, references=None, detail=None) -> str:
        """Returns the get data providers query for the WS Implementation"""
        return self.query_builder_common_with_item(self._ws_implementation.get_data_providers,
                                                   agency_id, resources, version, item_id, references, detail)

    def get_data_consumers(self, agency_id=None, resources=None,
                           version=None, item_id=None, references=None, detail=None) -> str:
        """Returns the get data consumers query for the WS Implementation"""
        return self.query_builder_common_with_item(self._ws_implementation.get_data_consumers,
                                                   agency_id, resources, version, item_id, references, detail)

    def get_organisation_unit_schemes(self, agency_id=None, resources=None,
                                      version=None, item_id=None, references=None, detail=None) -> str:
        """Returns the get organisation unit schemes query for the WS Implementation"""
        return self.query_builder_common_with_item(self._ws_implementation.get_organisation_unit_schemes,
                                                   agency_id, resources, version, item_id, references, detail)

    def get_transformation_schemes(self, agency_id=None, resources=None,
                                   version=None, item_id=None, references=None, detail=None) -> str:
        """Returns the get transformation schemes query for the WS Implementation"""
        return self.query_builder_common_with_item(self._ws_implementation.get_transformation_schemes,
                                                   agency_id, resources, version, item_id, references, detail)

    def get_ruleset_schemes(self, agency_id=None, resources=None,
                            version=None, item_id=None, references=None, detail=None) -> str:
        """Returns the get ruleset schemes query for the WS Implementation"""
        return self.query_builder_common_with_item(self._ws_implementation.get_ruleset_schemes,
                                                   agency_id, resources, version, item_id, references, detail)

    def get_user_defined_operator_schemes(self, agency_id=None, resources=None,
                                          version=None, item_id=None, references=None, detail=None) -> str:
        """Returns the get user defined operator schemes query for the WS Implementation"""
        return self.query_builder_common_with_item(self._ws_implementation.get_user_defined_operator_schemes,
                                                   agency_id, resources, version, item_id, references, detail)

    def get_custom_type_schemes(self, agency_id=None, resources=None,
                                version=None, item_id=None, references=None, detail=None) -> str:
        """Returns the get custom type schemes query for the WS Implementation"""
        return self.query_builder_common_with_item(self._ws_implementation.get_custom_type_schemes,
                                                   agency_id, resources, version, item_id, references, detail)

    def get_name_personalisation_schemes(self, agency_id=None, resources=None,
                                         version=None, item_id=None, references=None, detail=None) -> str:
        """Returns the get name personalisation schemes query for the WS Implementation"""
        return self.query_builder_common_with_item(self._ws_implementation.get_name_personalisation_schemes,
                                                   agency_id, resources, version, item_id, references, detail)

    def get_name_alias_schemes(self, agency_id=None, resources=None,
                               version=None, item_id=None, references=None, detail=None) -> str:
        """Returns the get name alias schemes query for the WS Implementation"""
        return self.query_builder_common_with_item(self._ws_implementation.get_name_alias_schemes,
                                                   agency_id, resources, version, item_id, references, detail)
