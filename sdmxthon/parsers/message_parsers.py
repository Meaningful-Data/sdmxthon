from .data_generic import DataSetType as GenericDataSet, TimeSeriesDataSetType as GenericTimeSeriesDataSet
from .data_parser import DataParser
from .data_structure import DataSetType as StructureDataSet, \
    TimeSeriesDataSetType as StructureTimeSeriesDataSet
from .footer_parser import FooterType
from .gdscollector import GdsCollector
from .header_parser import BaseHeaderType, GenericDataHeaderType
from ..model.component import DataStructureDefinition, DataFlowDefinition
from ..model.itemScheme import Codelist, AgencyScheme, ConceptScheme


class MessageType(DataParser):
    """MessageType is an abstract dim_type which is used by all of the messages, to
    allow inheritance of common features. Every message consists of a
    mandatory header, followed by optional payload (which may occur
    multiple times), and finally an optional footer section for conveying
    error, warning, and informational messages."""

    def __init__(self, Header=None, Footer=None, gds_collector_=None, **kwargs_):
        super(MessageType, self).__init__(gds_collector_, **kwargs_)
        self._gds_collector_ = gds_collector_
        self._header = Header
        self._footer = Footer

    @staticmethod
    def factory(*args_, **kwargs_):
        return MessageType(**kwargs_)

    @property
    def header(self):
        return self._header

    @header.setter
    def header(self, value):
        self._header = value

    @property
    def footer(self):
        return self._footer

    @footer.setter
    def footer(self, value):
        self._footer = value

    def has_content_(self):
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

    def __init__(self, Header=None, Footer=None, DataSet=None, gds_collector_=None, **kwargs_):
        super(GenericDataType, self).__init__(Header, Footer, gds_collector_, **kwargs_)

        if DataSet is None:
            self._dataSet = []
        else:
            self._dataSet = DataSet

        if gds_collector_ is not None:
            self._gds_collector = gds_collector_
        else:
            self._gds_collector = GdsCollector()

    @staticmethod
    def factory(*args_, **kwargs_):
        return GenericDataType(*args_, **kwargs_)

    @property
    def dataset(self):
        return self._dataSet

    @dataset.setter
    def dataset(self, value):
        if value is None:
            self._dataSet = []
        elif isinstance(value, list):
            self._dataSet = value
        else:
            raise TypeError('Dataset must be a list')

    def add_DataSet(self, value):
        self._dataSet.append(value)

    def insert_DataSet_at(self, index, value):
        self._dataSet.insert(index, value)

    def replace_DataSet_at(self, index, value):
        self._dataSet[index] = value

    def has_content_(self):
        if (self._header is not None or self._dataSet or
                self._footer is not None or super(GenericDataType, self).has_content_()):
            return True
        else:
            return False

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Header':
            obj_ = GenericDataHeaderType.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self._header = obj_
            obj_.original_tagname_ = 'Header'
        elif nodeName_ == 'DataSet':
            obj_ = GenericDataSet.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self._dataSet.append(obj_)
            obj_.original_tag_name_ = 'DataSet'
        elif nodeName_ == 'Footer':
            obj_ = FooterType.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self._footer = obj_
            obj_.original_tag_name_ = 'Footer'


# end class GenericDataType

class CodelistsType(DataParser):
    def __init__(self, codelist=None, name=None, gds_collector_=None, **kwargs_):
        super(CodelistsType, self).__init__(gds_collector_, **kwargs_)

        if codelist is None:
            self._codelists = {}
        else:
            self._codelists = codelist

        if name is None:
            self._name = ''
        else:
            self._name = name

        if gds_collector_ is not None:
            self._gds_collector = gds_collector_
        else:
            self._gds_collector = GdsCollector()

    @staticmethod
    def factory(*args_, **kwargs_):
        return CodelistsType(*args_, **kwargs_)

    @property
    def codelists(self):
        return self._codelists

    @codelists.setter
    def codelists(self, value):
        self._codelists = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def has_content_(self):
        if self._codelists is not None or super(CodelistsType, self).has_content_():
            return True
        else:
            return False

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Codelist':
            obj_ = Codelist.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self._codelists[obj_.unique_id] = obj_


class ConceptsType(DataParser):
    def __init__(self, concepts=None, name=None, gds_collector_=None, **kwargs_):
        super(ConceptsType, self).__init__(gds_collector_, **kwargs_)

        self._cl_references = []
        if concepts is None:
            self._concepts = {}
        else:
            self._concepts = concepts

        if name is None:
            self._name = ''
        else:
            self._name = name

        if gds_collector_ is not None:
            self._gds_collector = gds_collector_
        else:
            self._gds_collector = GdsCollector()

    @staticmethod
    def factory(*args_, **kwargs_):
        return ConceptsType(*args_, **kwargs_)

    @property
    def concepts(self):
        return self._concepts

    @concepts.setter
    def concepts(self, value):
        self._concepts = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def has_content_(self):
        if len(self.concepts) > 0 or super(ConceptsType, self).has_content_():
            return True
        else:
            return False

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'ConceptScheme':
            obj_ = ConceptScheme.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self.concepts[obj_.unique_id] = obj_


