from SDMXThon.common.refs import ProvisionAgreementRefType, DataflowRefType, DataStructureRefType, DataProviderRefType
from SDMXThon.utils.data_parser import DataParser, UseCapturedNS_
from SDMXThon.utils.xml_base import showIndent, quote_xml


class ReferenceType(DataParser):
    """ReferenceType is an abstract base type. It is used as the basis for all
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
    urn:sdmx:org.package-name.class-name=agency-id:(maintainable-parent-
    object-id[maintainable-parent-object-version].)?(container-object-
    id.)?object-id([object-version])?."""
    __hash__ = DataParser.__hash__
    subclass = None
    superclass = None

    def __init__(self, Ref=None, URN=None, gds_collector_=None, **kwargs_):
        super(ReferenceType, self).__init__(gds_collector_, **kwargs_)
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self._ref = Ref
        self._ref_nsprefix_ = None
        self._urn = URN
        self._urn_nsprefix_ = None
        self._namespacedef = 'xmlns:common="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common"'
        self._namespaceprefix = "common"
        self.original_tagname_ = 'Ref'

    def factory(*args_, **kwargs_):
        return ReferenceType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def has_content_(self):
        if (self._ref is not None or self._urn is not None):
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

    def export_children(self, outfile, level, pretty_print=True, has_parent=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''

        if self._ref is not None:
            self._ref.export(outfile, level, pretty_print=pretty_print, has_parent=has_parent)

        if self._urn is not None:
            namespaceprefix_ = self._urn_nsprefix_ + ':' if (UseCapturedNS_ and self._urn_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sURN>%s</%sURN>%s' % (
                namespaceprefix_, self.gds_encode(self.gds_format_string(quote_xml(self._urn), input_name='URN')),
                namespaceprefix_, eol_))

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Ref':
            type_name_ = child_.attrib.get('{http://www.w3.org/2001/XMLSchema-instance}type')

            if type_name_ is None:
                type_name_ = child_.attrib.get('type')

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
            value_ = self.gds_parse_string(value_, node, 'URN')
            value_ = self.gds_validate_string(value_, node, 'URN')
            self._urn = value_
            self._urn_nsprefix_ = child_.prefix


# end class ReferenceType

class MaintainableReferenceBaseType(ReferenceType):
    """MaintainableReferenceBaseType is an abstract base type for referencing a
    maintainable object. It consists of a URN and/or a complete set of
    reference fields; agency, id, and version."""
    __hash__ = ReferenceType.__hash__
    subclass = None
    superclass = ReferenceType

    def __init__(self, Ref=None, URN=None, gds_collector_=None, **kwargs_):
        super(MaintainableReferenceBaseType, self).__init__(Ref, URN, gds_collector_, **kwargs_)
        self._name = 'MaintainableReferenceBaseType'

    def factory(*args_, **kwargs_):
        return MaintainableReferenceBaseType(*args_, **kwargs_)

    factory = staticmethod(factory)


# end class MaintainableReferenceBaseType

class StructureReferenceBaseType(MaintainableReferenceBaseType):
    """StructureReferneceBaseType is a specific type of MaintainableReference
    that is used for referencing structure definitions. It consists of a
    URN and/or a complete set of reference fields; agency, id, and
    version."""
    __hash__ = MaintainableReferenceBaseType.__hash__
    subclass = None
    superclass = MaintainableReferenceBaseType

    def __init__(self, Ref=None, URN=None, gds_collector_=None, **kwargs_):
        super(StructureReferenceBaseType, self).__init__(Ref, URN, gds_collector_, **kwargs_)
        self._name = 'MaintainableReferenceBaseType'

    def factory(*args_, **kwargs_):
        return StructureReferenceBaseType(*args_, **kwargs_)

    factory = staticmethod(factory)


# end class StructureReferenceBaseType

class DataStructureReferenceType(StructureReferenceBaseType):
    """DataStructureReferenceType is a type for referencing a data structure
    definition object. It consists of a URN and/or a complete set of
    reference fields."""
    __hash__ = StructureReferenceBaseType.__hash__
    subclass = None
    superclass = StructureReferenceBaseType

    def __init__(self, Ref=None, URN=None, gds_collector_=None, **kwargs_):
        super(DataStructureReferenceType, self).__init__(Ref, URN, gds_collector_, **kwargs_)
        self._name = 'DataStructureReferenceType'

    def factory(*args_, **kwargs_):
        return DataStructureReferenceType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Ref':
            obj_ = DataStructureRefType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._ref = obj_
            obj_.original_tag_name_ = 'Ref'

        elif nodeName_ == 'URN':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'URN')
            value_ = self.gds_validate_string(value_, node, 'URN')
            self._urn = value_
            self._urn_nsprefix_ = child_.prefix
        # end class DataStructureReferenceType


class StructureUsageReferenceBaseType(MaintainableReferenceBaseType):
    """StructureUsageReferenceBaseType is a specific type of
    MaintainableReference that is used for referencing structure usages. It
    consists of a URN and/or a complete set of reference fields; agency,
    id, and version."""
    __hash__ = MaintainableReferenceBaseType.__hash__
    subclass = None
    superclass = MaintainableReferenceBaseType

    def __init__(self, Ref=None, URN=None, gds_collector_=None, **kwargs_):
        super(StructureUsageReferenceBaseType, self).__init__(Ref, URN, gds_collector_, **kwargs_)
        self._name = 'StructureUsageReferenceBaseType'

    def factory(*args_, **kwargs_):
        return StructureUsageReferenceBaseType(*args_, **kwargs_)

    factory = staticmethod(factory)


# end class StructureUsageReferenceBaseType

