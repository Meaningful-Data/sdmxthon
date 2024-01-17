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
    METADATA_STRUCTURE_DETAIL_OPTIONS = []
    SCHEMA_EXPLICIT_MEASURE = []

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
    def get_data_datastructures(self, agency_id=None, resources=None,
                                version=None, key=None, c=None, updated_after=None,
                                first_n_observations=None, last_n_observations=None,
                                dimension_at_observation=None, attributes=None,
                                measures=None, include_history=None):
        """
        Returns URL and params to get data (datastructure)

        :param agency_id: The agency id of the data (datastructure)
        :type agency_id: str

        :param resources: The resources to query
        :type resources: str

        :param version: The version of the data (datastructure)
        :type version: str

        :param key: The key is constructed as a dot ('.')
                    separated list of dimension filtered values.
        :type key: str

        :param c: Filter data by component value
        :type c: str

        :param updated_after: Data filtered by the last update date
        :type updated_after: str

        :param first_n_observations: Number of first observations to be returned
                                     per key
        :type first_n_observations: int

        :param last_n_observations: Number of last observations to be returned
                                    per key
        :type last_n_observations: int

        :param dimension_at_observation: The dimension at observation
                                         of the data (datastructure)
        :type dimension_at_observation: str

        :param attributes: Attributes of the data (datastructure)
        :type attributes: str

        :param measures: The measures of the data (datastructure)
        :type measures: str

        :param include_history: The include history of the data (by datastructure)
                                (true, false)
        :type include_history: str
        """

    @abstractmethod
    def get_data_dataflows(self, agency_id=None, resources=None,
                           version=None, key=None, c=None, updated_after=None,
                           first_n_observations=None, last_n_observations=None,
                           dimension_at_observation=None, attributes=None,
                           measures=None, include_history=None):
        """
        Returns URL and params to get data (dataflow)

        :param agency_id: The agency id of the data (dataflow)
        :type agency_id: str

        :param resources: The resources to query
        :type resources: str

        :param version: The version of the data (dataflow)
        :type version: str

        :param key: The key is constructed as a dot ('.')
                    separated list of dimension filtered values.
        :type key: str

        :param c: Filter data by component value
        :type c: str

        :param updated_after: Data filtered by the last update date
        :type updated_after: str

        :param first_n_observations: Number of first observations to be returned
                                     per key
        :type first_n_observations: int

        :param last_n_observations: Number of last observations to be returned
                                    per key
        :type last_n_observations: int

        :param dimension_at_observation: The dimension at observation
                                         of the data (dataflow)
        :type dimension_at_observation: str

        :param attributes: Attributes of the dataflows
        :type attributes: str

        :param measures: The measures of the dataflows
        :type measures: str

        :param include_history: The include history of the data (by dataflow)
                                (true, false)
        :type include_history: str
        """

    @abstractmethod
    def get_data_provision_agreements(self, agency_id=None, resources=None,
                                      version=None, key=None, c=None, updated_after=None,
                                      first_n_observations=None, last_n_observations=None,
                                      dimension_at_observation=None, attributes=None,
                                      measures=None, include_history=None):
        """
        Returns URL and params to get data (provision agreement)

        :param agency_id: The agency id of the data (provision agreement)
        :type agency_id: str

        :param resources: The resources to query
        :type resources: str

        :param version: The version of the data (provision agreement)
        :type version: str

        :param key: The key is constructed as a dot ('.')
                    separated list of dimension filtered values.
        :type key: str

        :param c: Filter data by component value
        :type c: str

        :param updated_after: Data filtered by the last update date
        :type updated_after: str

        :param first_n_observations: Number of first observations to be returned
                                     per key
        :type first_n_observations: int

        :param last_n_observations: Number of last observations to be returned
                                    per key
        :type last_n_observations: int

        :param dimension_at_observation: The dimension at observation
                                         of the data (provision agreement)
        :type dimension_at_observation: str

        :param attributes: Attributes of the data (provision agreement)
        :type attributes: str

        :param measures: The measures of the data (provision agreement)
        :type measures: str

        :param include_history: The include history of the data (by provision agreement)
                                (true, false)
        :type include_history: str
        """

    @abstractmethod
    def get_data_all_contexts(self, agency_id=None, resources=None,
                              version=None, key=None, c=None, updated_after=None,
                              first_n_observations=None, last_n_observations=None,
                              dimension_at_observation=None, attributes=None,
                              measures=None, include_history=None):
        """
        Returns URL and params to get data (all possible contexts)

        :param agency_id: The agency id of data (all possible contexts)
        :type agency_id: str

        :param resources: The resources to query
        :type resources: str

        :param version: The version of the data (all possible contexts)
        :type version: str

        :param key: The key is constructed as a dot ('.')
                    separated list of dimension filtered values.
        :type key: str

        :param c: Filter data by component value
        :type c: str

        :param updated_after: Data filtered by the last update date
        :type updated_after: str

        :param first_n_observations: Number of first observations to be returned
                                     per key
        :type first_n_observations: int

        :param last_n_observations: Number of last observations to be returned
                                    per key
        :type last_n_observations: int

        :param dimension_at_observation: The dimension at observation
                                         of the data (all possible contexts)
        :type dimension_at_observation: str

        :param attributes: Attributes of the data (all possible contexts)
        :type attributes: str

        :param measures: The measures of the data (all possible contexts)
        :type measures: str

        :param include_history: The include history of the data (by all possible contexts)
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

        :param flow: The id of the constraints
        :type flow: str

        :param key: The key is constructed as a dot ('.')
                    separated list of dimension filtered values.
        :type key: str

        :param provider: The provider of the constraints
        :type provider: str

        :param component_id: The component id of the constraints
        :type component_id: str

        :param mode: The mode parameter (exact, available)
        :type mode: str

        :param references: The references parameter (all, children, descendants)
        :type references: str

        :param start_period: The start period of the constraints
        :type start_period: str

        :param end_period: The end period of the constraints
        :type end_period: str

        :param updated_after: Data filtered by the last update date
        :type updated_after: str
        """

    @abstractmethod
    def get_constraint_datastructures(self, agency_id=None, resources=None,
                                      version=None, key=None, component_id=None, c=None,
                                      mode=None, references=None, updated_after=None):
        """
        Returns URL and params to get the constraints (datastructure)

        :param agency_id: The agency id of the constraints (datastructure)
        :type agency_id: str

        :param resources: The resources to query
        :type resources: str

        :param version: The version of the constraints (datastructure)
        :type version: str

        :param key: The key is constructed as a dot ('.')
                    separated list of dimension filtered values.
        :type key: str

        :param component_id: The component id of the constraints (datastructure)
        :type component_id: str

        :param c: Filter data by component value
        :type c: str

        :param mode: The mode parameter (exact, available)
        :type mode: str

        :param references: The references parameter (none, all, datastructure,conceptscheme,
                                                     codelist, dataproviderscheme, dataflow)
        :type references: str

        :param updated_after: Data filtered by the last update date
        :type updated_after: str
        """

    @abstractmethod
    def get_constraint_dataflows(self, agency_id=None, resources=None,
                                 version=None, key=None, component_id=None, c=None,
                                 mode=None, references=None, updated_after=None):
        """
        Returns URL and params to get the constraints (dataflow)

        :param agency_id: The agency id of the constraints (dataflow)
        :type agency_id: str

        :param resources: The resources to query
        :type resources: str

        :param version: The version of the constraints (dataflow)
        :type version: str

        :param key: The key is constructed as a dot ('.')
                    separated list of dimension filtered values.
        :type key: str

        :param component_id: The component id of the constraints (dataflow)
        :type component_id: str

        :param c: Filter data by component value
        :type c: str

        :param mode: The mode parameter (exact, available)
        :type mode: str

        :param references: The references parameter (none, all, datastructure,conceptscheme,
                                                     codelist, dataproviderscheme, dataflow)
        :type references: str

        :param updated_after: Data filtered by the last update date
        :type updated_after: str
        """

    @abstractmethod
    def get_constraint_provision_agreements(self, agency_id=None, resources=None,
                                            version=None, key=None, component_id=None, c=None,
                                            mode=None, references=None, updated_after=None):
        """
        Returns URL and params to get the constraints (provision agreement)

        :param agency_id: The agency id of the constraints (provision agreements)
        :type agency_id: str

        :param resources: The resources to query
        :type resources: str

        :param version: The version of the constraints (provision agreements)
        :type version: str

        :param key: The key is constructed as a dot ('.')
                    separated list of dimension filtered values.
        :type key: str

        :param component_id: The component id of the constraints (provision agreements)
        :type component_id: str

        :param c: Filter data by component value
        :type c: str

        :param mode: The mode parameter (exact, available)
        :type mode: str

        :param references: The references parameter (none, all, datastructure,conceptscheme,
                                                     codelist, dataproviderscheme, dataflow)
        :type references: str

        :param updated_after: Data filtered by the last update date
        :type updated_after: str
        """

    @abstractmethod
    def get_constraint_all_contexts(self, agency_id=None, resources=None,
                                    version=None, key=None, component_id=None, c=None,
                                    mode=None, references=None, updated_after=None):
        """
        Returns URL and params to get the constraints

        :param agency_id: The agency id of the constraints (all possible contexts)
        :type agency_id: str

        :param resources: The resources to query
        :type resources: str

        :param version: The version of the constraints (all possible contexts)
        :type version: str

        :param key: The key is constructed as a dot ('.')
                    separated list of dimension filtered values.
        :type key: str

        :param component_id: The component id of the constraints (all possible contexts)
        :type component_id: str

        :param c: Filter data by component value
        :type c: str

        :param mode: The mode parameter (exact, available)
        :type mode: str

        :param references: The references parameter (none, all, datastructure,conceptscheme,
                                                     codelist, dataproviderscheme, dataflow)
        :type references: str

        :param updated_after: Data filtered by the last update date
        :type updated_after: str
        """

    @abstractmethod
    def get_schema_datastructures(self, agency_id=None, resources=None,
                                  version=None, dimension_at_observation=None,
                                  explicit_measure=None):
        """
        Returns URL and params to get the schema (datastructure)

        :param agency_id: The agency id of the schema (datastructure)
        :type agency_id: str

        :param resources: The resources to query
        :type resources: str

        :param version: The version of the schema (datastructure)
        :type version: str

        :param dimension_at_observation: The dimension at observation
        :type dimension_at_observation: str

        :param explicit_measure: Indicates whether observations are strongly typed
        :type explicit_measure: str
        """

    @abstractmethod
    def get_schema_meta_datastructures(self, agency_id=None, resources=None,
                                       version=None, dimension_at_observation=None,
                                       explicit_measure=None):
        """
        Returns URL and params to get the schema (metadatastructure)

        :param agency_id: The agency id of the schema (metadatastructure)
        :type agency_id: str

        :param resources: The resources to query
        :type resources: str

        :param version: The version of the schema (metadatastructure)
        :type version: str

        :param dimension_at_observation: The dimension at observation
        :type dimension_at_observation: str

        :param explicit_measure: Indicates whether observations are strongly typed
        :type explicit_measure: str
        """

    @abstractmethod
    def get_schema_dataflows(self, agency_id=None, resources=None,
                             version=None, dimension_at_observation=None,
                             explicit_measure=None):
        """
        Returns URL and params to get the schema (dataflow)

        :param agency_id: The agency id of the schema (dataflow)
        :type agency_id: str

        :param resources: The resources to query
        :type resources: str

        :param version: The version of the schema (dataflow)
        :type version: str

        :param dimension_at_observation: The dimension at observation
        :type dimension_at_observation: str

        :param explicit_measure: Indicates whether observations are strongly typed
        :type explicit_measure: str
        """

    @abstractmethod
    def get_schema_meta_dataflows(self, agency_id=None, resources=None,
                                  version=None, dimension_at_observation=None,
                                  explicit_measure=None):
        """
        Returns URL and params to get the schema (metadataflow)

        :param agency_id: The agency id of the schema (metadataflow)
        :type agency_id: str

        :param resources: The resources to query
        :type resources: str

        :param version: The version of the schema (metadataflow)
        :type version: str

        :param dimension_at_observation: The dimension at observation
        :type dimension_at_observation: str

        :param explicit_measure: Indicates whether observations are strongly typed
        :type explicit_measure: str
        """

    @abstractmethod
    def get_schema_provision_agreements(self, agency_id=None, resources=None,
                                        version=None, dimension_at_observation=None,
                                        explicit_measure=None):
        """
        Returns URL and params to get the schema (provision agreement)

        :param agency_id: The agency id of the schema (provision agreement)
        :type agency_id: str

        :param resources: The resources to query
        :type resources: str

        :param version: The version of the schema (provision agreement)
        :type version: str

        :param dimension_at_observation: The dimension at observation
        :type dimension_at_observation: str

        :param explicit_measure: Indicates whether observations are strongly typed
        :type explicit_measure: str
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
    def get_schemas_datastructure(self, agency_id=None, resources=None,
                                  version=None, dimension_at_observation=None,
                                  explicit_measure=None):
        """
        Returns URL and params to get the schema (datastructure)

        :param agency_id: The agency id of the schema (datastructure)
        :type agency_id: str

        :param resources: The resources to query
        :type resources: str

        :param version: The version of the schema (datastructure)
        :type version: str

        :param dimension_at_observation: The dimension at observation
        :type dimension_at_observation: str

        :param explicit_measure: Indicates whether observations are strongly typed
        :type explicit_measure: str
        """

    @abstractmethod
    def get_schemas_meta_datastructure(self, agency_id=None, resources=None,
                                       version=None, dimension_at_observation=None,
                                       explicit_measure=None):
        """
        Returns URL and params to get the schema (metadatastructure)

        :param agency_id: The agency id of the schema (metadatastructure)
        :type agency_id: str

        :param resources: The resources to query
        :type resources: str

        :param version: The version of the schema (metadatastructure)
        :type version: str

        :param dimension_at_observation: The dimension at observation
        :type dimension_at_observation: str

        :param explicit_measure: Indicates whether observations are strongly typed
        :type explicit_measure: str
        """

    @abstractmethod
    def get_schemas_dataflow(self, agency_id=None, resources=None,
                             version=None, dimension_at_observation=None,
                             explicit_measure=None):
        """
        Returns URL and params to get the schema (dataflow)

        :param agency_id: The agency id of the schema (dataflow)
        :type agency_id: str

        :param resources: The resources to query
        :type resources: str

        :param version: The version of the schema (dataflow)
        :type version: str

        :param dimension_at_observation: The dimension at observation
        :type dimension_at_observation: str

        :param explicit_measure: Indicates whether observations are strongly typed
        :type explicit_measure: str
        """

    @abstractmethod
    def get_schemas_meta_dataflow(self, agency_id=None, resources=None,
                                  version=None, dimension_at_observation=None,
                                  explicit_measure=None):
        """
        Returns URL and params to get the schema (metadataflow)

        :param agency_id: The agency id of the schema (metadataflow)
        :type agency_id: str

        :param resources: The resources to query
        :type resources: str

        :param version: The version of the schema (metadataflow)
        :type version: str

        :param dimension_at_observation: The dimension at observation
        :type dimension_at_observation: str

        :param explicit_measure: Indicates whether observations are strongly typed
        :type explicit_measure: str
        """

    @abstractmethod
    def get_schemas_provision_agreement(self, agency_id=None, resources=None,
                                        version=None, dimension_at_observation=None,
                                        explicit_measure=None):
        """
        Returns URL and params to get the schema (provision agreement)

        :param agency_id: The agency id of the schema (provision agreement)
        :type agency_id: str

        :param resources: The resources to query
        :type resources: str

        :param version: The version of the schema (provision agreement)
        :type version: str

        :param dimension_at_observation: The dimension at observation
        :type dimension_at_observation: str

        :param explicit_measure: Indicates whether observations are strongly typed
        :type explicit_measure: str
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

    @abstractmethod
    def get_concept_scheme_item(self, agency_id, resources, version,
                                item_id, references=None, detail=None) -> str:
        """
        Returns query to retrieve concept schemes in Item Scheme Queries (V2.0.0)
        """

    @abstractmethod
    def get_codelist_item(self, agency_id, resources, version,
                          item_id, references=None, detail=None) -> str:
        """
        Returns query to retrieve codelists in Item Scheme Queries (V2.0.0)
        """

    @abstractmethod
    def get_category_scheme_item(self, agency_id, resources, version,
                                 item_id, references=None, detail=None) -> str:
        """
        Returns query to retrieve category schemes in Item Scheme Queries (V2.0.0)
        """

    @abstractmethod
    def get_agency_scheme_item(self, agency_id, resources, version,
                               item_id, references=None, detail=None) -> str:
        """
        Returns query to retrieve agency schemes in Item Scheme Queries (V2.0.0)
        """

    @abstractmethod
    def get_data_provider_scheme_item(self, agency_id, resources, version,
                                      item_id, references=None, detail=None) -> str:
        """
        Returns query to retrieve data provider schemes in Item Scheme Queries (V2.0.0)
        """

    @abstractmethod
    def get_data_consumer_scheme_item(self, agency_id, resources, version,
                                      item_id, references=None, detail=None) -> str:
        """
        Returns query to retrieve data consumer schemes in Item Scheme Queries (V2.0.0)
        """

    @abstractmethod
    def get_organisation_unit_scheme_item(self, agency_id, resources, version,
                                          item_id, references=None, detail=None) -> str:
        """
        Returns query to retrieve organisation unit schemes in Item Scheme Queries (V2.0.0)
        """

    @abstractmethod
    def get_transformation_scheme_item(self, agency_id, resources, version,
                                       item_id, references=None, detail=None) -> str:
        """
        Returns query to retrieve transformation schemes in Item Scheme Queries (V2.0.0)
        """

    @abstractmethod
    def get_ruleset_scheme_item(self, agency_id, resources, version,
                                item_id, references=None, detail=None) -> str:
        """
        Returns query to retrieve ruleset schemes in Item Scheme Queries (V2.0.0)
        """

    @abstractmethod
    def get_user_defined_operator_scheme_item(self, agency_id, resources, version,
                                              item_id, references=None, detail=None) -> str:
        """
        Returns query to retrieve user defined operator schemes in Item Scheme Queries (V2.0.0)
        """

    @abstractmethod
    def get_custom_type_scheme_item(self, agency_id, resources, version,
                                    item_id, references=None, detail=None) -> str:
        """
        Returns query to retrieve custom type schemes in Item Scheme Queries (V2.0.0)
        """

    @abstractmethod
    def get_name_personalisation_scheme_item(self, agency_id, resources, version,
                                             item_id, references=None, detail=None) -> str:
        """
        Returns query to retrieve name personalisation schemes in Item Scheme Queries (V2.0.0)
        """

    @abstractmethod
    def get_vtl_mapping_scheme_item(self, agency_id, resources, version,
                                    item_id, references=None, detail=None) -> str:
        """
        Returns query to retrieve name personalisation schemes in Item Scheme Queries (V2.0.0)
        """

    @abstractmethod
    def get_value_list_item(self, agency_id, resources, version,
                            item_id, references=None, detail=None) -> str:
        """
        Returns query to retrieve value lists  in Item Scheme Queries (V2.0.0)
        """

    @abstractmethod
    def get_metadata_dsds(self, agency_id, resources, version,
                          detail=None) -> str:
        """
        Returns query to retrieve data structure definitions in Metadata Queries (by structure) (V2.0.0)
        """

    @abstractmethod
    def get_metadata_mdsds(self, agency_id, resources, version,
                           detail=None) -> str:
        """
        Returns query to retrieve metadata structure definitions in Metadata Queries (by structure) (V2.0.0)
        """

    @abstractmethod
    def get_metadata_dataflows(self, agency_id, resources, version,
                               detail=None) -> str:
        """
        Returns query to retrieve dataflows in Metadata Queries (by structure) (V2.0.0)
        """

    @abstractmethod
    def get_metadata_metadata_flows(self, agency_id, resources, version,
                                    detail=None) -> str:
        """
        Returns query to retrieve metadata flows in Metadata Queries (by structure) (V2.0.0)
        """

    @abstractmethod
    def get_metadata_provision_agreements(self, agency_id, resources, version,
                                          detail=None) -> str:
        """
        Returns query to retrieve provision agreements in Metadata Queries (by structure) (V2.0.0)
        """

    @abstractmethod
    def get_metadata_structure_sets(self, agency_id, resources, version,
                                    detail=None) -> str:
        """
        Returns query to retrieve structure sets in Metadata Queries (by structure) (V2.0.0)
        """

    @abstractmethod
    def get_metadata_processes(self, agency_id, resources, version,
                               detail=None) -> str:
        """
        Returns query to retrieve processes in Metadata Queries (by structure) (V2.0.0)
        """

    @abstractmethod
    def get_metadata_categorisations(self, agency_id, resources, version,
                                     detail=None) -> str:
        """
        Returns query to retrieve categorisations in Metadata Queries (by structure) (V2.0.0)
        """

    @abstractmethod
    def get_metadata_data_constraints(self, agency_id, resources, version,
                                      detail=None) -> str:
        """
        Returns query to retrieve data constraints in Metadata Queries (by structure) (V2.0.0)
        """

    @abstractmethod
    def get_metadata_metadata_constraints(self, agency_id, resources, version,
                                          detail=None) -> str:
        """
        Returns query to retrieve metadata constraints in Metadata Queries (by structure) (V2.0.0)
        """

    @abstractmethod
    def get_metadata_concept_schemes(self, agency_id, resources, version,
                                     detail=None) -> str:
        """
        Returns query to retrieve concept schemes in Metadata Queries (by structure) (V2.0.0)
        """

    @abstractmethod
    def get_metadata_code_lists(self, agency_id, resources, version,
                                detail=None) -> str:
        """
        Returns query to retrieve code lists in Metadata Queries (by structure) (V2.0.0)
        """

    @abstractmethod
    def get_metadata_category_schemes(self, agency_id, resources, version,
                                      detail=None) -> str:
        """
        Returns query to retrieve category schemes in Metadata Queries (by structure) (V2.0.0)
        """

    @abstractmethod
    def get_metadata_hierarchies(self, agency_id, resources, version,
                                 detail=None) -> str:
        """
        Returns query to retrieve hierarchies in Metadata Queries (by structure) (V2.0.0)
        """

    @abstractmethod
    def get_metadata_hierarchy_associations(self, agency_id, resources, version,
                                            detail=None) -> str:
        """
        Returns query to retrieve hierarchy associations in Metadata Queries (by structure) (V2.0.0)
        """

    @abstractmethod
    def get_metadata_agency_schemes(self, agency_id, resources, version,
                                    detail=None) -> str:
        """
        Returns query to retrieve agency schemes in Metadata Queries (by structure) (V2.0.0)
        """

    @abstractmethod
    def get_metadata_data_provider_schemes(self, agency_id, resources, version,
                                           detail=None) -> str:
        """
        Returns query to retrieve data provider schemes in Metadata Queries (by structure) (V2.0.0)
        """

    @abstractmethod
    def get_metadata_data_consumer_schemes(self, agency_id, resources, version,
                                           detail=None) -> str:
        """
        Returns query to retrieve data consumer schemes in Metadata Queries (by structure) (V2.0.0)
        """

    @abstractmethod
    def get_metadata_organisation_unit_schemes(self, agency_id, resources, version,
                                               detail=None) -> str:
        """
        Returns query to retrieve organisation unit schemes in Metadata Queries (by structure) (V2.0.0)
        """

    @abstractmethod
    def get_metadata_transformation_schemes(self, agency_id, resources, version,
                                            detail=None) -> str:
        """
        Returns query to retrieve transformation schemes in Metadata Queries (by structure) (V2.0.0)
        """

    @abstractmethod
    def get_metadata_ruleset_schemes(self, agency_id, resources, version,
                                     detail=None) -> str:
        """
        Returns query to retrieve ruleset schemes in Metadata Queries (by structure) (V2.0.0)
        """

    @abstractmethod
    def get_metadata_user_defined_operator_schemes(self, agency_id, resources, version,
                                                   detail=None) -> str:
        """
        Returns query to retrieve user defined operator schemes in Metadata Queries (by structure) (V2.0.0)
        """

    @abstractmethod
    def get_metadata_custom_type_schemes(self, agency_id, resources, version,
                                         detail=None) -> str:
        """
        Returns query to retrieve custom type schemes in Metadata Queries (by structure) (V2.0.0)
        """

    @abstractmethod
    def get_metadata_name_personalisation_schemes(self, agency_id, resources, version,
                                                  detail=None) -> str:
        """
        Returns query to retrieve name personalisation schemes in Metadata Queries (by structure) (V2.0.0)
        """

    @abstractmethod
    def get_metadata_vtl_mapping_schemes(self, agency_id, resources, version,
                                         detail=None) -> str:
        """
        Returns query to retrieve vtl mapping schemes in Metadata Queries (by structure) (V2.0.0)
        """

    @abstractmethod
    def get_metadata_value_lists(self, agency_id, resources, version,
                                 detail=None) -> str:
        """
        Returns query to retrieve value lists in Metadata Queries (by structure) (V2.0.0)
        """

    @abstractmethod
    def get_metadata_structure_maps(self, agency_id, resources, version,
                                    detail=None) -> str:
        """
        Returns query to retrieve structure maps in Metadata Queries (by structure) (V2.0.0)
        """

    @abstractmethod
    def get_metadata_representation_maps(self, agency_id, resources, version,
                                         detail=None) -> str:
        """
        Returns query to retrieve representation maps in Metadata Queries (by structure) (V2.0.0)
        """

    @abstractmethod
    def get_metadata_concept_scheme_maps(self, agency_id, resources, version,
                                         detail=None) -> str:
        """
        Returns query to retrieve concept scheme maps in Metadata Queries (by structure) (V2.0.0)
        """

    @abstractmethod
    def get_metadata_category_scheme_maps(self, agency_id, resources, version,
                                          detail=None) -> str:
        """
        Returns query to retrieve category scheme maps in Metadata Queries (by structure) (V2.0.0)
        """

    @abstractmethod
    def get_metadata_organisation_scheme_maps(self, agency_id, resources, version,
                                              detail=None) -> str:
        """
        Returns query to retrieve organisation scheme maps in Metadata Queries (by structure) (V2.0.0)
        """

    @abstractmethod
    def get_metadata_reporting_taxonomy_maps(self, agency_id, resources, version,
                                             detail=None) -> str:
        """
        Returns query to retrieve reporting taxonomy maps in Metadata Queries (by structure) (V2.0.0)
        """

    @abstractmethod
    def get_metadata_metadataflow_query(self, agency_id, resources, version,
                                        provider_id, detail=None) -> str:
        """
        Returns query to retrieve metadata in Metadata Queries (by metadataflow) (V2.0.0)
        """

    @abstractmethod
    def get_metadata_metadataset_query(self, provider_id=None, resources=None,
                                       version=None, detail=None) -> str:
        """
        Returns query to retrieve metadata in Metadata Queries (by metadataset) (V2.0.0)
        """

    def validate_references(self, reference: str):
        """
        Validates that the reference is one of the allowed values
        """

        if reference not in self.REFERENCES_OPTIONS:
            raise ValueError(f"references must be one of the following values: "
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

    def validate_metadata_structural_detail(self, detail: str):
        """
        Validates that the detail is one of the allowed values
        """
        if detail not in self.METADATA_STRUCTURE_DETAIL_OPTIONS:
            raise ValueError(f"detail must be one of the following values: "
                             f"{self.METADATA_STRUCTURE_DETAIL_OPTIONS}")

    def validate_explicit_measure(self, explicit_measure: str):
        """
        Validates that the explicit measure is one of the allowed values
        """
        if explicit_measure not in self.SCHEMA_EXPLICIT_MEASURE:
            raise ValueError(f"explicitMeasure must be one of the following values: "
                             f"{self.SCHEMA_EXPLICIT_MEASURE}")


class SdmxWs2p0(SdmxWebservice):
    """
    SDMX Web Service 2.0 specification

    :param REFERENCES_OPTIONS: The allowed values for the references parameter
                            (none, parents, parentsandsiblings, ancestors,
                            children, descendants, all, datastructure,
                            metadatastructure, categoryscheme, conceptscheme, codelist,
                            hierarchy, hierarchyassociation, agencyscheme, dataproviderscheme,
                            dataconsumerscheme, organisationunitscheme, dataflow, metadataflow,
                            reportingtaxonomy, provisionagreement, structureset, process,
                            categorisation, dataconstraint, metadataconstraint, transformationscheme,
                            rulesetscheme, userdefinedoperatorscheme, customtypescheme,
                            namepersonalisationscheme, namealiasscheme, valuelist, structuremap,
                            representationmap, conceptscheme, categoryschememap, organisationschememap,
                            reportingtaxonomymap)
    :type REFERENCES_OPTIONS: list[str]

    :param STRUCTURE_DETAIL_OPTIONS: The allowed values for the detail parameter
                            (full, allstubs, referencestubs, allcompletestubs,
                             referencecompletestubs, referencepartial, raw)
    :type STRUCTURE_DETAIL_OPTIONS: list[str]

    :param DATA_DETAIL_OPTIONS: The allowed values for the detail parameter
    :type DATA_DETAIL_OPTIONS: list[str]
    """

    REFERENCES_OPTIONS = ['none', 'parents', 'parentsandsiblings', 'ancestors',
                          'children', 'descendants', 'all', 'datastructure',
                          'metadatastructure', 'categoryscheme', 'conceptscheme', 'codelist',
                          'hierarchy', 'hierarchyassociation', 'agencyscheme', 'dataproviderscheme',
                          'dataconsumerscheme', 'organisationunitscheme', 'dataflow', 'metadataflow',
                          'reportingtaxonomy', 'provisionagreement', 'structureset', 'process',
                          'categorisation', 'dataconstraint', 'metadataconstraint', 'transformationscheme',
                          'rulesetscheme', 'userdefinedoperatorscheme', 'customtypescheme',
                          'namepersonalisationscheme', 'namealiasscheme', 'valuelist', 'structuremap',
                          'representationmap', 'conceptscheme', 'categoryschememap', 'organisationschememap',
                          'reportingtaxonomymap']

    STRUCTURE_DETAIL_OPTIONS = ['full', 'allstubs', 'referencestubs',
                                'allcompletestubs', 'referencecompletestubs',
                                'referencepartial', 'raw']

    METADATA_STRUCTURE_DETAIL_OPTIONS = ['full', 'allstubs']

    DATA_HISTORY_OPTIONS = ['true', 'false']

    CONSTRAINTS_MODE_OPTIONS = ['exact', 'available']

    CONSTRAINTS_REFERENCES_OPTIONS = ['none', 'all', 'datastructure', 'conceptscheme',
                                      'codelist', 'dataproviderscheme', 'dataflow']

    SCHEMA_EXPLICIT_MEASURE = ['true', 'false']

    def common_data_queries(self, context, agency_id=None, resources=None,
                            version=None, key=None, c=None, updated_after=None,
                            first_n_observations=None, last_n_observations=None,
                            dimension_at_observation=None, attributes=None,
                            measures=None, include_history=None):
        agency_id = agency_id if agency_id else "all"
        resources = resources if resources else "all"
        version = version if version else "latest"
        key = key if key else "all"

        base_query = f"/data/{context}/{agency_id}/{resources}/{version}/{key}"
        params = ""
        if c:
            initial = "&" if "?" in params else "?"
            params += f"{initial}c={c}"
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
        if attributes:
            initial = "&" if "?" in params else "?"
            params += f"{initial}attributes={attributes}"
        if measures:
            initial = "&" if "?" in params else "?"
            params += f"{initial}measures={measures}"
        if include_history:
            initial = "&" if "?" in params else "?"
            params += f"{initial}includeHistory={include_history}"

        return base_query + params

    def common_constraints_queries(self, context, agency_id=None, resources=None,
                                   version=None, key=None, component_id=None, c=None,
                                   mode=None, references=None, updated_after=None):
        agency_id = agency_id if agency_id else "all"
        resources = resources if resources else "all"
        version = version if version else "latest"
        key = key if key else "all"
        component_id = component_id if component_id else "all"

        base_query = f"/availability/{context}/{agency_id}/{resources}/{version}/{key}/{component_id}"
        params = ""
        if c:
            initial = "&" if "?" in params else "?"
            params += f"{initial}c={c}"
        if mode:
            initial = "&" if "?" in params else "?"
            params += f"{initial}mode={mode}"
        if references:
            initial = "&" if "?" in params else "?"
            params += f"{initial}references={references}"
        if updated_after:
            initial = "&" if "?" in params else "?"
            params += f"{initial}updatedAfter={updated_after}"

        return base_query + params

    def common_schema_queries(self, context, agency_id=None, resources=None,
                              version=None, dimension_at_observation=None,
                              explicit_measure=None):
        agency_id = agency_id if agency_id else "all"
        resources = resources if resources else "all"
        version = version if version else "latest"

        base_query = f"/schema/{context}/{agency_id}/{resources}/{version}"
        params = ""
        if dimension_at_observation:
            initial = "&" if "?" in params else "?"
            params += f"{initial}dimension_at_observation={dimension_at_observation}"
        if explicit_measure:
            initial = "&" if "?" in params else "?"
            params += f"{initial}explicit_measure={explicit_measure}"

        return base_query + params

    def common_structure_queries(self, structure_type, agency_id=None, resources=None,
                                 version=None, references=None, detail=None) -> str:
        agency_id = agency_id if agency_id else "all"
        resources = resources if resources else "all"
        version = version if version else "latest"

        base_query = f"/structure/{structure_type}/{agency_id}/{resources}/{version}"
        params = ""
        if references:
            initial = "&" if "?" in params else "?"
            params += f"{initial}references={references}"
        if detail:
            initial = "&" if "?" in params else "?"
            params += f"{initial}detail={detail}"

        return base_query + params

    def common_item_scheme_queries(self, item_scheme_type, agency_id=None, resources=None,
                                   version=None, item_id=None, references=None, detail=None) -> str:
        agency_id = agency_id if agency_id else "all"
        resources = resources if resources else "all"
        version = version if version else "latest"
        item_id = item_id if item_id else "all"

        base_query = f"/structure/{item_scheme_type}/{agency_id}/{resources}/{version}/{item_id}"
        params = ""
        if references:
            initial = "&" if "?" in params else "?"
            params += f"{initial}references={references}"
        if detail:
            initial = "&" if "?" in params else "?"
            params += f"{initial}detail={detail}"

        return base_query + params

    def common_metadata_structure_queries(self, structure_type, agency_id=None, resources=None,
                                          version=None, detail=None) -> str:
        agency_id = agency_id if agency_id else "all"
        resources = resources if resources else "all"
        version = version if version else "latest"

        base_query = f"/metadata/structure/{structure_type}/{agency_id}/{resources}/{version}"
        params = ""
        if detail:
            initial = "&" if "?" in params else "?"
            params += f"{initial}detail={detail}"

        return base_query + params

    def get_data(self, flow, key=None, provider=None, start_period=None,
                 end_period=None, updated_after=None,
                 first_n_observations=None, last_n_observations=None,
                 dimension_at_observation=None,
                 detail=None, include_history=None) -> str:
        pass

    def get_data_datastructures(self, agency_id=None, resources=None,
                                version=None, key=None, c=None, updated_after=None,
                                first_n_observations=None, last_n_observations=None,
                                dimension_at_observation=None, attributes=None,
                                measures=None, include_history=None):
        """
        Returns URL and params to get data

        :param agency_id: The id of the data (datastructure)
        :param resources: The resources to query
        :param version: The version of the data (datastructure)
        :param key: The key is constructed as a dot ('.') separated list of
                    dimension filtered values.
        :param c: Filter data by component value
        :param updated_after: Data filtered by the last update date
        :param first_n_observations: Number of first observations to be returned
                                     per key
        :param last_n_observations: Number of last observations to be returned
                                    per key
        :param dimension_at_observation: The dimension at observation
        :param attributes: Attributes of the data (datastructure)
        :param measures: Measures of the data (datastructure)
        :param include_history: Value to include history (true, false)
        :return: The URL and params formatted
        """
        return self.common_data_queries("datastructure", agency_id, resources, version, key, c,
                                        updated_after, first_n_observations, last_n_observations,
                                        dimension_at_observation, attributes, measures,
                                        include_history)

    def get_data_dataflows(self, agency_id=None, resources=None,
                           version=None, key=None, c=None, updated_after=None,
                           first_n_observations=None, last_n_observations=None,
                           dimension_at_observation=None, attributes=None,
                           measures=None, include_history=None):
        """
        Returns URL and params to get data

        :param agency_id: The id of the data (dataflow)
        :param resources: The resources to query
        :param version: The version of the data (dataflow)
        :param key: The key is constructed as a dot ('.') separated list of
                    dimension filtered values.
        :param c: Filter data by component value
        :param updated_after: Data filtered by the last update date
        :param first_n_observations: Number of first observations to be returned
                                     per key
        :param last_n_observations: Number of last observations to be returned
                                    per key
        :param dimension_at_observation: The dimension at observation
        :param attributes: Attributes of the data (dataflow)
        :param measures: Measures of the data (dataflow)
        :param include_history: Value to include history (true, false)
        :return: The URL and params formatted
        """
        return self.common_data_queries("dataflow", agency_id, resources, version, key, c,
                                        updated_after, first_n_observations, last_n_observations,
                                        dimension_at_observation, attributes, measures,
                                        include_history)

    def get_data_provision_agreements(self, agency_id=None, resources=None,
                                      version=None, key=None, c=None, updated_after=None,
                                      first_n_observations=None, last_n_observations=None,
                                      dimension_at_observation=None, attributes=None,
                                      measures=None, include_history=None):
        """
        Returns URL and params to get data

        :param agency_id: The id of the data (provision agreement)
        :param resources: The resources to query
        :param version: The version of the data (provision agreement)
        :param key: The key is constructed as a dot ('.') separated list of
                    dimension filtered values.
        :param c: Filter data by component value
        :param updated_after: Data filtered by the last update date
        :param first_n_observations: Number of first observations to be returned
                                     per key
        :param last_n_observations: Number of last observations to be returned
                                    per key
        :param dimension_at_observation: The dimension at observation
        :param attributes: Attributes of the data (provision agreement)
        :param measures: Measures of the data (provision agreement)
        :param include_history: Value to include history (true, false)
        :return: The URL and params formatted
        """
        return self.common_data_queries("provisionagreement", agency_id, resources, version, key, c,
                                        updated_after, first_n_observations, last_n_observations,
                                        dimension_at_observation, attributes, measures,
                                        include_history)

    def get_data_all_contexts(self, agency_id=None, resources=None,
                              version=None, key=None, c=None, updated_after=None,
                              first_n_observations=None, last_n_observations=None,
                              dimension_at_observation=None, attributes=None,
                              measures=None, include_history=None):
        """
        Returns URL and params to get data

        :param agency_id: The id of the data (all possible contexts)
        :param resources: The resources to query
        :param version: The version of the data (all possible contexts)
        :param key: The key is constructed as a dot ('.') separated list of
                    dimension filtered values.
        :param c: Filter data by component value
        :param updated_after: Data filtered by the last update date
        :param first_n_observations: Number of first observations to be returned
                                     per key
        :param last_n_observations: Number of last observations to be returned
                                    per key
        :param dimension_at_observation: The dimension at observation
        :param attributes: Attributes of the data (all possible contexts)
        :param measures: Measures of the data (all possible contexts)
        :param include_history: Value to include history (true, false)
        :return: The URL and params formatted
        """
        return self.common_data_queries("all", agency_id, resources, version, key, c,
                                        updated_after, first_n_observations, last_n_observations,
                                        dimension_at_observation, attributes, measures,
                                        include_history)

    def get_constraints(self, flow, key=None, provider=None, component_id=None,
                        mode=None, references=None, start_period=None,
                        end_period=None, updated_after=None):
        pass

    def get_constraint_datastructures(self, agency_id=None, resources=None,
                                      version=None, key=None, component_id=None, c=None,
                                      mode=None, references=None, updated_after=None):
        """
                Returns URL and params to get constraints

                :param agency_id: The id of the constraint (datastructure)
                :param resources: The resources to query
                :param version: The version of the constraint (datastructure)
                :param key: The key is constructed as a dot ('.') separated list of
                            dimension filtered values.
                :param component_id: The id of the dimension of constraint (datastructure)
                :param c: Filter data by component value
                :param version: The version of the constraint (datastructure)
                :param mode: The mode parameter (exact, available)
                :param references: The references parameter (none, all, datastructure,conceptscheme,
                                                            codelist, dataproviderscheme, dataflow)
                :param updated_after: Data filtered by the last update date
                """

        return self.common_constraints_queries("datastructure", agency_id, resources, version, key,
                                               component_id, c, mode, references, updated_after)

    def get_constraint_dataflows(self, agency_id=None, resources=None,
                                 version=None, key=None, component_id=None, c=None,
                                 mode=None, references=None, updated_after=None):
        """
                Returns URL and params to get constraints

                :param agency_id: The id of the constraint (dataflow)
                :param resources: The resources to query
                :param version: The version of the constraint (dataflow)
                :param key: The key is constructed as a dot ('.') separated list of
                            dimension filtered values.
                :param component_id: The id of the dimension of constraint (dataflow)
                :param c: Filter data by component value
                :param version: The version of the constraint (dataflow)
                :param mode: The mode parameter (exact, available)
                :param references: The references parameter (none, all, datastructure,conceptscheme,
                                                            codelist, dataproviderscheme, dataflow)
                :param updated_after: Data filtered by the last update date
                """

        return self.common_constraints_queries("dataflow", agency_id, resources, version, key,
                                               component_id, c, mode, references, updated_after)

    def get_constraint_provision_agreements(self, agency_id=None, resources=None,
                                            version=None, key=None, component_id=None, c=None,
                                            mode=None, references=None, updated_after=None):
        """
                Returns URL and params to get constraints

                :param agency_id: The id of the constraint (provision agreement)
                :param resources: The resources to query
                :param version: The version of the constraint (provision agreement)
                :param key: The key is constructed as a dot ('.') separated list of
                            dimension filtered values.
                :param component_id: The id of the dimension of constraint (provision agreement)
                :param c: Filter data by component value
                :param version: The version of the constraint (provision agreement)
                :param mode: The mode parameter (exact, available)
                :param references: The references parameter (none, all, datastructure,conceptscheme,
                                                            codelist, dataproviderscheme, dataflow)
                :param updated_after: Data filtered by the last update date
                """

        return self.common_constraints_queries("provisionagreement", agency_id, resources, version, key,
                                               component_id, c, mode, references, updated_after)

    def get_constraint_all_contexts(self, agency_id=None, resources=None,
                                    version=None, key=None, component_id=None, c=None,
                                    mode=None, references=None, updated_after=None):
        """
                Returns URL and params to get constraints

                :param agency_id: The id of the constraint (all possible contexts)
                :param resources: The resources to query
                :param version: The version of the constraint (all possible contexts)
                :param key: The key is constructed as a dot ('.') separated list of
                            dimension filtered values.
                :param component_id: The id of the dimension of constraint (all possible contexts)
                :param c: Filter data by component value
                :param version: The version of the constraint (all possible contexts)
                :param mode: The mode parameter (exact, available)
                :param references: The references parameter (none, all, datastructure,conceptscheme,
                                                            codelist, dataproviderscheme, dataflow)
                :param updated_after: Data filtered by the last update date
                """

        return self.common_constraints_queries("all", agency_id, resources, version, key,
                                               component_id, c, mode, references, updated_after)

    def get_schema_datastructures(self, agency_id=None, resources=None,
                                  version=None, dimension_at_observation=None,
                                  explicit_measure=None):
        """
                Returns URL and params to get schema (datastructure)

                :param agency_id: The id of the schema (datastructure)
                :param resources: The resources to query
                :param version: The version of the schema (datastructure)
                :param dimension_at_observation: The dimension at observation
                :param explicit_measure: Indicates whether observations are strongly typed
                                          (false, true)
                """

        return self.common_schema_queries("datastructure", agency_id, resources, version,
                                          dimension_at_observation, explicit_measure)

    def get_schema_meta_datastructures(self, agency_id=None, resources=None,
                                       version=None, dimension_at_observation=None,
                                       explicit_measure=None):
        """
                Returns URL and params to get schema (metadatastructure)

                :param agency_id: The id of the schema (metadatastructure)
                :param resources: The resources to query
                :param version: The version of the schema (metadatastructure)
                :param dimension_at_observation: The dimension at observation
                :param explicit_measure: Indicates whether observations are strongly typed
                                          (false, true)
                """

        return self.common_schema_queries("metadatastructure", agency_id, resources, version,
                                          dimension_at_observation, explicit_measure)

    def get_schema_dataflows(self, agency_id=None, resources=None,
                             version=None, dimension_at_observation=None,
                             explicit_measure=None):
        """
                Returns URL and params to get schema (dataflow)

                :param agency_id: The id of the schema (dataflow)
                :param resources: The resources to query
                :param version: The version of the schema (dataflow)
                :param dimension_at_observation: The dimension at observation
                :param explicit_measure: Indicates whether observations are strongly typed
                                          (false, true)
                """

        return self.common_schema_queries("dataflow", agency_id, resources, version,
                                          dimension_at_observation, explicit_measure)

    def get_schema_meta_dataflows(self, agency_id=None, resources=None,
                                  version=None, dimension_at_observation=None,
                                  explicit_measure=None):
        """
                Returns URL and params to get schema (metadataflow)

                :param agency_id: The id of the schema (metadataflow)
                :param resources: The resources to query
                :param version: The version of the schema (metadataflow)
                :param dimension_at_observation: The dimension at observation
                :param explicit_measure: Indicates whether observations are strongly typed
                                          (false, true)
                """

        return self.common_schema_queries("metadataflow", agency_id, resources, version,
                                          dimension_at_observation, explicit_measure)

    def get_schema_provision_agreements(self, agency_id=None, resources=None,
                                        version=None, dimension_at_observation=None,
                                        explicit_measure=None):
        """
                Returns URL and params to get schema (provision agreement)

                :param agency_id: The id of the schema (provision agreement)
                :param resources: The resources to query
                :param version: The version of the schema (provision agreement)
                :param dimension_at_observation: The dimension at observation
                :param explicit_measure: Indicates whether observations are strongly typed
                                          (false, true)
                """

        return self.common_schema_queries("provisionagreement", agency_id, resources, version,
                                          dimension_at_observation, explicit_measure)

    def get_dsds(self, agency_id=None, resources=None,
                 version=None, references=None, detail=None) -> str:

        """
        Returns URL and params to get datastructure

        :param agency_id: The agency id of the data structure definitions
        :param resources: The resources to query
        :param version: The version of the data structure definitions
        :param references: The references parameter (none, parents, parentsandsiblings,
                            ancestors, children, descendants, all, datastructure,
                            metadatastructure, categoryscheme, conceptscheme,
                            codelist, hierarchy, hierarchyassociation, agencyscheme,
                            dataproviderscheme, dataconsumerscheme, organisationunitscheme,
                            dataflow, metadataflow, reportingtaxonomy, provisionagreement,
                            structureset, process, categorisation, dataconstraint,
                            metadataconstraint, transformationscheme, rulesetscheme,
                            userdefinedoperatorscheme, customtypescheme,namepersonalisationscheme,
                            namealiasscheme, valuelist, structuremap, representationmap,
                            conceptscheme, categoryschememap, organisationschememap,
                            reportingtaxonomymap)
        :param detail: The detail parameter (full, allstubs, referencestubs,
                        allcompletestubs, referencecompletestubs, referencepartial, raw)

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
        :param references: The references parameter (none, parents, parentsandsiblings,
                            ancestors, children, descendants, all, datastructure,
                            metadatastructure, categoryscheme, conceptscheme,
                            codelist, hierarchy, hierarchyassociation, agencyscheme,
                            dataproviderscheme, dataconsumerscheme, organisationunitscheme,
                            dataflow, metadataflow, reportingtaxonomy, provisionagreement,
                            structureset, process, categorisation, dataconstraint,
                            metadataconstraint, transformationscheme, rulesetscheme,
                            userdefinedoperatorscheme, customtypescheme,namepersonalisationscheme,
                            namealiasscheme, valuelist, structuremap, representationmap,
                            conceptscheme, categoryschememap, organisationschememap,
                            reportingtaxonomymap)
        :param detail: The detail parameter (full, allstubs, referencestubs,
                        allcompletestubs, referencecompletestubs, referencepartial, raw)

        :return: The URL and params formatted
        """

        return self.common_structure_queries("metadatastructure", agency_id, resources,
                                             version, references, detail)

    def get_data_flows(self, agency_id=None, resources=None,
                       version=None, references=None, detail=None) -> str:
        """
        Returns URL and params to get dataflows

        :param agency_id: The agency id of the dataflows
        :param resources: The resources to query
        :param version: The version of the dataflows
        :param references: The references parameter (none, parents, parentsandsiblings,
                            ancestors, children, descendants, all, datastructure,
                            metadatastructure, categoryscheme, conceptscheme,
                            codelist, hierarchy, hierarchyassociation, agencyscheme,
                            dataproviderscheme, dataconsumerscheme, organisationunitscheme,
                            dataflow, metadataflow, reportingtaxonomy, provisionagreement,
                            structureset, process, categorisation, dataconstraint,
                            metadataconstraint, transformationscheme, rulesetscheme,
                            userdefinedoperatorscheme, customtypescheme,namepersonalisationscheme,
                            namealiasscheme, valuelist, structuremap, representationmap,
                            conceptscheme, categoryschememap, organisationschememap,
                            reportingtaxonomymap)
        :param detail: The detail parameter (full, allstubs, referencestubs,
                        allcompletestubs, referencecompletestubs, referencepartial, raw)

        :return: The URL and params formatted
        """
        return self.common_structure_queries("dataflow", agency_id, resources,
                                             version, references, detail)

    def get_meta_data_flows(self, agency_id=None, resources=None,
                            version=None, references=None, detail=None) -> str:

        """
        Returns URL and params to get metadata_flows

        :param agency_id: The agency id of metadata_flows
        :param resources: The resources to query
        :param version: The version of the metadata_flows
        :param references: The references parameter (none, parents, parentsandsiblings,
                            ancestors, children, descendants, all, datastructure,
                            metadatastructure, categoryscheme, conceptscheme,
                            codelist, hierarchy, hierarchyassociation, agencyscheme,
                            dataproviderscheme, dataconsumerscheme, organisationunitscheme,
                            dataflow, metadataflow, reportingtaxonomy, provisionagreement,
                            structureset, process, categorisation, dataconstraint,
                            metadataconstraint, transformationscheme, rulesetscheme,
                            userdefinedoperatorscheme, customtypescheme,namepersonalisationscheme,
                            namealiasscheme, valuelist, structuremap, representationmap,
                            conceptscheme, categoryschememap, organisationschememap,
                            reportingtaxonomymap)
        :param detail: The detail parameter (full, allstubs, referencestubs,
                        allcompletestubs, referencecompletestubs, referencepartial, raw)

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
        :param references: The references parameter (none, parents, parentsandsiblings,
                            ancestors, children, descendants, all, datastructure,
                            metadatastructure, categoryscheme, conceptscheme,
                            codelist, hierarchy, hierarchyassociation, agencyscheme,
                            dataproviderscheme, dataconsumerscheme, organisationunitscheme,
                            dataflow, metadataflow, reportingtaxonomy, provisionagreement,
                            structureset, process, categorisation, dataconstraint,
                            metadataconstraint, transformationscheme, rulesetscheme,
                            userdefinedoperatorscheme, customtypescheme,namepersonalisationscheme,
                            namealiasscheme, valuelist, structuremap, representationmap,
                            conceptscheme, categoryschememap, organisationschememap,
                            reportingtaxonomymap)
        :param detail: The detail parameter (full, allstubs, referencestubs,
                        allcompletestubs, referencecompletestubs, referencepartial, raw)

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
        :param references: The references parameter (none, parents, parentsandsiblings,
                            ancestors, children, descendants, all, datastructure,
                            metadatastructure, categoryscheme, conceptscheme,
                            codelist, hierarchy, hierarchyassociation, agencyscheme,
                            dataproviderscheme, dataconsumerscheme, organisationunitscheme,
                            dataflow, metadataflow, reportingtaxonomy, provisionagreement,
                            structureset, process, categorisation, dataconstraint,
                            metadataconstraint, transformationscheme, rulesetscheme,
                            userdefinedoperatorscheme, customtypescheme,namepersonalisationscheme,
                            namealiasscheme, valuelist, structuremap, representationmap,
                            conceptscheme, categoryschememap, organisationschememap,
                            reportingtaxonomymap)
        :param detail: The detail parameter (full, allstubs, referencestubs,
                        allcompletestubs, referencecompletestubs, referencepartial, raw)

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
        :param references: The references parameter (none, parents, parentsandsiblings,
                            ancestors, children, descendants, all, datastructure,
                            metadatastructure, categoryscheme, conceptscheme,
                            codelist, hierarchy, hierarchyassociation, agencyscheme,
                            dataproviderscheme, dataconsumerscheme, organisationunitscheme,
                            dataflow, metadataflow, reportingtaxonomy, provisionagreement,
                            structureset, process, categorisation, dataconstraint,
                            metadataconstraint, transformationscheme, rulesetscheme,
                            userdefinedoperatorscheme, customtypescheme,namepersonalisationscheme,
                            namealiasscheme, valuelist, structuremap, representationmap,
                            conceptscheme, categoryschememap, organisationschememap,
                            reportingtaxonomymap)
        :param detail: The detail parameter (full, allstubs, referencestubs,
                        allcompletestubs, referencecompletestubs, referencepartial, raw)

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
        :param references: The references parameter (none, parents, parentsandsiblings,
                            ancestors, children, descendants, all, datastructure,
                            metadatastructure, categoryscheme, conceptscheme,
                            codelist, hierarchy, hierarchyassociation, agencyscheme,
                            dataproviderscheme, dataconsumerscheme, organisationunitscheme,
                            dataflow, metadataflow, reportingtaxonomy, provisionagreement,
                            structureset, process, categorisation, dataconstraint,
                            metadataconstraint, transformationscheme, rulesetscheme,
                            userdefinedoperatorscheme, customtypescheme,namepersonalisationscheme,
                            namealiasscheme, valuelist, structuremap, representationmap,
                            conceptscheme, categoryschememap, organisationschememap,
                            reportingtaxonomymap)
        :param detail: The detail parameter (full, allstubs, referencestubs,
                        allcompletestubs, referencecompletestubs, referencepartial, raw)

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
        :param references: The references parameter (none, parents, parentsandsiblings,
                            ancestors, children, descendants, all, datastructure,
                            metadatastructure, categoryscheme, conceptscheme,
                            codelist, hierarchy, hierarchyassociation, agencyscheme,
                            dataproviderscheme, dataconsumerscheme, organisationunitscheme,
                            dataflow, metadataflow, reportingtaxonomy, provisionagreement,
                            structureset, process, categorisation, dataconstraint,
                            metadataconstraint, transformationscheme, rulesetscheme,
                            userdefinedoperatorscheme, customtypescheme,namepersonalisationscheme,
                            namealiasscheme, valuelist, structuremap, representationmap,
                            conceptscheme, categoryschememap, organisationschememap,
                            reportingtaxonomymap)
        :param detail: The detail parameter (full, allstubs, referencestubs,
                        allcompletestubs, referencecompletestubs, referencepartial, raw)

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
        :param references: The references parameter (none, parents, parentsandsiblings,
                            ancestors, children, descendants, all, datastructure,
                            metadatastructure, categoryscheme, conceptscheme,
                            codelist, hierarchy, hierarchyassociation, agencyscheme,
                            dataproviderscheme, dataconsumerscheme, organisationunitscheme,
                            dataflow, metadataflow, reportingtaxonomy, provisionagreement,
                            structureset, process, categorisation, dataconstraint,
                            metadataconstraint, transformationscheme, rulesetscheme,
                            userdefinedoperatorscheme, customtypescheme,namepersonalisationscheme,
                            namealiasscheme, valuelist, structuremap, representationmap,
                            conceptscheme, categoryschememap, organisationschememap,
                            reportingtaxonomymap)
        :param detail: The detail parameter (full, allstubs, referencestubs,
                        allcompletestubs, referencecompletestubs, referencepartial, raw)

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
        :param references: The references parameter (none, parents, parentsandsiblings,
                            ancestors, children, descendants, all, datastructure,
                            metadatastructure, categoryscheme, conceptscheme,
                            codelist, hierarchy, hierarchyassociation, agencyscheme,
                            dataproviderscheme, dataconsumerscheme, organisationunitscheme,
                            dataflow, metadataflow, reportingtaxonomy, provisionagreement,
                            structureset, process, categorisation, dataconstraint,
                            metadataconstraint, transformationscheme, rulesetscheme,
                            userdefinedoperatorscheme, customtypescheme,namepersonalisationscheme,
                            namealiasscheme, valuelist, structuremap, representationmap,
                            conceptscheme, categoryschememap, organisationschememap,
                            reportingtaxonomymap)
        :param detail: The detail parameter (full, allstubs, referencestubs,
                        allcompletestubs, referencecompletestubs, referencepartial, raw)

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
        :param references: The references parameter (none, parents, parentsandsiblings,
                            ancestors, children, descendants, all, datastructure,
                            metadatastructure, categoryscheme, conceptscheme,
                            codelist, hierarchy, hierarchyassociation, agencyscheme,
                            dataproviderscheme, dataconsumerscheme, organisationunitscheme,
                            dataflow, metadataflow, reportingtaxonomy, provisionagreement,
                            structureset, process, categorisation, dataconstraint,
                            metadataconstraint, transformationscheme, rulesetscheme,
                            userdefinedoperatorscheme, customtypescheme,namepersonalisationscheme,
                            namealiasscheme, valuelist, structuremap, representationmap,
                            conceptscheme, categoryschememap, organisationschememap,
                            reportingtaxonomymap)
        :param detail: The detail parameter (full, allstubs, referencestubs,
                        allcompletestubs, referencecompletestubs, referencepartial, raw)

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
        :param references: The references parameter (none, parents, parentsandsiblings,
                            ancestors, children, descendants, all, datastructure,
                            metadatastructure, categoryscheme, conceptscheme,
                            codelist, hierarchy, hierarchyassociation, agencyscheme,
                            dataproviderscheme, dataconsumerscheme, organisationunitscheme,
                            dataflow, metadataflow, reportingtaxonomy, provisionagreement,
                            structureset, process, categorisation, dataconstraint,
                            metadataconstraint, transformationscheme, rulesetscheme,
                            userdefinedoperatorscheme, customtypescheme,namepersonalisationscheme,
                            namealiasscheme, valuelist, structuremap, representationmap,
                            conceptscheme, categoryschememap, organisationschememap,
                            reportingtaxonomymap)
        :param detail: The detail parameter (full, allstubs, referencestubs,
                        allcompletestubs, referencecompletestubs, referencepartial, raw)

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
        :param references: The references parameter (none, parents, parentsandsiblings,
                            ancestors, children, descendants, all, datastructure,
                            metadatastructure, categoryscheme, conceptscheme,
                            codelist, hierarchy, hierarchyassociation, agencyscheme,
                            dataproviderscheme, dataconsumerscheme, organisationunitscheme,
                            dataflow, metadataflow, reportingtaxonomy, provisionagreement,
                            structureset, process, categorisation, dataconstraint,
                            metadataconstraint, transformationscheme, rulesetscheme,
                            userdefinedoperatorscheme, customtypescheme,namepersonalisationscheme,
                            namealiasscheme, valuelist, structuremap, representationmap,
                            conceptscheme, categoryschememap, organisationschememap,
                            reportingtaxonomymap)
        :param detail: The detail parameter (full, allstubs, referencestubs,
                        allcompletestubs, referencecompletestubs, referencepartial, raw)

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
        :param references: The references parameter (none, parents, parentsandsiblings,
                            ancestors, children, descendants, all, datastructure,
                            metadatastructure, categoryscheme, conceptscheme,
                            codelist, hierarchy, hierarchyassociation, agencyscheme,
                            dataproviderscheme, dataconsumerscheme, organisationunitscheme,
                            dataflow, metadataflow, reportingtaxonomy, provisionagreement,
                            structureset, process, categorisation, dataconstraint,
                            metadataconstraint, transformationscheme, rulesetscheme,
                            userdefinedoperatorscheme, customtypescheme,namepersonalisationscheme,
                            namealiasscheme, valuelist, structuremap, representationmap,
                            conceptscheme, categoryschememap, organisationschememap,
                            reportingtaxonomymap)
        :param detail: The detail parameter (full, allstubs, referencestubs,
                        allcompletestubs, referencecompletestubs, referencepartial, raw)

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
        :param references: The references parameter (none, parents, parentsandsiblings,
                            ancestors, children, descendants, all, datastructure,
                            metadatastructure, categoryscheme, conceptscheme,
                            codelist, hierarchy, hierarchyassociation, agencyscheme,
                            dataproviderscheme, dataconsumerscheme, organisationunitscheme,
                            dataflow, metadataflow, reportingtaxonomy, provisionagreement,
                            structureset, process, categorisation, dataconstraint,
                            metadataconstraint, transformationscheme, rulesetscheme,
                            userdefinedoperatorscheme, customtypescheme,namepersonalisationscheme,
                            namealiasscheme, valuelist, structuremap, representationmap,
                            conceptscheme, categoryschememap, organisationschememap,
                            reportingtaxonomymap)
        :param detail: The detail parameter (full, allstubs, referencestubs,
                        allcompletestubs, referencecompletestubs, referencepartial, raw)

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
        :param references: The references parameter (none, parents, parentsandsiblings,
                            ancestors, children, descendants, all, datastructure,
                            metadatastructure, categoryscheme, conceptscheme,
                            codelist, hierarchy, hierarchyassociation, agencyscheme,
                            dataproviderscheme, dataconsumerscheme, organisationunitscheme,
                            dataflow, metadataflow, reportingtaxonomy, provisionagreement,
                            structureset, process, categorisation, dataconstraint,
                            metadataconstraint, transformationscheme, rulesetscheme,
                            userdefinedoperatorscheme, customtypescheme,namepersonalisationscheme,
                            namealiasscheme, valuelist, structuremap, representationmap,
                            conceptscheme, categoryschememap, organisationschememap,
                            reportingtaxonomymap)
        :param detail: The detail parameter (full, allstubs, referencestubs,
                        allcompletestubs, referencecompletestubs, referencepartial, raw)

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
        :param references: The references parameter (none, parents, parentsandsiblings,
                            ancestors, children, descendants, all, datastructure,
                            metadatastructure, categoryscheme, conceptscheme,
                            codelist, hierarchy, hierarchyassociation, agencyscheme,
                            dataproviderscheme, dataconsumerscheme, organisationunitscheme,
                            dataflow, metadataflow, reportingtaxonomy, provisionagreement,
                            structureset, process, categorisation, dataconstraint,
                            metadataconstraint, transformationscheme, rulesetscheme,
                            userdefinedoperatorscheme, customtypescheme,namepersonalisationscheme,
                            namealiasscheme, valuelist, structuremap, representationmap,
                            conceptscheme, categoryschememap, organisationschememap,
                            reportingtaxonomymap)
        :param detail: The detail parameter (full, allstubs, referencestubs,
                        allcompletestubs, referencecompletestubs, referencepartial, raw)

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
        :param references: The references parameter (none, parents, parentsandsiblings,
                            ancestors, children, descendants, all, datastructure,
                            metadatastructure, categoryscheme, conceptscheme,
                            codelist, hierarchy, hierarchyassociation, agencyscheme,
                            dataproviderscheme, dataconsumerscheme, organisationunitscheme,
                            dataflow, metadataflow, reportingtaxonomy, provisionagreement,
                            structureset, process, categorisation, dataconstraint,
                            metadataconstraint, transformationscheme, rulesetscheme,
                            userdefinedoperatorscheme, customtypescheme,namepersonalisationscheme,
                            namealiasscheme, valuelist, structuremap, representationmap,
                            conceptscheme, categoryschememap, organisationschememap,
                            reportingtaxonomymap)
        :param detail: The detail parameter (full, allstubs, referencestubs,
                        allcompletestubs, referencecompletestubs, referencepartial, raw)

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
        :param references: The references parameter (none, parents, parentsandsiblings,
                            ancestors, children, descendants, all, datastructure,
                            metadatastructure, categoryscheme, conceptscheme,
                            codelist, hierarchy, hierarchyassociation, agencyscheme,
                            dataproviderscheme, dataconsumerscheme, organisationunitscheme,
                            dataflow, metadataflow, reportingtaxonomy, provisionagreement,
                            structureset, process, categorisation, dataconstraint,
                            metadataconstraint, transformationscheme, rulesetscheme,
                            userdefinedoperatorscheme, customtypescheme,namepersonalisationscheme,
                            namealiasscheme, valuelist, structuremap, representationmap,
                            conceptscheme, categoryschememap, organisationschememap,
                            reportingtaxonomymap)
        :param detail: The detail parameter (full, allstubs, referencestubs,
                        allcompletestubs, referencecompletestubs, referencepartial, raw)

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
        :param references: The references parameter (none, parents, parentsandsiblings,
                            ancestors, children, descendants, all, datastructure,
                            metadatastructure, categoryscheme, conceptscheme,
                            codelist, hierarchy, hierarchyassociation, agencyscheme,
                            dataproviderscheme, dataconsumerscheme, organisationunitscheme,
                            dataflow, metadataflow, reportingtaxonomy, provisionagreement,
                            structureset, process, categorisation, dataconstraint,
                            metadataconstraint, transformationscheme, rulesetscheme,
                            userdefinedoperatorscheme, customtypescheme,namepersonalisationscheme,
                            namealiasscheme, valuelist, structuremap, representationmap,
                            conceptscheme, categoryschememap, organisationschememap,
                            reportingtaxonomymap)
        :param detail: The detail parameter (full, allstubs, referencestubs,
                        allcompletestubs, referencecompletestubs, referencepartial, raw)

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
        :param references: The references parameter (none, parents, parentsandsiblings,
                            ancestors, children, descendants, all, datastructure,
                            metadatastructure, categoryscheme, conceptscheme,
                            codelist, hierarchy, hierarchyassociation, agencyscheme,
                            dataproviderscheme, dataconsumerscheme, organisationunitscheme,
                            dataflow, metadataflow, reportingtaxonomy, provisionagreement,
                            structureset, process, categorisation, dataconstraint,
                            metadataconstraint, transformationscheme, rulesetscheme,
                            userdefinedoperatorscheme, customtypescheme,namepersonalisationscheme,
                            namealiasscheme, valuelist, structuremap, representationmap,
                            conceptscheme, categoryschememap, organisationschememap,
                            reportingtaxonomymap)
        :param detail: The detail parameter (full, allstubs, referencestubs,
                        allcompletestubs, referencecompletestubs, referencepartial, raw)

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
        :param references: The references parameter (none, parents, parentsandsiblings,
                            ancestors, children, descendants, all, datastructure,
                            metadatastructure, categoryscheme, conceptscheme,
                            codelist, hierarchy, hierarchyassociation, agencyscheme,
                            dataproviderscheme, dataconsumerscheme, organisationunitscheme,
                            dataflow, metadataflow, reportingtaxonomy, provisionagreement,
                            structureset, process, categorisation, dataconstraint,
                            metadataconstraint, transformationscheme, rulesetscheme,
                            userdefinedoperatorscheme, customtypescheme,namepersonalisationscheme,
                            namealiasscheme, valuelist, structuremap, representationmap,
                            conceptscheme, categoryschememap, organisationschememap,
                            reportingtaxonomymap)
        :param detail: The detail parameter (full, allstubs, referencestubs,
                        allcompletestubs, referencecompletestubs, referencepartial, raw)

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
        :param references: The references parameter (none, parents, parentsandsiblings,
                            ancestors, children, descendants, all, datastructure,
                            metadatastructure, categoryscheme, conceptscheme,
                            codelist, hierarchy, hierarchyassociation, agencyscheme,
                            dataproviderscheme, dataconsumerscheme, organisationunitscheme,
                            dataflow, metadataflow, reportingtaxonomy, provisionagreement,
                            structureset, process, categorisation, dataconstraint,
                            metadataconstraint, transformationscheme, rulesetscheme,
                            userdefinedoperatorscheme, customtypescheme,namepersonalisationscheme,
                            namealiasscheme, valuelist, structuremap, representationmap,
                            conceptscheme, categoryschememap, organisationschememap,
                            reportingtaxonomymap)
        :param detail: The detail parameter (full, allstubs, referencestubs,
                        allcompletestubs, referencecompletestubs, referencepartial, raw)

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
        :param references: The references parameter (none, parents, parentsandsiblings,
                            ancestors, children, descendants, all, datastructure,
                            metadatastructure, categoryscheme, conceptscheme,
                            codelist, hierarchy, hierarchyassociation, agencyscheme,
                            dataproviderscheme, dataconsumerscheme, organisationunitscheme,
                            dataflow, metadataflow, reportingtaxonomy, provisionagreement,
                            structureset, process, categorisation, dataconstraint,
                            metadataconstraint, transformationscheme, rulesetscheme,
                            userdefinedoperatorscheme, customtypescheme,namepersonalisationscheme,
                            namealiasscheme, valuelist, structuremap, representationmap,
                            conceptscheme, categoryschememap, organisationschememap,
                            reportingtaxonomymap)
        :param detail: The detail parameter (full, allstubs, referencestubs,
                        allcompletestubs, referencecompletestubs, referencepartial, raw)

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
        :param references: The references parameter (none, parents, parentsandsiblings,
                            ancestors, children, descendants, all, datastructure,
                            metadatastructure, categoryscheme, conceptscheme,
                            codelist, hierarchy, hierarchyassociation, agencyscheme,
                            dataproviderscheme, dataconsumerscheme, organisationunitscheme,
                            dataflow, metadataflow, reportingtaxonomy, provisionagreement,
                            structureset, process, categorisation, dataconstraint,
                            metadataconstraint, transformationscheme, rulesetscheme,
                            userdefinedoperatorscheme, customtypescheme,namepersonalisationscheme,
                            namealiasscheme, valuelist, structuremap, representationmap,
                            conceptscheme, categoryschememap, organisationschememap,
                            reportingtaxonomymap)
        :param detail: The detail parameter (full, allstubs, referencestubs,
                        allcompletestubs, referencecompletestubs, referencepartial, raw)

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
        :param references: The references parameter (none, parents, parentsandsiblings,
                            ancestors, children, descendants, all, datastructure,
                            metadatastructure, categoryscheme, conceptscheme,
                            codelist, hierarchy, hierarchyassociation, agencyscheme,
                            dataproviderscheme, dataconsumerscheme, organisationunitscheme,
                            dataflow, metadataflow, reportingtaxonomy, provisionagreement,
                            structureset, process, categorisation, dataconstraint,
                            metadataconstraint, transformationscheme, rulesetscheme,
                            userdefinedoperatorscheme, customtypescheme,namepersonalisationscheme,
                            namealiasscheme, valuelist, structuremap, representationmap,
                            conceptscheme, categoryschememap, organisationschememap,
                            reportingtaxonomymap)
        :param detail: The detail parameter (full, allstubs, referencestubs,
                        allcompletestubs, referencecompletestubs, referencepartial, raw)

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
        :param references: The references parameter (none, parents, parentsandsiblings,
                            ancestors, children, descendants, all, datastructure,
                            metadatastructure, categoryscheme, conceptscheme,
                            codelist, hierarchy, hierarchyassociation, agencyscheme,
                            dataproviderscheme, dataconsumerscheme, organisationunitscheme,
                            dataflow, metadataflow, reportingtaxonomy, provisionagreement,
                            structureset, process, categorisation, dataconstraint,
                            metadataconstraint, transformationscheme, rulesetscheme,
                            userdefinedoperatorscheme, customtypescheme,namepersonalisationscheme,
                            namealiasscheme, valuelist, structuremap, representationmap,
                            conceptscheme, categoryschememap, organisationschememap,
                            reportingtaxonomymap)
        :param detail: The detail parameter (full, allstubs, referencestubs,
                        allcompletestubs, referencecompletestubs, referencepartial, raw)

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
        :param references: The references parameter (none, parents, parentsandsiblings,
                            ancestors, children, descendants, all, datastructure,
                            metadatastructure, categoryscheme, conceptscheme,
                            codelist, hierarchy, hierarchyassociation, agencyscheme,
                            dataproviderscheme, dataconsumerscheme, organisationunitscheme,
                            dataflow, metadataflow, reportingtaxonomy, provisionagreement,
                            structureset, process, categorisation, dataconstraint,
                            metadataconstraint, transformationscheme, rulesetscheme,
                            userdefinedoperatorscheme, customtypescheme,namepersonalisationscheme,
                            namealiasscheme, valuelist, structuremap, representationmap,
                            conceptscheme, categoryschememap, organisationschememap,
                            reportingtaxonomymap)
        :param detail: The detail parameter (full, allstubs, referencestubs,
                        allcompletestubs, referencecompletestubs, referencepartial, raw)

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
        :param references: The references parameter (none, parents, parentsandsiblings,
                            ancestors, children, descendants, all, datastructure,
                            metadatastructure, categoryscheme, conceptscheme,
                            codelist, hierarchy, hierarchyassociation, agencyscheme,
                            dataproviderscheme, dataconsumerscheme, organisationunitscheme,
                            dataflow, metadataflow, reportingtaxonomy, provisionagreement,
                            structureset, process, categorisation, dataconstraint,
                            metadataconstraint, transformationscheme, rulesetscheme,
                            userdefinedoperatorscheme, customtypescheme,namepersonalisationscheme,
                            namealiasscheme, valuelist, structuremap, representationmap,
                            conceptscheme, categoryschememap, organisationschememap,
                            reportingtaxonomymap)
        :param detail: The detail parameter (full, allstubs, referencestubs,
                        allcompletestubs, referencecompletestubs, referencepartial, raw)

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
        :param references: The references parameter (none, parents, parentsandsiblings,
                            ancestors, children, descendants, all, datastructure,
                            metadatastructure, categoryscheme, conceptscheme,
                            codelist, hierarchy, hierarchyassociation, agencyscheme,
                            dataproviderscheme, dataconsumerscheme, organisationunitscheme,
                            dataflow, metadataflow, reportingtaxonomy, provisionagreement,
                            structureset, process, categorisation, dataconstraint,
                            metadataconstraint, transformationscheme, rulesetscheme,
                            userdefinedoperatorscheme, customtypescheme,namepersonalisationscheme,
                            namealiasscheme, valuelist, structuremap, representationmap,
                            conceptscheme, categoryschememap, organisationschememap,
                            reportingtaxonomymap)
        :param detail: The detail parameter (full, allstubs, referencestubs,
                        allcompletestubs, referencecompletestubs, referencepartial, raw)

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
        :param references: The references parameter (none, parents, parentsandsiblings,
                            ancestors, children, descendants, all, datastructure,
                            metadatastructure, categoryscheme, conceptscheme,
                            codelist, hierarchy, hierarchyassociation, agencyscheme,
                            dataproviderscheme, dataconsumerscheme, organisationunitscheme,
                            dataflow, metadataflow, reportingtaxonomy, provisionagreement,
                            structureset, process, categorisation, dataconstraint,
                            metadataconstraint, transformationscheme, rulesetscheme,
                            userdefinedoperatorscheme, customtypescheme,namepersonalisationscheme,
                            namealiasscheme, valuelist, structuremap, representationmap,
                            conceptscheme, categoryschememap, organisationschememap,
                            reportingtaxonomymap)
        :param detail: The detail parameter (full, allstubs, referencestubs,
                        allcompletestubs, referencecompletestubs, referencepartial, raw)

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

    def get_concept_scheme_item(self, agency_id=None, resources=None,
                                version=None, item_id=None, references=None, detail=None) -> str:

        """
        Returns URL and params to get concept schemes

        :param agency_id: The agency id of concept schemes in Item Scheme Queries
        :param resources: The resources to query
        :param version: The version of the concept schemes
        :param item_id: The id of the item to be returned
        :param references: The references parameter (none, parents, parentsandsiblings,
                            ancestors, children, descendants, all, datastructure,
                            metadatastructure, categoryscheme, conceptscheme,
                            codelist, hierarchy, hierarchyassociation, agencyscheme,
                            dataproviderscheme, dataconsumerscheme, organisationunitscheme,
                            dataflow, metadataflow, reportingtaxonomy, provisionagreement,
                            structureset, process, categorisation, dataconstraint,
                            metadataconstraint, transformationscheme, rulesetscheme,
                            userdefinedoperatorscheme, customtypescheme,namepersonalisationscheme,
                            namealiasscheme, valuelist, structuremap, representationmap,
                            conceptscheme, categoryschememap, organisationschememap,
                            reportingtaxonomymap)
        :param detail: The detail parameter (full, allstubs, referencestubs,
                        allcompletestubs, referencecompletestubs, referencepartial, raw)

        :return: The URL and params formatted
        """

        return self.common_item_scheme_queries("conceptscheme", agency_id, resources,
                                               version, item_id, references, detail)

    def get_codelist_item(self, agency_id=None, resources=None,
                          version=None, item_id=None, references=None, detail=None) -> str:

        """
        Returns URL and params to get codelists in Item Scheme Queries

        :param agency_id: The agency id of codelists
        :param resources: The resources to query
        :param version: The version of the codelists
        :param item_id: The id of the item to be returned
        :param references: The references parameter (none, parents, parentsandsiblings,
                            ancestors, children, descendants, all, datastructure,
                            metadatastructure, categoryscheme, conceptscheme,
                            codelist, hierarchy, hierarchyassociation, agencyscheme,
                            dataproviderscheme, dataconsumerscheme, organisationunitscheme,
                            dataflow, metadataflow, reportingtaxonomy, provisionagreement,
                            structureset, process, categorisation, dataconstraint,
                            metadataconstraint, transformationscheme, rulesetscheme,
                            userdefinedoperatorscheme, customtypescheme,namepersonalisationscheme,
                            namealiasscheme, valuelist, structuremap, representationmap,
                            conceptscheme, categoryschememap, organisationschememap,
                            reportingtaxonomymap)
        :param detail: The detail parameter (full, allstubs, referencestubs,
                        allcompletestubs, referencecompletestubs, referencepartial, raw)

        :return: The URL and params formatted
        """

        return self.common_item_scheme_queries("codelist", agency_id, resources,
                                               version, item_id, references, detail)

    def get_category_scheme_item(self, agency_id=None, resources=None,
                                 version=None, item_id=None, references=None, detail=None) -> str:

        """
        Returns URL and params to get category schemes in Item Scheme Queries

        :param agency_id: The agency id of category schemes
        :param resources: The resources to query
        :param version: The version of the category schemes
        :param item_id: The id of the item to be returned
        :param references: The references parameter (none, parents, parentsandsiblings,
                            ancestors, children, descendants, all, datastructure,
                            metadatastructure, categoryscheme, conceptscheme,
                            codelist, hierarchy, hierarchyassociation, agencyscheme,
                            dataproviderscheme, dataconsumerscheme, organisationunitscheme,
                            dataflow, metadataflow, reportingtaxonomy, provisionagreement,
                            structureset, process, categorisation, dataconstraint,
                            metadataconstraint, transformationscheme, rulesetscheme,
                            userdefinedoperatorscheme, customtypescheme,namepersonalisationscheme,
                            namealiasscheme, valuelist, structuremap, representationmap,
                            conceptscheme, categoryschememap, organisationschememap,
                            reportingtaxonomymap)
        :param detail: The detail parameter (full, allstubs, referencestubs,
                        allcompletestubs, referencecompletestubs, referencepartial, raw)

        :return: The URL and params formatted
        """

        return self.common_item_scheme_queries("categoryscheme", agency_id, resources,
                                               version, item_id, references, detail)

    def get_agency_scheme_item(self, agency_id=None, resources=None,
                               version=None, item_id=None, references=None, detail=None) -> str:

        """
        Returns URL and params to get agency schemes in Item Scheme Queries

        :param agency_id: The agency id of category schemes
        :param resources: The resources to query
        :param version: The version of the category schemes
        :param item_id: The id of the item to be returned
        :param references: The references parameter (none, parents, parentsandsiblings,
                            ancestors, children, descendants, all, datastructure,
                            metadatastructure, categoryscheme, conceptscheme,
                            codelist, hierarchy, hierarchyassociation, agencyscheme,
                            dataproviderscheme, dataconsumerscheme, organisationunitscheme,
                            dataflow, metadataflow, reportingtaxonomy, provisionagreement,
                            structureset, process, categorisation, dataconstraint,
                            metadataconstraint, transformationscheme, rulesetscheme,
                            userdefinedoperatorscheme, customtypescheme,namepersonalisationscheme,
                            namealiasscheme, valuelist, structuremap, representationmap,
                            conceptscheme, categoryschememap, organisationschememap,
                            reportingtaxonomymap)
        :param detail: The detail parameter (full, allstubs, referencestubs,
                        allcompletestubs, referencecompletestubs, referencepartial, raw)

        :return: The URL and params formatted
        """

        return self.common_item_scheme_queries("agencyscheme", agency_id, resources,
                                               version, item_id, references, detail)

    def get_data_provider_scheme_item(self, agency_id=None, resources=None,
                                      version=None, item_id=None, references=None, detail=None) -> str:

        """
        Returns URL and params to get data provider schemes in Item Scheme Queries

        :param agency_id: The agency id of data provider schemes
        :param resources: The resources to query
        :param version: The version of the data provider schemes
        :param item_id: The id of the item to be returned
        :param references: The references parameter (none, parents, parentsandsiblings,
                            ancestors, children, descendants, all, datastructure,
                            metadatastructure, categoryscheme, conceptscheme,
                            codelist, hierarchy, hierarchyassociation, agencyscheme,
                            dataproviderscheme, dataconsumerscheme, organisationunitscheme,
                            dataflow, metadataflow, reportingtaxonomy, provisionagreement,
                            structureset, process, categorisation, dataconstraint,
                            metadataconstraint, transformationscheme, rulesetscheme,
                            userdefinedoperatorscheme, customtypescheme,namepersonalisationscheme,
                            namealiasscheme, valuelist, structuremap, representationmap,
                            conceptscheme, categoryschememap, organisationschememap,
                            reportingtaxonomymap)
        :param detail: The detail parameter (full, allstubs, referencestubs,
                        allcompletestubs, referencecompletestubs, referencepartial, raw)

        :return: The URL and params formatted
        """

        return self.common_item_scheme_queries("dataproviderscheme", agency_id, resources,
                                               version, item_id, references, detail)

    def get_data_consumer_scheme_item(self, agency_id=None, resources=None,
                                      version=None, item_id=None, references=None, detail=None) -> str:

        """
        Returns URL and params to get data provider schemes in Item Scheme Queries

        :param agency_id: The agency id of data consumer schemes
        :param resources: The resources to query
        :param version: The version of the data consumer schemes
        :param item_id: The id of the item to be returned
        :param references: The references parameter (none, parents, parentsandsiblings,
                            ancestors, children, descendants, all, datastructure,
                            metadatastructure, categoryscheme, conceptscheme,
                            codelist, hierarchy, hierarchyassociation, agencyscheme,
                            dataproviderscheme, dataconsumerscheme, organisationunitscheme,
                            dataflow, metadataflow, reportingtaxonomy, provisionagreement,
                            structureset, process, categorisation, dataconstraint,
                            metadataconstraint, transformationscheme, rulesetscheme,
                            userdefinedoperatorscheme, customtypescheme,namepersonalisationscheme,
                            namealiasscheme, valuelist, structuremap, representationmap,
                            conceptscheme, categoryschememap, organisationschememap,
                            reportingtaxonomymap)
        :param detail: The detail parameter (full, allstubs, referencestubs,
                        allcompletestubs, referencecompletestubs, referencepartial, raw)

        :return: The URL and params formatted
        """

        return self.common_item_scheme_queries("dataconsumerscheme", agency_id, resources,
                                               version, item_id, references, detail)

    def get_organisation_unit_scheme_item(self, agency_id=None, resources=None,
                                          version=None, item_id=None, references=None, detail=None) -> str:

        """
        Returns URL and params to get data provider schemes in Item Scheme Queries

        :param agency_id: The agency id of organisation unit schemes
        :param resources: The resources to query
        :param version: The version of the organisation unit schemes
        :param item_id: The id of the item to be returned
        :param references: The references parameter (none, parents, parentsandsiblings,
                            ancestors, children, descendants, all, datastructure,
                            metadatastructure, categoryscheme, conceptscheme,
                            codelist, hierarchy, hierarchyassociation, agencyscheme,
                            dataproviderscheme, dataconsumerscheme, organisationunitscheme,
                            dataflow, metadataflow, reportingtaxonomy, provisionagreement,
                            structureset, process, categorisation, dataconstraint,
                            metadataconstraint, transformationscheme, rulesetscheme,
                            userdefinedoperatorscheme, customtypescheme,namepersonalisationscheme,
                            namealiasscheme, valuelist, structuremap, representationmap,
                            conceptscheme, categoryschememap, organisationschememap,
                            reportingtaxonomymap)
        :param detail: The detail parameter (full, allstubs, referencestubs,
                        allcompletestubs, referencecompletestubs, referencepartial, raw)

        :return: The URL and params formatted
        """

        return self.common_item_scheme_queries("organisationunitscheme", agency_id, resources,
                                               version, item_id, references, detail)

    def get_transformation_scheme_item(self, agency_id=None, resources=None,
                                       version=None, item_id=None, references=None, detail=None) -> str:

        """
        Returns URL and params to get transformation schemes in Item Scheme Queries

        :param agency_id: The agency id of transformation schemes
        :param resources: The resources to query
        :param version: The version of the transformation schemes
        :param item_id: The id of the item to be returned
        :param references: The references parameter (none, parents, parentsandsiblings,
                            ancestors, children, descendants, all, datastructure,
                            metadatastructure, categoryscheme, conceptscheme,
                            codelist, hierarchy, hierarchyassociation, agencyscheme,
                            dataproviderscheme, dataconsumerscheme, organisationunitscheme,
                            dataflow, metadataflow, reportingtaxonomy, provisionagreement,
                            structureset, process, categorisation, dataconstraint,
                            metadataconstraint, transformationscheme, rulesetscheme,
                            userdefinedoperatorscheme, customtypescheme,namepersonalisationscheme,
                            namealiasscheme, valuelist, structuremap, representationmap,
                            conceptscheme, categoryschememap, organisationschememap,
                            reportingtaxonomymap)
        :param detail: The detail parameter (full, allstubs, referencestubs,
                        allcompletestubs, referencecompletestubs, referencepartial, raw)

        :return: The URL and params formatted
        """

        return self.common_item_scheme_queries("transformationscheme", agency_id, resources,
                                               version, item_id, references, detail)

    def get_ruleset_scheme_item(self, agency_id=None, resources=None,
                                version=None, item_id=None, references=None, detail=None) -> str:

        """
        Returns URL and params to get ruleset schemes in Item Scheme Queries

        :param agency_id: The agency id of ruleset schemes
        :param resources: The resources to query
        :param version: The version of the ruleset schemes
        :param item_id: The id of the item to be returned
        :param references: The references parameter (none, parents, parentsandsiblings,
                            ancestors, children, descendants, all, datastructure,
                            metadatastructure, categoryscheme, conceptscheme,
                            codelist, hierarchy, hierarchyassociation, agencyscheme,
                            dataproviderscheme, dataconsumerscheme, organisationunitscheme,
                            dataflow, metadataflow, reportingtaxonomy, provisionagreement,
                            structureset, process, categorisation, dataconstraint,
                            metadataconstraint, transformationscheme, rulesetscheme,
                            userdefinedoperatorscheme, customtypescheme,namepersonalisationscheme,
                            namealiasscheme, valuelist, structuremap, representationmap,
                            conceptscheme, categoryschememap, organisationschememap,
                            reportingtaxonomymap)
        :param detail: The detail parameter (full, allstubs, referencestubs,
                        allcompletestubs, referencecompletestubs, referencepartial, raw)

        :return: The URL and params formatted
        """

        return self.common_item_scheme_queries("rulesetscheme", agency_id, resources,
                                               version, item_id, references, detail)

    def get_user_defined_operator_scheme_item(self, agency_id=None, resources=None,
                                              version=None, item_id=None, references=None, detail=None) -> str:

        """
        Returns URL and params to get user defined operator schemes in Item Scheme Queries

        :param agency_id: The agency id of user defined operator schemes
        :param resources: The resources to query
        :param version: The version of the user defined operator schemes
        :param item_id: The id of the item to be returned
        :param references: The references parameter (none, parents, parentsandsiblings,
                            ancestors, children, descendants, all, datastructure,
                            metadatastructure, categoryscheme, conceptscheme,
                            codelist, hierarchy, hierarchyassociation, agencyscheme,
                            dataproviderscheme, dataconsumerscheme, organisationunitscheme,
                            dataflow, metadataflow, reportingtaxonomy, provisionagreement,
                            structureset, process, categorisation, dataconstraint,
                            metadataconstraint, transformationscheme, rulesetscheme,
                            userdefinedoperatorscheme, customtypescheme,namepersonalisationscheme,
                            namealiasscheme, valuelist, structuremap, representationmap,
                            conceptscheme, categoryschememap, organisationschememap,
                            reportingtaxonomymap)
        :param detail: The detail parameter (full, allstubs, referencestubs,
                        allcompletestubs, referencecompletestubs, referencepartial, raw)

        :return: The URL and params formatted
        """

        return self.common_item_scheme_queries("userdefinedoperatorscheme", agency_id, resources,
                                               version, item_id, references, detail)

    def get_custom_type_scheme_item(self, agency_id=None, resources=None,
                                    version=None, item_id=None, references=None, detail=None) -> str:

        """
        Returns URL and params to get custom type schemes in Item Scheme Queries

        :param agency_id: The agency id of custom type schemes
        :param resources: The resources to query
        :param version: The version of the custom type schemes
        :param item_id: The id of the item to be returned
        :param references: The references parameter (none, parents, parentsandsiblings,
                            ancestors, children, descendants, all, datastructure,
                            metadatastructure, categoryscheme, conceptscheme,
                            codelist, hierarchy, hierarchyassociation, agencyscheme,
                            dataproviderscheme, dataconsumerscheme, organisationunitscheme,
                            dataflow, metadataflow, reportingtaxonomy, provisionagreement,
                            structureset, process, categorisation, dataconstraint,
                            metadataconstraint, transformationscheme, rulesetscheme,
                            userdefinedoperatorscheme, customtypescheme,namepersonalisationscheme,
                            namealiasscheme, valuelist, structuremap, representationmap,
                            conceptscheme, categoryschememap, organisationschememap,
                            reportingtaxonomymap)
        :param detail: The detail parameter (full, allstubs, referencestubs,
                        allcompletestubs, referencecompletestubs, referencepartial, raw)

        :return: The URL and params formatted
        """

        return self.common_item_scheme_queries("customtypescheme", agency_id, resources,
                                               version, item_id, references, detail)

    def get_name_personalisation_scheme_item(self, agency_id=None, resources=None,
                                             version=None, item_id=None, references=None, detail=None) -> str:

        """
        Returns URL and params to get name personalisation schemes in Item Scheme Queries

        :param agency_id: The agency id of name personalisation schemes
        :param resources: The resources to query
        :param version: The version of the name personalisation schemes
        :param item_id: The id of the item to be returned
        :param references: The references parameter (none, parents, parentsandsiblings,
                            ancestors, children, descendants, all, datastructure,
                            metadatastructure, categoryscheme, conceptscheme,
                            codelist, hierarchy, hierarchyassociation, agencyscheme,
                            dataproviderscheme, dataconsumerscheme, organisationunitscheme,
                            dataflow, metadataflow, reportingtaxonomy, provisionagreement,
                            structureset, process, categorisation, dataconstraint,
                            metadataconstraint, transformationscheme, rulesetscheme,
                            userdefinedoperatorscheme, customtypescheme,namepersonalisationscheme,
                            namealiasscheme, valuelist, structuremap, representationmap,
                            conceptscheme, categoryschememap, organisationschememap,
                            reportingtaxonomymap)
        :param detail: The detail parameter (full, allstubs, referencestubs,
                        allcompletestubs, referencecompletestubs, referencepartial, raw)

        :return: The URL and params formatted
        """

        return self.common_item_scheme_queries("namepersonalisationscheme", agency_id, resources,
                                               version, item_id, references, detail)

    def get_vtl_mapping_scheme_item(self, agency_id=None, resources=None,
                                    version=None, item_id=None, references=None, detail=None) -> str:

        """
        Returns URL and params to get vtl mapping schemes in Item Scheme Queries

        :param agency_id: The agency id of vtl mapping schemes
        :param resources: The resources to query
        :param version: The version of the vtl mapping schemes
        :param item_id: The id of the item to be returned
        :param references: The references parameter (none, parents, parentsandsiblings,
                            ancestors, children, descendants, all, datastructure,
                            metadatastructure, categoryscheme, conceptscheme,
                            codelist, hierarchy, hierarchyassociation, agencyscheme,
                            dataproviderscheme, dataconsumerscheme, organisationunitscheme,
                            dataflow, metadataflow, reportingtaxonomy, provisionagreement,
                            structureset, process, categorisation, dataconstraint,
                            metadataconstraint, transformationscheme, rulesetscheme,
                            userdefinedoperatorscheme, customtypescheme,namepersonalisationscheme,
                            namealiasscheme, valuelist, structuremap, representationmap,
                            conceptscheme, categoryschememap, organisationschememap,
                            reportingtaxonomymap)
        :param detail: The detail parameter (full, allstubs, referencestubs,
                        allcompletestubs, referencecompletestubs, referencepartial, raw)

        :return: The URL and params formatted
        """

        return self.common_item_scheme_queries("vtlmappingscheme", agency_id, resources,
                                               version, item_id, references, detail)

    def get_value_list_item(self, agency_id=None, resources=None,
                            version=None, item_id=None, references=None, detail=None) -> str:

        """
        Returns URL and params to get value lists in Item Scheme Queries

        :param agency_id: The agency id of value lists
        :param resources: The resources to query
        :param version: The version of the value lists
        :param item_id: The id of the item to be returned
        :param references: The references parameter (none, parents, parentsandsiblings,
                            ancestors, children, descendants, all, datastructure,
                            metadatastructure, categoryscheme, conceptscheme,
                            codelist, hierarchy, hierarchyassociation, agencyscheme,
                            dataproviderscheme, dataconsumerscheme, organisationunitscheme,
                            dataflow, metadataflow, reportingtaxonomy, provisionagreement,
                            structureset, process, categorisation, dataconstraint,
                            metadataconstraint, transformationscheme, rulesetscheme,
                            userdefinedoperatorscheme, customtypescheme,namepersonalisationscheme,
                            namealiasscheme, valuelist, structuremap, representationmap,
                            conceptscheme, categoryschememap, organisationschememap,
                            reportingtaxonomymap)
        :param detail: The detail parameter (full, allstubs, referencestubs,
                        allcompletestubs, referencecompletestubs, referencepartial, raw)

        :return: The URL and params formatted
        """

        return self.common_item_scheme_queries("valuelist", agency_id, resources,
                                               version, item_id, references, detail)

    def get_metadata_dsds(self, agency_id=None, resources=None,
                          version=None, detail=None) -> str:

        """
        Returns URL and params to get data structure definitions in metadata queries (by structure)

        :param agency_id: The agency id of the data structure definitions in metadata queries (by structure)
        :param resources: The resources to query
        :param version: The version of the data structure definitions in metadata queries (by structure)
        :param detail: The detail parameter (full, allstubs)

        :return: The URL and params formatted
        """

        return self.common_metadata_structure_queries("datastructure", agency_id, resources,
                                                      version, detail)

    def get_metadata_mdsds(self, agency_id=None, resources=None,
                           version=None, detail=None) -> str:

        """
        Returns URL and params to get metadata structure definitions in metadata queries (by structure)

        :param agency_id: The agency id of the metadata structure definitions in metadata queries (by structure)
        :param resources: The resources to query
        :param version: The version of the metadata structure definitions in metadata queries (by structure)
        :param detail: The detail parameter (full, allstubs)

        :return: The URL and params formatted
        """

        return self.common_metadata_structure_queries("metadatastructure", agency_id, resources,
                                                      version, detail)

    def get_metadata_dataflows(self, agency_id=None, resources=None,
                               version=None, detail=None) -> str:

        """
        Returns URL and params to get dataflows in metadata queries (by structure)

        :param agency_id: The agency id of the dataflows in metadata queries (by structure)
        :param resources: The resources to query
        :param version: The version of the dataflows in metadata queries (by structure)
        :param detail: The detail parameter (full, allstubs)

        :return: The URL and params formatted
        """

        return self.common_metadata_structure_queries("dataflow", agency_id, resources,
                                                      version, detail)

    def get_metadata_metadata_flows(self, agency_id=None, resources=None,
                                    version=None, detail=None) -> str:

        """
        Returns URL and params to get metadata flows in metadata queries (by structure)

        :param agency_id: The agency id of the metadata flows in metadata queries (by structure)
        :param resources: The resources to query
        :param version: The version of the metadata flows in metadata queries (by structure)
        :param detail: The detail parameter (full, allstubs)

        :return: The URL and params formatted
        """

        return self.common_metadata_structure_queries("metadataflow", agency_id, resources,
                                                      version, detail)

    def get_metadata_provision_agreements(self, agency_id=None, resources=None,
                                          version=None, detail=None) -> str:

        """
        Returns URL and params to get provision agreements in metadata queries (by structure)

        :param agency_id: The agency id of the provision agreements in metadata queries (by structure)
        :param resources: The resources to query
        :param version: The version of the provision agreements in metadata queries (by structure)
        :param detail: The detail parameter (full, allstubs)

        :return: The URL and params formatted
        """

        return self.common_metadata_structure_queries("provisionagreement", agency_id, resources,
                                                      version, detail)

    def get_metadata_structure_sets(self, agency_id=None, resources=None,
                                    version=None, detail=None) -> str:

        """
        Returns URL and params to get structure sets in metadata queries (by structure)

        :param agency_id: The agency id of the structure sets in metadata queries (by structure)
        :param resources: The resources to query
        :param version: The version of the structure sets in metadata queries (by structure)
        :param detail: The detail parameter (full, allstubs)

        :return: The URL and params formatted
        """

        return self.common_metadata_structure_queries("structureset", agency_id, resources,
                                                      version, detail)

    def get_metadata_processes(self, agency_id=None, resources=None,
                               version=None, detail=None) -> str:

        """
        Returns URL and params to get processes in metadata queries (by structure)

        :param agency_id: The agency id of the processes in metadata queries (by structure)
        :param resources: The resources to query
        :param version: The version of the processes in metadata queries (by structure)
        :param detail: The detail parameter (full, allstubs)

        :return: The URL and params formatted
        """

        return self.common_metadata_structure_queries("process", agency_id, resources,
                                                      version, detail)

    def get_metadata_categorisations(self, agency_id=None, resources=None,
                                     version=None, detail=None) -> str:

        """
        Returns URL and params to get categorisations in metadata queries (by structure)

        :param agency_id: The agency id of the categorisations in metadata queries (by structure)
        :param resources: The resources to query
        :param version: The version of the categorisations in metadata queries (by structure)
        :param detail: The detail parameter (full, allstubs)

        :return: The URL and params formatted
        """

        return self.common_metadata_structure_queries("categorisation", agency_id, resources,
                                                      version, detail)

    def get_metadata_data_constraints(self, agency_id=None, resources=None,
                                      version=None, detail=None) -> str:

        """
        Returns URL and params to get data constraints in metadata queries (by structure)

        :param agency_id: The agency id of the data constraints in metadata queries (by structure)
        :param resources: The resources to query
        :param version: The version of the data constraints in metadata queries (by structure)
        :param detail: The detail parameter (full, allstubs)

        :return: The URL and params formatted
        """

        return self.common_metadata_structure_queries("dataconstraint", agency_id, resources,
                                                      version, detail)

    def get_metadata_metadata_constraints(self, agency_id=None, resources=None,
                                          version=None, detail=None) -> str:

        """
        Returns URL and params to get metadata constraints in metadata queries (by structure)

        :param agency_id: The agency id of the metadata constraints in metadata queries (by structure)
        :param resources: The resources to query
        :param version: The version of the metadata constraints in metadata queries (by structure)
        :param detail: The detail parameter (full, allstubs)

        :return: The URL and params formatted
        """

        return self.common_metadata_structure_queries("metadataconstraint", agency_id, resources,
                                                      version, detail)

    def get_metadata_concept_schemes(self, agency_id=None, resources=None,
                                     version=None, detail=None) -> str:

        """
        Returns URL and params to get concept schemes in metadata queries (by structure)

        :param agency_id: The agency id of the concept schemes in metadata queries (by structure)
        :param resources: The resources to query
        :param version: The version of the concept schemes in metadata queries (by structure)
        :param detail: The detail parameter (full, allstubs)

        :return: The URL and params formatted
        """

        return self.common_metadata_structure_queries("conceptscheme", agency_id, resources,
                                                      version, detail)

    def get_metadata_code_lists(self, agency_id=None, resources=None,
                                version=None, detail=None) -> str:

        """
        Returns URL and params to get code lists in metadata queries (by structure)

        :param agency_id: The agency id of the code lists in metadata queries (by structure)
        :param resources: The resources to query
        :param version: The version of the code lists in metadata queries (by structure)
        :param detail: The detail parameter (full, allstubs)

        :return: The URL and params formatted
        """

        return self.common_metadata_structure_queries("codelist", agency_id, resources,
                                                      version, detail)

    def get_metadata_category_schemes(self, agency_id=None, resources=None,
                                      version=None, detail=None) -> str:

        """
        Returns URL and params to get category schemes in metadata queries (by structure)

        :param agency_id: The agency id of the category schemes in metadata queries (by structure)
        :param resources: The resources to query
        :param version: The version of the category schemes in metadata queries (by structure)
        :param detail: The detail parameter (full, allstubs)

        :return: The URL and params formatted
        """

        return self.common_metadata_structure_queries("categoryscheme", agency_id, resources,
                                                      version, detail)

    def get_metadata_hierarchies(self, agency_id=None, resources=None,
                                 version=None, detail=None) -> str:

        """
        Returns URL and params to get hierarchies in metadata queries (by structure)

        :param agency_id: The agency id of the hierarchies in metadata queries (by structure)
        :param resources: The resources to query
        :param version: The version of the hierarchies in metadata queries (by structure)
        :param detail: The detail parameter (full, allstubs)

        :return: The URL and params formatted
        """

        return self.common_metadata_structure_queries("hierarchy", agency_id, resources,
                                                      version, detail)

    def get_metadata_hierarchy_associations(self, agency_id=None, resources=None,
                                            version=None, detail=None) -> str:

        """
        Returns URL and params to get hierarchy associations in metadata queries (by structure)

        :param agency_id: The agency id of the hierarchy associations in metadata queries (by structure)
        :param resources: The resources to query
        :param version: The version of the hierarchy associations in metadata queries (by structure)
        :param detail: The detail parameter (full, allstubs)

        :return: The URL and params formatted
        """

        return self.common_metadata_structure_queries("hierarchyassociation", agency_id, resources,
                                                      version, detail)

    def get_metadata_agency_schemes(self, agency_id=None, resources=None,
                                    version=None, detail=None) -> str:

        """
        Returns URL and params to get agency schemes in metadata queries (by structure)

        :param agency_id: The agency id of the agency schemes in metadata queries (by structure)
        :param resources: The resources to query
        :param version: The version of the agency schemes in metadata queries (by structure)
        :param detail: The detail parameter (full, allstubs)

        :return: The URL and params formatted
        """

        return self.common_metadata_structure_queries("agencyscheme", agency_id, resources,
                                                      version, detail)

    def get_metadata_data_provider_schemes(self, agency_id=None, resources=None,
                                           version=None, detail=None) -> str:

        """
        Returns URL and params to get data provider schemes in metadata queries (by structure)

        :param agency_id: The agency id of the data provider schemes in metadata queries (by structure)
        :param resources: The resources to query
        :param version: The version of the data provider schemes in metadata queries (by structure)
        :param detail: The detail parameter (full, allstubs)

        :return: The URL and params formatted
        """

        return self.common_metadata_structure_queries("dataproviderscheme", agency_id, resources,
                                                      version, detail)

    def get_metadata_data_consumer_schemes(self, agency_id=None, resources=None,
                                           version=None, detail=None) -> str:

        """
        Returns URL and params to get data consumer schemes in metadata queries (by structure)

        :param agency_id: The agency id of the data consumer schemes in metadata queries (by structure)
        :param resources: The resources to query
        :param version: The version of the data consumer schemes in metadata queries (by structure)
        :param detail: The detail parameter (full, allstubs)

        :return: The URL and params formatted
        """

        return self.common_metadata_structure_queries("dataconsumerscheme", agency_id, resources,
                                                      version, detail)

    def get_metadata_organisation_unit_schemes(self, agency_id=None, resources=None,
                                               version=None, detail=None) -> str:

        """
        Returns URL and params to get organisation unit schemes in metadata queries (by structure)

        :param agency_id: The agency id of the organisation unit schemes in metadata queries (by structure)
        :param resources: The resources to query
        :param version: The version of the organisation unit schemes in metadata queries (by structure)
        :param detail: The detail parameter (full, allstubs)

        :return: The URL and params formatted
        """

        return self.common_metadata_structure_queries("organisationunitscheme", agency_id, resources,
                                                      version, detail)

    def get_metadata_transformation_schemes(self, agency_id=None, resources=None,
                                            version=None, detail=None) -> str:

        """
        Returns URL and params to get transformation schemes in metadata queries (by structure)

        :param agency_id: The agency id of the transformation schemes in metadata queries (by structure)
        :param resources: The resources to query
        :param version: The version of the transformation schemes in metadata queries (by structure)
        :param detail: The detail parameter (full, allstubs)

        :return: The URL and params formatted
        """

        return self.common_metadata_structure_queries("transformationscheme", agency_id, resources,
                                                      version, detail)

    def get_metadata_ruleset_schemes(self, agency_id=None, resources=None,
                                     version=None, detail=None) -> str:

        """
        Returns URL and params to get ruleset schemes in metadata queries (by structure)

        :param agency_id: The agency id of the ruleset schemes in metadata queries (by structure)
        :param resources: The resources to query
        :param version: The version of the ruleset schemes in metadata queries (by structure)
        :param detail: The detail parameter (full, allstubs)

        :return: The URL and params formatted
        """

        return self.common_metadata_structure_queries("rulesetscheme", agency_id, resources,
                                                      version, detail)

    def get_metadata_user_defined_operator_schemes(self, agency_id=None, resources=None,
                                                   version=None, detail=None) -> str:

        """
        Returns URL and params to get user defined operator schemes in metadata queries (by structure)

        :param agency_id: The agency id of the user defined operator schemes in metadata queries (by structure)
        :param resources: The resources to query
        :param version: The version of the user defined operator schemes in metadata queries (by structure)
        :param detail: The detail parameter (full, allstubs)

        :return: The URL and params formatted
        """

        return self.common_metadata_structure_queries("userdefinedoperatorscheme", agency_id, resources,
                                                      version, detail)

    def get_metadata_custom_type_schemes(self, agency_id=None, resources=None,
                                         version=None, detail=None) -> str:

        """
        Returns URL and params to get custom type schemes in metadata queries (by structure)

        :param agency_id: The agency id of the custom type schemes in metadata queries (by structure)
        :param resources: The resources to query
        :param version: The version of the custom type schemes in metadata queries (by structure)
        :param detail: The detail parameter (full, allstubs)

        :return: The URL and params formatted
        """

        return self.common_metadata_structure_queries("customtypescheme", agency_id, resources,
                                                      version, detail)

    def get_metadata_name_personalisation_schemes(self, agency_id=None, resources=None,
                                                  version=None, detail=None) -> str:

        """
        Returns URL and params to get name personalisation schemes in metadata queries (by structure)

        :param agency_id: The agency id of the name personalisation schemes in metadata queries (by structure)
        :param resources: The resources to query
        :param version: The version of the name personalisation schemes in metadata queries (by structure)
        :param detail: The detail parameter (full, allstubs)

        :return: The URL and params formatted
        """

        return self.common_metadata_structure_queries("namepersonalisationscheme", agency_id, resources,
                                                      version, detail)

    def get_metadata_vtl_mapping_schemes(self, agency_id=None, resources=None,
                                         version=None, detail=None) -> str:

        """
        Returns URL and params to get vtl mapping schemes in metadata queries (by structure)

        :param agency_id: The agency id of the vtl mapping schemes in metadata queries (by structure)
        :param resources: The resources to query
        :param version: The version of the vtl mapping schemes in metadata queries (by structure)
        :param detail: The detail parameter (full, allstubs)

        :return: The URL and params formatted
        """

        return self.common_metadata_structure_queries("vtlmappingscheme", agency_id, resources,
                                                      version, detail)

    def get_metadata_value_lists(self, agency_id=None, resources=None,
                                 version=None, detail=None) -> str:

        """
        Returns URL and params to get value lists in metadata queries (by structure)

        :param agency_id: The agency id of the value lists in metadata queries (by structure)
        :param resources: The resources to query
        :param version: The version of the value lists in metadata queries (by structure)
        :param detail: The detail parameter (full, allstubs)

        :return: The URL and params formatted
        """

        return self.common_metadata_structure_queries("valuelist", agency_id, resources,
                                                      version, detail)

    def get_metadata_structure_maps(self, agency_id=None, resources=None,
                                    version=None, detail=None) -> str:

        """
        Returns URL and params to get structure maps in metadata queries (by structure)

        :param agency_id: The agency id of the structure maps in metadata queries (by structure)
        :param resources: The resources to query
        :param version: The version of the structure maps in metadata queries (by structure)
        :param detail: The detail parameter (full, allstubs)

        :return: The URL and params formatted
        """

        return self.common_metadata_structure_queries("structuremap", agency_id, resources,
                                                      version, detail)

    def get_metadata_representation_maps(self, agency_id=None, resources=None,
                                         version=None, detail=None) -> str:

        """
        Returns URL and params to get representation maps in metadata queries (by structure)

        :param agency_id: The agency id of the representation maps in metadata queries (by structure)
        :param resources: The resources to query
        :param version: The version of the representation maps in metadata queries (by structure)
        :param detail: The detail parameter (full, allstubs)

        :return: The URL and params formatted
        """

        return self.common_metadata_structure_queries("representationmap", agency_id, resources,
                                                      version, detail)

    def get_metadata_concept_scheme_maps(self, agency_id=None, resources=None,
                                         version=None, detail=None) -> str:

        """
        Returns URL and params to get concept scheme maps in metadata queries (by structure)

        :param agency_id: The agency id of the concept scheme maps in metadata queries (by structure)
        :param resources: The resources to query
        :param version: The version of the concept scheme maps in metadata queries (by structure)
        :param detail: The detail parameter (full, allstubs)

        :return: The URL and params formatted
        """

        return self.common_metadata_structure_queries("conceptschememap", agency_id, resources,
                                                      version, detail)

    def get_metadata_category_scheme_maps(self, agency_id=None, resources=None,
                                          version=None, detail=None) -> str:

        """
        Returns URL and params to get category scheme maps in metadata queries (by structure)

        :param agency_id: The agency id of the category scheme maps in metadata queries (by structure)
        :param resources: The resources to query
        :param version: The version of the category scheme maps in metadata queries (by structure)
        :param detail: The detail parameter (full, allstubs)

        :return: The URL and params formatted
        """

        return self.common_metadata_structure_queries("categoryschememap", agency_id, resources,
                                                      version, detail)

    def get_metadata_organisation_scheme_maps(self, agency_id=None, resources=None,
                                              version=None, detail=None) -> str:

        """
        Returns URL and params to get organisation scheme maps in metadata queries (by structure)

        :param agency_id: The agency id of the organisation scheme maps in metadata queries (by structure)
        :param resources: The resources to query
        :param version: The version of the organisation scheme maps in metadata queries (by structure)
        :param detail: The detail parameter (full, allstubs)

        :return: The URL and params formatted
        """

        return self.common_metadata_structure_queries("organisationschememap", agency_id, resources,
                                                      version, detail)

    def get_metadata_reporting_taxonomy_maps(self, agency_id=None, resources=None,
                                             version=None, detail=None) -> str:

        """
        Returns URL and params to get reporting taxonomy maps in metadata queries (by structure)

        :param agency_id: The agency id of the reporting taxonomy maps in metadata queries (by structure)
        :param resources: The resources to query
        :param version: The version of the reporting taxonomy maps in metadata queries (by structure)
        :param detail: The detail parameter (full, allstubs)

        :return: The URL and params formatted
        """

        return self.common_metadata_structure_queries("reportingtaxonomymap", agency_id, resources,
                                                      version, detail)

    def get_metadata_metadataflow_query(self, agency_id=None, resources=None,
                                        version=None, provider_id=None, detail=None) -> str:

        """
        Returns URL and params to get metadata (by metadataflow)

        :param agency_id: The agency id of the metadata (by metadataflow)
        :param resources: The resources to query
        :param version: The version of the metadata (by metadataflow)
        :param provider_id: The provider of metadata
        :param detail: The detail parameter (full, allstubs)

        :return: The URL and params formatted
        """

        agency_id = agency_id if agency_id else "all"
        resources = resources if resources else "all"
        version = version if version else "latest"
        provider_id = provider_id if provider_id else "all"

        base_query = f"/metadata/metadataflow/{agency_id}/{resources}/{version}/{provider_id}"
        params = ""
        if detail:
            initial = "&" if "?" in params else "?"
            params += f"{initial}detail={detail}"

        return base_query + params

    def get_metadata_metadataset_query(self, provider_id=None, resources=None,
                                       version=None, detail=None) -> str:
        """
        Returns URL and params to get metadata (by metadatasets)

        :param provider_id: The provider of metadata
        :param resources: The resources to query
        :param version: The version of the metadata (by metadatasets)
        :param provider_id: The provider of metadata
        :param detail: The detail parameter (full, allstubs)

        :return: The URL and params formatted
        """

        provider_id = provider_id if provider_id else "all"
        resources = resources if resources else "all"
        version = version if version else "latest"

        base_query = f"/metadata/metadataset/{provider_id}/{resources}/{version}"
        params = ""
        if detail:
            initial = "&" if "?" in params else "?"
            params += f"{initial}detail={detail}"

        return base_query + params

    def get_schemas_datastructure(self, agency_id=None, resources=None,
                                  version=None, dimension_at_observation=None,
                                  explicit_measure=None):
        pass

    def get_schemas_meta_datastructure(self, agency_id=None, resources=None,
                                       version=None, dimension_at_observation=None,
                                       explicit_measure=None):
        pass

    def get_schemas_dataflow(self, agency_id=None, resources=None,
                             version=None, dimension_at_observation=None,
                             explicit_measure=None):
        pass

    def get_schemas_meta_dataflow(self, agency_id=None, resources=None,
                                  version=None, dimension_at_observation=None,
                                  explicit_measure=None):
        pass

    def get_schemas_provision_agreement(self, agency_id=None, resources=None,
                                        version=None, dimension_at_observation=None,
                                        explicit_measure=None):
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

    def common_schemas_queries(self, context, agency_id=None, resources=None,
                               version=None, dimension_at_observation=None,
                               explicit_measure=None):
        agency_id = agency_id if agency_id else "all"
        resources = resources if resources else "all"
        version = version if version else "latest"

        base_query = f"/schema/{context}/{agency_id}/{resources}/{version}"
        params = ""
        if dimension_at_observation:
            initial = "&" if "?" in params else "?"
            params += f"{initial}dimension_at_observation={dimension_at_observation}"
        if explicit_measure:
            initial = "&" if "?" in params else "?"
            params += f"{initial}explicit_measure={explicit_measure}"

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

    def get_data_datastructures(self, agency_id=None, resources=None,
                                version=None, key=None, c=None, updated_after=None,
                                first_n_observations=None, last_n_observations=None,
                                dimension_at_observation=None, attributes=None,
                                measures=None, include_history=None):
        pass

    def get_data_dataflows(self, agency_id=None, resources=None,
                           version=None, key=None, c=None, updated_after=None,
                           first_n_observations=None, last_n_observations=None,
                           dimension_at_observation=None, attributes=None,
                           measures=None, include_history=None):
        pass

    def get_data_provision_agreements(self, agency_id=None, resources=None,
                                      version=None, key=None, c=None, updated_after=None,
                                      first_n_observations=None, last_n_observations=None,
                                      dimension_at_observation=None, attributes=None,
                                      measures=None, include_history=None):
        pass

    def get_data_all_contexts(self, agency_id=None, resources=None,
                              version=None, key=None, c=None, updated_after=None,
                              first_n_observations=None, last_n_observations=None,
                              dimension_at_observation=None, attributes=None,
                              measures=None, include_history=None):
        pass

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

    def get_constraint_datastructures(self, agency_id=None, resources=None,
                                      version=None, key=None, component_id=None, c=None,
                                      mode=None, references=None, updated_after=None):
        pass

    def get_constraint_dataflows(self, agency_id=None, resources=None,
                                 version=None, key=None, component_id=None, c=None,
                                 mode=None, references=None, updated_after=None):
        pass

    def get_constraint_provision_agreements(self, agency_id=None, resources=None,
                                            version=None, key=None, component_id=None, c=None,
                                            mode=None, references=None, updated_after=None):
        pass

    def get_constraint_all_contexts(self, agency_id=None, resources=None,
                                    version=None, key=None, component_id=None, c=None,
                                    mode=None, references=None, updated_after=None):
        pass

    def get_schema_datastructures(self, agency_id=None, resources=None,
                                  version=None, dimension_at_observation=None,
                                  explicit_measure=None):
        pass

    def get_schema_meta_datastructures(self, agency_id=None, resources=None,
                                       version=None, dimension_at_observation=None,
                                       explicit_measure=None):
        pass

    def get_schema_dataflows(self, agency_id=None, resources=None,
                             version=None, dimension_at_observation=None,
                             explicit_measure=None):
        pass

    def get_schema_meta_dataflows(self, agency_id=None, resources=None,
                                  version=None, dimension_at_observation=None,
                                  explicit_measure=None):
        pass

    def get_schema_provision_agreements(self, agency_id=None, resources=None,
                                        version=None, dimension_at_observation=None,
                                        explicit_measure=None):
        pass

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

    def get_schemas_datastructure(self, agency_id=None, resources=None,
                                  version=None, dimension_at_observation=None,
                                  explicit_measure=None):
        """
                Returns URL and params to get schema (datastructure)

                :param agency_id: The id of the schema (datastructure)
                :param resources: The resources to query
                :param version: The version of the schema (datastructure)
                :param dimension_at_observation: The dimension at observation
                :param explicit_measure: Indicates whether observations are strongly typed
                                          (true, false)
                """

        return self.common_schemas_queries("datastructure", agency_id, resources, version,
                                           dimension_at_observation, explicit_measure)

    def get_schemas_meta_datastructure(self, agency_id=None, resources=None,
                                       version=None, dimension_at_observation=None,
                                       explicit_measure=None):
        """
                Returns URL and params to get schema (metadatastructure)

                :param agency_id: The id of the schema (metadatastructure)
                :param resources: The resources to query
                :param version: The version of the schema (metadatastructure)
                :param dimension_at_observation: The dimension at observation
                :param explicit_measure: Indicates whether observations are strongly typed
                                          (true, false)
                """

        return self.common_schemas_queries("metadatastructure", agency_id, resources, version,
                                           dimension_at_observation, explicit_measure)

    def get_schemas_dataflow(self, agency_id=None, resources=None,
                             version=None, dimension_at_observation=None,
                             explicit_measure=None):
        """
                Returns URL and params to get schema (dataflow)

                :param agency_id: The id of the schema (dataflow)
                :param resources: The resources to query
                :param version: The version of the schema (dataflow)
                :param dimension_at_observation: The dimension at observation
                :param explicit_measure: Indicates whether observations are strongly typed
                                          (true, false)
                """

        return self.common_schemas_queries("dataflow", agency_id, resources, version,
                                           dimension_at_observation, explicit_measure)

    def get_schemas_meta_dataflow(self, agency_id=None, resources=None,
                                  version=None, dimension_at_observation=None,
                                  explicit_measure=None):
        """
                Returns URL and params to get schema (metadataflow)

                :param agency_id: The id of the schema (metadataflow)
                :param resources: The resources to query
                :param version: The version of the schema (metadataflow)
                :param dimension_at_observation: The dimension at observation
                :param explicit_measure: Indicates whether observations are strongly typed
                                          (true, false)
                """

        return self.common_schemas_queries("metadataflow", agency_id, resources, version,
                                           dimension_at_observation, explicit_measure)

    def get_schemas_provision_agreement(self, agency_id=None, resources=None,
                                        version=None, dimension_at_observation=None,
                                        explicit_measure=None):
        """
                Returns URL and params to get schema (provision agreement)

                :param agency_id: The id of the schema (provision agreement)
                :param resources: The resources to query
                :param version: The version of the schema (provision agreement)
                :param dimension_at_observation: The dimension at observation
                :param explicit_measure: Indicates whether observations are strongly typed
                                          (true, false)
                """

        return self.common_schemas_queries("provisionagreement", agency_id, resources, version,
                                           dimension_at_observation, explicit_measure)

    def get_concept_scheme_item(self, agency_id=None, resources=None, version=None,
                                item_id=None, references=None, detail=None) -> str:
        pass

    def get_codelist_item(self, agency_id=None, resources=None,
                          version=None, item_id=None, references=None, detail=None) -> str:
        pass

    def get_category_scheme_item(self, agency_id=None, resources=None,
                                 version=None, item_id=None, references=None, detail=None) -> str:
        pass

    def get_agency_scheme_item(self, agency_id=None, resources=None,
                               version=None, item_id=None, references=None, detail=None) -> str:
        pass

    def get_data_provider_scheme_item(self, agency_id=None, resources=None,
                                      version=None, item_id=None, references=None, detail=None) -> str:
        pass

    def get_data_consumer_scheme_item(self, agency_id=None, resources=None,
                                      version=None, item_id=None, references=None, detail=None) -> str:
        pass

    def get_organisation_unit_scheme_item(self, agency_id=None, resources=None,
                                          version=None, item_id=None, references=None, detail=None) -> str:
        pass

    def get_transformation_scheme_item(self, agency_id=None, resources=None,
                                       version=None, item_id=None, references=None, detail=None) -> str:
        pass

    def get_ruleset_scheme_item(self, agency_id=None, resources=None,
                                version=None, item_id=None, references=None, detail=None) -> str:
        pass

    def get_user_defined_operator_scheme_item(self, agency_id=None, resources=None,
                                              version=None, item_id=None, references=None, detail=None) -> str:
        pass

    def get_custom_type_scheme_item(self, agency_id=None, resources=None,
                                    version=None, item_id=None, references=None, detail=None) -> str:
        pass

    def get_name_personalisation_scheme_item(self, agency_id=None, resources=None,
                                             version=None, item_id=None, references=None, detail=None) -> str:
        pass

    def get_vtl_mapping_scheme_item(self, agency_id=None, resources=None,
                                    version=None, item_id=None, references=None, detail=None) -> str:
        pass

    def get_value_list_item(self, agency_id=None, resources=None,
                            version=None, item_id=None, references=None, detail=None) -> str:
        pass

    def get_metadata_dsds(self, agency_id=None, resources=None,
                          version=None, detail=None) -> str:
        pass

    def get_metadata_mdsds(self, agency_id=None, resources=None,
                           version=None, detail=None) -> str:
        pass

    def get_metadata_dataflows(self, agency_id=None, resources=None,
                               version=None, detail=None) -> str:
        pass

    def get_metadata_metadata_flows(self, agency_id=None, resources=None,
                                    version=None, detail=None) -> str:
        pass

    def get_metadata_provision_agreements(self, agency_id=None, resources=None,
                                          version=None, detail=None) -> str:
        pass

    def get_metadata_structure_sets(self, agency_id=None, resources=None,
                                    version=None, detail=None) -> str:
        pass

    def get_metadata_processes(self, agency_id=None, resources=None,
                               version=None, detail=None) -> str:
        pass

    def get_metadata_categorisations(self, agency_id=None, resources=None,
                                     version=None, detail=None) -> str:
        pass

    def get_metadata_data_constraints(self, agency_id=None, resources=None,
                                      version=None, detail=None) -> str:
        pass

    def get_metadata_metadata_constraints(self, agency_id=None, resources=None,
                                          version=None, detail=None) -> str:
        pass

    def get_metadata_concept_schemes(self, agency_id=None, resources=None,
                                     version=None, detail=None) -> str:
        pass

    def get_metadata_code_lists(self, agency_id=None, resources=None,
                                version=None, detail=None) -> str:
        pass

    def get_metadata_category_schemes(self, agency_id=None, resources=None,
                                      version=None, detail=None) -> str:
        pass

    def get_metadata_hierarchies(self, agency_id=None, resources=None,
                                 version=None, detail=None) -> str:
        pass

    def get_metadata_hierarchy_associations(self, agency_id=None, resources=None,
                                            version=None, detail=None) -> str:
        pass

    def get_metadata_agency_schemes(self, agency_id=None, resources=None,
                                    version=None, detail=None) -> str:
        pass

    def get_metadata_data_provider_schemes(self, agency_id=None, resources=None,
                                           version=None, detail=None) -> str:
        pass

    def get_metadata_data_consumer_schemes(self, agency_id=None, resources=None,
                                           version=None, detail=None) -> str:
        pass

    def get_metadata_organisation_unit_schemes(self, agency_id=None, resources=None,
                                               version=None, detail=None) -> str:
        pass

    def get_metadata_transformation_schemes(self, agency_id=None, resources=None,
                                            version=None, detail=None) -> str:
        pass

    def get_metadata_ruleset_schemes(self, agency_id=None, resources=None,
                                     version=None, detail=None) -> str:
        pass

    def get_metadata_user_defined_operator_schemes(self, agency_id=None, resources=None,
                                                   version=None, detail=None) -> str:
        pass

    def get_metadata_custom_type_schemes(self, agency_id=None, resources=None,
                                         version=None, detail=None) -> str:
        pass

    def get_metadata_name_personalisation_schemes(self, agency_id=None, resources=None,
                                                  version=None, detail=None) -> str:
        pass

    def get_metadata_vtl_mapping_schemes(self, agency_id=None, resources=None,
                                         version=None, detail=None) -> str:
        pass

    def get_metadata_value_lists(self, agency_id=None, resources=None,
                                 version=None, detail=None) -> str:
        pass

    def get_metadata_structure_maps(self, agency_id=None, resources=None,
                                    version=None, detail=None) -> str:
        pass

    def get_metadata_representation_maps(self, agency_id=None, resources=None,
                                         version=None, detail=None) -> str:
        pass

    def get_metadata_concept_scheme_maps(self, agency_id=None, resources=None,
                                         version=None, detail=None) -> str:
        pass

    def get_metadata_category_scheme_maps(self, agency_id=None, resources=None,
                                          version=None, detail=None) -> str:
        pass

    def get_metadata_organisation_scheme_maps(self, agency_id=None, resources=None,
                                              version=None, detail=None) -> str:
        pass

    def get_metadata_reporting_taxonomy_maps(self, agency_id=None, resources=None,
                                             version=None, detail=None) -> str:
        pass

    def get_metadata_metadataflow_query(self, agency_id=None, resources=None,
                                        version=None, provider_id=None, detail=None) -> str:
        pass

    def get_metadata_metadataset_query(self, agency_id=None, resources=None,
                                       version=None, provider_id=None, detail=None) -> str:
        pass


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

    def get_data_datastructures(self, agency_id=None, resources=None,
                                version=None, key=None, c=None, updated_after=None,
                                first_n_observations=None, last_n_observations=None,
                                dimension_at_observation=None, attributes=None,
                                measures=None, include_history=None):
        """Returns the data (datastructure) query for the WS Implementation"""

        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if include_history:
            self._ws_implementation.validate_data_history(include_history)

        return self._ws_implementation.get_data_datastructures(agency_id, resources, version,
                                                               key, c, updated_after,
                                                               first_n_observations, last_n_observations,
                                                               dimension_at_observation, attributes,
                                                               measures, include_history)

    def get_data_dataflows(self, agency_id=None, resources=None,
                           version=None, key=None, c=None, updated_after=None,
                           first_n_observations=None, last_n_observations=None,
                           dimension_at_observation=None, attributes=None,
                           measures=None, include_history=None):
        """Returns the data (dataflow) query for the WS Implementation"""

        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if include_history:
            self._ws_implementation.validate_data_history(include_history)

        return self._ws_implementation.get_data_dataflows(agency_id, resources, version,
                                                          key, c, updated_after,
                                                          first_n_observations, last_n_observations,
                                                          dimension_at_observation, attributes,
                                                          measures, include_history)

    def get_data_provision_agreements(self, agency_id=None, resources=None,
                                      version=None, key=None, c=None, updated_after=None,
                                      first_n_observations=None, last_n_observations=None,
                                      dimension_at_observation=None, attributes=None,
                                      measures=None, include_history=None):
        """Returns the data (provision agreement) query for the WS Implementation"""

        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if include_history:
            self._ws_implementation.validate_data_history(include_history)

        return (self._ws_implementation.
                get_data_provision_agreements(agency_id, resources, version,
                                              key, c, updated_after,
                                              first_n_observations, last_n_observations,
                                              dimension_at_observation, attributes,
                                              measures, include_history))

    def get_data_all_contexts(self, agency_id=None, resources=None,
                              version=None, key=None, c=None, updated_after=None,
                              first_n_observations=None, last_n_observations=None,
                              dimension_at_observation=None, attributes=None,
                              measures=None, include_history=None):
        """Returns the data (all possible contexts) query for the WS Implementation"""

        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if include_history:
            self._ws_implementation.validate_data_history(include_history)

        return (self._ws_implementation.get_data_all_contexts(agency_id, resources, version,
                                                              key, c, updated_after,
                                                              first_n_observations, last_n_observations,
                                                              dimension_at_observation, attributes,
                                                              measures, include_history))

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

    def get_constraint_datastructures(self, agency_id=None, resources=None,
                                      version=None, key=None, component_id=None, c=None,
                                      mode=None, references=None, updated_after=None):
        """Returns the constraints (datastructure) query for the WS Implementation"""

        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if mode:
            self._ws_implementation.validate_constraints_mode(mode)
        if references:
            self._ws_implementation.validate_constraints_references(references)

        return (self._ws_implementation.get_constraint_datastructures(agency_id, resources, version,
                                                                      key, component_id, c, mode,
                                                                      references, updated_after))

    def get_constraint_dataflows(self, agency_id=None, resources=None,
                                 version=None, key=None, component_id=None, c=None,
                                 mode=None, references=None, updated_after=None):
        """Returns the constraints (dataflows) query for the WS Implementation"""

        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if mode:
            self._ws_implementation.validate_constraints_mode(mode)
        if references:
            self._ws_implementation.validate_constraints_references(references)

        return (self._ws_implementation.get_constraint_dataflows(agency_id, resources, version,
                                                                 key, component_id, c, mode,
                                                                 references, updated_after))

    def get_constraint_provision_agreements(self, agency_id=None, resources=None,
                                            version=None, key=None, component_id=None, c=None,
                                            mode=None, references=None, updated_after=None):
        """Returns the constraints (provision agreements) query for the WS Implementation"""

        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if mode:
            self._ws_implementation.validate_constraints_mode(mode)
        if references:
            self._ws_implementation.validate_constraints_references(references)

        return (self._ws_implementation.
                get_constraint_provision_agreements(agency_id, resources, version,
                                                    key, component_id, c, mode,
                                                    references, updated_after))

    def get_constraint_all_contexts(self, agency_id=None, resources=None,
                                    version=None, key=None, component_id=None, c=None,
                                    mode=None, references=None, updated_after=None):
        """Returns the constraints (all possible contexts) query for the WS Implementation"""

        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if mode:
            self._ws_implementation.validate_constraints_mode(mode)
        if references:
            self._ws_implementation.validate_constraints_references(references)

        return (self._ws_implementation.
                get_constraint_all_contexts(agency_id, resources, version,
                                            key, component_id, c, mode,
                                            references, updated_after))

    def get_schema_datastructures(self, agency_id=None, resources=None,
                                  version=None, dimension_at_observation=None,
                                  explicit_measure=None):
        """Returns the schema (datastructure) query for the WS Implementation"""

        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if explicit_measure:
            self._ws_implementation.validate_explicit_measure(explicit_measure)

        return (self._ws_implementation.
                get_schema_datastructures(agency_id, resources, version,
                                          dimension_at_observation, explicit_measure))

    def get_schema_meta_datastructures(self, agency_id=None, resources=None,
                                       version=None, dimension_at_observation=None,
                                       explicit_measure=None):
        """Returns the schema (metadatastructure) query for the WS Implementation"""

        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if explicit_measure:
            self._ws_implementation.validate_explicit_measure(explicit_measure)

        return (self._ws_implementation.
                get_schema_meta_datastructures(agency_id, resources, version,
                                               dimension_at_observation, explicit_measure))

    def get_schema_dataflows(self, agency_id=None, resources=None,
                             version=None, dimension_at_observation=None,
                             explicit_measure=None):
        """Returns the schema (dataflow) query for the WS Implementation"""

        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if explicit_measure:
            self._ws_implementation.validate_explicit_measure(explicit_measure)

        return (self._ws_implementation.
                get_schema_dataflows(agency_id, resources, version,
                                     dimension_at_observation, explicit_measure))

    def get_schema_meta_dataflows(self, agency_id=None, resources=None,
                                  version=None, dimension_at_observation=None,
                                  explicit_measure=None):
        """Returns the schema (metadataflow) query for the WS Implementation"""

        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if explicit_measure:
            self._ws_implementation.validate_explicit_measure(explicit_measure)

        return (self._ws_implementation.
                get_schema_meta_dataflows(agency_id, resources, version,
                                          dimension_at_observation, explicit_measure))

    def get_schema_provision_agreements(self, agency_id=None, resources=None,
                                        version=None, dimension_at_observation=None,
                                        explicit_measure=None):
        """Returns the schema (provision agreement) query for the WS Implementation"""

        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if explicit_measure:
            self._ws_implementation.validate_explicit_measure(explicit_measure)

        return (self._ws_implementation.
                get_schema_provision_agreements(agency_id, resources, version,
                                                dimension_at_observation, explicit_measure))

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

    def get_schemas_datastructure(self, agency_id=None, resources=None,
                                  version=None, dimension_at_observation=None,
                                  explicit_measure=None):
        """Returns the schema (datastructure) query for the WS Implementation"""

        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if explicit_measure:
            self._ws_implementation.validate_explicit_measure(explicit_measure)

        return (self._ws_implementation.
                get_schemas_datastructure(agency_id, resources, version,
                                          dimension_at_observation, explicit_measure))

    def get_schemas_meta_datastructure(self, agency_id=None, resources=None,
                                       version=None, dimension_at_observation=None,
                                       explicit_measure=None):
        """Returns the schema (metadatastructure) query for the WS Implementation"""

        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if explicit_measure:
            self._ws_implementation.validate_explicit_measure(explicit_measure)

        return (self._ws_implementation.
                get_schemas_meta_datastructure(agency_id, resources, version,
                                               dimension_at_observation, explicit_measure))

    def get_schemas_dataflow(self, agency_id=None, resources=None,
                             version=None, dimension_at_observation=None,
                             explicit_measure=None):
        """Returns the schema (dataflows) query for the WS Implementation"""

        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if explicit_measure:
            self._ws_implementation.validate_explicit_measure(explicit_measure)

        return (self._ws_implementation.
                get_schemas_dataflow(agency_id, resources, version,
                                     dimension_at_observation, explicit_measure))

    def get_schemas_meta_dataflow(self, agency_id=None, resources=None,
                                  version=None, dimension_at_observation=None,
                                  explicit_measure=None):
        """Returns the schema (metadataflows) query for the WS Implementation"""

        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if explicit_measure:
            self._ws_implementation.validate_explicit_measure(explicit_measure)

        return (self._ws_implementation.
                get_schemas_meta_dataflow(agency_id, resources, version,
                                          dimension_at_observation, explicit_measure))

    def get_schemas_provision_agreement(self, agency_id=None, resources=None,
                                        version=None, dimension_at_observation=None,
                                        explicit_measure=None):
        """Returns the schema (metadataflows) query for the WS Implementation"""

        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if explicit_measure:
            self._ws_implementation.validate_explicit_measure(explicit_measure)

        return (self._ws_implementation.
                get_schemas_provision_agreement(agency_id, resources, version,
                                                dimension_at_observation, explicit_measure))

    def get_concept_scheme_item(self, agency_id=None, resources=None,
                                version=None, item_id=None, references=None, detail=None) -> str:
        """Returns the get concept scheme in Item Scheme query for the WS Implementation"""
        return self.query_builder_common_with_item(self._ws_implementation.get_concept_scheme_item,
                                                   agency_id, resources, version, item_id, references, detail)

    def get_codelist_item(self, agency_id=None, resources=None,
                          version=None, item_id=None, references=None, detail=None) -> str:
        """Returns the get codelists in Item Scheme query for the WS Implementation"""
        return self.query_builder_common_with_item(self._ws_implementation.get_codelist_item,
                                                   agency_id, resources, version, item_id, references, detail)

    def get_category_scheme_item(self, agency_id=None, resources=None,
                                 version=None, item_id=None, references=None, detail=None) -> str:
        """Returns the get category schemes in Item Scheme query for the WS Implementation"""
        return self.query_builder_common_with_item(self._ws_implementation.get_category_scheme_item,
                                                   agency_id, resources, version, item_id, references, detail)

    def get_agency_scheme_item(self, agency_id=None, resources=None,
                               version=None, item_id=None, references=None, detail=None) -> str:
        """Returns the get agency schemes in Item Scheme query for the WS Implementation"""
        return self.query_builder_common_with_item(self._ws_implementation.get_agency_scheme_item,
                                                   agency_id, resources, version, item_id, references, detail)

    def get_data_provider_scheme_item(self, agency_id=None, resources=None,
                                      version=None, item_id=None, references=None, detail=None) -> str:
        """Returns the get data provider schemes in Item Scheme query for the WS Implementation"""
        return self.query_builder_common_with_item(self._ws_implementation.get_data_provider_scheme_item,
                                                   agency_id, resources, version, item_id, references, detail)

    def get_data_consumer_scheme_item(self, agency_id=None, resources=None,
                                      version=None, item_id=None, references=None, detail=None) -> str:
        """Returns the get data consumer schemes in Item Scheme query for the WS Implementation"""
        return self.query_builder_common_with_item(self._ws_implementation.get_data_consumer_scheme_item,
                                                   agency_id, resources, version, item_id, references, detail)

    def get_organisation_unit_scheme_item(self, agency_id=None, resources=None,
                                          version=None, item_id=None, references=None, detail=None) -> str:
        """Returns the get organisation unit schemes in Item Scheme query for the WS Implementation"""
        return self.query_builder_common_with_item(self._ws_implementation.get_organisation_unit_scheme_item,
                                                   agency_id, resources, version, item_id, references, detail)

    def get_transformation_scheme_item(self, agency_id=None, resources=None,
                                       version=None, item_id=None, references=None, detail=None) -> str:
        """Returns the get transformation schemes in Item Scheme query for the WS Implementation"""
        return self.query_builder_common_with_item(self._ws_implementation.get_transformation_scheme_item,
                                                   agency_id, resources, version, item_id, references, detail)

    def get_ruleset_scheme_item(self, agency_id=None, resources=None,
                                version=None, item_id=None, references=None, detail=None) -> str:
        """Returns the get ruleset schemes in Item Scheme query for the WS Implementation"""
        return self.query_builder_common_with_item(self._ws_implementation.get_ruleset_scheme_item,
                                                   agency_id, resources, version, item_id, references, detail)

    def get_user_defined_operator_scheme_item(self, agency_id=None, resources=None,
                                              version=None, item_id=None, references=None, detail=None) -> str:
        """Returns the get user defined operator schemes in Item Scheme query for the WS Implementation"""
        return self.query_builder_common_with_item(self._ws_implementation.get_user_defined_operator_scheme_item,
                                                   agency_id, resources, version, item_id, references, detail)

    def get_custom_type_scheme_item(self, agency_id=None, resources=None,
                                    version=None, item_id=None, references=None, detail=None) -> str:
        """Returns the get custom type schemes in Item Scheme query for the WS Implementation"""
        return self.query_builder_common_with_item(self._ws_implementation.get_custom_type_scheme_item,
                                                   agency_id, resources, version, item_id, references, detail)

    def get_name_personalisation_scheme_item(self, agency_id=None, resources=None,
                                             version=None, item_id=None, references=None, detail=None) -> str:
        """Returns the get name personalisation schemes in Item Scheme query for the WS Implementation"""
        return self.query_builder_common_with_item(self._ws_implementation.get_name_personalisation_scheme_item,
                                                   agency_id, resources, version, item_id, references, detail)

    def get_vtl_mapping_scheme_item(self, agency_id=None, resources=None,
                                    version=None, item_id=None, references=None, detail=None) -> str:
        """Returns the get vtl mapping schemes in Item Scheme query for the WS Implementation"""
        return self.query_builder_common_with_item(self._ws_implementation.get_vtl_mapping_scheme_item,
                                                   agency_id, resources, version, item_id, references, detail)

    def get_value_list_item(self, agency_id=None, resources=None,
                            version=None, item_id=None, references=None, detail=None) -> str:
        """Returns the get value list schemes in Item Scheme query for the WS Implementation"""
        return self.query_builder_common_with_item(self._ws_implementation.get_value_list_item,
                                                   agency_id, resources, version, item_id, references, detail)

    def get_metadata_dsds(self, agency_id=None, resources=None,
                          version=None, detail=None) -> str:
        """Returns the data structure definitions query in metadata
        queries (by structure) for the WS Implementation"""
        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if detail:
            self._ws_implementation.validate_structural_detail(detail)

        return self._ws_implementation.get_metadata_dsds(agency_id, resources, version, detail)

    def get_metadata_mdsds(self, agency_id=None, resources=None,
                           version=None, detail=None) -> str:
        """Returns the metadata structure definitions query in metadata
        queries (by structure) for the WS Implementation"""
        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if detail:
            self._ws_implementation.validate_structural_detail(detail)

        return self._ws_implementation.get_metadata_mdsds(agency_id, resources, version, detail)

    def get_metadata_dataflows(self, agency_id=None, resources=None,
                               version=None, detail=None) -> str:
        """Returns the dataflows query in metadata
        queries (by structure) for the WS Implementation"""
        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if detail:
            self._ws_implementation.validate_structural_detail(detail)

        return self._ws_implementation.get_metadata_dataflows(agency_id, resources, version, detail)

    def get_metadata_metadata_flows(self, agency_id=None, resources=None,
                                    version=None, detail=None) -> str:
        """Returns the metadata flows query in metadata
        queries (by structure) for the WS Implementation"""
        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if detail:
            self._ws_implementation.validate_structural_detail(detail)

        return self._ws_implementation.get_metadata_metadata_flows(agency_id, resources, version, detail)

    def get_metadata_provision_agreements(self, agency_id=None, resources=None,
                                          version=None, detail=None) -> str:
        """Returns the provision agreements query in metadata
        queries (by structure) for the WS Implementation"""
        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if detail:
            self._ws_implementation.validate_structural_detail(detail)

        return self._ws_implementation.get_metadata_provision_agreements(agency_id, resources, version, detail)

    def get_metadata_structure_sets(self, agency_id=None, resources=None,
                                    version=None, detail=None) -> str:
        """Returns the structure sets query in metadata
        queries (by structure) for the WS Implementation"""
        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if detail:
            self._ws_implementation.validate_structural_detail(detail)

        return self._ws_implementation.get_metadata_structure_sets(agency_id, resources, version, detail)

    def get_metadata_processes(self, agency_id=None, resources=None,
                               version=None, detail=None) -> str:
        """Returns the processes query in metadata
        queries (by structure) for the WS Implementation"""
        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if detail:
            self._ws_implementation.validate_structural_detail(detail)

        return self._ws_implementation.get_metadata_processes(agency_id, resources, version, detail)

    def get_metadata_categorisations(self, agency_id=None, resources=None,
                                     version=None, detail=None) -> str:
        """Returns the categorisations query in metadata
        queries (by structure) for the WS Implementation"""
        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if detail:
            self._ws_implementation.validate_structural_detail(detail)

        return self._ws_implementation.get_metadata_categorisations(agency_id, resources, version, detail)

    def get_metadata_data_constraints(self, agency_id=None, resources=None,
                                      version=None, detail=None) -> str:
        """Returns the data constraints query in metadata
        queries (by structure) for the WS Implementation"""
        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if detail:
            self._ws_implementation.validate_structural_detail(detail)

        return self._ws_implementation.get_metadata_data_constraints(agency_id, resources, version, detail)

    def get_metadata_metadata_constraints(self, agency_id=None, resources=None,
                                          version=None, detail=None) -> str:
        """Returns the metadata constraints query in metadata
        queries (by structure) for the WS Implementation"""
        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if detail:
            self._ws_implementation.validate_structural_detail(detail)

        return self._ws_implementation.get_metadata_metadata_constraints(agency_id, resources, version, detail)

    def get_metadata_concept_schemes(self, agency_id=None, resources=None,
                                     version=None, detail=None) -> str:
        """Returns the concept schemes query in metadata
        queries (by structure) for the WS Implementation"""
        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if detail:
            self._ws_implementation.validate_structural_detail(detail)

        return self._ws_implementation.get_metadata_concept_schemes(agency_id, resources, version, detail)

    def get_metadata_code_lists(self, agency_id=None, resources=None,
                                version=None, detail=None) -> str:
        """Returns the code lists query in metadata
        queries (by structure) for the WS Implementation"""
        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if detail:
            self._ws_implementation.validate_structural_detail(detail)

        return self._ws_implementation.get_metadata_code_lists(agency_id, resources, version, detail)

    def get_metadata_category_schemes(self, agency_id=None, resources=None,
                                      version=None, detail=None) -> str:
        """Returns the category schemes query in metadata
        queries (by structure) for the WS Implementation"""
        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if detail:
            self._ws_implementation.validate_structural_detail(detail)

        return self._ws_implementation.get_metadata_category_schemes(agency_id, resources, version, detail)

    def get_metadata_hierarchies(self, agency_id=None, resources=None,
                                 version=None, detail=None) -> str:
        """Returns the hierarchies query in metadata
        queries (by structure) for the WS Implementation"""
        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if detail:
            self._ws_implementation.validate_structural_detail(detail)

        return self._ws_implementation.get_metadata_hierarchies(agency_id, resources, version, detail)

    def get_metadata_hierarchy_associations(self, agency_id=None, resources=None,
                                            version=None, detail=None) -> str:
        """Returns the hierarchy associations query in metadata
        queries (by structure) for the WS Implementation"""
        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if detail:
            self._ws_implementation.validate_structural_detail(detail)

        return self._ws_implementation.get_metadata_hierarchy_associations(agency_id, resources, version, detail)

    def get_metadata_agency_schemes(self, agency_id=None, resources=None,
                                    version=None, detail=None) -> str:
        """Returns the agency schemes query in metadata
        queries (by structure) for the WS Implementation"""
        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if detail:
            self._ws_implementation.validate_structural_detail(detail)

        return self._ws_implementation.get_metadata_agency_schemes(agency_id, resources, version, detail)

    def get_metadata_data_provider_schemes(self, agency_id=None, resources=None,
                                           version=None, detail=None) -> str:
        """Returns the data provider schemes query in metadata
        queries (by structure) for the WS Implementation"""
        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if detail:
            self._ws_implementation.validate_structural_detail(detail)

        return self._ws_implementation.get_metadata_data_provider_schemes(agency_id, resources, version, detail)

    def get_metadata_data_consumer_schemes(self, agency_id=None, resources=None,
                                           version=None, detail=None) -> str:
        """Returns the data consumer schemes query in metadata
        queries (by structure) for the WS Implementation"""
        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if detail:
            self._ws_implementation.validate_structural_detail(detail)

        return self._ws_implementation.get_metadata_data_consumer_schemes(agency_id, resources, version, detail)

    def get_metadata_organisation_unit_schemes(self, agency_id=None, resources=None,
                                               version=None, detail=None) -> str:
        """Returns the organisation unit schemes query in metadata
        queries (by structure) for the WS Implementation"""
        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if detail:
            self._ws_implementation.validate_structural_detail(detail)

        return self._ws_implementation.get_metadata_organisation_unit_schemes(agency_id, resources, version, detail)

    def get_metadata_transformation_schemes(self, agency_id=None, resources=None,
                                            version=None, detail=None) -> str:
        """Returns the transformation schemes query in metadata
        queries (by structure) for the WS Implementation"""
        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if detail:
            self._ws_implementation.validate_structural_detail(detail)

        return self._ws_implementation.get_metadata_transformation_schemes(agency_id, resources, version, detail)

    def get_metadata_ruleset_schemes(self, agency_id=None, resources=None,
                                     version=None, detail=None) -> str:
        """Returns the ruleset schemes query in metadata
        queries (by structure) for the WS Implementation"""
        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if detail:
            self._ws_implementation.validate_structural_detail(detail)

        return self._ws_implementation.get_metadata_ruleset_schemes(agency_id, resources, version, detail)

    def get_metadata_user_defined_operator_schemes(self, agency_id=None, resources=None,
                                                   version=None, detail=None) -> str:
        """Returns the user defined operator schemes query in metadata
        queries (by structure) for the WS Implementation"""
        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if detail:
            self._ws_implementation.validate_structural_detail(detail)

        return self._ws_implementation.get_metadata_user_defined_operator_schemes(
            agency_id, resources, version, detail)

    def get_metadata_custom_type_schemes(self, agency_id=None, resources=None,
                                         version=None, detail=None) -> str:
        """Returns the custom type schemes query in metadata
        queries (by structure) for the WS Implementation"""
        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if detail:
            self._ws_implementation.validate_structural_detail(detail)

        return self._ws_implementation.get_metadata_custom_type_schemes(agency_id, resources, version, detail)

    def get_metadata_name_personalisation_schemes(self, agency_id=None, resources=None,
                                                  version=None, detail=None) -> str:
        """Returns the name personalisation schemes query in metadata
        queries (by structure) for the WS Implementation"""
        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if detail:
            self._ws_implementation.validate_structural_detail(detail)

        return self._ws_implementation.get_metadata_name_personalisation_schemes(agency_id, resources, version, detail)

    def get_metadata_vtl_mapping_schemes(self, agency_id=None, resources=None,
                                         version=None, detail=None) -> str:
        """Returns the vtl mapping schemes query in metadata
        queries (by structure) for the WS Implementation"""
        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if detail:
            self._ws_implementation.validate_structural_detail(detail)

        return self._ws_implementation.get_metadata_vtl_mapping_schemes(agency_id, resources, version, detail)

    def get_metadata_value_lists(self, agency_id=None, resources=None,
                                 version=None, detail=None) -> str:
        """Returns the value lists query in metadata
        queries (by structure) for the WS Implementation"""
        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if detail:
            self._ws_implementation.validate_structural_detail(detail)

        return self._ws_implementation.get_metadata_value_lists(agency_id, resources, version, detail)

    def get_metadata_structure_maps(self, agency_id=None, resources=None,
                                    version=None, detail=None) -> str:
        """Returns the structure maps query in metadata
        queries (by structure) for the WS Implementation"""
        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if detail:
            self._ws_implementation.validate_structural_detail(detail)

        return self._ws_implementation.get_metadata_structure_maps(agency_id, resources, version, detail)

    def get_metadata_representation_maps(self, agency_id=None, resources=None,
                                         version=None, detail=None) -> str:
        """Returns the representation maps query in metadata
        queries (by structure) for the WS Implementation"""
        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if detail:
            self._ws_implementation.validate_structural_detail(detail)

        return self._ws_implementation.get_metadata_representation_maps(agency_id, resources, version, detail)

    def get_metadata_concept_scheme_maps(self, agency_id=None, resources=None,
                                         version=None, detail=None) -> str:
        """Returns the concept scheme maps query in metadata
        queries (by structure) for the WS Implementation"""
        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if detail:
            self._ws_implementation.validate_structural_detail(detail)

        return self._ws_implementation.get_metadata_concept_scheme_maps(agency_id, resources, version, detail)

    def get_metadata_category_scheme_maps(self, agency_id=None, resources=None,
                                          version=None, detail=None) -> str:
        """Returns the category scheme maps query in metadata
        queries (by structure) for the WS Implementation"""
        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if detail:
            self._ws_implementation.validate_structural_detail(detail)

        return self._ws_implementation.get_metadata_category_scheme_maps(agency_id, resources, version, detail)

    def get_metadata_organisation_scheme_maps(self, agency_id=None, resources=None,
                                              version=None, detail=None) -> str:
        """Returns the organisation scheme maps query in metadata
        queries (by structure) for the WS Implementation"""
        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if detail:
            self._ws_implementation.validate_structural_detail(detail)

        return self._ws_implementation.get_metadata_organisation_scheme_maps(agency_id, resources, version, detail)

    def get_metadata_reporting_taxonomy_maps(self, agency_id=None, resources=None,
                                             version=None, detail=None) -> str:
        """Returns the reporting taxonomy maps query in metadata
        queries (by structure) for the WS Implementation"""
        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if detail:
            self._ws_implementation.validate_structural_detail(detail)

        return self._ws_implementation.get_metadata_reporting_taxonomy_maps(agency_id, resources, version, detail)

    def get_metadata_metadataflow_query(self, agency_id=None, resources=None,
                                        version=None, provider_id=None, detail=None) -> str:
        """Returns the metadata query in metadata
        queries (by metadataflow) for the WS Implementation"""
        resources = self.id_builder(resources)
        agency_id = agency_id if agency_id else "all"
        if detail:
            self._ws_implementation.validate_structural_detail(detail)

        return self._ws_implementation.get_metadata_metadataflow_query(agency_id, resources,
                                                                       version, provider_id, detail)

    def get_metadata_metadataset_query(self, provider_id=None, resources=None,
                                       version=None, detail=None) -> str:
        """Returns the metadata query in metadata
        queries (by metadataset) for the WS Implementation"""
        resources = self.id_builder(resources)
        provider_id = provider_id if provider_id else "all"
        if detail:
            self._ws_implementation.validate_structural_detail(detail)

        return self._ws_implementation.get_metadata_metadataset_query(provider_id, resources,
                                                                      version, detail)
