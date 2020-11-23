from SDMXThon.common.references import ProvisionAgreementReferenceType, DataStructureReferenceType, \
    DataflowReferenceType
from SDMXThon.utils.data_parser import DataParser
from SDMXThon.utils.xml_base import _cast, quote_attrib, find_attr_value_, raise_parse_error


class PayloadStructureType(DataParser):
    """PayloadStructureType is an abstract base type used to define the
    structural information for data or metadata sets. A reference to the
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
    subclass = None
    superclass = None

    def __init__(self, structureID=None, schemaURL=None, namespace=None, dimensionAtObservation=None,
                 explicitMeasures=None, serviceURL=None, structureURL=None, ProvisionAgrement=None, StructureUsage=None,
                 Structure=None, gds_collector_=None, **kwargs_):
        super(PayloadStructureType, self).__init__(gds_collector_, **kwargs_)
        self.gds_collector_ = gds_collector_
        self.gds_element_tree_node_ = None
        self.original_tag_name_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self._structureID = _cast(None, structureID)
        self._structureID_nsprefix_ = None
        self._schemaURL = _cast(None, schemaURL)
        self._schemaURL_nsprefix_ = None
        self._namespace = _cast(None, namespace)
        self._namespace_nsprefix_ = None
        self._dimensionAtObservation = _cast(None, dimensionAtObservation)
        self._dimensionAtObservation_nsprefix_ = None
        self._explicitMeasures = _cast(bool, explicitMeasures)
        self._explicitMeasures_nsprefix_ = None
        self._serviceURL = _cast(None, serviceURL)
        self._serviceURL_nsprefix_ = None
        self._structureURL = _cast(None, structureURL)
        self._structureURL_nsprefix_ = None
        self._provisionAgrement = ProvisionAgrement
        self._provisionAgrement_nsprefix_ = None
        self._structureUsage = StructureUsage
        self._structureUsage_nsprefix_ = None
        self._structure = Structure
        self._structure_nsprefix_ = None
        self._namespacedef = 'xmlns:common="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common"'
        self._namespaceprefix = "common"
        self._namespace_prefix = "common"

    def factory(*args_, **kwargs_):
        return PayloadStructureType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_ProvisionAgrement(self):
        return self._provisionAgrement

    def set_ProvisionAgrement(self, ProvisionAgrement):
        self._provisionAgrement = ProvisionAgrement

    def get_StructureUsage(self):
        return self._structureUsage

    def set_StructureUsage(self, StructureUsage):
        self._structureUsage = StructureUsage

    def get_Structure(self):
        return self._structure

    def set_Structure(self, Structure):
        self._structure = Structure

    def get_structureID(self):
        return self._structureID

    def set_structureID(self, structureID):
        self._structureID = structureID

    def get_schemaURL(self):
        return self._schemaURL

    def set_schemaURL(self, schemaURL):
        self._schemaURL = schemaURL

    def get_namespace(self):
        return self._namespace

    def set_namespace(self, namespace):
        self._namespace = namespace

    def get_dimensionAtObservation(self):
        return self._dimensionAtObservation

    def set_dimensionAtObservation(self, dimensionAtObservation):
        self._dimensionAtObservation = dimensionAtObservation

    def get_explicitMeasures(self):
        return self._explicitMeasures

    def set_explicitMeasures(self, explicitMeasures):
        self._explicitMeasures = explicitMeasures

    def get_serviceURL(self):
        return self._serviceURL

    def set_serviceURL(self, serviceURL):
        self._serviceURL = serviceURL

    def get_structureURL(self):
        return self._structureURL

    def set_structureURL(self, structureURL):
        self._structureURL = structureURL

    def validate_ObservationDimensionType(self, value):
        # Validate type ObservationDimensionType, a restriction on None.
        pass

    def has_content_(self):
        if (
                self._provisionAgrement is not None or
                self._structureUsage is not None or
                self._structure is not None
        ):
            return True
        else:
            return False

    def export_attributes(self, outfile, level, already_processed, namespace_prefix_='', name_='PayloadStructureType'):
        if self._structureID is not None and 'structureID' not in already_processed:
            already_processed.add('structureID')
            outfile.write(' structureID=%s' % (
                self.gds_encode(self.gds_format_string(quote_attrib(self._structureID), input_name='structureID')),))

        if self._schemaURL is not None and 'schemaURL' not in already_processed:
            already_processed.add('schemaURL')
            outfile.write(' schemaURL=%s' % (
                self.gds_encode(self.gds_format_string(quote_attrib(self._schemaURL), input_name='schemaURL')),))

        if self._namespace is not None and 'namespace' not in already_processed:
            already_processed.add('namespace')
            outfile.write(' namespace=%s' % (
                self.gds_encode(self.gds_format_string(quote_attrib(self._namespace), input_name='namespace')),))

        if self._dimensionAtObservation is not None and 'dimensionAtObservation' not in already_processed:
            already_processed.add('dimensionAtObservation')
            outfile.write(' dimensionAtObservation=%s' % (quote_attrib(self._dimensionAtObservation),))

        if self._explicitMeasures is not None and 'explicitMeasures' not in already_processed:
            already_processed.add('explicitMeasures')
            outfile.write(' explicitMeasures="%s"' % self.gds_format_boolean(self._explicitMeasures,
                                                                             input_name='explicitMeasures'))

        if self._serviceURL is not None and 'serviceURL' not in already_processed:
            already_processed.add('serviceURL')
            outfile.write(' serviceURL=%s' % (
                self.gds_encode(self.gds_format_string(quote_attrib(self._serviceURL), input_name='serviceURL')),))

        if self._structureURL is not None and 'structureURL' not in already_processed:
            already_processed.add('structureURL')
            outfile.write(' structureURL=%s' % (
                self.gds_encode(self.gds_format_string(quote_attrib(self._structureURL), input_name='structureURL')),))

    def export_attributes_as_dict(self, parent_dict: dict, data: list, valid_fields: list):
        if self._structureID is not None and 'structureID' in valid_fields:
            parent_dict.update({'structureID': self._structureID})

        if self._schemaURL is not None and 'schemaURL' in valid_fields:
            parent_dict.update({'schemaURL': self._schemaURL})

        if self._namespace is not None and 'namespace' in valid_fields:
            parent_dict.update({'namespace': self._namespace})

        if self._dimensionAtObservation is not None and 'dimensionAtObservation' in valid_fields:
            parent_dict.update({'dimensionAtObservation': self._dimensionAtObservation})

        if self._explicitMeasures is not None and 'explicitMeasures' in valid_fields:
            parent_dict.update({'explicitMeasures': self._explicitMeasures})

        if self._serviceURL is not None and 'serviceURL' in valid_fields:
            parent_dict.update({'serviceURL': self._serviceURL})

        if self._structureURL is not None and 'structureURL' in valid_fields:
            parent_dict.update({'structureURL': self._structureURL})

        if self._provisionAgrement is not None:
            self._provisionAgrement.export_attributes_as_dict(parent_dict, data, valid_fields)

        if self._structureUsage is not None:
            self._structureUsage.export_attributes_as_dict(parent_dict, data, valid_fields)

        if self._structure is not None:
            self._structure.export_attributes_as_dict(parent_dict, data, valid_fields)

    def export_children(self, outfile, level, pretty_print=True, has_parent=True, **kwargs):
        if self._provisionAgrement is not None:
            self._provisionAgrement.export(outfile, level, pretty_print=pretty_print, has_parent=has_parent)

        if self._structureUsage is not None:
            self._structureUsage.export(outfile, level, pretty_print=pretty_print, has_parent=has_parent)

        if self._structure is not None:
            self._structure.export(outfile, level, pretty_print=pretty_print, has_parent=has_parent)

    def build_attributes(self, node, attrs, already_processed):
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

        if value is not None and 'dimensionAtObservation' not in already_processed:
            already_processed.add('dimensionAtObservation')
            self._dimensionAtObservation = value
            self.validate_ObservationDimensionType(
                self._dimensionAtObservation)  # validate type ObservationDimensionType

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

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'ProvisionAgrement':
            obj_ = ProvisionAgreementReferenceType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._provisionAgrement = obj_
            obj_.original_tag_name_ = 'ProvisionAgrement'

        elif nodeName_ == 'StructureUsage':
            obj_ = DataflowReferenceType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._structureUsage = obj_
            obj_.original_tag_name_ = 'StructureUsage'

        elif nodeName_ == 'Structure':
            obj_ = DataStructureReferenceType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._structure = obj_
            obj_.original_tag_name_ = 'Structure'


# end class PayloadStructureType

class DataStructureType(PayloadStructureType):
    """DataStructureType is an abstract base type the forms the basis for the
    structural information for a data set."""
    __hash__ = DataParser.__hash__
    subclass = None
    superclass = PayloadStructureType

    def __init__(self, structureID=None, schemaURL=None, namespace=None, dimensionAtObservation=None,
                 explicitMeasures=None, serviceURL=None, structureURL=None, ProvisionAgrement=None, StructureUsage=None,
                 Structure=None, gds_collector_=None, **kwargs_):
        super(DataStructureType, self).__init__(structureID, schemaURL, namespace, dimensionAtObservation,
                                                explicitMeasures, serviceURL, structureURL, ProvisionAgrement,
                                                StructureUsage, Structure, **kwargs_)
        self._name = 'DataStructureType'

    def factory(*args_, **kwargs_):
        return DataStructureType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def export_attributes(self, outfile, level, already_processed, namespace_prefix_='', name_='DataStructureType'):
        super(DataStructureType, self).export_attributes(outfile, level, already_processed, namespace_prefix_,
                                                         name_='DataStructureType')


# end class DataStructureType

class GenericDataStructureType(DataStructureType):
    """GenericDataStructureType defines the structural information for a
    generic data set. A reference to the structure, either explicitly or
    through a dataflow or provision agreement is required as well as the
    dimension which occurs at the observation level."""
    __hash__ = DataParser.__hash__
    subclass = None
    superclass = DataStructureType

    def __init__(self, structureID=None, schemaURL=None, namespace=None, dimensionAtObservation=None,
                 explicitMeasures=None, serviceURL=None, structureURL=None, ProvisionAgrement=None, StructureUsage=None,
                 Structure=None, gds_collector_=None, **kwargs_):
        super(GenericDataStructureType, self).__init__(structureID, schemaURL, namespace, dimensionAtObservation,
                                                       explicitMeasures, serviceURL, structureURL, ProvisionAgrement,
                                                       StructureUsage, Structure, **kwargs_)
        self._name = 'GenericDataStructureType'
        self._namespace_prefix = 'message'

    def factory(*args_, **kwargs_):
        return GenericDataStructureType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def validate_ObservationDimensionType(self, value):
        # Validate type ObservationDimensionType, a restriction on None.
        pass

    def export_attributes(self, outfile, level, already_processed, namespace_prefix_='',
                          name_='GenericDataStructureType'):
        super(GenericDataStructureType, self).export_attributes(outfile, level, already_processed, namespace_prefix_,
                                                                name_='GenericDataStructureType')
# end class GenericDataStructureType
