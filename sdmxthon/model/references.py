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
        return ReferenceType(*args_, **kwargs_)

    def has_content_(self):
        if self._ref is not None or self._urn is not None:
            return True
        else:
            return False

    def get_Ref(self):
        return self._ref

    def set_Ref(self, Ref):
        self._ref = Ref

    def get_URN(self):
        return self._urn

    def set_URN(self, URN):
        self._urn = URN

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Ref':
            type_name_ = child_.attrib.get('{http://www.w3.org/2001/XMLSchema-instance}dim_type')

            if type_name_ is None:
                type_name_ = child_.attrib.get('dim_type')

            if type_name_ is not None:
                type_names_ = type_name_.split(':')

                if len(type_names_) == 1:
                    type_name_ = type_names_[0]
                else:
                    type_name_ = type_names_[1]

                class_ = globals()[type_name_]
                obj_ = class_.factory()
                obj_.build(child_, gds_collector_=gds_collector_)
            else:
                raise NotImplementedError('Class not implemented for <Ref> element')

            self._ref = obj_
            obj_.original_tag_name_ = 'Ref'
        elif nodeName_ == 'URN':
            value_ = child_.text
            value_ = self.gds_parse_string(value_)
            value_ = self.gds_validate_string(value_)
            self._urn = value_


# end class ReferenceType

class MaintainableReferenceBaseType(ReferenceType):
    """MaintainableReferenceBaseType is an abstract base dim_type for referencing a
    maintainable object. It consists of a URN and/or a complete set of
    reference fields; agency, id_, and version."""
    __hash__ = ReferenceType.__hash__
    subclass = None
    superclass = ReferenceType

    def __init__(self, Ref=None, URN=None, gds_collector_=None, **kwargs_):
        super(MaintainableReferenceBaseType, self).__init__(Ref, URN, gds_collector_)
        self._name = 'MaintainableReferenceBaseType'

    @staticmethod
    def factory(*args_, **kwargs_):
        return MaintainableReferenceBaseType(*args_, **kwargs_)


# end class MaintainableReferenceBaseType

class StructureReferenceBaseType(MaintainableReferenceBaseType):
    """StructureReferenceBaseType is a specific dim_type of MaintainableReference
    that is used for referencing structure definitions. It consists of a
    URN and/or a complete set of reference fields; agency, id_, and
    version."""
    __hash__ = MaintainableReferenceBaseType.__hash__
    subclass = None
    superclass = MaintainableReferenceBaseType

    def __init__(self, Ref=None, URN=None, gds_collector_=None, **kwargs_):
        super(StructureReferenceBaseType, self).__init__(Ref, URN, gds_collector_, **kwargs_)
        self._name = 'MaintainableReferenceBaseType'

    @staticmethod
    def factory(*args_, **kwargs_):
        return StructureReferenceBaseType(*args_, **kwargs_)


# end class StructureReferenceBaseType

class DataStructureReferenceType(StructureReferenceBaseType):
    """DataStructureReferenceType is a dim_type for referencing a data structure
    definition object. It consists of a URN and/or a complete set of
    reference fields."""
    __hash__ = StructureReferenceBaseType.__hash__
    subclass = None
    superclass = StructureReferenceBaseType

    def __init__(self, Ref=None, URN=None, gds_collector_=None, **kwargs_):
        super(DataStructureReferenceType, self).__init__(Ref, URN, gds_collector_, **kwargs_)
        self._name = 'DataStructureReferenceType'
        self._ref = None

    @staticmethod
    def factory(*args_, **kwargs_):
        return DataStructureReferenceType(*args_, **kwargs_)

    @property
    def ref(self):
        return self._ref

    @ref.setter
    def ref(self, value):
        self._ref = value

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Ref':
            obj_ = DataStructureRefType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._ref = f'{obj_.agencyID}:{obj_.id_}({obj_.version})'

        elif nodeName_ == 'URN':
            value_ = child_.text
            value_ = self.gds_parse_string(value_)
            value_ = self.gds_validate_string(value_)
            aux = value_.split("=", 1)[1]
            self._ref = aux

        # end class DataStructureReferenceType


