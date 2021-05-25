from SDMXThon.model.base import IdentifiableArtefact
from SDMXThon.model.itemScheme import Concept
from SDMXThon.model.representation import Representation
from SDMXThon.model.utils import generic_setter, int_setter
from SDMXThon.parsers.data_parser import DataParser
from SDMXThon.parsers.references import RelationshipRefType, RefBaseType
from SDMXThon.utils.handlers import add_indent, export_intern_data, \
    split_unique_id
from SDMXThon.utils.mappings import structureAbbr
from SDMXThon.utils.xml_base import find_attr_value_


class Component(IdentifiableArtefact):
    """ A component is an abstract super class used to define qualitative and
        quantitative data and metadata items that belong to a Component List
        and hence a Structure. Component is refined through its sub-classes."""

    def __init__(self, id_: str = None, uri: str = None, urn: str = None,
                 annotations=None, localRepresentation: Representation = None):
        super(Component, self).__init__(id_=id_, uri=uri, urn=urn,
                                        annotations=annotations)

        self._local_representation = localRepresentation
        self._concept_identity = None

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

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(Component, self)._build_attributes(node,
                                                 attrs,
                                                 already_processed)

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False,
                        gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'ConceptIdentity':
            obj_ = ConceptIdentityType._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._concept_identity = obj_.ref
        elif nodeName_ == 'LocalRepresentation':
            obj_ = Representation._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self.local_representation = obj_

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


class Dimension(Component, DataParser):
    """ A metadata concept used (most probably together with other metadata
        concepts) to classify a statistical series, e.g. a statistical concept
        indicating a certain economic activity or a geographical
        reference area."""

    def __init__(self, id_: str = None, uri: str = None, urn: str = None,
                 annotations=None, localRepresentation: Representation = None,
                 position: int = None):
        super(Dimension, self). \
            __init__(id_=id_, uri=uri, urn=urn,
                     annotations=annotations,
                     localRepresentation=localRepresentation)

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

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(Dimension, self)._build_attributes(node, attrs,
                                                 already_processed)

        value = find_attr_value_('position', node)
        if value is not None and 'position' not in already_processed:
            already_processed.add('position')
            self.position = value

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False,
                        gds_collector_=None):
        """Builds the childs of the XML element"""
        super(Dimension, self)._build_children(child_, node, nodeName_,
                                               fromsubclass_=False,
                                               gds_collector_=None)


class TimeDimension(Dimension, DataParser):
    """A metadata concept that identifies the component in the key structure
       that has the role of “time”.
    """

    def __init__(self, id_: str = None, uri: str = None, urn: str = None,
                 annotations=None,
                 localRepresentation: Representation = None,
                 position: int = None):
        super(TimeDimension, self). \
            __init__(id_=id_, uri=uri, urn=urn,
                     annotations=annotations,
                     localRepresentation=localRepresentation,
                     position=position)

    def __eq__(self, other):
        if isinstance(other, TimeDimension):
            return super(TimeDimension, self).__eq__(other)
        else:
            return False

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of TimeDimension"""
        return TimeDimension(*args_, **kwargs_)

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(TimeDimension, self) \
            ._build_attributes(node, attrs, already_processed)

    def _build_children(self, child_, node, nodeName_,
                        fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        super(TimeDimension, self) \
            ._build_children(child_, node, nodeName_,
                             fromsubclass_=False,
                             gds_collector_=None)


class Attribute(Component, DataParser):
    """A characteristic of an object or entity."""

    def __init__(self, id_: str = None, uri: str = None, urn: str = None,
                 annotations=None,
                 localRepresentation: Representation = None,
                 usageStatus: str = None, relatedTo=None):
        super(Attribute, self) \
            .__init__(id_=id_, uri=uri, urn=urn,
                      annotations=annotations,
                      localRepresentation=localRepresentation)

        self.usage_status = usageStatus
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
    def usage_status(self):
        """Defines the usage status of the Attribute
        (Mandatory, Conditional)"""
        return self._usageStatus

    @property
    def related_to(self):
        """Association to a AttributeRelationship."""
        return self._relatedTo

    @usage_status.setter
    def usage_status(self, value):
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

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(Attribute, self)._build_attributes(node, attrs,
                                                 already_processed)

        value = find_attr_value_('assignmentStatus', node)
        if value is not None and 'assignmentStatus' not in already_processed:
            already_processed.add('assignmentStatus')
            self.usage_status = value

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False,
                        gds_collector_=None):
        """Builds the childs of the XML element"""
        super(Attribute, self)._build_children(child_, node, nodeName_,
                                               fromsubclass_=False,
                                               gds_collector_=None)

        if nodeName_ == 'AttributeRelationship':
            obj_ = AttributeRelationshipType._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            if obj_.ref_id is None:
                self.related_to = None
            else:
                self.related_to = {'id': obj_.ref_id, 'type': obj_.ref_type}


class MeasureDimension(Dimension, DataParser):
    """ A statistical concept that identifies the component in the key
        structure that has an enumerated list of measures. This dimension has,
        as its representation the Concept Scheme that enumerates the
        measure concepts.
    """

    def __init__(self, id_: str = None, uri: str = None, urn: str = None,
                 annotations=None,
                 localRepresentation: Representation = None,
                 position: int = None):
        super(MeasureDimension, self). \
            __init__(id_=id_, uri=uri, urn=urn,
                     annotations=annotations,
                     localRepresentation=localRepresentation,
                     position=position)

    def __eq__(self, other):
        if isinstance(other, MeasureDimension):
            return super(MeasureDimension, self).__eq__(other)
        else:
            return False

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of MeasureDimension"""
        return MeasureDimension(*args_, **kwargs_)

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(MeasureDimension, self)._build_attributes(node, attrs,
                                                        already_processed)

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False,
                        gds_collector_=None):
        """Builds the childs of the XML element"""
        super(MeasureDimension, self)._build_children(child_, node, nodeName_,
                                                      fromsubclass_=False,
                                                      gds_collector_=None)