class DataStructuresType(DataParser):
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
    def factory(*args_, **kwargs_):
        return DataStructuresType(*args_, **kwargs_)

    @property
    def dsds(self):
        return self._dsds

    @dsds.setter
    def dsds(self, value):
        self._dsds = value

    @property
    def non_unique(self):
        return self._non_unique

    def add_non_unique(self, id_):
        if self._non_unique is None:
            self._non_unique = []
        self._non_unique.append(id_)

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'DataStructure':
            obj_ = DataStructureDefinition.factory()
            obj_.build(child_, gds_collector_=gds_collector_)

            if self._dsds is None:
                self._dsds = {}

            if obj_.unique_id in self.dsds:
                self.add_non_unique(obj_.unique_id)
            else:
                self.dsds[obj_.unique_id] = obj_


class OrganisationSchemesType(DataParser):
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
    def factory(*args_, **kwargs_):
        return OrganisationSchemesType(*args_, **kwargs_)

    @property
    def agencySchemes(self):
        return self._agency_schemes

    @agencySchemes.setter
    def agencySchemes(self, value):
        self._agency_schemes = value

    def has_content_(self):
        if self._agency_schemes is not None or super(OrganisationSchemesType, self).has_content_():
            return True
        else:
            return False

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'AgencyScheme':
            obj_ = AgencyScheme.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self._agency_schemes = obj_


class DataflowsType(DataParser):
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
    def factory(*args_, **kwargs_):
        return DataflowsType(*args_, **kwargs_)

    @property
    def dataflows(self):
        return self._dataflows

    @dataflows.setter
    def dataflows(self, value):
        self._dataflows = value

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Dataflow':
            obj_ = DataFlowDefinition.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self.dataflows[obj_.unique_id] = obj_


class Structures(DataParser):
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
    def factory(*args_, **kwargs_):
        return Structures(*args_, **kwargs_)

    @property
    def dataflows(self):
        return self._dataflows

    @dataflows.setter
    def dataflows(self, value):
        self._dataflows = value

    @property
    def organisations(self):
        return self._organisations

    @organisations.setter
    def organisations(self, value):
        self._organisations = value

    @property
    def dsds(self):
        return self._dsds

    @dsds.setter
    def dsds(self, value):
        self._dsds = value

    @property
    def codelists(self):
        return self._codelists

    @codelists.setter
    def codelists(self, value):
        self._codelists = value

    @property
    def concepts(self):
        return self._concepts

    @concepts.setter
    def concepts(self, value):
        self._concepts = value

    @property
    def errors(self):
        return self._errors

    def add_error(self, error):
        if self._errors is None:
            self._errors = []
        self._errors.append(error)

    def has_content_(self):
        if self._concepts is not None or self._codelists or self._dsds is not None \
                or super(Structures, self).has_content_():
            return True
        else:
            return False

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'OrganisationSchemes':
            obj_ = OrganisationSchemesType.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self._organisations = obj_.agencySchemes
        elif nodeName_ == 'Codelists':
            obj_ = CodelistsType.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self._codelists = obj_.codelists
        elif nodeName_ == 'Concepts':
            obj_ = ConceptsType.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self._concepts = obj_.concepts
        elif nodeName_ == 'DataStructures':
            obj_ = DataStructuresType.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            if obj_.non_unique is not None:
                for e in obj_.non_unique:
                    self.add_error({'Code': 'MS06', 'ErrorLevel': 'CRITICAL',
                                    'ObjectID': f'{e}', 'ObjectType': f'DSD',
                                    'Message': f'DSD {e} is not unique'})
            self._dsds = obj_.dsds

        elif nodeName_ == 'Dataflows':
            obj_ = DataflowsType.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self._dataflows = obj_.dataflows


class MetadataType(MessageType):
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
    def factory(*args_, **kwargs_):
        return MetadataType(*args_, **kwargs_)

    @property
    def structures(self):
        return self._structures

    @structures.setter
    def structures(self, value):
        self._structures = value

    def has_content_(self):
        if (self._header is not None or self._structures or
                self._footer is not None or super(MetadataType, self).has_content_()):
            return True
        else:
            return False

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Header':
            obj_ = GenericDataHeaderType.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self._header = obj_
        elif nodeName_ == 'Structures':
            obj_ = Structures.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self._structures = obj_
        elif nodeName_ == 'Footer':
            obj_ = FooterType.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self._footer = obj_


