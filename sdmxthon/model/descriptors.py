from sdmxthon.model.base import IdentifiableArtefact
from sdmxthon.model.component import Dimension, Attribute, PrimaryMeasure, \
    TimeDimension
from sdmxthon.parsers.data_parser import DataParser
from sdmxthon.parsers.references import RelationshipRefType, RefBaseType
from sdmxthon.utils.handlers import add_indent, export_intern_data


class GroupDimension(DataParser):
    """ Parser of a Dimension in a GroupDimensionDescriptor"""

    def __init__(self, gds_collector=None):
        super(GroupDimension, self).__init__(gds_collector)
        self._ref = None

    def __eq__(self, other):
        if isinstance(other, GroupDimension):
            return super(GroupDimension, self).__eq__(other)
        else:
            return False

    @property
    def ref(self):
        """Reference to the dimension"""
        return self._ref

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of GroupDimension"""
        return GroupDimension(*args_, **kwargs_)

    def _build_children(self, child_, node, nodeName_,
                        fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'DimensionReference':
            obj_ = RelationshipRefType._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._ref = obj_.ref


class ComponentList(IdentifiableArtefact):
    """An abstract definition of a list of components.
       A concrete example is a Dimension Descriptor which defines
       the list of Dimensions in a DataStructure Definition.
    """
    _componentType = None

    def __init__(self, id_: str = None, uri: str = None, urn: str = None,
                 annotations=None, components=None):

        super(ComponentList, self).__init__(id_=id_, uri=uri, urn=urn,
                                            annotations=annotations)
        self._components = {}
        if components is not None:
            for c in components.values():
                self.add_component(c)

    def __eq__(self, other):
        if isinstance(other, ComponentList):
            return (super(ComponentList, self).__eq__(other) and
                    self._components == other._components)
        else:
            return False

    def __str__(self):
        return f'<{self.__class__.__name__} - {self.id}>'

    def __unicode__(self):
        return f'<{self.__class__.__name__} - {self.id}>'

    def __repr__(self):
        return f'<{self.__class__.__name__} - {self.id}>'

    @property
    def components(self):
        """An aggregate association to one or more components
        which make up the list."""
        return self._components

    def add_component(self, value):
        """Method to add a Component to the ComponentList"""
        if isinstance(self, MeasureDescriptor) and len(self._components) == 1:
            raise ValueError('Measure Descriptor cannot have '
                             'more than one Primary Measure')
        elif isinstance(value, (Dimension, Attribute, PrimaryMeasure)):
            value.componentList = self
            self._components[value.id] = value
        elif isinstance(value, GroupDimension):
            value.componentList = self
            self._components[value.ref] = value
        else:
            raise TypeError(
                f"The object has to be of the dim_type "
                f"[Dimension, Attribute, PrimaryMeasure], "
                f"{value.__class__.__name__} provided")

    def __len__(self):
        return len(self.components)

    def __getitem__(self, value):
        return self.components[value]

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(ComponentList, self)._build_attributes(node, attrs,
                                                     already_processed)

    def _parse_XML(self, indent, label):
        prettyprint = indent != ''

        indent = add_indent(indent)

        data = super(ComponentList, self)._to_XML(prettyprint)

        outfile = ''

        attributes = data.get('Attributes') or None

        if attributes is not None:
            outfile += f'{indent}<{label}{attributes}>'
        else:
            outfile += f'{indent}<{label}>'

        outfile += export_intern_data(data, indent)

        for i in self.components.values():
            outfile += i._parse_XML(indent, self._componentType)

        outfile += f'{indent}</{label}>'

        return outfile


class DimensionDescriptor(ComponentList, DataParser):
    """An ordered set of metadata concepts that, combined, classify a
    statistical series, and whose values, when combined (the key) in an
    instance such as a data set, uniquely identify a specific observation
    """
    _componentType = "Dimension"

    def __init__(self, id_: str = None, uri: str = None, urn: str = None,
                 annotations=None, components=None):

        if components is None:
            components = {}
        super(DimensionDescriptor, self).__init__(id_=id_, uri=uri, urn=urn,
                                                  annotations=annotations,
                                                  components=components)

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of DimensionDescriptor"""
        return DimensionDescriptor(*args_, **kwargs_)

    def __eq__(self, other):
        if isinstance(other, DimensionDescriptor):
            return super(DimensionDescriptor, self).__eq__(other)
        else:
            return False

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(DimensionDescriptor, self). \
            _build_attributes(node, attrs, already_processed)

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False,
                        gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'Dimension':
            obj_ = Dimension._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self.add_component(obj_)
        elif nodeName_ == 'TimeDimension':
            obj_ = TimeDimension._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self.add_component(obj_)


