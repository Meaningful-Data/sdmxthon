from SDMXThon.utils.generateds import GenerateSuper
from SDMXThon.utils.mappings import ClassToNode, GenerateDSNamespaceDefs
from SDMXThon.utils.xml_base import showIndent, encode_str_2_3, get_all_text_, Tag_pattern_

Validate_simpletypes_ = True
UseCapturedNS_ = True
save_element_tree_node = True


class DataParser(GenerateSuper):
    __hash__ = GenerateSuper.__hash__
    subclass = None
    superclass = None

    def __init__(self, gds_collector, gds_collector_=None, **kwargs_):
        super().__init__(gds_collector)
        self.gds_collector_ = gds_collector_
        self.gds_element_tree_node_ = None
        self.original_tag_name_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self._namespace_prefix = ''
        self._namespace_def = ''
        self._name = ''
        self._value = ''
        self.__validate_NestedNCNameIDType_patterns = [['^([A-Za-z][A-Za-z0-9_\\-]*(\\.[A-Za-z][A-Za-z0-9_\\-]*)*)$'],
                                                       ['^([A-Za-z0-9_@$\\-]+(\\.[A-Za-z0-9_@$\\-]+)*)$']]
        self.__validate_IDType_patterns = [['^([A-Za-z0-9_@$\\-]+)$'],
                                           ['^([A-Za-z0-9_@$\\-]+(\\.[A-Za-z0-9_@$\\-]+)*)$']]
        self.__validate_VersionType_patterns = [['^([0-9]+(\\.[0-9]+)*)$']]
        self.__validate_NestedIDType_patterns = [['^([A-Za-z0-9_@$\\-]+(\\.[A-Za-z0-9_@$\\-]+)*)$']]
        self.__validate_NCNameIDType_patterns = [['^([A-Za-z][A-Za-z0-9_\\-]*)$'], ['^([A-Za-z0-9_@$\\-]+)$'],
                                                 ['^([A-Za-z0-9_@$\\-]+(\\.[A-Za-z0-9_@$\\-]+)*)$']]

    def get_ns_prefix_(self):
        return self._namespace_prefix

    def set_ns_prefix_(self, ns_prefix):
        self._namespace_prefix = ns_prefix

    def get_ns_def_(self):
        return self._namespace_def

    def set_ns_def_(self, ns_def):
        self._namespace_def = ns_def

    def has_content_(self):
        return False

    @staticmethod
    def factory(*args_, **kwargs_):
        pass

    def get_value_of_(self):
        return self._value

    def set_value_of_(self, value):
        self._value = value

    def export(self, outfile, level, pretty_print=True, has_parent=True):
        name_ = ''
        namespace_prefix_ = ''
        namespace_def_ = ''
        imported_ns_def_ = GenerateDSNamespaceDefs.get(self._name)

        if not has_parent:
            outfile.write('<?xml version="1.0" ' + "encoding='UTF-8'?>\n")
            if imported_ns_def_ is not None:
                namespace_def_ = imported_ns_def_
            else:
                namespace_def_ = self._namespace_def

        if len(namespace_def_) > 0:
            namespace_def_ = ' ' + namespace_def_

        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''

        if self.original_tag_name_ is not None:
            name_ = self.original_tag_name_
        else:
            name_ = ClassToNode[type(self).__name__]

        if len(self._namespace_prefix) > 0:
            namespace_prefix_ = self._namespace_prefix + ":"

        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespace_prefix_, name_, namespace_def_))
        already_processed = set()
        self.export_attributes(outfile, level, already_processed, namespace_prefix_, name_)

        if self.has_content_():
            outfile.write('>%s' % (eol_,))
            self.export_children(outfile, level + 1, pretty_print, True)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespace_prefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_,))

    def export_children(self, child_, outfile, level, pretty_print=True, has_parent=True):
        if child_ is not None:
            child_.export(outfile, level, pretty_print, has_parent)

    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_

        if save_element_tree_node:
            self.gds_element_tree_node_ = node

        already_processed = set()

        if node.prefix is not None:
            self._namespace_prefix = node.prefix
        else:
            self._namespace_prefix = ''

        self._value = get_all_text_(node)
        self.build_attributes(node, node.attrib, already_processed)

        for child in node:
            node_name_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.build_children(child, node, node_name_, gds_collector_=gds_collector_)

        return self

    def build_attributes(self, node, attributes_, already_processed):
        pass

    def validate_nested_NC_name_id_type(self, value):
        # Validate type NestedNCNameIDType, a restriction on NestedIDType.
        result = True

        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value,
                                                                                                  "lineno": lineno, })
                return False

            if not self.gds_validate_simple_patterns(self.__validate_NestedNCNameIDType_patterns, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (
                    encode_str_2_3(value), self.__validate_NestedNCNameIDType_patterns))
                result = False

        return result

    def validate_id_type(self, value):
        # Validate type IDType, a restriction on NestedIDType.
        result = True

        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value,
                                                                                                  "lineno": lineno, })
                return False

            if not self.gds_validate_simple_patterns(self.__validate_IDType_patterns, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (
                    encode_str_2_3(value), self.__validate_IDType_patterns))
                result = False

        return result

    def validate_version_type(self, value):
        # Validate type VersionType, a restriction on xs:string.
        result = True

        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value,
                                                                                                  "lineno": lineno, })
                return False

            if not self.gds_validate_simple_patterns(self.__validate_VersionType_patterns, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (
                    encode_str_2_3(value), self.__validate_VersionType_patterns))
                result = False

        return result

    def validate_nested_id_type(self, value):
        # Validate type NestedIDType, a restriction on xs:string.
        result = True

        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value,
                                                                                                  "lineno": lineno, })
                return False

            if not self.gds_validate_simple_patterns(self.__validate_NestedIDType_patterns, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (
                    encode_str_2_3(value), self.__validate_NestedIDType_patterns))
                result = False

        return result

    def validate_NC_name_id_type(self, value):
        # Validate type common:NCNameIDType, a restriction on IDType.
        result = True

        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value,
                                                                                                  "lineno": lineno, })
                return False

            if not self.gds_validate_simple_patterns(self.__validate_NCNameIDType_patterns, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (
                    encode_str_2_3(value), self.__validate_NCNameIDType_patterns,))
                result = False

        return result

    def validate_object_type_code_list_type(self, value):
        # Validate type ObjectTypeCodelistType, a restriction on xs:string.
        result = True
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                line_number = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(line_number)s is not of the correct base simple type (str)' % {"value": value,
                                                                                                       "line_number": line_number, })
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
                line_number = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(line_number)s does not match xsd enumeration restriction on ObjectTypeCodelistType'
                    % {"value": encode_str_2_3(value), "line_number": line_number})
                result = False

        return result

    def validate_package_type_code_list_type(self, value):
        # Validate type PackageTypeCodelistType, a restriction on xs:string.
        result = True
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value,
                                                                                                  "lineno": lineno, })
                result = False

            value = value
            enumerations = ['base', 'datastructure', 'metadatastructure', 'process', 'registry', 'mapping', 'codelist',
                            'categoryscheme', 'conceptscheme']

            if value not in enumerations:
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on PackageTypeCodelistType'
                    % {"value": encode_str_2_3(value), "lineno": lineno})
                result = False

        return result

    def export_attributes(self, outfile, level, already_processed, namespace_prefix_, name_):
        pass

    def validate(self):
        pass

    def export_attributes_as_dict(self, parent_dict: dict, data: list, valid_fields: list):
        pass
