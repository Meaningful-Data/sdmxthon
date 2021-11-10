from sdmxthon.model.base import IdentifiableArtefact
from sdmxthon.model.itemScheme import Concept
from sdmxthon.model.representation import Representation
from sdmxthon.model.utils import generic_setter, int_setter
from sdmxthon.utils.handlers import add_indent, export_intern_data, \
    split_unique_id
from sdmxthon.utils.mappings import structureAbbr


class Component(IdentifiableArtefact):
    """ A component is an abstract super class used to define qualitative and
        quantitative data and metadata items that belong to a Component List
        and hence a Structure. Component is refined through its sub-classes."""

    def __init__(self, id_: str = None, uri: str = None, urn: str = None,
                 annotations=None, local_representation: Representation = None,
                 concept_identity: Concept = None):
        super(Component, self).__init__(id_=id_, uri=uri, urn=urn,
                                        annotations=annotations)

        self._local_representation = local_representation
        self._concept_identity = concept_identity

    def __eq__(self, other):
        if isinstance(other, Component):
            return (super(Component, self).__eq__(other) and
                    self.local_representation == other.local_representation and
                    self._concept_identity == other._concept_identity)
        else:
            return False

    def __str__(self):
        return f'<{self.__class__.__name__} - {self.id}>'

    def __unicode__(self):
        return f'<{self.__class__.__name__} - {self.id}>'

    def __repr__(self):
        return f'<{self.__class__.__name__} - {self.id}>'

    @property
    def local_representation(self):
        """Association to the Representation of the Component if this is
        different from the coreRepresentation of the Concept which the
        Component uses (ConceptUsage) """
        return self._local_representation

    @local_representation.setter
    def local_representation(self, value: Representation):
        self._local_representation = generic_setter(value, Representation)

    @property
    def concept_identity(self):
        """Association to a Concept in a Concept Scheme that
            identifies and defines the semantic of the Component"""
        return self._concept_identity

    @concept_identity.setter
    def concept_identity(self, value: Concept):
        self._concept_identity = generic_setter(value, Concept)

    @property
    def representation(self):
        """Extracts the representation from a Component"""
        if self.local_representation is None and self.concept_identity is None:
            return None

        if self.local_representation is not None:
            return self.local_representation

        if isinstance(self.concept_identity, Concept) and \
                self.concept_identity.core_representation is not None:
            return self.concept_identity.core_representation
        else:
            return None

    def _parse_XML(self, indent, head):

        if isinstance(self, TimeDimension):
            head = 'TimeDimension'

        head = f'{structureAbbr}:' + head

        prettyprint = indent != ''

        data = super(Component, self)._to_XML(prettyprint)
        indent = add_indent(indent)
        if isinstance(self, Dimension):
            outfile = f'{indent}<{head}{data["Attributes"]} ' \
                      f'position="{self._position}">'
        elif isinstance(self, Attribute):
            outfile = f'{indent}<{head}{data["Attributes"]} ' \
                      f'assignmentStatus="{self._usageStatus}">'
        else:
            outfile = f'{indent}<{head}{data["Attributes"]}>'
        outfile += export_intern_data(data, indent)

        indent_child = add_indent(indent)

        if self.concept_identity is not None:
            indent_ref = add_indent(indent_child)
            outfile += f'{indent_child}<{structureAbbr}:ConceptIdentity>'

            if isinstance(self.concept_identity, dict):
                agencyID, id_, version = \
                    split_unique_id(self.concept_identity['CS'])

                outfile += f'{indent_ref}<Ref maintainableParentID="{id_}" ' \
                           f'package="conceptscheme" ' \
                           f'maintainableParentVersion="{version}" ' \
                           f'agencyID="{agencyID}" ' \
                           f'id="{self.concept_identity["CON"]}" ' \
                           f'class="Concept"/>'

            else:
                outfile += f'{indent_ref}<Ref ' \
                           f'maintainableParentID=' \
                           f'"{self.concept_identity.scheme.id}" ' \
                           f'package="conceptscheme" ' \
                           f'maintainableParentVersion=' \
                           f'"{self.concept_identity.scheme.version}" ' \
                           f'agencyID=' \
                           f'"{self.concept_identity.scheme.agencyID}" ' \
                           f'id="{self.concept_identity.id}" ' \
                           f'class="Concept"/>'

            outfile += f'{indent_child}</{structureAbbr}:ConceptIdentity>'

        if self.local_representation is not None:
            indent_enum = add_indent(indent_child)
            indent_ref = add_indent(indent_enum)
            outfile += f'{indent_child}<{structureAbbr}:LocalRepresentation>'
            if self.local_representation.codelist is not None:
                label_format = 'EnumerationFormat'
                outfile += f'{indent_enum}<{structureAbbr}:Enumeration>'
                if isinstance(self.local_representation.codelist, str):
                    agencyID, id_, version = \
                        split_unique_id(self.local_representation.codelist)

                    outfile += f'{indent_ref}<Ref package="codelist" ' \
                               f'agencyID="{agencyID}" ' \
                               f'id="{id_}" ' \
                               f'version="{version}" class="Codelist"/>'
                else:
                    agencyID = self.local_representation.codelist.agencyID
                    id_ = self.local_representation.codelist.id
                    version = self.local_representation.codelist.version
                    outfile += f'{indent_ref}<Ref package="codelist" ' \
                               f'agencyID="{agencyID}" id="{id_}" ' \
                               f'version="{version}" class="Codelist"/>'

                outfile += f'{indent_enum}</{structureAbbr}:Enumeration>'
            else:
                label_format = 'TextFormat'

            format_attributes = ' '

            if self.local_representation.type_ is not None:
                format_attributes = f' textType=' \
                                    f'"{self.local_representation.type_}"'

            if self.local_representation.facets is not None:
                for e in self.local_representation.facets:
                    format_attributes += f' {e.facet_type}="{e.facet_value}"'

            outfile += f'{indent_enum}<{structureAbbr}:' \
                       f'{label_format}{format_attributes}/>'

            outfile += f'{indent_child}</{structureAbbr}:LocalRepresentation>'

            if isinstance(self, Attribute):
                outfile += f'{indent_child}<{structureAbbr}:' \
                           f'AttributeRelationship>'

                if isinstance(self.related_to, dict):
                    if 'id' in self.related_to.keys():

                        if isinstance(self.related_to['id'], list):
                            for k in self.related_to['id']:
                                outfile += f'{indent_enum}<{structureAbbr}:' \
                                           f'{self.related_to["type"]}>'
                                outfile += f'{indent_ref}<Ref id="{k}"/>'
                                outfile += f'{indent_enum}</{structureAbbr}:' \
                                           f'{self.related_to["type"]}>'
                        else:
                            outfile += f'{indent_enum}<{structureAbbr}:' \
                                       f'{self.related_to["type"]}>'
                            outfile += f'{indent_ref}<Ref ' \
                                       f'id="{self.related_to["id"]}"/>'
                            outfile += f'{indent_enum}</{structureAbbr}:' \
                                       f'{self.related_to["type"]}>'
                    else:
                        for k in self.related_to:
                            outfile += f'{indent_enum}<{structureAbbr}' \
                                       f':Dimension>'
                            outfile += f'{indent_ref}<Ref id="{k}"/>'
                            outfile += f'{indent_enum}</{structureAbbr}' \
                                       f':Dimension>'
                elif isinstance(self.related_to, Dimension):
                    outfile += f'{indent_enum}<{structureAbbr}:Dimension>'
                    outfile += f'{indent_ref}<Ref id="{self.related_to.id}"/>'
                    outfile += f'{indent_enum}</{structureAbbr}:Dimension>'
                elif isinstance(self.related_to, PrimaryMeasure):
                    outfile += f'{indent_enum}<{structureAbbr}' \
                               f':PrimaryMeasure>'
                    outfile += f'{indent_ref}<Ref id="{self.related_to.id}"/>'
                    outfile += f'{indent_enum}</{structureAbbr}' \
                               f':PrimaryMeasure>'
                else:
                    outfile += f'{indent_enum}<{structureAbbr}:None/>'

                outfile += f'{indent_child}</{structureAbbr}' \
                           f':AttributeRelationship>'

        outfile += f'{indent}</{head}>'
        return outfile


