"""
    References file withholds all the Reference classes needed for parsing
"""

from ..parsers.data_parser import DataParser, Validate_simpletypes_
from ..utils.xml_base import find_attr_value_, cast, encode_str_2_3, raise_parse_error


class ReferenceType(DataParser):
    """ReferenceType is an abstract base dim_type. It is used as the basis for all
    references, to all for a top level generic object reference that can be
    substituted with an explicit reference to any object. Any reference can
    consist of a Ref (which contains all required reference fields
    separately) and/or a URN. These must result in the identification of
    the same object. Note that the Ref and URN elements are local and
    unqualified in order to allow for refinement of this structure outside
    of the namespace. This allows any reference to further refined by a
    different namespace. For example, a metadata structure definition
    specific metadata set might wish to restrict the URN to only allow for
    a value from an enumerated list. The general URN structure, for the
    purpose of mapping the reference fields is as follows:
    urn:sdmx:org.package-name.class-name=agency-id_:(maintainable-parent-
    object-id_[maintainable-parent-object-version].)?(container-object-
    id_.)?object-id_([object-version])?."""
    __hash__ = DataParser.__hash__
    subclass = None
    superclass = None

    def __init__(self, Ref=None, URN=None, gds_collector_=None):
        super(ReferenceType, self).__init__(gds_collector_)
        self.gds_collector_ = gds_collector_
        self._ref = Ref
        self._urn = URN

    @staticmethod
    def factory(*args_, **kwargs_):
        """Factory Method of ReferenceType"""
        return ReferenceType(*args_, **kwargs_)

    def has_content_(self):
        """Check if it has any content"""
        if self._ref is not None or self._urn is not None:
            return True
        else:
            return False

    @property
    def ref(self):
        """Component Reference"""
        return self._ref

    @ref.setter
    def ref(self, value):
        self._ref = value

    @property
    def urn(self):
        """Component URN"""
        return self._urn

    @urn.setter
    def urn(self, value):
        self._urn = value

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'Ref':
            obj_ = RefBaseType.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self._ref = f'{obj_.agencyID}:{obj_.id_}({obj_.version})'
        elif nodeName_ == 'URN':
            value_ = child_.text
            value_ = self.gds_parse_string(value_)
            value_ = self.gds_validate_string(value_)
            aux = value_.split("=", 1)[1]
            self._ref = aux


# end class ReferenceType

class RelationshipRefType(DataParser):
    """Parser of Relationships in the XML Element DimensionReference, PrimaryMeasure,
     Dimension and Parent of an Item """

    def __init__(self, gds_collector_=None):
        super().__init__(gds_collector_)
        self._ref = None

    @staticmethod
    def factory(*args_, **kwargs_):
        """Factory Method of RelationshipRefType"""
        return RelationshipRefType(*args_, **kwargs_)

    @property
    def ref(self):
        """Reference to the Component as String"""
        return self._ref

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'Ref':
            obj_ = RefIDType.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self._ref = obj_.id


