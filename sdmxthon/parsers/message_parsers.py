"""
    Message_parsers file contains all classes to parse a SDMX-ML Message
"""

from SDMXthon.model.component import DataStructureDefinition, DataFlowDefinition
from SDMXthon.model.header import Header
from SDMXthon.model.itemScheme import Codelist, AgencyScheme, ConceptScheme
from SDMXthon.utils.handlers import add_indent
from SDMXthon.utils.mappings import *
from .data_generic import DataSetType as GenericDataSet, TimeSeriesDataSetType as GenericTimeSeriesDataSet
from .data_parser import DataParser
from .data_structure import DataSetType as StructureDataSet
from .footer_parser import FooterType
from .gdscollector import GdsCollector


class MessageType(DataParser):
    """MessageType is an abstract dim_type which is used by all of the messages, to
    allow inheritance of common features. Every message consists of a
    mandatory header, followed by optional payload (which may occur
    multiple times), and finally an optional footer section for conveying
    error, warning, and informational messages."""

    def __init__(self, header=None, Footer=None, gds_collector_=None, **kwargs_):
        super(MessageType, self).__init__(gds_collector_, **kwargs_)
        self._gds_collector_ = gds_collector_
        self._header = header
        self._footer = Footer

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of MessageType"""
        return MessageType(**kwargs_)

    @property
    def header(self):
        """Header of the Message"""
        return self._header

    @header.setter
    def header(self, value):
        self._header = value

    @property
    def footer(self):
        """Footer of the Message"""
        return self._footer

    @footer.setter
    def footer(self, value):
        self._footer = value

    def _has_content_(self):
        """Check if it has any content"""
        if (
                self._header is not None or
                self._footer is not None
        ):
            return True
        else:
            return False


# end class MessageType

class GenericDataType(MessageType):
    """GenericDataType defines the contents of a generic data message."""
    __hash__ = DataParser.__hash__
    subclass = None
    superclass = MessageType

    def __init__(self, header=None, Footer=None, DataSet=None, gds_collector_=None, **kwargs_):
        super(GenericDataType, self).__init__(header, Footer, gds_collector_, **kwargs_)

        if DataSet is None:
            self._dataSet = []
        else:
            self._dataSet = DataSet

        if gds_collector_ is not None:
            self._gds_collector = gds_collector_
        else:
            self._gds_collector = GdsCollector()

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of GenericDataType"""
        return GenericDataType(*args_, **kwargs_)

    @property
    def dataset(self):
        """List of Datasets in a Generic Message"""
        return self._dataSet

    @dataset.setter
    def dataset(self, value):
        if value is None:
            self._dataSet = []
        elif isinstance(value, list):
            self._dataSet = value
        else:
            raise TypeError('Dataset must be a list')

    def _has_content_(self):
        """Check if it has any content"""
        if (self._header is not None or self._dataSet or
                self._footer is not None or super(GenericDataType, self)._has_content_()):
            return True
        else:
            return False

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'Header':
            obj_ = Header._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._header = obj_
            obj_.original_tagname_ = 'Header'
        elif nodeName_ == 'DataSet':
            obj_ = GenericDataSet._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._dataSet.append(obj_)
            obj_.original_tag_name_ = 'DataSet'
        elif nodeName_ == 'Footer':
            obj_ = FooterType._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._footer = obj_
            obj_.original_tag_name_ = 'Footer'


# end class GenericDataType

class CodelistsType(DataParser):
    """CodelistsType is the parser for the Codelists XML element"""

    def __init__(self, codelist=None, gds_collector_=None, **kwargs_):
        super(CodelistsType, self).__init__(gds_collector_, **kwargs_)

        if codelist is None:
            self._codelists = {}
        else:
            self._codelists = codelist

        if gds_collector_ is not None:
            self._gds_collector = gds_collector_
        else:
            self._gds_collector = GdsCollector()

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of CodelistsType"""
        return CodelistsType(*args_, **kwargs_)

    @property
    def codelists(self):
        """Dict of Codelists"""
        return self._codelists

    @codelists.setter
    def codelists(self, value):
        self._codelists = value

    def _has_content_(self):
        """Check if it has any content"""
        if self._codelists is not None or super(CodelistsType, self)._has_content_():
            return True
        else:
            return False

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'Codelist':
            obj_ = Codelist._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._codelists[obj_.unique_id] = obj_


class ConceptsType(DataParser):
    """ConceptsType is the parser for the Concepts XML element"""

    def __init__(self, concepts=None, gds_collector_=None, **kwargs_):
        super(ConceptsType, self).__init__(gds_collector_, **kwargs_)

        self._cl_references = []
        if concepts is None:
            self._concepts = {}
        else:
            self._concepts = concepts

        if gds_collector_ is not None:
            self._gds_collector = gds_collector_
        else:
            self._gds_collector = GdsCollector()

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of ConceptsType"""
        return ConceptsType(*args_, **kwargs_)

    @property
    def concepts(self):
        """Dict of Concepts"""
        return self._concepts

    @concepts.setter
    def concepts(self, value):
        self._concepts = value

    def _has_content_(self):
        """Check if it has any content"""
        if len(self.concepts) > 0 or super(ConceptsType, self)._has_content_():
            return True
        else:
            return False

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'ConceptScheme':
            obj_ = ConceptScheme._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self.concepts[obj_.unique_id] = obj_


