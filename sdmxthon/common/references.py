from .refs import ProvisionAgreementRefType, DataflowRefType, DataStructureRefType, DataProviderRefType
from ..utils.data_parser import DataParser
from ..utils.xml_base import find_attr_value_


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
