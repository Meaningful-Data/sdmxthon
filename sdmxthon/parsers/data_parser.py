from .gdscollector import GenerateSuper
from ..utils.xml_base import encode_str_2_3, Tag_pattern_

Validate_simpletypes_ = True
UseCapturedNS_ = True
save_element_tree_node = False


class DataParser(GenerateSuper):
    def __init__(self, gds_collector_=None, **kwargs_):
        super().__init__(gds_collector_)
        self._value = ''
        self.gds_collector_ = gds_collector_
        if save_element_tree_node:
            self.gds_element_tree_node_ = None
        self.__validate_NestedNCNameIDType_patterns = [['^([A-Za-z][A-Za-z0-9_\\-]*(\\.[A-Za-z][A-Za-z0-9_\\-]*)*)$'],
                                                       ['^([A-Za-z0-9_@$\\-]+(\\.[A-Za-z0-9_@$\\-]+)*)$']]
        self.__validate_IDType_patterns = [['^([A-Za-z0-9_@$\\-]+)$'],
                                           ['^([A-Za-z0-9_@$\\-]+(\\.[A-Za-z0-9_@$\\-]+)*)$']]
        self.__validate_VersionType_patterns = [['^([0-9]+(\\.[0-9]+)*)$']]
        self.__validate_NestedIDType_patterns = [['^([A-Za-z0-9_@$\\-]+(\\.[A-Za-z0-9_@$\\-]+)*)$']]
        self.__validate_NCNameIDType_patterns = [['^([A-Za-z][A-Za-z0-9_\\-]*)$'], ['^([A-Za-z0-9_@$\\-]+)$'],
                                                 ['^([A-Za-z0-9_@$\\-]+(\\.[A-Za-z0-9_@$\\-]+)*)$']]

    def has_content_(self):
        return False

    @staticmethod
    def factory(*args_, **kwargs_):
        pass

    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_

        if save_element_tree_node:
            self.gds_element_tree_node_ = node

        already_processed = set()

        self.build_attributes(node, node.attrib, already_processed)

        for child in node:
            node_name_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.build_children(child, node, node_name_, gds_collector_=gds_collector_)

        return self

    def build_attributes(self, node, attributes_, already_processed):
        pass

    def validate_nested_NC_name_id_type(self, value):
        # Validate dim_type NestedNCNameIDType, a restriction on NestedIDType.
        result = True

        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{value}": {lineno} is not of the correct base simple dim_type (str)')
                return False

            if not self.gds_validate_simple_patterns(self.__validate_NestedNCNameIDType_patterns, value):
                self.gds_collector_.add_message(f'Value "{encode_str_2_3(value)}" '
                                                f'does not match xsd pattern restrictions: '
                                                f'{self.__validate_NestedNCNameIDType_patterns}')
                result = False

        return result

    def validate_id_type(self, value):
        # Validate dim_type IDType, a restriction on NestedIDType.
        result = True

        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{value}": {lineno} is not of the correct base simple dim_type (str)')
                return False

            if not self.gds_validate_simple_patterns(self.__validate_IDType_patterns, value):
                self.gds_collector_.add_message(f'Value "{encode_str_2_3(value)}" '
                                                f'does not match xsd pattern restrictions: '
                                                f'{self.__validate_IDType_patterns}')
                result = False

        return result

    def validate_version_type(self, value):
        # Validate dim_type VersionType, a restriction on xs:string.
        result = True

        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{value}": {lineno} is not of the correct base simple dim_type (str)')
                return False

            if not self.gds_validate_simple_patterns(self.__validate_VersionType_patterns, value):
                self.gds_collector_.add_message(f'Value "{encode_str_2_3(value)}" '
                                                f'does not match xsd pattern restrictions: '
                                                f'{self.__validate_IDType_patterns}')
                result = False

        return result

    def validate_nested_id_type(self, value):
        # Validate dim_type NestedIDType, a restriction on xs:string.
        result = True

        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{value}": {lineno} is not of the correct base simple dim_type (str)')
                return False

            if not self.gds_validate_simple_patterns(self.__validate_NestedIDType_patterns, value):
                self.gds_collector_.add_message(f'Value "{encode_str_2_3(value)}" '
                                                f'does not match xsd pattern restrictions: '
                                                f'{self.__validate_IDType_patterns}')
                result = False

        return result

    def validate_NC_name_id_type(self, value):
        # Validate dim_type common:NCNameIDType, a restriction on IDType.
        result = True

        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{value}": {lineno} is not of the correct base simple dim_type (str)')
                return False

            if not self.gds_validate_simple_patterns(self.__validate_NCNameIDType_patterns, value):
                self.gds_collector_.add_message(f'Value "{encode_str_2_3(value)}" '
                                                f'does not match xsd pattern restrictions: '
                                                f'{self.__validate_IDType_patterns}')
                result = False

        return result

    def validate_object_type_code_list_type(self, value):
        # Validate dim_type ObjectTypeCodelistType, a restriction on xs:string.
        result = True
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{value}": {lineno} is not of the correct base simple dim_type (str)')
                result = False

            value = value
            enumerations = ['Any', 'Agency', 'AgencyScheme', 'AttachmentConstraint', 'Attribute', 'AttributeDescriptor',
                            'Categorisation', 'Category', 'CategorySchemeMap', 'CategoryScheme', 'Code', 'CodeMap',
                            'Codelist', 'CodelistMap', 'ComponentMap', 'Concept', 'ConceptMap', 'ConceptScheme',
                            'ConceptSchemeMap', 'Constraint', 'ConstraintTarget', 'ContentConstraint', 'Dataflow',
                            'DataConsumer', 'DataConsumerScheme', 'DataProvider', 'DataProviderScheme', 'DataSetTarget',
                            'DataStructure', 'Dimension', 'DimensionDescriptor', 'DimensionDescriptorValuesTarget',
                            'GroupDimensionDescriptor', 'HierarchicalCode', 'HierarchicalCodelist', 'Hierarchy',
                            'HybridCodelistMap', 'HybridCodeMap', 'IdentifiableObjectTarget', 'Level',
                            'MeasureDescriptor', 'MeasureDimension', 'Metadataflow', 'MetadataAttribute', 'MetadataSet',
                            'MetadataStructure', 'MetadataTarget', 'Organisation', 'OrganisationMap',
                            'OrganisationScheme', 'OrganisationSchemeMap', 'OrganisationUnit', 'OrganisationUnitScheme',
                            'PrimaryMeasure', 'Process', 'ProcessStep', 'ProvisionAgreement', 'ReportingCategory',
                            'ReportingCategoryMap', 'ReportingTaxonomy', 'ReportingTaxonomyMap',
                            'ReportingYearStartDay', 'ReportPeriodTarget', 'ReportStructure', 'StructureMap',
                            'StructureSet', 'TimeDimension', 'Transition']

            if value not in enumerations:
                self.gds_collector_.add_message(f'Value "{encode_str_2_3(value)}" '
                                                f'does not match xsd pattern restrictions: '
                                                f'{self.__validate_IDType_patterns}')
                result = False

        return result

    def validate_package_type_code_list_type(self, value):
        # Validate dim_type PackageTypeCodelistType, a restriction on xs:string.
        result = True
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{value}": {lineno} is not of the correct base simple dim_type (str)')
                result = False

            value = value
            enumerations = ['base', 'datastructure', 'metadatastructure', 'process', 'registry', 'mapping', 'codelist',
                            'categoryscheme', 'conceptscheme']

            if value not in enumerations:
                self.gds_collector_.add_message(f'Value "{encode_str_2_3(value)}" '
                                                f'does not match xsd pattern restrictions: '
                                                f'{self.__validate_IDType_patterns}')
                result = False

        return result

    def export_attributes(self, outfile, level, already_processed, namespace_prefix_, name_):
        pass

    def validate(self):
        pass

    def export_attributes_as_dict(self, parent_dict: dict, data: list, valid_fields: list):
        pass

    def build_children(self, child, node, node_name_, gds_collector_):
        pass