class DataStructuresType(DataParser):
    """DataStructuresType is the parser for the DataStructures XML element"""

    def __init__(self, dsds=None, gds_collector_=None, **kwargs_):
        super(DataStructuresType, self).__init__(gds_collector_, **kwargs_)

        self._cl_references = []
        self._dsds = dsds

        self._non_unique = None

        if gds_collector_ is not None:
            self._gds_collector = gds_collector_
        else:
            self._gds_collector = GdsCollector()

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of DataStructuresType"""
        return DataStructuresType(*args_, **kwargs_)

    @property
    def dsds(self):
        """Dict of DSDs"""
        return self._dsds

    @dsds.setter
    def dsds(self, value):
        self._dsds = value

    @property
    def non_unique(self):
        """Dict of non-unique dsds"""
        return self._non_unique

    def add_non_unique(self, id_):
        """Method to add a non-unique DSD to generate the error"""
        if self._non_unique is None:
            self._non_unique = []
        self._non_unique.append(id_)

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'DataStructure':
            obj_ = DataStructureDefinition._factory()
            obj_._build(child_, gds_collector_=gds_collector_)

            if self._dsds is None:
                self._dsds = {}

            if obj_.unique_id in self.dsds:
                self.add_non_unique(obj_.unique_id)
            else:
                self.dsds[obj_.unique_id] = obj_


class OrganisationSchemesType(DataParser):
    """OrganisationSchemesType is the parser for the OrganisationScheme XML element"""

    def __init__(self, agency_scheme=None, gds_collector_=None, **kwargs_):
        super(OrganisationSchemesType, self).__init__(gds_collector_, **kwargs_)

        if agency_scheme is None:
            self._agency_schemes = []
        else:
            self._agency_schemes = agency_scheme

        if gds_collector_ is not None:
            self._gds_collector = gds_collector_
        else:
            self._gds_collector = GdsCollector()

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of OrganisationSchemesType"""
        return OrganisationSchemesType(*args_, **kwargs_)

    @property
    def agencySchemes(self):
        """Getter of the AgencyScheme"""
        return self._agency_schemes

    @agencySchemes.setter
    def agencySchemes(self, value):
        self._agency_schemes = value

    def _has_content_(self):
        """Check if it has any content"""
        if self._agency_schemes is not None or super(OrganisationSchemesType, self)._has_content_():
            return True
        else:
            return False

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'AgencyScheme':
            obj_ = AgencyScheme._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._agency_schemes = obj_