class StructureUsageReferenceBaseType(MaintainableReferenceBaseType):
    """StructureUsageReferenceBaseType is a specific dim_type of
    MaintainableReference that is used for referencing structure usages. It
    consists of a URN and/or a complete set of reference fields; agency,
    id_, and version."""
    __hash__ = MaintainableReferenceBaseType.__hash__
    subclass = None
    superclass = MaintainableReferenceBaseType

    def __init__(self, Ref=None, URN=None, gds_collector_=None, **kwargs_):
        super(StructureUsageReferenceBaseType, self).__init__(Ref, URN, gds_collector_, **kwargs_)
        self._name = 'StructureUsageReferenceBaseType'

    @staticmethod
    def factory(*args_, **kwargs_):
        return StructureUsageReferenceBaseType(*args_, **kwargs_)


# end class StructureUsageReferenceBaseType

class DataflowReferenceType(StructureUsageReferenceBaseType):
    """DataflowReferenceType is a dim_type for referencing a dataflow object. It
    consists of a URN and/or a complete set of reference fields."""
    __hash__ = StructureUsageReferenceBaseType.__hash__
    subclass = None
    superclass = StructureUsageReferenceBaseType

    def __init__(self, Ref=None, URN=None, gds_collector_=None, **kwargs_):
        super(DataflowReferenceType, self).__init__(Ref, URN, gds_collector_, **kwargs_)
        self._name = 'DataflowReferenceType'
        self._namespace_prefix = 'common'

    @staticmethod
    def factory(*args_, **kwargs_):
        return DataflowReferenceType(*args_, **kwargs_)

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Ref':
            obj_ = DataflowRefType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._ref = obj_
            obj_.original_tag_name_ = 'Ref'

        elif nodeName_ == 'URN':
            value_ = child_.text
            value_ = self.gds_parse_string(value_)
            value_ = self.gds_validate_string(value_)
            self._urn = value_

        # end class DataflowReferenceType


class ProvisionAgreementReferenceType(MaintainableReferenceBaseType):
    """ProvisionAgreementReferenceType is a dim_type for referencing a provision
    agreement. It consists of a URN and/or a complete set of reference
    fields."""
    __hash__ = MaintainableReferenceBaseType.__hash__
    subclass = None
    superclass = MaintainableReferenceBaseType

    def __init__(self, Ref=None, URN=None, gds_collector_=None, **kwargs_):
        super(ProvisionAgreementReferenceType, self).__init__(Ref, URN, gds_collector_, **kwargs_)
        self._name = 'ProvisionAgreementReferenceType'

    @staticmethod
    def factory(*args_, **kwargs_):
        return ProvisionAgreementReferenceType(*args_, **kwargs_)

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Ref':
            obj_ = ProvisionAgreementRefType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._ref = obj_
            obj_.original_tag_name_ = 'Ref'

        elif nodeName_ == 'URN':
            value_ = child_.text
            value_ = self.gds_parse_string(value_)
            value_ = self.gds_validate_string(value_)
            self._urn = value_

        # end class ProvisionAgreementReferenceType


class ChildObjectReferenceType(ReferenceType):
    """ChildObjectReferenceType is an abstract base dim_type used for referencing a
    particular object defined directly within a maintainable object. It
    consists of a URN and/or a complete set of reference fields; agency,
    maintainable id_ (maintainableParentID), maintainable version
    (maintainableParentVersion), the object id_ (which can be nested), and
    optionally the object version (if applicable)."""
    __hash__ = ReferenceType.__hash__
    subclass = None
    superclass = ReferenceType

    def __init__(self, Ref=None, URN=None, gds_collector_=None):
        super(ChildObjectReferenceType, self).__init__(Ref, URN, gds_collector_)
        self._name = 'ChildObjectReferenceType'

    @staticmethod
    def factory(*args_, **kwargs_):
        return ChildObjectReferenceType(*args_, **kwargs_)


