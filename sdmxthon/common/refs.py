from ..utils.data_parser import DataParser, Validate_simpletypes_
from ..utils.xml_base import _cast, find_attr_value_, quote_attrib, encode_str_2_3, raise_parse_error


class RefBaseType(DataParser):
    """RefBaseType is an abstract base dim_type the defines the basis for any set
    of complete reference fields. This should be refined by derived types
    so that only the necessary fields are available and required as
    necessary. This can be used for both full and local references (when
    some of the values are implied from another context). A local reference
    is indicated with the local attribute. The values in this dim_type
    correspond directly to the components of the URN structure, and thus
    can be used to compose a URN when the local attribute value is false.
    As this is the case, any reference components which are not part of the
    URN structure should not be present in the derived types.The agencyID
    attribute identifies the maintenance agency for the object being
    referenced (agency-id in the URN structure). This is optional to allow
    for local references (where the other reference fields are inferred
    from another context), but all complete references will require
    this.The maintainableParentID attribute identifies the maintainable
    object in which the referenced object is defined, if applicable
    (maintainable-parent-object-id in the URN structure). This is only used
    in references where the referenced object is not itself
    maintainable.The maintainableParentVersion attribute identifies the
    version of the maintainable object in which the referenced object is
    defined (maintainable-parent-object-version in the URN structure). This
    is only used in references where the referenced object is not itself
    maintainable. This should only be used when the maintainableParentID is
    present. If this is available, a default of 1.0 will always apply.The
    containerID attribute identifies the object within a maintainable
    object in which the referenced object is defined (container-object-id
    in the URN structure). This is only used in references where the
    referenced object is not contained directly within a maintainable
    object (e.g. a Component within a ComponentList, within a maintainable
    Structure). If the container has a fixed identifier, this attribute
    will not be present.The id attribute identifies the object being
    referenced, and is therefore always required.The version attribute
    identifies the version of the object being reference, if applicable. If
    this is available, a default value of 1.0 will always apply.The local
    attribute indicates whether this set of reference fields is meant for
    local referencing, in which case some of the reference fields will be
    implied from another context. Concrete instances of this class will
    always fix this value to either true or false, depending on their
    intended usage. If the value is fixed to true, then the complete set of
    reference fields will be required and a URN can be fully composed from
    the values.The class attribute indicates the class name of the object
    being referenced. This attribute allows any reference to be processed
    generically from this definition. References derived from this should
    fix the value of this attribute to indicate the dim_type of object that is
    being referenced, or in the case that a reference which allows specific
    types of fields, the representation should be sub-setted to the
    appropriate values.The package attribute indicates the package name for
    the object being referenced. This attribute allows any reference to be
    processed generically from this definition. References derived from
    this should fix the value of this attribute to indicate the dim_type of
    object that is being referenced, or in the case that a reference which
    allows specific types of fields, the representation should be sub-
    setted to the appropriate values."""
    __hash__ = DataParser.__hash__
    subclass = None
    superclass = None

    def __init__(self, agencyID=None, maintainableParentID=None, maintainableParentVersion=None, containerID=None,
                 idx=None, version=None, local=None, class_=None, package=None, gds_collector_=None, **kwargs_):
        super(RefBaseType, self).__init__(gds_collector_, **kwargs_)
        self._namespacedef = 'xmlns:common="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common"'
        self._namespaceprefix = "common"
        self._name = 'RefBaseType'
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self._agencyID = agencyID
        self._agencyID_nsprefix_ = None
        self._maintainableParentID = maintainableParentID
        self._maintainableParentID_nsprefix_ = None
        self._maintainableParentVersion = maintainableParentVersion
        self._maintainableParentVersion_nsprefix_ = None
        self._containerID = _cast(None, containerID)
        self._containerID_nsprefix_ = None
        self._id = idx
        self._id_nsprefix_ = None
        self._version = version
        self._version_nsprefix_ = None
        self._local = _cast(bool, local)
        self._local_nsprefix_ = None
        self._class_ = class_
        self._class__nsprefix_ = None
        self._package = package
        self._package_nsprefix_ = None

    def factory(*args_, **kwargs_):
        return RefBaseType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_agencyID(self):
        return self._agencyID

    def set_agencyID(self, agencyID):
        self._agencyID = agencyID

    def get_maintainableParentID(self):
        return self._maintainableParentID

    def set_maintainableParentID(self, maintainableParentID):
        self._maintainableParentID = maintainableParentID

    def get_maintainableParentVersion(self):
        return self._maintainableParentVersion

    def set_maintainableParentVersion(self, maintainableParentVersion):
        self._maintainableParentVersion = maintainableParentVersion

    def get_containerID(self):
        return self._containerID

    def set_containerID(self, containerID):
        self._containerID = containerID

    def get_id(self):
        return self._id

    def set_id(self, idx):
        self._id = idx

    def get_version(self):
        return self._version

    def set_version(self, version):
        self._version = version

    def get_local(self):
        return self._local

    def set_local(self, local):
        self._local = local

    def get_class(self):
        return self._class_

    def set_class(self, class_):
        self._class_ = class_

    def get_package(self):
        return self._package

    def set_package(self, package):
        self._package = package

    def validate_object_type_code_list_type(self, value):
        # Validate dim_type ObjectTypeCodelistType, a restriction on xs:string.
        result = True

        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple dim_type (str)' % {"value": value,
                                                                                                      "lineno": lineno, })
                return False

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
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on ObjectTypeCodelistType' % {
                        "value": encode_str_2_3(value), "lineno": lineno})
                result = False

        return result

    def validate_package_type_code_list_type(self, value):
        # Validate dim_type PackageTypeCodelistType, a restriction on xs:string.
        result = True

        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple dim_type (str)' % {"value": value,
                                                                                                      "lineno": lineno, })
                return False

            value = value
            enumerations = ['base', 'datastructure', 'metadatastructure', 'process', 'registry', 'mapping', 'codelist',
                            'categoryscheme', 'conceptscheme']

            if value not in enumerations:
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on PackageTypeCodelistType' % {
                        "value": encode_str_2_3(value), "lineno": lineno})
                result = False

        return result

    def export_attributes(self, outfile, level, already_processed, namespace_prefix_='', name_='RefBaseType'):
        if self._agencyID is not None and 'agencyID' not in already_processed:
            already_processed.add('agencyID')
            outfile.write(' agencyID=%s' % (quote_attrib(self._agencyID),))

        if self._maintainableParentID is not None and 'maintainableParentID' not in already_processed:
            already_processed.add('maintainableParentID')
            outfile.write(' maintainableParentID=%s' % (quote_attrib(self._maintainableParentID),))

        if self._maintainableParentVersion is not None and 'maintainableParentVersion' not in already_processed:
            already_processed.add('maintainableParentVersion')
            outfile.write(' maintainableParentVersion=%s' % (self.gds_encode(
                self.gds_format_string(quote_attrib(self._maintainableParentVersion),
                                       input_name='maintainableParentVersion')),))

        if self._containerID is not None and 'containerID' not in already_processed:
            already_processed.add('containerID')
            outfile.write(' containerID=%s' % (
                self.gds_encode(self.gds_format_string(quote_attrib(self._containerID), input_name='containerID')),))

        if self._id is not None and 'id' not in already_processed:
            already_processed.add('id')
            outfile.write(
                ' id=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self._id), input_name='id')),))

        if self._version is not None and 'version' not in already_processed:
            already_processed.add('version')
            outfile.write(' version=%s' % (
                self.gds_encode(self.gds_format_string(quote_attrib(self._version), input_name='version')),))

        if self._local is not None and 'local' not in already_processed:
            already_processed.add('local')
            outfile.write(' local="%s"' % self.gds_format_boolean(self._local, input_name='local'))

        if self._class_ is not None and 'class_' not in already_processed:
            already_processed.add('class_')
            outfile.write(' class=%s' % (
                self.gds_encode(self.gds_format_string(quote_attrib(self._class_), input_name='class')),))

        if self._package is not None and 'package' not in already_processed:
            already_processed.add('package')
            outfile.write(' package=%s' % (
                self.gds_encode(self.gds_format_string(quote_attrib(self._package), input_name='package')),))

    def export_attributes_as_dict(self, parent_dict: dict, data: list, valid_fields: list):
        if self._agencyID is not None and 'agencyID' in valid_fields:
            parent_dict.update({'agencyID': self._agencyID})

        if self._maintainableParentID is not None and 'maintainableParentID' in valid_fields:
            parent_dict.update({'maintainableParentID': self._maintainableParentID})

        if self._maintainableParentVersion is not None and 'maintainableParentVersion' in valid_fields:
            parent_dict.update({'maintainableParentVersion': self._maintainableParentVersion})

        if self._containerID is not None and 'containerID' in valid_fields:
            parent_dict.update({'containerID': self._containerID})

        if self._id is not None and 'id' in valid_fields:
            parent_dict.update({'id': self._id})

        if self._version is not None and 'version' in valid_fields:
            parent_dict.update({'version': self._version})

        if self._local is not None and 'local' in valid_fields:
            parent_dict.update({'local': self._local})

        if self._class_ is not None and 'class_' in valid_fields:
            parent_dict.update({'class_': self._class_})

        if self._package is not None and 'package' in valid_fields:
            parent_dict.update({'package': self._package})

    def build_attributes(self, node, attrs, already_processed):
        value = find_attr_value_('agencyID', node)

        if value is not None and 'agencyID' not in already_processed:
            already_processed.add('agencyID')
            self._agencyID = value
            self.validate_nested_NC_name_id_type(self._agencyID)  # validate dim_type NestedNCNameIDType

        value = find_attr_value_('maintainableParentID', node)
        if value is not None and 'maintainableParentID' not in already_processed:
            already_processed.add('maintainableParentID')
            self._maintainableParentID = value
            self.validate_id_type(self._maintainableParentID)  # validate dim_type IDType

        value = find_attr_value_('maintainableParentVersion', node)
        if value is not None and 'maintainableParentVersion' not in already_processed:
            already_processed.add('maintainableParentVersion')
            self._maintainableParentVersion = value
            self.validate_version_type(self._maintainableParentVersion)  # validate dim_type VersionType

        value = find_attr_value_('containerID', node)
        if value is not None and 'containerID' not in already_processed:
            already_processed.add('containerID')
            self._containerID = value
            self.validate_nested_id_type(self._containerID)  # validate dim_type NestedIDType

        value = find_attr_value_('id', node)
        if value is not None and 'id' not in already_processed:
            already_processed.add('id')
            self._id = value
            self.validate_nested_id_type(self._id)  # validate dim_type NestedIDType

        value = find_attr_value_('version', node)
        if value is not None and 'version' not in already_processed:
            already_processed.add('version')
            self._version = value
            self.validate_version_type(self._version)  # validate dim_type VersionType

        value = find_attr_value_('local', node)
        if value is not None and 'local' not in already_processed:
            already_processed.add('local')
            if value in ('true', '1'):
                self._local = True
            elif value in ('false', '0'):
                self._local = False
            else:
                raise_parse_error(node, 'Bad boolean attribute')

        value = find_attr_value_('class', node)
        if value is not None and 'class' not in already_processed:
            already_processed.add('class')
            self._class_ = value
            self.validate_object_type_code_list_type(self._class_)  # validate dim_type ObjectTypeCodelistType

        value = find_attr_value_('package', node)
        if value is not None and 'package' not in already_processed:
            already_processed.add('package')
            self._package = value
            self.validate_package_type_code_list_type(self._package)  # validate dim_type PackageTypeCodelistType


# end class RefBaseType

class MaintainableRefBaseType(RefBaseType):
    """MaintainableRefBaseType is an abstract base dim_type for referencing a
    maintainable object."""
    __hash__ = RefBaseType.__hash__
    subclass = None
    superclass = RefBaseType

    def __init__(self, agencyID=None, maintainableParentID=None, maintainableParentVersion=None, containerID=None,
                 idx=None, version=None, local=None, class_=None, package=None, gds_collector_=None, **kwargs_):
        super(MaintainableRefBaseType, self).__init__(agencyID, maintainableParentID, maintainableParentVersion,
                                                      containerID, idx, version, local, class_, package, gds_collector_,
                                                      **kwargs_)
        self._name = 'MaintainableRefBaseType'

    def factory(*args_, **kwargs_):
        return MaintainableRefBaseType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def validate_object_type_code_list_type(self, value):
        # Validate dim_type MaintainableTypeCodelistType, a restriction on ObjectTypeCodelistType.
        result = True

        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple dim_type (str)' % {"value": value,
                                                                                                      "lineno": lineno, })
                result = False

            value = value
            enumerations = ['Any', 'AgencyScheme', 'AttachmentConstraint', 'Categorisation', 'CategoryScheme',
                            'Codelist', 'ConceptScheme', 'Constraint', 'ContentConstraint', 'Dataflow',
                            'DataConsumerScheme', 'DataProviderScheme', 'DataStructure', 'HierarchicalCodelist',
                            'Metadataflow', 'MetadataStructure', 'OrganisationScheme', 'OrganisationUnitScheme',
                            'Process', 'ProvisionAgreement', 'ReportingTaxonomy', 'StructureSet']

            if value not in enumerations:
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on MaintainableTypeCodelistType' % {
                        "value": encode_str_2_3(value), "lineno": lineno})
                result = False

        return result

    def validate_package_type_code_list_type(self, value):
        # Validate dim_type PackageTypeCodelistType, a restriction on xs:string.
        result = True

        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple dim_type (str)' % {"value": value,
                                                                                                      "lineno": lineno, })
                result = False

            value = value
            enumerations = ['base', 'datastructure', 'metadatastructure', 'process', 'registry', 'mapping', 'codelist',
                            'categoryscheme', 'conceptscheme']

            if value not in enumerations:
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on PackageTypeCodelistType' % {
                        "value": encode_str_2_3(value), "lineno": lineno})
                result = False

        return result