class DataflowsType(DataParser):
    """DataflowsType is the parser for the DataFlowDefinition XML element"""

    def __init__(self, dataflows=None, gds_collector_=None, **kwargs_):
        super(DataflowsType, self).__init__(gds_collector_, **kwargs_)

        if dataflows is None:
            self._dataflows = {}
        else:
            self._dataflows = dataflows

        if gds_collector_ is not None:
            self._gds_collector = gds_collector_
        else:
            self._gds_collector = GdsCollector()

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of DataflowsType"""
        return DataflowsType(*args_, **kwargs_)

    @property
    def dataflows(self):
        """Dict of Dataflows"""
        return self._dataflows

    @dataflows.setter
    def dataflows(self, value):
        self._dataflows = value

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'Dataflow':
            obj_ = DataFlowDefinition._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self.dataflows[obj_.unique_id] = obj_


class Structures(DataParser):
    """Structures class is the Metadata holder to access all elements in a Structures SDMX_ML file"""
    __hash__ = DataParser.__hash__

    def __init__(self, codelists=None, concepts=None, dsds=None, organisations=None, dataflows=None,
                 gds_collector_=None, **kwargs_):
        super(Structures, self).__init__(gds_collector_, **kwargs_)

        self._dataflows = dataflows

        self._dsds = dsds

        self._codelists = codelists

        self._organisations = organisations

        self._concepts = concepts

        self._errors = None

        if gds_collector_ is not None:
            self._gds_collector = gds_collector_
        else:
            self._gds_collector = GdsCollector()

    def __eq__(self, other):
        if isinstance(other, Structures):
            if self.codelists is not None:
                for e in self.codelists.values():
                    e._checked = False

            if self.concepts is not None:
                for e in self.concepts.values():
                    e._checked = False

            return (self._dataflows == other._dataflows and self._dsds == other._dsds
                    and self._codelists == other._codelists and self._organisations == other._organisations
                    and self._concepts == other._concepts and self._errors == other._errors)

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of Structures"""
        return Structures(*args_, **kwargs_)

    @property
    def dataflows(self):
        """Dict of dataflows"""
        return self._dataflows

    @dataflows.setter
    def dataflows(self, value):
        self._dataflows = value

    @property
    def organisations(self):
        """Dict of OrganisationScheme"""
        return self._organisations

    @organisations.setter
    def organisations(self, value):
        self._organisations = value

    @property
    def dsds(self):
        """Dict of DataStructureDefinition"""
        return self._dsds

    @dsds.setter
    def dsds(self, value):
        self._dsds = value

    @property
    def codelists(self):
        """Dict of Codelists"""
        return self._codelists

    @codelists.setter
    def codelists(self, value):
        self._codelists = value

    @property
    def concepts(self):
        """Dict of Concepts"""
        return self._concepts

    @concepts.setter
    def concepts(self, value):
        self._concepts = value

    @property
    def errors(self):
        """List of Errors"""
        return self._errors

    def add_error(self, error):
        """Method to add an error in the Structures"""
        if self._errors is None:
            self._errors = []
        self._errors.append(error)

    def _has_content_(self):
        """Check if it has any content"""
        if self._concepts is not None or self._codelists or self._dsds is not None \
                or super(Structures, self)._has_content_():
            return True
        else:
            return False

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'OrganisationSchemes':
            obj_ = OrganisationSchemesType._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._organisations = obj_.agencySchemes
        elif nodeName_ == 'Codelists':
            obj_ = CodelistsType._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._codelists = obj_.codelists
        elif nodeName_ == 'Concepts':
            obj_ = ConceptsType._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._concepts = obj_.concepts
        elif nodeName_ == 'DataStructures':
            obj_ = DataStructuresType._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            if obj_.non_unique is not None:
                for e in obj_.non_unique:
                    self.add_error({'Code': 'MS06', 'ErrorLevel': 'CRITICAL',
                                    'ObjectID': f'{e}', 'ObjectType': f'DSD',
                                    'Message': f'DSD {e} is not unique'})
            self._dsds = obj_.dsds

        elif nodeName_ == 'Dataflows':
            obj_ = DataflowsType._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._dataflows = obj_.dataflows

    def to_XML(self, prettyprint=True):

        if prettyprint:
            indent = '\t'
            newline = '\n'
        else:
            indent = newline = ''

        outfile = f'{indent}<{messageAbbr}:Structures>'
        if self.organisations is not None:
            indent_child = newline + add_indent(indent)
            outfile += f'{indent_child}<{structureAbbr}:OrganisationSchemes>'
            outfile += self.organisations._parse_XML(indent_child, f'{structureAbbr}:AgencyScheme')
            outfile += f'{indent_child}</{structureAbbr}:OrganisationSchemes>'
        if self.codelists is not None:
            indent_child = newline + add_indent(indent)
            outfile += f'{indent_child}<{structureAbbr}:Codelists>'
            for e in self.codelists.values():
                outfile += e._parse_XML(indent_child, f'{structureAbbr}:Codelist')
            outfile += f'{indent_child}</{structureAbbr}:Codelists>'

        if self.concepts is not None:
            indent_child = newline + add_indent(indent)
            outfile += f'{indent_child}<{structureAbbr}:Concepts>'
            for e in self.concepts.values():
                outfile += e._parse_XML(indent_child, f'{structureAbbr}:ConceptScheme')
            outfile += f'{indent_child}</{structureAbbr}:Concepts>'

        if self.dsds is not None:
            indent_child = newline + add_indent(indent)
            outfile += f'{indent_child}<{structureAbbr}:DataStructures>'
            for e in self.dsds.values():
                outfile += e._parse_XML(indent_child, f'{structureAbbr}:DataStructure')
            outfile += f'{indent_child}</{structureAbbr}:DataStructures>'

        if self.dataflows is not None:
            indent_child = newline + add_indent(indent)
            outfile += f'{indent_child}<{structureAbbr}:Dataflows>'
            for e in self.dataflows.values():
                outfile += e._parse_XML(indent_child, f'{structureAbbr}:Dataflow')
            outfile += f'{indent_child}</{structureAbbr}:Dataflows>'

        outfile += f'{newline}{indent}</{messageAbbr}:Structures>{newline}'

        return outfile