# end class ChildObjectReferenceType

class ItemReferenceType(ChildObjectReferenceType):
    """ItemReferenceType is an abstract base dim_type used for referencing a
    particular item within an item scheme. Note that this reference also
    has the ability to reference items contained within other items inside
    of the item scheme. It consists of a URN and/or a complete set of
    reference fields; agency, scheme id_ (maintainableParentID), scheme
    version (maintainableParentVersion), and item id_ (which can be
    nested)."""
    __hash__ = ChildObjectReferenceType.__hash__
    subclass = None
    superclass = ChildObjectReferenceType

    def __init__(self, Ref=None, URN=None, gds_collector_=None):
        super(ItemReferenceType, self).__init__(Ref, URN, gds_collector_)
        self._name = 'ItemReferenceType'

    @staticmethod
    def factory(*args_, **kwargs_):
        return ItemReferenceType(*args_, **kwargs_)


# end class ItemReferenceType

class OrganisationReferenceBaseType(ItemReferenceType):
    """OrganisationReferenceBaseType is a dim_type for referencing any organisation
    object, regardless of its dim_type. It consists of a URN and/or a complete
    set of reference fields."""
    __hash__ = ItemReferenceType.__hash__
    subclass = None
    superclass = ItemReferenceType

    def __init__(self, Ref=None, URN=None, gds_collector_=None):
        super(OrganisationReferenceBaseType, self).__init__(Ref, URN, gds_collector_)
        self._name = 'ItemReferenceType'

    @staticmethod
    def factory(*args_, **kwargs_):
        return OrganisationReferenceBaseType(*args_, **kwargs_)


# end class OrganisationReferenceBaseType

class DataProviderReferenceType(OrganisationReferenceBaseType):
    """DataProviderReferenceType is a dim_type for referencing a data provider. It
    consists of a URN and/or a complete set of reference fields."""
    __hash__ = OrganisationReferenceBaseType.__hash__
    subclass = None
    superclass = OrganisationReferenceBaseType

    def __init__(self, Ref=None, URN=None, gds_collector_=None):
        super(DataProviderReferenceType, self).__init__(Ref, URN, gds_collector_)
        self._name = 'ItemReferenceType'

    @staticmethod
    def factory(*args_, **kwargs_):
        return DataProviderReferenceType(*args_, **kwargs_)

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Ref':
            obj_ = DataProviderRefType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._ref = obj_
            obj_.original_tag_name_ = 'Ref'

        elif nodeName_ == 'URN':
            value_ = child_.text
            value_ = self.gds_parse_string(value_)
            value_ = self.gds_validate_string(value_)
            self._urn = value_

            # end class DataProviderReferenceType


class RefIDType(DataParser):
    def __init__(self, gds_collector_=None):
        super().__init__(gds_collector_)
        self._id = None

    @staticmethod
    def factory(*args_, **kwargs_):
        return RefIDType(*args_, **kwargs_)

    @property
    def id(self):
        return self._id

    def build_attributes(self, node, attrs, already_processed):
        value = find_attr_value_('id', node)
        if value is not None and 'id' not in already_processed:
            already_processed.add('id')
            self._id = value