class StructureOrUsageRefBaseType(MaintainableRefBaseType):
    """StructureOrUsageRefBaseType is an abstract base dim_type for referencing a
    structure or structure usage."""
    __hash__ = MaintainableRefBaseType.__hash__
    subclass = None
    superclass = MaintainableRefBaseType

    def __init__(self, agencyID=None, maintainableParentID=None, maintainableParentVersion=None, containerID=None,
                 idx=None, version=None, local=None, class_=None, package=None, gds_collector_=None, **kwargs_):
        super(StructureOrUsageRefBaseType, self).__init__(agencyID, maintainableParentID, maintainableParentVersion,
                                                          containerID, idx, version, local, class_, package,
                                                          gds_collector_, **kwargs_)
        self._name = 'StructureOrUsageRefBaseType'

    def factory(*args_, **kwargs_):
        return StructureOrUsageRefBaseType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def validate_object_type_code_list_type(self, value):
        # Validate dim_type StructureOrUsageTypeCodelistType, a restriction on MaintainableTypeCodelistType.
        result = True

        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple dim_type (str)' % {"value": value,
                                                                                                      "lineno": lineno, })
                result = False

            value = value
            enumerations = ['Dataflow', 'DataStructure', 'Metadataflow', 'MetadataStructure']

            if value not in enumerations:
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on StructureOrUsageTypeCodelistType' % {
                        "value": encode_str_2_3(value), "lineno": lineno})
                result = False

        return result

    def validate_package_type_code_list_type(self, value):
        # Validate dim_type StructurePackageTypeCodelistType, a restriction on PackageTypeCodelistType.
        result = True

        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple dim_type (str)' % {"value": value,
                                                                                                      "lineno": lineno, })
                result = False

            value = value
            enumerations = ['datastructure', 'metadatastructure']

            if value not in enumerations:
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on StructurePackageTypeCodelistType' % {
                        "value": encode_str_2_3(value), "lineno": lineno})
                result = False

        return result