class DataflowReferenceType(StructureUsageReferenceBaseType):
    """DataflowReferenceType is a type for referencing a dataflow object. It
    consists of a URN and/or a complete set of reference fields."""
    __hash__ = StructureUsageReferenceBaseType.__hash__
    subclass = None
    superclass = StructureUsageReferenceBaseType

    def __init__(self, Ref=None, URN=None, gds_collector_=None, **kwargs_):
        super(DataflowReferenceType, self).__init__(Ref, URN, gds_collector_, **kwargs_)
        self._name = 'DataflowReferenceType'
        self._namespace_prefix = 'common'

    def factory(*args_, **kwargs_):
        return DataflowReferenceType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Ref':
            obj_ = DataflowRefType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._ref = obj_
            obj_.original_tag_name_ = 'Ref'

        elif nodeName_ == 'URN':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'URN')
            value_ = self.gds_validate_string(value_, node, 'URN')
            self._urn = value_
            self._urn_nsprefix_ = child_.prefix

        # end class DataflowReferenceType


class ProvisionAgreementReferenceType(MaintainableReferenceBaseType):
    """ProvisionAgreementReferenceType is a type for referencing a provision
    agreement. It consists of a URN and/or a complete set of reference
    fields."""
    __hash__ = MaintainableReferenceBaseType.__hash__
    subclass = None
    superclass = MaintainableReferenceBaseType

    def __init__(self, Ref=None, URN=None, gds_collector_=None, **kwargs_):
        super(ProvisionAgreementReferenceType, self).__init__(Ref, URN, gds_collector_, **kwargs_)
        self._name = 'ProvisionAgreementReferenceType'

    def factory(*args_, **kwargs_):
        return ProvisionAgreementReferenceType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Ref':
            obj_ = ProvisionAgreementRefType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._ref = obj_
            obj_.original_tag_name_ = 'Ref'

        elif nodeName_ == 'URN':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'URN')
            value_ = self.gds_validate_string(value_, node, 'URN')
            self._urn = value_
            self._urn_nsprefix_ = child_.prefix

        # end class ProvisionAgreementReferenceType


class ChildObjectReferenceType(ReferenceType):
    """ChildObjectReferenceType is an abstract base type used for referencing a
    particular object defined directly within a maintainable object. It
    consists of a URN and/or a complete set of reference fields; agency,
    maintainable id (maintainableParentID), maintainable version
    (maintainableParentVersion), the object id (which can be nested), and
    optionally the object version (if applicable)."""
    __hash__ = ReferenceType.__hash__
    subclass = None
    superclass = ReferenceType

    def __init__(self, Ref=None, URN=None, gds_collector_=None, **kwargs_):
        super(ChildObjectReferenceType, self).__init__(Ref, URN, gds_collector_, **kwargs_)
        self._name = 'ChildObjectReferenceType'

    def factory(*args_, **kwargs_):
        return ChildObjectReferenceType(*args_, **kwargs_)

    factory = staticmethod(factory)


# end class ChildObjectReferenceType

class ItemReferenceType(ChildObjectReferenceType):
    """ItemReferenceType is an abstract base type used for referencing a
    particular item within an item scheme. Note that this reference also
    has the ability to reference items contained within other items inside
    of the item scheme. It consists of a URN and/or a complete set of
    reference fields; agency, scheme id (maintainableParentID), scheme
    version (maintainableParentVersion), and item id (which can be
    nested)."""
    __hash__ = ChildObjectReferenceType.__hash__
    subclass = None
    superclass = ChildObjectReferenceType

    def __init__(self, Ref=None, URN=None, gds_collector_=None, **kwargs_):
        super(ItemReferenceType, self).__init__(Ref, URN, gds_collector_, **kwargs_)
        self._name = 'ItemReferenceType'

    def factory(*args_, **kwargs_):
        return ItemReferenceType(*args_, **kwargs_)

    factory = staticmethod(factory)


# end class ItemReferenceType

class OrganisationReferenceBaseType(ItemReferenceType):
    """OrganisationReferenceBaseType is a type for referencing any organisation
    object, regardless of its type. It consists of a URN and/or a complete
    set of reference fields."""
    __hash__ = ItemReferenceType.__hash__
    subclass = None
    superclass = ItemReferenceType

    def __init__(self, Ref=None, URN=None, gds_collector_=None, **kwargs_):
        super(OrganisationReferenceBaseType, self).__init__(Ref, URN, gds_collector_, **kwargs_)
        self._name = 'ItemReferenceType'

    def factory(*args_, **kwargs_):
        return OrganisationReferenceBaseType(*args_, **kwargs_)

    factory = staticmethod(factory)


# end class OrganisationReferenceBaseType

class DataProviderReferenceType(OrganisationReferenceBaseType):
    """DataProviderReferenceType is a type for referencing a data provider. It
    consists of a URN and/or a complete set of reference fields."""
    __hash__ = OrganisationReferenceBaseType.__hash__
    subclass = None
    superclass = OrganisationReferenceBaseType

    def __init__(self, Ref=None, URN=None, gds_collector_=None, **kwargs_):
        super(DataProviderReferenceType, self).__init__(Ref, URN, gds_collector_, **kwargs_)
        self._name = 'ItemReferenceType'

    def factory(*args_, **kwargs_):
        return DataProviderReferenceType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Ref':
            obj_ = DataProviderRefType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._ref = obj_
            obj_.original_tag_name_ = 'Ref'

        elif nodeName_ == 'URN':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'URN')
            value_ = self.gds_validate_string(value_, node, 'URN')
            self._urn = value_
            self._urn_nsprefix_ = child_.prefix

            # end class DataProviderReferenceType