class RefIDType(DataParser):
    """Parser of a Reference which has an ID only"""

    def __init__(self, gds_collector_=None):
        super().__init__(gds_collector_)
        self._id = None

    @staticmethod
    def factory(*args_, **kwargs_):
        """Factory Method of RefIDType"""
        return RefIDType(*args_, **kwargs_)

    @property
    def id(self):
        """ID of the Component Referenced"""
        return self._id

    def build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        value = find_attr_value_('id', node)
        if value is not None and 'id' not in already_processed:
            already_processed.add('id')
            self._id = value


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
    referenced (agency-id_ in the URN structure). This is optional to allow
    for local references (where the other reference fields are inferred
    from another context), but all complete references will require
    this.The maintainableParentID attribute identifies the maintainable
    object in which the referenced object is defined, if applicable
    (maintainable-parent-object-id_ in the URN structure). This is only used
    in references where the referenced object is not itself
    maintainable.The maintainableParentVersion attribute identifies the
    version of the maintainable object in which the referenced object is
    defined (maintainable-parent-object-version in the URN structure). This
    is only used in references where the referenced object is not itself
    maintainable. This should only be used when the maintainableParentID is
    present. If this is available, a default of 1.0 will always apply.The
    containerID attribute identifies the object within a maintainable
    object in which the referenced object is defined (container-object-id_
    in the URN structure). This is only used in references where the
    referenced object is not contained directly within a maintainable
    object (e.g. a Component within a ComponentList, within a maintainable
    Structure). If the container has a fixed identifier, this attribute
    will not be present.The id_ attribute identifies the object being
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
    types of fields, the representation should be sub-set to the
    appropriate values.The package attribute indicates the package name for
    the object being referenced. This attribute allows any reference to be
    processed generically from this definition. References derived from
    this should fix the value of this attribute to indicate the dim_type of
    object that is being referenced, or in the case that a reference which
    allows specific types of fields, the representation should be sub-
    set to the appropriate values."""
    __hash__ = DataParser.__hash__
    subclass = None
    superclass = None

    def __init__(self, agencyID=None, maintainableParentID=None, maintainableParentVersion=None, containerID=None,
                 idx=None, version=None, local=None, class_=None, package=None, gds_collector_=None, **kwargs_):
        super(RefBaseType, self).__init__(gds_collector_, **kwargs_)
        self.gds_collector_ = gds_collector_
        self._agencyID = agencyID
        self._maintainableParentID = maintainableParentID
        self._maintainableParentVersion = maintainableParentVersion
        self._containerID = cast(None, containerID)
        self._id = idx
        self._version = version
        self._local = local
        self._class_ = class_
        self._package = package

    @staticmethod
    def factory(*args_, **kwargs_):
        """Factory Method of RefBaseType"""
        return RefBaseType(*args_, **kwargs_)

    @property
    def agencyID(self):
        """Gets the attribute AgencyID of the reference"""
        return self._agencyID

    @agencyID.setter
    def agencyID(self, value):
        self._agencyID = value

    @property
    def maintainableParentID(self):
        """Gets the attribute maintainableParentID of the reference"""
        return self._maintainableParentID

    @maintainableParentID.setter
    def maintainableParentID(self, value):
        self._maintainableParentID = value

    @property
    def maintainableParentVersion(self):
        """Gets the attribute maintainableParentVersion of the reference"""
        return self._maintainableParentVersion

    @maintainableParentVersion.setter
    def maintainableParentVersion(self, value):
        self._maintainableParentVersion = value

    @property
    def containerID(self):
        """Gets the attribute containerID of the reference"""
        return self._containerID

    @containerID.setter
    def containerID(self, value):
        self._containerID = value

    @property
    def id_(self):
        """Gets the attribute id of the reference"""
        return self._id

    @id_.setter
    def id_(self, value):
        self._id = value

    @property
    def version(self):
        """Gets the attribute version of the reference"""
        return self._version

    @version.setter
    def version(self, value):
        self._version = value

    @property
    def local(self):
        """Gets the attribute local of the reference"""
        return self._local

    @local.setter
    def local(self, value):
        self._local = value

    @property
    def class_(self):
        """Gets the attribute class_ of the reference"""
        return self._class_

    @class_.setter
    def class_(self, value):
        self._class_ = value

    @property
    def package(self):
        """Gets the attribute package of the reference"""
        return self._package

    @package.setter
    def package(self, value):
        self._package = value

    def validate_object_type_code_list_type(self, value):
        """Validate dim_type ObjectTypeCodelistType, a restriction on xs:string."""
        result = True

        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{value}":{lineno} is not of the correct base simple dim_type (str)')
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
                    f'Value "{encode_str_2_3(value)}":{lineno} does not match xsd enumeration restriction')
                result = False

        return result

    def validate_package_type_code_list_type(self, value):
        """Validate dim_type PackageTypeCodelistType, a restriction on xs:string."""
        result = True

        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{value}":{lineno} is not of the correct base simple dim_type (str)')
                return False

            value = value
            enumerations = ['base', 'datastructure', 'metadatastructure', 'process', 'registry', 'mapping', 'codelist',
                            'categoryscheme', 'conceptscheme']

            if value not in enumerations:
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{encode_str_2_3(value)}":{lineno} does not match xsd enumeration restriction')
                result = False

        return result

    def build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
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
            self.validate_object_type_code_list_type(self._class_)

        value = find_attr_value_('package', node)
        if value is not None and 'package' not in already_processed:
            already_processed.add('package')
            self._package = value
            self.validate_package_type_code_list_type(self._package)