# end class StructureOrUsageRefBaseType

class StructureRefBaseType(StructureOrUsageRefBaseType):
    """StructureRefBaseType is an abstract base dim_type for referencing a
    structure."""
    __hash__ = StructureOrUsageRefBaseType.__hash__
    subclass = None
    superclass = StructureOrUsageRefBaseType

    def __init__(self, agencyID=None, maintainableParentID=None, maintainableParentVersion=None, containerID=None,
                 idx=None, version=None, local=None, class_=None, package=None, gds_collector_=None, **kwargs_):
        super(StructureOrUsageRefBaseType, self).__init__(agencyID, maintainableParentID, maintainableParentVersion,
                                                          containerID, idx, version, local, class_, package, **kwargs_)
        self._name = 'StructureRefBaseType'

    def factory(*args_, **kwargs_):
        return StructureRefBaseType(*args_, **kwargs_)

    factory = staticmethod(factory)


# end class StructureRefBaseType


class DataStructureRefType(StructureRefBaseType):
    """DataStructureRefType contains a set of reference fields for a data
    structure definition."""
    __hash__ = StructureRefBaseType.__hash__
    subclass = None
    superclass = StructureRefBaseType

    def __init__(self, agencyID=None, maintainableParentID=None, maintainableParentVersion=None, containerID=None,
                 id=None, version=None, local=None, class_=None, package=None, gds_collector_=None, **kwargs_):
        super(DataStructureRefType, self).__init__(agencyID, maintainableParentID, maintainableParentVersion,
                                                   containerID, id, version, local, class_, package, **kwargs_)
        self._name = 'DataStructureRefType'

    def factory(*args_, **kwargs_):
        return DataStructureRefType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def validate_object_type_code_list_type(self, value):
        # Validate dim_type StructureTypeCodelistType, a restriction on StructureOrUsageTypeCodelistType.
        result = True
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple dim_type (str)' % {"value": value,
                                                                                                      "lineno": lineno, })
                return False

            value = value
            enumerations = ['DataStructure', 'MetadataStructure']

            if value not in enumerations:
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on StructureTypeCodelistType' % {
                        "value": encode_str_2_3(value), "lineno": lineno})
                result = False

        return result

    def validate_package_type_code_list_type(self, value):
        # Validate dim_type StructurePackageTypeCodelistType, a restriction on PackageTypeCodelistType.
        result = True
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple dim_type (str)' % {"value": value,
                                                                                                      "lineno": lineno, })
                return False

            value = value
            enumerations = ['datastructure', 'metadatastructure']

            if value not in enumerations:
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on StructurePackageTypeCodelistType' % {
                        "value": encode_str_2_3(value), "lineno": lineno})
                result = False

        return result