class Dimension(Component):
    """ A metadata concept used (most probably together with other metadata
        concepts) to classify a statistical series, e.g. a statistical concept
        indicating a certain economic activity or a geographical
        reference area."""

    def __init__(self, id_: str = None, uri: str = None, urn: str = None,
                 annotations=None, local_representation: Representation = None,
                 concept_identity: Concept = None,
                 position: int = None):
        super(Dimension, self). \
            __init__(id_=id_, uri=uri, urn=urn,
                     annotations=annotations,
                     local_representation=local_representation,
                     concept_identity=concept_identity)

        self.position = position

    def __eq__(self, other):
        if isinstance(other, Dimension):
            return super(Dimension, self).__eq__(
                other) and self._position == other._position
        else:
            return False

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of Dimension"""
        return Dimension(*args_, **kwargs_)

    @property
    def position(self):
        """Position of the Dimension in the DimensionList"""
        return self._position

    @position.setter
    def position(self, value):
        self._position = int_setter(value)


class TimeDimension(Dimension):
    """A metadata concept that identifies the component in the key structure
       that has the role of “time”.
    """

    def __init__(self, id_: str = None, uri: str = None, urn: str = None,
                 annotations=None,
                 local_representation: Representation = None,
                 concept_identity: Concept = None,
                 position: int = None):
        super(TimeDimension, self). \
            __init__(id_=id_, uri=uri, urn=urn,
                     annotations=annotations,
                     local_representation=local_representation,
                     concept_identity=concept_identity,
                     position=position)

    def __eq__(self, other):
        if isinstance(other, TimeDimension):
            return super(TimeDimension, self).__eq__(other)
        else:
            return False


class Attribute(Component):
    """A characteristic of an object or entity."""

    def __init__(self, id_: str = None, uri: str = None, urn: str = None,
                 annotations=None,
                 local_representation: Representation = None,
                 concept_identity: Concept = None,
                 assignmentStatus: str = None,
                 relatedTo=None):
        super(Attribute, self) \
            .__init__(id_=id_, uri=uri, urn=urn,
                      annotations=annotations,
                      local_representation=local_representation,
                      concept_identity=concept_identity)

        self.assignment_status = assignmentStatus
        self.related_to = relatedTo

    def __eq__(self, other):
        if isinstance(other, Attribute):
            return (super(Attribute, self).__eq__(other) and
                    self._usageStatus == other._usageStatus and
                    self._relatedTo == other._relatedTo)
        else:
            return False

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of Attribute"""
        return Attribute(*args_, **kwargs_)

    @property
    def assignment_status(self):
        """Defines the usage status of the Attribute
        (Mandatory, Conditional)"""
        return self._usageStatus

    @property
    def related_to(self):
        """Association to a AttributeRelationship."""
        return self._relatedTo

    @assignment_status.setter
    def assignment_status(self, value):
        if value in ["Mandatory", "Conditional"] or value is None:
            self._usageStatus = value
        else:
            raise ValueError(
                "The value for usageStatus has to be 'Mandatory' "
                "or 'Conditional'")

    @related_to.setter
    def related_to(self, value):
        if value is None:
            self._relatedTo = "NoSpecifiedRelationship"
        else:
            self._relatedTo = value