class RelationshipRefType(DataParser):
    def __init__(self, gds_collector_=None):
        super().__init__(gds_collector_)
        self._ref = None

    @staticmethod
    def factory(*args_, **kwargs_):
        return RelationshipRefType(*args_, **kwargs_)

    @property
    def ref(self):
        return self._ref

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Ref':
            obj_ = RefIDType.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self._ref = obj_.id


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
        self.parent_object_ = kwargs_.get('parent_object_')
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
        return RefBaseType(*args_, **kwargs_)

    @property
    def agencyID(self):
        return self._agencyID

    @agencyID.setter
    def agencyID(self, value):
        self._agencyID = value

    @property
    def maintainableParentID(self):
        return self._maintainableParentID

    @maintainableParentID.setter
    def maintainableParentID(self, value):
        self._maintainableParentID = value

    @property
    def maintainableParentVersion(self):
        return self._maintainableParentVersion

    @maintainableParentVersion.setter
    def maintainableParentVersion(self, value):
        self._maintainableParentVersion = value

    @property
    def containerID(self):
        return self._containerID

    @containerID.setter
    def containerID(self, value):
        self._containerID = value

    @property
    def id_(self):
        return self._id

    @id_.setter
    def id_(self, value):
        self._id = value

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value):
        self._version = value

    @property
    def local(self):
        return self._local

    @local.setter
    def local(self, value):
        self._local = value

    @property
    def class_(self):
        return self._class_

    @class_.setter
    def class_(self, value):
        self._class_ = value

    @property
    def package(self):
        return self._package

    @package.setter
    def package(self, value):
        self._package = value

    def validate_object_type_code_list_type(self, value):
        # Validate dim_type ObjectTypeCodelistType, a restriction on xs:string.
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
        # Validate dim_type PackageTypeCodelistType, a restriction on xs:string.
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
            self.validate_object_type_code_list_type(self._class_)  # validate dim_type ObjectTypeCodelistType

        value = find_attr_value_('package', node)
        if value is not None and 'package' not in already_processed:
            already_processed.add('package')
            self._package = value
            self.validate_package_type_code_list_type(self._package)  # validate dim_type PackageTypeCodelistType


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

    @staticmethod
    def factory(*args_, **kwargs_):
        return MaintainableRefBaseType(*args_, **kwargs_)

    def validate_object_type_code_list_type(self, value):
        # Validate dim_type MaintainableTypeCodelistType, a restriction on ObjectTypeCodelistType.
        result = True

        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{value}":{lineno} is not of the correct base simple dim_type (str)')
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
                    f'Value "{encode_str_2_3(value)}":{lineno} does not match xsd enumeration restriction')
                result = False

        return result

    def validate_package_type_code_list_type(self, value):
        # Validate dim_type PackageTypeCodelistType, a restriction on xs:string.
        result = True

        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{value}":{lineno} is not of the correct base simple dim_type (str)')
                result = False

            value = value
            enumerations = ['base', 'datastructure', 'metadatastructure', 'process', 'registry', 'mapping', 'codelist',
                            'categoryscheme', 'conceptscheme']

            if value not in enumerations:
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{encode_str_2_3(value)}":{lineno} does not match xsd enumeration restriction')
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

    @staticmethod
    def factory(*args_, **kwargs_):
        return StructureOrUsageRefBaseType(*args_, **kwargs_)

    def validate_object_type_code_list_type(self, value):
        # Validate dim_type StructureOrUsageTypeCodelistType, a restriction on MaintainableTypeCodelistType.
        result = True

        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{value}":{lineno} is not of the correct base simple dim_type (str)')
                result = False

            value = value
            enumerations = ['Dataflow', 'DataStructure', 'Metadataflow', 'MetadataStructure']

            if value not in enumerations:
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{encode_str_2_3(value)}":{lineno} does not match xsd enumeration restriction')
                result = False

        return result

    def validate_package_type_code_list_type(self, value):
        # Validate dim_type StructurePackageTypeCodelistType, a restriction on PackageTypeCodelistType.
        result = True

        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{value}":{lineno} is not of the correct base simple dim_type (str)')
                result = False

            value = value
            enumerations = ['datastructure', 'metadatastructure']

            if value not in enumerations:
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{encode_str_2_3(value)}":{lineno} does not match xsd enumeration restriction')
                result = False

        return result


class StructureRefBaseType(StructureOrUsageRefBaseType):
    """StructureRefBaseType is an abstract base dim_type for referencing a
    structure."""
    __hash__ = StructureOrUsageRefBaseType.__hash__
    subclass = None
    superclass = StructureOrUsageRefBaseType

    def __init__(self, agencyID=None, maintainableParentID=None, maintainableParentVersion=None, containerID=None,
                 idx=None, version=None, local=None, class_=None, package=None, gds_collector_=None, **kwargs_):
        super(StructureOrUsageRefBaseType, self).__init__(agencyID, maintainableParentID, maintainableParentVersion,
                                                          containerID, idx, version, local, class_, package,
                                                          gds_collector_, **kwargs_)
        self._name = 'StructureRefBaseType'

    @staticmethod
    def factory(*args_, **kwargs_):
        return StructureRefBaseType(*args_, **kwargs_)