class MetadataType(MessageType):
    """MetadataType is a type of Message that starts with the tag Structure and contains the Metadata information"""
    __hash__ = DataParser.__hash__
    superclass = MessageType

    def __init__(self, header=None, footer=None, structures=None, gds_collector_=None, **kwargs_):
        super(MetadataType, self).__init__(header, footer, gds_collector_, **kwargs_)

        self._structures = structures

        if gds_collector_ is not None:
            self._gds_collector = gds_collector_
        else:
            self._gds_collector = GdsCollector()

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of MetadataType"""
        return MetadataType(*args_, **kwargs_)

    @property
    def structures(self):
        """Reference to the Structure in the Message"""
        return self._structures

    @structures.setter
    def structures(self, value):
        self._structures = value

    def _has_content_(self):
        """Check if it has any content"""
        if (self._header is not None or self._structures or
                self._footer is not None or super(MetadataType, self)._has_content_()):
            return True
        else:
            return False

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'Header':
            obj_ = Header._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._header = obj_
        elif nodeName_ == 'Structures':
            obj_ = Structures._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._structures = obj_
        elif nodeName_ == 'Footer':
            obj_ = FooterType._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._footer = obj_


class StructureSpecificDataType(MessageType):
    """StructureSpecificDataType defines the structure of the structure
    specific data message. Note that the data set payload dim_type is abstract,
    and therefore it will have to be assigned a dim_type in an instance. This
    dim_type must be derived from the base dim_type referenced. This base dim_type
    defines a general structure which can be followed to allow for generic
    processing of the data even if the exact details of the data structure
    specific format are not known."""
    __hash__ = MessageType.__hash__
    subclass = None
    superclass = MessageType

    def __init__(self, header=None, Footer=None, DataSet=None, gds_collector_=None, **kwargs_):
        super(StructureSpecificDataType, self).__init__(header, Footer, gds_collector_, **kwargs_)

        if DataSet is None:
            self._dataSet = []
        else:
            self._dataSet = DataSet
        self._name = 'StructureSpecificDataType'

        if gds_collector_ is not None:
            self.gds_collector_ = gds_collector_
        else:
            self.gds_collector_ = GdsCollector()

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of StructureSpecificDataType"""
        return StructureSpecificDataType(*args_, **kwargs_)

    @property
    def dataset(self):
        """List of Datasets in a Structure Specific Message"""
        return self._dataSet

    @dataset.setter
    def dataset(self, value):
        if value is None:
            self._dataSet = []
        elif isinstance(value, list):
            self._dataSet = value
        else:
            raise TypeError('Dataset must be a list')

    def _has_content_(self):
        """Check if it has any content"""
        if self._header is not None or self._dataSet or self._footer is not None \
                or super(MessageType, self)._has_content_():
            return True
        else:
            return False

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'Header':
            obj_ = Header._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._header = obj_
            obj_.original_tagname_ = 'Header'
        elif nodeName_ == 'DataSet':
            obj_ = StructureDataSet._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._dataSet.append(obj_)
            obj_.original_tag_name_ = 'DataSet'
        elif nodeName_ == 'Footer':
            obj_ = FooterType._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._footer = obj_
            obj_.original_tag_name_ = 'Footer'


# end class StructureSpecificDataType


class GenericTimeSeriesDataType(GenericDataType):
    """GenericDataType defines the contents of a generic data message."""
    __hash__ = GenericDataType.__hash__
    subclass = None
    superclass = GenericDataType

    def __init__(self, header=None, Footer=None, DataSet=None, gds_collector_=None, **kwargs_):
        super(GenericTimeSeriesDataType, self).__init__(header, Footer, DataSet, gds_collector_,
                                                        **kwargs_)

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of GenericTimeSeriesDataType"""
        return GenericTimeSeriesDataType(*args_, **kwargs_)

    @property
    def dataset(self):
        """List of Datasets in a Generic Time Series Message"""
        return self._dataSet

    @dataset.setter
    def dataset(self, value):
        if value is None:
            self._dataSet = []
        elif isinstance(value, list):
            self._dataSet = value
        else:
            raise TypeError('Dataset must be a list')

    def _has_content_(self):
        """Check if it has any content"""
        if (self._header is not None or self._dataSet or self._footer is not None
                or super(GenericDataType, self)._has_content_()):
            return True
        else:
            return False

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'Header':
            obj_ = Header._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._header = obj_
            obj_.original_tagname_ = 'Header'
        elif nodeName_ == 'DataSet':
            obj_ = GenericTimeSeriesDataSet._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._dataSet.append(obj_)
            obj_.original_tag_name_ = 'DataSet'
        elif nodeName_ == 'Footer':
            obj_ = FooterType._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._footer = obj_
            obj_.original_tag_name_ = 'Footer'