# end class DataStructureRefType

class StructureUsageRefBaseType(StructureOrUsageRefBaseType):
    """StructureUsageRefBaseType is an abstract base dim_type for referencing a
    structure usage."""
    __hash__ = StructureOrUsageRefBaseType.__hash__
    subclass = None
    superclass = StructureOrUsageRefBaseType

    def __init__(self, agencyID=None, maintainableParentID=None, maintainableParentVersion=None, containerID=None,
                 idx=None, version=None, local=None, class_=None, package=None, gds_collector_=None, **kwargs_):
        super(StructureUsageRefBaseType, self).__init__(agencyID, maintainableParentID, maintainableParentVersion,
                                                        containerID, idx, version, local, class_, package,
                                                        gds_collector_, **kwargs_)
        self._name = 'StructureUsageRefBaseType'

    def factory(*args_, **kwargs_):
        return StructureUsageRefBaseType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def validate_object_type_code_list_type(self, value):
        # Validate dim_type StructureUsageTypeCodelistType, a restriction on StructureOrUsageTypeCodelistType.
        result = True
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple dim_type (str)' % {"value": value,
                                                                                                      "lineno": lineno, })
                result = False
            value = value

            enumerations = ['Dataflow', 'Metadataflow']
            if value not in enumerations:
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on StructureUsageTypeCodelistType' % {
                        "value": encode_str_2_3(value), "lineno": lineno})
                result = False

        return result

    def validate_package_type_code_list_type(self, value):
        # Validate dim_type StructurePackageTypeCodelistType, a restriction on PackageTypeCodelistType.
        result = True
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple dim_type (str)' % {"value": value,
                                                                                                      "lineno": lineno, })
                result = False

            value = value
            enumerations = ['datastructure', 'metadatastructure']

            if value not in enumerations:
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on StructurePackageTypeCodelistType' % {
                        "value": encode_str_2_3(value), "lineno": lineno})
                result = False

        return result