class DataStructureRefType(StructureRefBaseType):
    """DataStructureRefType contains a set of reference fields for a data
    structure definition."""
    __hash__ = StructureRefBaseType.__hash__
    subclass = None
    superclass = StructureRefBaseType

    def __init__(self, agencyID=None, maintainableParentID=None, maintainableParentVersion=None, containerID=None,
                 id_=None, version=None, local=None, class_=None, package=None, gds_collector_=None, **kwargs_):
        super(DataStructureRefType, self).__init__(agencyID, maintainableParentID, maintainableParentVersion,
                                                   containerID, id_, version, local, class_, package, gds_collector_,
                                                   **kwargs_)
        self._name = 'DataStructureRefType'

    @staticmethod
    def factory(*args_, **kwargs_):
        return DataStructureRefType(*args_, **kwargs_)

    def validate_object_type_code_list_type(self, value):
        # Validate dim_type StructureTypeCodelistType, a restriction on StructureOrUsageTypeCodelistType.
        result = True
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{value}":{lineno} is not of the correct base simple dim_type (str)')
                return False

            value = value
            enumerations = ['DataStructure', 'MetadataStructure']

            if value not in enumerations:
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{encode_str_2_3(value)}":{lineno} does not match xsd enumeration restriction')
                result = False

        return result

    def validate_package_type_code_list_type(self, value):
        # Validate dim_type StructurePackageTypeCodelistType, a restriction on PackageTypeCodelistType.
        result = True
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{value}":{lineno} is not of the correct base simple dim_type (str)')
                return False

            value = value
            enumerations = ['datastructure', 'metadatastructure']

            if value not in enumerations:
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{encode_str_2_3(value)}":{lineno} does not match xsd enumeration restriction')
                result = False

        return result


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

    @staticmethod
    def factory(*args_, **kwargs_):
        return StructureUsageRefBaseType(*args_, **kwargs_)

    def validate_object_type_code_list_type(self, value):
        # Validate dim_type StructureUsageTypeCodelistType, a restriction on StructureOrUsageTypeCodelistType.
        result = True
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{value}":{lineno} is not of the correct base simple dim_type (str)')
                result = False
            value = value

            enumerations = ['Dataflow', 'Metadataflow']
            if value not in enumerations:
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{encode_str_2_3(value)}":{lineno} does not match xsd enumeration restriction')
                result = False

        return result

    def validate_package_type_code_list_type(self, value):
        # Validate dim_type StructurePackageTypeCodelistType, a restriction on PackageTypeCodelistType.
        result = True
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{value}":{lineno} is not of the correct base simple dim_type (str)')
                result = False

            value = value
            enumerations = ['datastructure', 'metadatastructure']

            if value not in enumerations:
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{encode_str_2_3(value)}":{lineno} does not match xsd enumeration restriction')
                result = False

        return result