class AttributeDescriptor(ComponentList, DataParser):
    """A set metadata concepts that define the attributes of a
    Data Structure Definition."""

    _componentType = "Attribute"

    def __init__(self, id_: str = None, uri: str = None, urn: str = None,
                 annotations=None, components=None):
        if components is None:
            components = {}

        super(AttributeDescriptor, self).__init__(id_=id_, uri=uri, urn=urn,
                                                  annotations=annotations,
                                                  components=components)

    @staticmethod
    def _factory(*args_, **kwargs_):

        """Factory Method of AttributeDescriptor"""
        return AttributeDescriptor(*args_, **kwargs_)

    def __eq__(self, other):
        if isinstance(other, AttributeDescriptor):
            return super(AttributeDescriptor, self).__eq__(other)
        else:
            return False

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(AttributeDescriptor, self). \
            _build_attributes(node, attrs, already_processed)

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False,
                        gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'Attribute':
            obj_ = Attribute._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self.add_component(obj_)


class MeasureDescriptor(ComponentList, DataParser):
    """A metadata concept that defines the measure of a
    Data Structure Definition"""

    _componentType = "PrimaryMeasure"

    def __init__(self, id_: str = None, uri: str = None, urn: str = None,
                 annotations=None, components=None):

        if components is None:
            components = {}
        super(MeasureDescriptor, self).__init__(id_=id_, uri=uri, urn=urn,
                                                annotations=annotations,
                                                components=components)

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of MeasureDescriptor"""
        return MeasureDescriptor(*args_, **kwargs_)

    def __eq__(self, other):
        if isinstance(other, MeasureDescriptor):
            return super(MeasureDescriptor, self).__eq__(other)
        else:
            return False

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(MeasureDescriptor, self). \
            _build_attributes(node, attrs, already_processed)

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False,
                        gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'PrimaryMeasure':
            obj_ = PrimaryMeasure._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self.add_component(obj_)


class GroupDimensionDescriptor(ComponentList, DataParser):
    """A set metadata concepts that define a partial key derived from the
    Dimension Descriptor in a Data Structure Definition.
    """

    _componentType = "Dimension"

    def __init__(self, id_: str = None, uri: str = None, urn: str = None,
                 annotations=None, components=None):
        if components is None:
            components = {}
        super(GroupDimensionDescriptor, self). \
            __init__(id_=id_, uri=uri, urn=urn,
                     annotations=annotations, components=components)

    def __eq__(self, other):
        if isinstance(other, GroupDimensionDescriptor):
            return super(GroupDimensionDescriptor, self).__eq__(other)
        else:
            return False

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of GroupDimensionDescriptor"""
        return GroupDimensionDescriptor(*args_, **kwargs_)

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(GroupDimensionDescriptor, self). \
            _build_attributes(node, attrs, already_processed)

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False,
                        gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'GroupDimension':
            obj_ = GroupDimension._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self.add_component(obj_)


class StructureType(DataParser):
    """Parser of the Structure of a DataFlowDefinition"""

    def __init__(self, gds_collector_=None):
        super().__init__(gds_collector_)
        self._ref = None

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of Structure"""
        return StructureType(*args_, **kwargs_)

    @property
    def ref(self):
        """Reference to the DataStructureDefinition"""
        return self._ref

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False,
                        gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'Ref':
            obj_ = RefBaseType._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._ref = f"{obj_.agencyID}:{obj_.id_}({obj_.version})"


class DataStructureComponentType(DataParser):
    """Parser of the DataStructureComponent XML element"""

    def __init__(self, gds_collector_=None):
        super().__init__(gds_collector_)
        self._measure_descriptor = None
        self._attribute_descriptor = None
        self._dimension_descriptor = None
        self._groupDimensionDescriptor = None

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of DataStructureComponentType"""
        return DataStructureComponentType(*args_, **kwargs_)

    @property
    def dimensionDescriptor(self):
        """An ordered set of metadata concepts that, combined, classify a
        statistical series, and whose values, when combined (the key) in an
        instance such as a data set, uniquely identify a specific
        observation """
        return self._dimension_descriptor

    @property
    def attributeDescriptor(self):
        """A set metadata concepts that define the attributes of a Data
        Structure Definition. """
        return self._attribute_descriptor

    @property
    def measureDescriptor(self):
        """A metadata concept that defines the measure of a Data Structure
        Definition """
        return self._measure_descriptor

    @property
    def groupDimensionDescriptor(self):
        """A set metadata concepts that define a partial key derived
           from the Dimension Descriptor in a Data Structure Definition."""
        return self._groupDimensionDescriptor

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False,
                        gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'DimensionList':
            obj_ = DimensionDescriptor._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._dimension_descriptor = obj_
        elif nodeName_ == 'AttributeList':
            obj_ = AttributeDescriptor._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._attribute_descriptor = obj_
        elif nodeName_ == 'MeasureList':
            obj_ = MeasureDescriptor._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._measure_descriptor = obj_
        elif nodeName_ == 'Group':
            obj_ = GroupDimensionDescriptor._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._groupDimensionDescriptor = obj_
