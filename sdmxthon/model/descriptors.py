from sdmxthon.model.base import IdentifiableArtefact
from sdmxthon.model.component import Attribute, Dimension, PrimaryMeasure
from sdmxthon.parsers.writer_aux import add_indent, export_intern_data


class GroupDimension(object):
    """ Parser of a Dimension in a GroupDimensionDescriptor"""

    def __init__(self):
        self._ref = None

    def __eq__(self, other):
        if isinstance(other, GroupDimension):
            return super(GroupDimension, self).__eq__(other)

        return False

    @property
    def ref(self):
        """Reference to the dimension"""
        return self._ref


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
        if isinstance(value, (Dimension, Attribute, PrimaryMeasure)):
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


class DimensionDescriptor(ComponentList, object):
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

    def __eq__(self, other):
        if isinstance(other, DimensionDescriptor):
            return super(DimensionDescriptor, self).__eq__(other)

        return False


class AttributeDescriptor(ComponentList, object):
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

    def __eq__(self, other):
        if isinstance(other, AttributeDescriptor):
            return super(AttributeDescriptor, self).__eq__(other)

        return False


class MeasureDescriptor(ComponentList, object):
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

    def __eq__(self, other):
        if isinstance(other, MeasureDescriptor):
            return super(MeasureDescriptor, self).__eq__(other)

        return False