class DataflowRefType(StructureUsageRefBaseType):
    """DataflowRefType contains a set of reference fields for a data flow."""
    __hash__ = StructureUsageRefBaseType.__hash__
    subclass = None
    superclass = StructureUsageRefBaseType

    def __init__(self, agencyID=None, maintainableParentID=None, maintainableParentVersion=None, containerID=None,
                 id_=None, version=None, local=None, class_=None, package=None, gds_collector_=None, **kwargs_):
        super(DataflowRefType, self).__init__(agencyID, maintainableParentID, maintainableParentVersion, containerID,
                                              id_, version, local, class_, package, gds_collector_, **kwargs_)
        self._name = 'DataflowRefType'

    @staticmethod
    def factory(*args_, **kwargs_):
        return DataflowRefType(*args_, **kwargs_)

    def validate_object_type_code_list_type(self, value):
        # Validate dim_type StructureUsageTypeCodelistType, a restriction on StructureOrUsageTypeCodelistType.
        result = True
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{value}":{lineno} is not of the correct base simple dim_type (str)')
                return False

            value = value
            enumerations = ['Dataflow', 'Metadataflow']

            if value not in enumerations:
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{encode_str_2_3(value)}":{lineno} does not match xsd enumeration restriction')
                result = False

        return result

    def validate_package_type_code_list_type(self, value):
        # Validate dim_type StructurePackageTypeCodelistType, a restriction on PackageTypeCodelistType.
        result = True
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{value}":{lineno} is not of the correct base simple dim_type (str)')
                return False

            value = value
            enumerations = ['datastructure', 'metadatastructure']

            if value not in enumerations:
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{encode_str_2_3(value)}":{lineno} does not match xsd enumeration restriction')
                result = False

        return result


class ProvisionAgreementRefType(MaintainableRefBaseType):
    """ProvisionAgreementRefType contains a set of reference fields for a
    provision agreement."""
    __hash__ = MaintainableRefBaseType.__hash__
    subclass = None
    superclass = MaintainableRefBaseType

    def __init__(self, agencyID=None, maintainableParentID=None, maintainableParentVersion=None, containerID=None,
                 id_=None, version=None, local=None, class_=None, package=None, gds_collector_=None, **kwargs_):
        super(ProvisionAgreementRefType, self).__init__(agencyID, maintainableParentID, maintainableParentVersion,
                                                        containerID, id_, version, local, class_, package,
                                                        gds_collector_, **kwargs_)
        self._name = 'ProvisionAgreementRefType'

    @staticmethod
    def factory(*args_, **kwargs_):
        return ProvisionAgreementRefType(*args_, **kwargs_)

    def validate_object_type_code_list_type(self, value):
        # Validate dim_type MaintainableTypeCodelistType, a restriction on ObjectTypeCodelistType.
        result = True
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{value}":{lineno} is not of the correct base simple dim_type (str)')
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
                    f'Value "{encode_str_2_3(value)}":{lineno} does not match xsd enumeration restriction')
                result = False

        return result

    def validate_package_type_code_list_type(self, value):
        # Validate dim_type PackageTypeCodelistType, a restriction on xs:string.
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