class PrimaryMeasure(Component, DataParser):
    """The metadata concept that is the phenomenon to be measured in a
    data set. In a data set the instance of the measure is often called
    the observation."""

    def __init__(self, id_: str = None, uri: str = None, urn: str = None,
                 annotations=None,
                 localRepresentation: Representation = None):

        super(PrimaryMeasure, self). \
            __init__(id_=id_, uri=uri, urn=urn,
                     annotations=annotations,
                     localRepresentation=localRepresentation)

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of PrimaryMeasure"""
        return PrimaryMeasure(*args_, **kwargs_)

    def __eq__(self, other):
        if isinstance(other, PrimaryMeasure):
            return super(PrimaryMeasure, self).__eq__(other)
        else:
            return False

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(PrimaryMeasure, self)._build_attributes(node, attrs,
                                                      already_processed)

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False,
                        gds_collector_=None):
        """Builds the childs of the XML element"""
        super(PrimaryMeasure, self)._build_children(child_, node, nodeName_,
                                                    fromsubclass_=False,
                                                    gds_collector_=None)


class AttributeRelationshipType(DataParser):
    """Parser of the Attribute Relationship"""

    def __init__(self, gds_collector_=None):
        super().__init__(gds_collector_)
        self._ref_id = None
        self._ref_type = None

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of AttributeRelationshipType"""
        return AttributeRelationshipType(*args_, **kwargs_)

    @property
    def ref_id(self):
        """ID of the component referenced"""
        return self._ref_id

    @property
    def ref_type(self):
        """Type of the component referenced (Dimension, PrimaryMeasure)"""
        return self._ref_type

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False,
                        gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'None':
            self._ref_id = None
            self._ref_type = None
        elif nodeName_ == 'PrimaryMeasure':
            obj_ = RelationshipRefType._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._ref_id = obj_.ref
            self._ref_type = 'PrimaryMeasure'
        elif nodeName_ == 'Dimension':
            obj_ = RelationshipRefType._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            if self._ref_id is None:
                self._ref_id = obj_.ref
            elif not isinstance(self._ref_id, list):
                self._ref_id = [self._ref_id]
            if isinstance(self._ref_id, list):
                self._ref_id.append(obj_.ref)
            self._ref_type = 'Dimension'


class ConceptIdentityType(DataParser):
    """Parser of the Concept Identity of a Component"""

    def __init__(self, gds_collector_=None):
        super().__init__(gds_collector_)
        self._ref = None

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of ConceptIdentityType"""
        return ConceptIdentityType(*args_, **kwargs_)

    @property
    def ref(self):
        """Reference to a Concept in the Concept Identity, specifying the
        Concept Scheme unique ID and Concept ID in it"""
        return self._ref

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False,
                        gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'Ref':
            obj_ = RefBaseType._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._ref = {"CS": f"{obj_.agencyID}:{obj_.maintainableParentID}"
                               f"({obj_.maintainableParentVersion})",
                         "CON": f"{obj_.id_}"}
