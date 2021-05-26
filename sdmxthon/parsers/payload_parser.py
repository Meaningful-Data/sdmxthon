"""
    Data_Structure has the parsers for the information of data sets
"""

from sdmxthon.parsers.data_parser import DataParser
from sdmxthon.parsers.references import ReferenceType
from sdmxthon.utils.xml_base import cast, find_attr_value_, raise_parse_error


class PayloadStructureType(DataParser):
    """PayloadStructureType is an abstract base dim_type used to define the
    structural information for data sets. A reference to the
    structure is provided (either explicitly or through a reference to a
    structure usage).The structureID attribute uniquely identifies the
    structure for the purpose of referencing it from the payload. This is
    only used in structure specific formats. Although it is required, it is
    only useful when more than one data set is present in the message.The
    schemaURL attribute provides a location from which the structure
    specific schema can be located.The namespace attribute is used to
    provide the namespace for structure-specific formats. By communicating
    this information in the header, it is possible to generate the
    structure specific schema while processing the message.The
    dimensionAtObservation is used to reference the dimension at the
    observation level for data messages. This can also be given the
    explicit value of "AllDimensions" which denotes that the cross
    sectional data is in the flat format.The explicitMeasures indicates
    whether explicit measures are used in the cross sectional format. This
    is only applicable for the measure dimension as the dimension at the
    observation level or the flat structure."""
    __hash__ = DataParser.__hash__

    def __init__(self, structureID=None, schemaURL=None, namespace=None,
                 dimensionAtObservation=None,
                 explicitMeasures=None, serviceURL=None, structureURL=None,
                 ProvisionAgreement=None,
                 StructureUsage=None, Structure=None, gds_collector_=None,
                 **kwargs_):
        super(PayloadStructureType, self).__init__(gds_collector_, **kwargs_)
        self.gds_collector_ = gds_collector_
        self._structureID = cast(None, structureID)
        self._schemaURL = cast(None, schemaURL)
        self._namespace = cast(None, namespace)
        self._dimension_at_observation = cast(None, dimensionAtObservation)
        self._explicitMeasures = cast(bool, explicitMeasures)
        self._serviceURL = cast(None, serviceURL)
        self._structureURL = cast(None, structureURL)
        self._provisionAgreement = ProvisionAgreement
        self._structureUsage = StructureUsage
        self._structure = Structure

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of PayloadStructureType"""
        return PayloadStructureType(*args_, **kwargs_)

    @property
    def provisionAgreement(self):
        """Links the Data Provider to the relevant Structure Usage
        (e.g. DataflowDefinition or MetadataflowDefinition) for which the
        provider supplies data or metadata The agreement may constrain
        the scope of the data or metadata that can be provided,
        by means of a Constraint. """
        return self._provisionAgreement

    @provisionAgreement.setter
    def provisionAgreement(self, value):
        self._provisionAgreement = value

    @property
    def structureUsage(self):
        """References the DataFlowDefinition"""
        return self._structureUsage

    @structureUsage.setter
    def structureUsage(self, value):
        self._structureUsage = value

    @property
    def structure(self):
        """References the DataStructureDefinition"""
        return self._structure

    @structure.setter
    def structure(self, value):
        self._structure = value

    @property
    def structureID(self):
        """Identifies the structure"""
        return self._structureID

    @structureID.setter
    def structureID(self, value):
        self._structureID = value

    @property
    def dimensionAtObservation(self):
        """Gets the dimensionAtObservation in the structure"""
        return self._dimension_at_observation

    @dimensionAtObservation.setter
    def dimensionAtObservation(self, value):
        self._dimension_at_observation = value

    @property
    def schemaURL(self):
        """URL of the Schema"""
        return self._schemaURL

    @schemaURL.setter
    def schemaURL(self, value):
        self._schemaURL = value

    @property
    def serviceURL(self):
        """URL of the Service"""
        return self._serviceURL

    @serviceURL.setter
    def serviceURL(self, value):
        self._serviceURL = value

    @property
    def structureURL(self):
        """URL of the Structure"""
        return self._structureURL

    @structureURL.setter
    def structureURL(self, value):
        self._structureURL = value

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        value = find_attr_value_('structureID', node)

        if value is not None and 'structureID' not in already_processed:
            already_processed.add('structureID')
            self._structureID = value

        value = find_attr_value_('schemaURL', node)

        if value is not None and 'schemaURL' not in already_processed:
            already_processed.add('schemaURL')
            self._schemaURL = value

        value = find_attr_value_('namespace', node)

        if value is not None and 'namespace' not in already_processed:
            already_processed.add('namespace')
            self._namespace = value

        value = find_attr_value_('dimensionAtObservation', node)

        if (value is not None and
                'dimensionAtObservation' not in already_processed):
            already_processed.add('dimensionAtObservation')
            self._dimension_at_observation = value

        value = find_attr_value_('explicitMeasures', node)

        if value is not None and 'explicitMeasures' not in already_processed:
            already_processed.add('explicitMeasures')
            if value in ('true', '1'):
                self._explicitMeasures = True
            elif value in ('false', '0'):
                self._explicitMeasures = False
            else:
                raise_parse_error(node, 'Bad boolean attribute')

        value = find_attr_value_('serviceURL', node)

        if value is not None and 'serviceURL' not in already_processed:
            already_processed.add('serviceURL')
            self._serviceURL = value

        value = find_attr_value_('structureURL', node)

        if value is not None and 'structureURL' not in already_processed:
            already_processed.add('structureURL')
            self._structureURL = value

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False,
                        gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'ProvisionAgreement':
            obj_ = ReferenceType._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._provisionAgreement = obj_.ref

        elif nodeName_ == 'StructureUsage':
            obj_ = ReferenceType._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._structureUsage = obj_.ref

        elif nodeName_ == 'Structure':
            obj_ = ReferenceType._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._structure = obj_.ref


# end class PayloadStructureType

class DataStructureType(PayloadStructureType):
    """DataStructureType is an abstract base dim_type the forms the basis
    for the structural information for a data set. """
    __hash__ = DataParser.__hash__
    subclass = None
    superclass = PayloadStructureType

    def __init__(self, structureID=None, schemaURL=None, namespace=None,
                 dimensionAtObservation=None,
                 explicitMeasures=None, serviceURL=None, structureURL=None,
                 ProvisionAgreement=None,
                 StructureUsage=None, Structure=None, gds_collector_=None,
                 **kwargs_):
        super(DataStructureType, self).__init__(structureID, schemaURL,
                                                namespace,
                                                dimensionAtObservation,
                                                explicitMeasures, serviceURL,
                                                structureURL,
                                                ProvisionAgreement,
                                                StructureUsage, Structure,
                                                **kwargs_)
        self._gds_collector = gds_collector_

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of DataStructureType"""
        return DataStructureType(*args_, **kwargs_)


# end class DataStructureType

class GenericDataStructureType(DataStructureType):
    """GenericDataStructureType defines the structural information for a
    generic data set. A reference to the structure, either explicitly or
    through a dataflow or provision agreement is required as well as the
    dimension which occurs at the observation level."""

    def __init__(self, structureID=None, schemaURL=None, namespace=None,
                 dimensionAtObservation=None,
                 explicitMeasures=None, serviceURL=None, structureURL=None,
                 ProvisionAgreement=None,
                 StructureUsage=None, Structure=None, gds_collector_=None,
                 **kwargs_):
        super(GenericDataStructureType, self).__init__(structureID, schemaURL,
                                                       namespace,
                                                       dimensionAtObservation,
                                                       explicitMeasures,
                                                       serviceURL,
                                                       structureURL,
                                                       ProvisionAgreement,
                                                       StructureUsage,
                                                       Structure, **kwargs_)
        self._gds_collector = gds_collector_
        self._name = 'GenericDataStructureType'

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of GenericDataStructureType"""
        return GenericDataStructureType(*args_, **kwargs_)

    @property
    def structureID(self):
        """ID of the Structure"""
        return self._structureID

    @structureID.setter
    def structureID(self, value):
        self.structureID = value
# end class GenericDataStructureType