class ChildObjectRefBaseType(RefBaseType):
    """ChildObjectRefBaseType is an abstract base dim_type for referencing any
    child object defined directly within a maintainable object."""
    __hash__ = RefBaseType.__hash__
    subclass = None
    superclass = RefBaseType

    def __init__(self, agencyID=None, maintainableParentID=None, maintainableParentVersion=None, containerID=None,
                 id_=None, version=None, local=None, class_=None, package=None, gds_collector_=None, **kwargs_):
        super(ChildObjectRefBaseType, self).__init__(agencyID, maintainableParentID, maintainableParentVersion,
                                                     containerID, id_, version, local, class_, package,
                                                     gds_collector_, **kwargs_)
        self._namespacedef = 'xmlns:message="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message"'
        self._name = 'ChildObjectRefBaseType'

    @staticmethod
    def factory(*args_, **kwargs_):
        return ChildObjectRefBaseType(*args_, **kwargs_)

    def validate_object_type_code_list_type(self, value):
        # Validate dim_type ObjectTypeCodelistType, a restriction on xs:string.
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
        # Validate dim_type PackageTypeCodelistType, a restriction on xs:string.
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
                 id_=None, version=None, local=None, class_=None, package=None, gds_collector_=None, **kwargs_):
        super(ItemRefBaseType, self).__init__(agencyID, maintainableParentID, maintainableParentVersion, containerID,
                                              id_, version, local, class_, package, gds_collector_, **kwargs_)
        self._namespacedef = 'xmlns:message="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message"'
        self._name = 'ItemRefBaseType'

    @staticmethod
    def factory(*args_, **kwargs_):
        return ItemRefBaseType(*args_, **kwargs_)

    def validate_object_type_code_list_type(self, value):
        # Validate dim_type ItemTypeCodelistType, a restriction on ObjectTypeCodelistType.
        result = True
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{value}":{lineno} is not of the correct base simple dim_type (str)')
                return False

            value = value
            enumerations = ['Agency', 'Category', 'Code', 'Concept', 'DataConsumer', 'DataProvider', 'OrganisationUnit',
                            'ReportingCategory']

            if value not in enumerations:
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{encode_str_2_3(value)}":{lineno} does not match xsd enumeration restriction')
                result = False

        return result

    def validate_package_type_code_list_type(self, value):
        # Validate dim_type ItemSchemePackageTypeCodelistType, a restriction on PackageTypeCodelistType.
        result = True
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{value}":{lineno} is not of the correct base simple dim_type (str)')
                return False

            value = value
            enumerations = ['base', 'codelist', 'categoryscheme', 'conceptscheme']

            if value not in enumerations:
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{encode_str_2_3(value)}":{lineno} does not match xsd enumeration restriction')
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
                 id_=None, version=None, local=None, class_=None, package=None, gds_collector_=None, **kwargs_):
        super(OrganisationRefBaseType, self).__init__(agencyID, maintainableParentID, maintainableParentVersion,
                                                      containerID, id_, version, local, class_, package,
                                                      gds_collector_, **kwargs_)
        self._name = 'ItemRefBaseType'

    @staticmethod
    def factory(*args_, **kwargs_):
        return OrganisationRefBaseType(*args_, **kwargs_)

    def validate_object_type_code_list_type(self, value):
        # Validate dim_type OrganisationTypeCodelistType, a restriction on ItemTypeCodelistType.
        result = True

        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{value}":{lineno} is not of the correct base simple dim_type (str)')
                return False

            value = value
            enumerations = ['Agency', 'DataConsumer', 'DataProvider', 'OrganisationUnit']

            if value not in enumerations:
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{encode_str_2_3(value)}":{lineno} does not match xsd enumeration restriction')
                result = False

        return result

    def validate_package_type_code_list_type(self, value):
        # Validate dim_type ItemSchemePackageTypeCodelistType, a restriction on PackageTypeCodelistType.
        result = True
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{value}":{lineno} is not of the correct base simple dim_type (str)')
                return False

            value = value
            enumerations = ['base', 'codelist', 'categoryscheme', 'conceptscheme']

            if value not in enumerations:
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{encode_str_2_3(value)}":{lineno} does not match xsd enumeration restriction')
                result = False

        return result


class DataProviderRefType(OrganisationRefBaseType):
    """DataProviderRefType contains a set of reference fields for referencing a
    data provider within a data provider scheme."""
    __hash__ = OrganisationRefBaseType.__hash__
    subclass = None
    superclass = OrganisationRefBaseType

    def __init__(self, agencyID=None, maintainableParentID=None, maintainableParentVersion=None, containerID=None,
                 id_=None, version=None, local=None, class_=None, package=None, gds_collector_=None, **kwargs_):
        super(DataProviderRefType, self).__init__(agencyID, maintainableParentID, maintainableParentVersion,
                                                  containerID, id_, version, local, class_, package,
                                                  gds_collector_, **kwargs_)
        self._name = 'DataProviderRefType'

    @staticmethod
    def factory(*args_, **kwargs_):
        return DataProviderRefType(*args_, **kwargs_)

    def validate_object_type_code_list_type(self, value):
        # Validate dim_type OrganisationTypeCodelistType, a restriction on ItemTypeCodelistType.
        result = True
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{value}":{lineno} is not of the correct base simple dim_type (str)')
                return False

            value = value
            enumerations = ['Agency', 'DataConsumer', 'DataProvider', 'OrganisationUnit']

            if value not in enumerations:
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{encode_str_2_3(value)}":{lineno} does not match xsd enumeration restriction')
                result = False

        return result