# end class StructureUsageRefBaseType

class DataflowRefType(StructureUsageRefBaseType):
    """DataflowRefType contains a set of reference fields for a data flow."""
    __hash__ = StructureUsageRefBaseType.__hash__
    subclass = None
    superclass = StructureUsageRefBaseType

    def __init__(self, agencyID=None, maintainableParentID=None, maintainableParentVersion=None, containerID=None,
                 id=None, version=None, local=None, class_=None, package=None, gds_collector_=None, **kwargs_):
        super(DataflowRefType, self).__init__(agencyID, maintainableParentID, maintainableParentVersion, containerID,
                                              id, version, local, class_, package, **kwargs_)
        self._name = 'DataflowRefType'

    def factory(*args_, **kwargs_):
        return DataflowRefType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def validate_object_type_code_list_type(self, value):
        # Validate dim_type StructureUsageTypeCodelistType, a restriction on StructureOrUsageTypeCodelistType.
        result = True
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple dim_type (str)' % {"value": value,
                                                                                                      "lineno": lineno, })
                return False

            value = value
            enumerations = ['Dataflow', 'Metadataflow']

            if value not in enumerations:
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on StructureUsageTypeCodelistType' % {
                        "value": encode_str_2_3(value), "lineno": lineno})
                result = False

        return result

    def validate_package_type_code_list_type(self, value):
        # Validate dim_type StructurePackageTypeCodelistType, a restriction on PackageTypeCodelistType.
        result = True
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple dim_type (str)' % {"value": value,
                                                                                                      "lineno": lineno, })
                return False

            value = value
            enumerations = ['datastructure', 'metadatastructure']

            if value not in enumerations:
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on StructurePackageTypeCodelistType' % {
                        "value": encode_str_2_3(value), "lineno": lineno})
                result = False

        return result