class StructureSpecificDataHeaderType(BaseHeaderType):
    """StructureSpecificDataHeaderType defines the header structure for a
    structure specific data message."""
    __hash__ = BaseHeaderType.__hash__
    subclass = None
    superclass = BaseHeaderType

    def __init__(self, ID=None, Test=False, Prepared=None, Sender=None, Receiver=None, Name=None, Structure=None,
                 DataProvider=None, DataSetAction=None, DataSetID=None, Extracted=None, ReportingBegin=None,
                 ReportingEnd=None, EmbargoDate=None, Source=None, gds_collector_=None, **kwargs_):
        super(StructureSpecificDataHeaderType, self).__init__(ID, Test, Prepared, Sender, Receiver, Name, Structure,
                                                              DataProvider, DataSetAction, DataSetID, Extracted,
                                                              ReportingBegin, ReportingEnd, EmbargoDate, Source,
                                                              gds_collector_, **kwargs_)
        self._name = 'GenericDataHeaderType'

    @staticmethod
    def factory(*args_, **kwargs_):
        return StructureSpecificDataHeaderType(*args_, **kwargs_)

    def validate_HeaderTimeType(self, value):
        result = True
        return result

    def validate_ObservationalTimePeriodType(self, value):
        result = True
        return result


# end class StructureSpecificDataHeaderType

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

    def __init__(self, Header=None, Footer=None, DataSet=None, gds_collector_=None, **kwargs_):
        super(StructureSpecificDataType, self).__init__(Header, Footer, gds_collector_, **kwargs_)

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
    def factory(*args_, **kwargs_):
        return StructureSpecificDataType(*args_, **kwargs_)

    @property
    def dataset(self):
        return self._dataSet

    @dataset.setter
    def dataset(self, value):
        if value is None:
            self._dataSet = []
        elif isinstance(value, list):
            self._dataSet = value
        else:
            raise TypeError('Dataset must be a list')

    def add_DataSet(self, value):
        self._dataSet.append(value)

    def insert_DataSet_at(self, index, value):
        self._dataSet.insert(index, value)

    def replace_DataSet_at(self, index, value):
        self._dataSet[index] = value

    def has_content_(self):
        if self._header is not None or self._dataSet or self._footer is not None \
                or super(MessageType, self).has_content_():
            return True
        else:
            return False

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Header':
            obj_ = StructureSpecificDataHeaderType.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self._header = obj_
            obj_.original_tagname_ = 'Header'
        elif nodeName_ == 'DataSet':
            obj_ = StructureDataSet.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self._dataSet.append(obj_)
            obj_.original_tag_name_ = 'DataSet'
        elif nodeName_ == 'Footer':
            obj_ = FooterType.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self._footer = obj_
            obj_.original_tag_name_ = 'Footer'


# end class StructureSpecificDataType


class GenericTimeSeriesDataType(GenericDataType):
    """GenericDataType defines the contents of a generic data message."""
    __hash__ = GenericDataType.__hash__
    subclass = None
    superclass = GenericDataType

    def __init__(self, Header=None, Footer=None, DataSet=None, gds_collector_=None, **kwargs_):
        super(GenericTimeSeriesDataType, self).__init__(Header, Footer, DataSet, gds_collector_,
                                                        **kwargs_)

    @staticmethod
    def factory(*args_, **kwargs_):
        return GenericTimeSeriesDataType(*args_, **kwargs_)

    @property
    def dataset(self):
        return self._dataSet

    @dataset.setter
    def dataset(self, value):
        if value is None:
            self._dataSet = []
        elif isinstance(value, list):
            self._dataSet = value
        else:
            raise TypeError('Dataset must be a list')

    def add_DataSet(self, value):
        self._dataSet.append(value)

    def insert_DataSet_at(self, index, value):
        self._dataSet.insert(index, value)

    def replace_DataSet_at(self, index, value):
        self._dataSet[index] = value

    def has_content_(self):
        if (self._header is not None or self._dataSet or self._footer is not None
                or super(GenericDataType, self).has_content_()):
            return True
        else:
            return False

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Header':
            obj_ = GenericTimeSeriesDataHeaderType.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self._header = obj_
            obj_.original_tagname_ = 'Header'
        elif nodeName_ == 'DataSet':
            obj_ = GenericTimeSeriesDataSet.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self._dataSet.append(obj_)
            obj_.original_tag_name_ = 'DataSet'
        elif nodeName_ == 'Footer':
            obj_ = FooterType.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self._footer = obj_
            obj_.original_tag_name_ = 'Footer'