class MeasureDimension(Dimension):
    """ A statistical concept that identifies the component in the key
        structure that has an enumerated list of measures. This dimension has,
        as its representation the Concept Scheme that enumerates the
        measure concepts.
    """

    def __init__(self, id_: str = None, uri: str = None, urn: str = None,
                 annotations=None,
                 local_representation: Representation = None,
                 concept_identity: Concept = None,
                 position: int = None):
        super(MeasureDimension, self). \
            __init__(id_=id_, uri=uri, urn=urn,
                     annotations=annotations,
                     local_representation=local_representation,
                     concept_identity=concept_identity,
                     position=position)

    def __eq__(self, other):
        if isinstance(other, MeasureDimension):
            return super(MeasureDimension, self).__eq__(other)
        else:
            return False


class PrimaryMeasure(Component, object):
    """The metadata concept that is the phenomenon to be measured in a
    data set. In a data set the instance of the measure is often called
    the observation."""

    def __init__(self, id_: str = None, uri: str = None, urn: str = None,
                 annotations=None,
                 local_representation: Representation = None,
                 concept_identity: Concept = None):

        super(PrimaryMeasure, self). \
            __init__(id_=id_, uri=uri, urn=urn,
                     annotations=annotations,
                     concept_identity=concept_identity,
                     local_representation=local_representation)

    def __eq__(self, other):
        if isinstance(other, PrimaryMeasure):
            return super(PrimaryMeasure, self).__eq__(other)
        else:
            return False