# end class DataflowRefType

class ProvisionAgreementRefType(MaintainableRefBaseType):
    """ProvisionAgreementRefType contains a set of reference fields for a
    provision agreement."""
    __hash__ = MaintainableRefBaseType.__hash__
    subclass = None
    superclass = MaintainableRefBaseType

    def __init__(self, agencyID=None, maintainableParentID=None, maintainableParentVersion=None, containerID=None,
                 id=None, version=None, local=None, class_=None, package=None, gds_collector_=None, **kwargs_):
        super(ProvisionAgreementRefType, self).__init__(agencyID, maintainableParentID, maintainableParentVersion,
                                                        containerID, id, version, local, class_, package, **kwargs_)
        self._name = 'ProvisionAgreementRefType'

    def factory(*args_, **kwargs_):
        return ProvisionAgreementRefType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def validate_object_type_code_list_type(self, value):
        # Validate dim_type MaintainableTypeCodelistType, a restriction on ObjectTypeCodelistType.
        result = True
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple dim_type (str)' % {"value": value,
                                                                                                      "lineno": lineno, })
                return False

            value = value
            enumerations = ['Any', 'AgencyScheme', 'AttachmentConstraint', 'Categorisation', 'CategoryScheme',
                            'Codelist', 'ConceptScheme', 'Constraint', 'ContentConstraint', 'Dataflow',
                            'DataConsumerScheme', 'DataProviderScheme', 'DataStructure', 'HierarchicalCodelist',
                            'Metadataflow', 'MetadataStructure', 'OrganisationScheme', 'OrganisationUnitScheme',
                            'Process', 'ProvisionAgreement', 'ReportingTaxonomy', 'StructureSet']

            if value not in enumerations:
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on MaintainableTypeCodelistType' % {
                        "value": encode_str_2_3(value), "lineno": lineno})
                result = False

        return result

    def validate_package_type_code_list_type(self, value):
        # Validate dim_type PackageTypeCodelistType, a restriction on xs:string.
        result = True
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple dim_type (str)' % {"value": value,
                                                                                                      "lineno": lineno, })
                return False

            value = value
            enumerations = ['base', 'datastructure', 'metadatastructure', 'process', 'registry', 'mapping', 'codelist',
                            'categoryscheme', 'conceptscheme']

            if value not in enumerations:
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on PackageTypeCodelistType' % {
                        "value": encode_str_2_3(value), "lineno": lineno})
                result = False

        return result