class GenericTimeSeriesDataHeaderType(GenericDataHeaderType):
    """GenericTimeSeriesDataHeaderType defines the header structure for a time
    series only generic data message."""
    __hash__ = GenericDataHeaderType.__hash__
    subclass = None
    superclass = GenericDataHeaderType

    def __init__(self, ID=None, Test=False, Prepared=None, Sender=None, Receiver=None, Name=None, Structure=None,
                 DataProvider=None, DataSetAction=None, DataSetID=None, Extracted=None, ReportingBegin=None,
                 ReportingEnd=None, EmbargoDate=None, Source=None, gds_collector_=None, **kwargs_):
        super(GenericTimeSeriesDataHeaderType, self).__init__(ID, Test, Prepared, Sender, Receiver, Name, Structure,
                                                              DataProvider, DataSetAction, DataSetID, Extracted,
                                                              ReportingBegin, ReportingEnd, EmbargoDate, Source,
                                                              gds_collector_, **kwargs_)
        self._name = 'GenericTimeSeriesDataHeaderType'

    @staticmethod
    def factory(*args_, **kwargs_):
        return GenericTimeSeriesDataHeaderType(*args_, **kwargs_)

    def validate_HeaderTimeType(self, value):
        pass

    def validate_ObservationalTimePeriodType(self, value):
        pass


class StructureSpecificTimeSeriesDataType(StructureSpecificDataType):
    """StructureSpecificTimeSeriesDataType defines the structure of the
    structure specific time series data message."""

    __hash__ = StructureSpecificDataType.__hash__
    subclass = None
    superclass = StructureSpecificDataType

    def __init__(self, Header=None, Footer=None, DataSet=None, gds_collector_=None, **kwargs_):
        super(StructureSpecificTimeSeriesDataType, self).__init__(Header, Footer, DataSet,
                                                                  gds_collector_, **kwargs_)

        if DataSet is None:
            self._dataSet = []
        else:
            self._dataSet = DataSet

        self._name = 'StructureSpecificTimeSeriesDataType'

        if gds_collector_ is not None:
            self.gds_collector_ = gds_collector_
        else:
            self.gds_collector_ = GdsCollector()

    @staticmethod
    def factory(*args_, **kwargs_):
        return StructureSpecificDataType(*args_, **kwargs_)

    @property
    def dataset(self):
        return self._dataSet

    @dataset.setter
    def dataset(self, value):
        if value is None:
            self._dataSet = []
        elif isinstance(value, list):
            self._dataSet = value
        else:
            raise TypeError('Dataset must be a list')

    def add_DataSet(self, value):
        self._dataSet.append(value)

    def insert_DataSet_at(self, index, value):
        self._dataSet.insert(index, value)

    def replace_DataSet_at(self, index, value):
        self._dataSet[index] = value

    def has_content_(self):
        if (self._header is not None or self._dataSet or self._footer is not None
                or super(StructureSpecificDataType, self).has_content_()):
            return True
        else:
            return False

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Header':
            obj_ = StructureSpecificTimeSeriesDataHeaderType.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self._header = obj_
            obj_.original_tagname_ = 'Header'
        elif nodeName_ == 'DataSet':
            obj_ = StructureTimeSeriesDataSet.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self._dataSet.append(obj_)
            obj_.original_tag_name_ = 'DataSet'
        elif nodeName_ == 'Footer':
            obj_ = FooterType.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self._footer = obj_
            obj_.original_tag_name_ = 'Footer'


# end class StructureSpecificDataType


class StructureSpecificTimeSeriesDataHeaderType(StructureSpecificDataHeaderType):
    """StructureSpecificTimeSeriesDataHeaderType defines the header structure
    for a time series only structure specific data message."""
    __hash__ = StructureSpecificDataHeaderType.__hash__
    subclass = None
    superclass = StructureSpecificDataHeaderType

    def __init__(self, ID=None, Test=False, Prepared=None, Sender=None, Receiver=None, Name=None, Structure=None,
                 DataProvider=None, DataSetAction=None, DataSetID=None, Extracted=None, ReportingBegin=None,
                 ReportingEnd=None, EmbargoDate=None, Source=None, gds_collector_=None, **kwargs_):
        super(StructureSpecificTimeSeriesDataHeaderType, self).__init__(ID, Test, Prepared, Sender, Receiver, Name,
                                                                        Structure, DataProvider, DataSetAction,
                                                                        DataSetID,
                                                                        Extracted, ReportingBegin, ReportingEnd,
                                                                        EmbargoDate,
                                                                        Source, gds_collector_, **kwargs_)
        self._name = 'StructureSpecificTimeSeriesDataHeaderType'

    @staticmethod
    def factory(*args_, **kwargs_):
        return StructureSpecificTimeSeriesDataHeaderType(*args_, **kwargs_)

    def validate_HeaderTimeType(self, value):
        result = True
        return result

    def validate_ObservationalTimePeriodType(self, value):
        result = True
        return result
