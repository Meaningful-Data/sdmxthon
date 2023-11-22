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
    DATA_HISTORY_OPTIONS = []
    CONSTRAINTS_MODE_OPTIONS = []
    CONSTRAINTS_REFERENCES_OPTIONS = []

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

    @abstractmethod
    def get_constraints(self, flow, key=None, provider=None, component_id=None,
                        mode=None, references=None, start_period=None,
                        end_period=None, updated_after=None):
        """
        Returns query to get availability constraints
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

    def get_process(self, agency_id, resources,
                    version, references=None, detail=None) -> str:
        """
        Returns query to retrieve processes
        """

    def get_categorisation(self, agency_id, resources,
                           version, references=None, detail=None) -> str:
        """
        Returns query to retrieve categorisations
        """

    def get_content_constraint(self, agency_id, resources,
                               version, references=None, detail=None) -> str:
        """
        Returns query to retrieve content constraints
        """

    def get_actual_constraint(self, agency_id, resources,
                              version, references=None, detail=None) -> str:
        """
        Returns query to retrieve actual constraints
        """

    def get_allowed_constraint(self, agency_id, resources,
                               version, references=None, detail=None) -> str:
        """
        Returns query to retrieve allowed constraints
        """

    def get_attachment_constraint(self, agency_id, resources,
                                  version, references=None, detail=None) -> str:
        """
        Returns query to retrieve attachment constraints
        """

    def get_structure(self, agency_id, resources,
                      version, references=None, detail=None) -> str:
        """
        Returns query to retrieve structure
        """

    def get_concept_scheme(self, agency_id, resources,
                           version, references=None, detail=None) -> str:
        """
        Returns query to retrieve concept schemes
        """

    def get_code_list(self, agency_id, resources,
                      version, references=None, detail=None) -> str:
        """
        Returns query to retrieve codelists
        """

    def get_category_scheme(self, agency_id, resources,
                            version, references=None, detail=None) -> str:
        """
        Returns query to retrieve category schemes
        """

    def get_hierarchical_codelist(self, agency_id, resources,
                                  version, references=None, detail=None) -> str:
        """
        Returns query to retrieve hierarchical codelists
        """

    def get_organisation_scheme(self, agency_id, resources,
                                version, references=None, detail=None) -> str:
        """
        Returns query to retrieve organisation schemes
        """

    def get_agency_scheme(self, agency_id, resources,
                          version, references=None, detail=None) -> str:
        """
        Returns query to retrieve agency schemes
        """

    def get_data_provider_scheme(self, agency_id, resources,
                                 version, references=None, detail=None) -> str:
        """
        Returns query to retrieve data provider schemes
        """

    def get_data_consumer_scheme(self, agency_id, resources,
                                 version, references=None, detail=None) -> str:
        """
        Returns query to retrieve data consumer schemes
        """

    def get_organisation_unit_scheme(self, agency_id, resources,
                                     version, references=None, detail=None) -> str:
        """
        Returns query to retrieve organisation unit schemes
        """

    def get_transformation_scheme(self, agency_id, resources,
                                  version, references=None, detail=None) -> str:
        """
        Returns query to retrieve transformation schemes
        """

    def get_ruleset_scheme(self, agency_id, resources,
                           version, references=None, detail=None) -> str:
        """
        Returns query to retrieve ruleset schemes
        """

    def get_user_defined_operator_scheme(self, agency_id, resources,
                                         version, references=None, detail=None) -> str:
        """
        Returns query to retrieve user defined operator schemes
        """

    def get_custom_type_scheme(self, agency_id, resources,
                               version, references=None, detail=None) -> str:
        """
        Returns query to retrieve custom type schemes
        """

    def get_name_personalisation_scheme(self, agency_id, resources,
                                        version, references=None, detail=None) -> str:
        """
        Returns query to retrieve name personalisation schemes
        """

    def get_name_alias_scheme(self, agency_id, resources,
                              version, references=None, detail=None) -> str:
        """
        Returns query to retrieve name alias schemes
        """

    def get_concepts(self, agency_id, resources,
                     version, item_id, references=None, detail=None) -> str:
        """
        Returns query to retrieve concepts
        """

    def get_codes(self, agency_id, resources,
                  version, item_id, references=None, detail=None) -> str:
        """
        Returns query to retrieve codes
        """

    def get_categories(self, agency_id, resources,
                       version, item_id, references=None, detail=None) -> str:
        """
        Returns query to retrieve categories
        """

    def get_hierarchies(self, agency_id, resources,
                        version, item_id, references=None, detail=None) -> str:
        """
        Returns query to retrieve hierarchies
        """

    def get_organisations(self, agency_id, resources,
                          version, item_id, references=None, detail=None) -> str:
        """
        Returns query to retrieve organisations
        """

    def get_agencies(self, agency_id, resources,
                     version, item_id, references=None, detail=None) -> str:
        """
        Returns query to retrieve agencies
        """

    def get_data_providers(self, agency_id, resources,
                           version, item_id, references=None, detail=None) -> str:
        """
        Returns query to retrieve data providers
        """

    def get_data_consumers(self, agency_id, resources,
                           version, item_id, references=None, detail=None) -> str:
        """
        Returns query to retrieve data consumers
        """

    def get_organisation_unit_schemes(self, agency_id, resources,
                                      version, item_id, references=None, detail=None) -> str:
        """
        Returns query to retrieve get organisation unit schemes
        """

    def get_transformation_schemes(self, agency_id, resources,
                                   version, item_id, references=None, detail=None) -> str:
        """
        Returns query to retrieve get transformation schemes
        """

    def get_ruleset_schemes(self, agency_id, resources,
                            version, item_id, references=None, detail=None) -> str:
        """
        Returns query to retrieve get ruleset schemes
        """

    def get_user_defined_operator_schemes(self, agency_id, resources,
                                          version, item_id, references=None, detail=None) -> str:
        """
        Returns query to retrieve get user defined operator schemes
        """

    def get_custom_type_schemes(self, agency_id, resources,
                                version, item_id, references=None, detail=None) -> str:
        """
        Returns query to retrieve get custom type schemes
        """

    def get_name_personalisation_schemes(self, agency_id, resources,
                                         version, item_id, references=None, detail=None) -> str:
        """
        Returns query to retrieve get name personalisation schemes
        """

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
            raise ValueError(f"reference must be one of the following values: "
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
        return self.build_query("dataflow", agency_id, resources, version, references, detail)

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
        return self.build_query("datastructure", agency_id, resources, version, references, detail)

    def get_constraints(self, flow, key=None, provider=None, component_id=None,
                        mode=None, references=None, start_period=None,
                        end_period=None, updated_after=None):

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