# end class ProvisionAgreementRefType

class ChildObjectRefBaseType(RefBaseType):
    """ChildObjectRefBaseType is an abstract base dim_type for referencing any
    child object defined directly within a maintainable object."""
    __hash__ = RefBaseType.__hash__
    subclass = None
    superclass = RefBaseType

    def __init__(self, agencyID=None, maintainableParentID=None, maintainableParentVersion=None, containerID=None,
                 id=None, version=None, local=None, class_=None, package=None, gds_collector_=None, **kwargs_):
        super(ChildObjectRefBaseType, self).__init__(agencyID, maintainableParentID, maintainableParentVersion,
                                                     containerID, id, version, local, class_, package, **kwargs_)
        self._namespacedef = 'xmlns:message="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message"'
        self._name = 'ChildObjectRefBaseType'

    def factory(*args_, **kwargs_):
        return ChildObjectRefBaseType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def validate_object_type_code_list_type(self, value):
        # Validate dim_type ObjectTypeCodelistType, a restriction on xs:string.
        result = True
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple dim_type (str)' % {"value": value,
                                                                                                      "lineno": lineno, })
                return False

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
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on ObjectTypeCodelistType' % {
                        "value": encode_str_2_3(value), "lineno": lineno})
                result = False
            return result

    def validate_package_type_code_list_type(self, value):
        # Validate dim_type PackageTypeCodelistType, a restriction on xs:string.
        result = True
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple dim_type (str)' % {"value": value,
                                                                                                      "lineno": lineno, })
                return False

            value = value
            enumerations = ['base', 'datastructure', 'metadatastructure', 'process', 'registry', 'mapping', 'codelist',
                            'categoryscheme', 'conceptscheme']

            if value not in enumerations:
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on PackageTypeCodelistType' % {
                        "value": encode_str_2_3(value), "lineno": lineno})
                result = False

        return result


# end class ChildObjectRefBaseType

class ItemRefBaseType(ChildObjectRefBaseType):
    """ItemRefBaseType is an abstract base dim_type for referencing an item within
    an item scheme.The maintainableParentID references the item scheme in
    which the item being referenced is defined.The
    maintainableParentVersion attribute references the version of the item
    scheme in which the item being referenced is defined. If not supplied,
    a default value of 1.0 is assumed."""
    __hash__ = ChildObjectRefBaseType.__hash__
    subclass = None
    superclass = ChildObjectRefBaseType

    def __init__(self, agencyID=None, maintainableParentID=None, maintainableParentVersion=None, containerID=None,
                 id=None, version=None, local=None, class_=None, package=None, gds_collector_=None, **kwargs_):
        super(ItemRefBaseType, self).__init__(agencyID, maintainableParentID, maintainableParentVersion, containerID,
                                              id, version, local, class_, package, **kwargs_)
        self._namespacedef = 'xmlns:message="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message"'
        self._name = 'ItemRefBaseType'

    def factory(*args_, **kwargs_):
        return ItemRefBaseType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def validate_object_type_code_list_type(self, value):
        # Validate dim_type ItemTypeCodelistType, a restriction on ObjectTypeCodelistType.
        result = True
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple dim_type (str)' % {"value": value,
                                                                                                      "lineno": lineno, })
                return False

            value = value
            enumerations = ['Agency', 'Category', 'Code', 'Concept', 'DataConsumer', 'DataProvider', 'OrganisationUnit',
                            'ReportingCategory']

            if value not in enumerations:
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on ItemTypeCodelistType' % {
                        "value": encode_str_2_3(value), "lineno": lineno})
                result = False

        return result

    def validate_package_type_code_list_type(self, value):
        # Validate dim_type ItemSchemePackageTypeCodelistType, a restriction on PackageTypeCodelistType.
        result = True
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple dim_type (str)' % {"value": value,
                                                                                                      "lineno": lineno, })
                return False

            value = value
            enumerations = ['base', 'codelist', 'categoryscheme', 'conceptscheme']

            if value not in enumerations:
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on ItemSchemePackageTypeCodelistType' % {
                        "value": encode_str_2_3(value), "lineno": lineno})
                result = False

        return result
    # end class ItemRefBaseType


class OrganisationRefBaseType(ItemRefBaseType):
    """OrganisationRefBaseType is an abstract base dim_type which references an
    organisation from within a organisation scheme. Reference fields are
    required for both the scheme and the organisation.The
    maintainableParentID references the organisation scheme in which the
    organisation being referenced is defined.The maintainableParentVersion
    attribute references the version of the organisation scheme in which
    the organisation being referenced is defined. If not supplied, a
    default value of 1.0 is assumed."""
    __hash__ = ItemRefBaseType.__hash__
    subclass = None
    superclass = ItemRefBaseType

    def __init__(self, agencyID=None, maintainableParentID=None, maintainableParentVersion=None, containerID=None,
                 id=None, version=None, local=None, class_=None, package=None, gds_collector_=None, **kwargs_):
        super(OrganisationRefBaseType, self).__init__(agencyID, maintainableParentID, maintainableParentVersion,
                                                      containerID, id, version, local, class_, package, **kwargs_)
        self._name = 'ItemRefBaseType'

    def factory(*args_, **kwargs_):
        return OrganisationRefBaseType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def validate_object_type_code_list_type(self, value):
        # Validate dim_type OrganisationTypeCodelistType, a restriction on ItemTypeCodelistType.
        result = True

        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple dim_type (str)' % {"value": value,
                                                                                                      "lineno": lineno, })
                return False

            value = value
            enumerations = ['Agency', 'DataConsumer', 'DataProvider', 'OrganisationUnit']

            if value not in enumerations:
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on OrganisationTypeCodelistType' % {
                        "value": encode_str_2_3(value), "lineno": lineno})
                result = False

        return result

    def validate_package_type_code_list_type(self, value):
        # Validate dim_type ItemSchemePackageTypeCodelistType, a restriction on PackageTypeCodelistType.
        result = True
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple dim_type (str)' % {"value": value,
                                                                                                      "lineno": lineno, })
                return False

            value = value
            enumerations = ['base', 'codelist', 'categoryscheme', 'conceptscheme']

            if value not in enumerations:
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on ItemSchemePackageTypeCodelistType' % {
                        "value": encode_str_2_3(value), "lineno": lineno})
                result = False

        return result


# end class OrganisationRefBaseType

class DataProviderRefType(OrganisationRefBaseType):
    """DataProviderRefType contains a set of reference fields for referencing a
    data provider within a data provider scheme."""
    __hash__ = OrganisationRefBaseType.__hash__
    subclass = None
    superclass = OrganisationRefBaseType

    def __init__(self, agencyID=None, maintainableParentID=None, maintainableParentVersion=None, containerID=None,
                 id=None, version=None, local=None, class_=None, package=None, gds_collector_=None, **kwargs_):
        super(DataProviderRefType, self).__init__(agencyID, maintainableParentID, maintainableParentVersion,
                                                  containerID, id, version, local, class_, package, **kwargs_)
        self._name = 'DataProviderRefType'

    def factory(*args_, **kwargs_):
        return DataProviderRefType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def validate_object_type_code_list_type(self, value):
        # Validate dim_type OrganisationTypeCodelistType, a restriction on ItemTypeCodelistType.
        result = True
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple dim_type (str)' % {"value": value,
                                                                                                      "lineno": lineno, })
                return False

            value = value
            enumerations = ['Agency', 'DataConsumer', 'DataProvider', 'OrganisationUnit']

            if value not in enumerations:
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on OrganisationTypeCodelistType' % {
                        "value": encode_str_2_3(value), "lineno": lineno})
                result = False

        return result
# end class DataProviderRefType
