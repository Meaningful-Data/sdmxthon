from typing import List

from SDMXThon.model.utils import FacetType, string_setter, FacetValueType
from SDMXThon.parsers.data_parser import DataParser
from SDMXThon.parsers.references import RefBaseType
from SDMXThon.utils.xml_base import find_attr_value_


class Facet:
    """Defines the format for the content of the Component when reported in a data
       or metadata set."""

    def __init__(self, facetType: str = None, facetValue: str = None, facetValueType: str = None):
        self.facet_type = facetType
        self.facet_value = facetValue
        self.facet_value_type = facetValueType

    def __str__(self):
        return f'<{self.facet_type} - {self.facet_value}>'

    def __unicode__(self):
        return f'<{self.facet_type} - {self.facet_value}>'

    def __repr__(self):
        return f'<{self.facet_type} - {self.facet_value}>'

    @property
    def facet_type(self):
        """A specific content type which is constrained by the FacetType enumeration"""
        return self._facetType

    @property
    def facet_value(self):
        """The value of the Facet"""
        return self._facetValue

    @property
    def facet_value_type(self):
        """The format of the value of a Component when reported in a data or metadata set.
            This is constrained by the FacetValueType enumeration."""
        return self._facetValueType

    @facet_type.setter
    def facet_type(self, value):
        if isinstance(value, str) or value is None:
            if value in FacetType or value is None:
                self._facetType = value
            else:
                raise ValueError(f"The facet {value} is not recognised")
        else:
            raise ValueError("Facet dim_type should be of the str dim_type")

    @facet_value.setter
    def facet_value(self, value):
        self._facetValue = string_setter(value)

    @facet_value_type.setter
    def facet_value_type(self, value):
        if isinstance(value, str) or value is None:
            if value in FacetValueType or value is None:
                self._facetValueType = value
            else:
                raise ValueError(f"The facet value dim_type {value} is not recognised")
        else:
            raise ValueError("Facet value dim_type should be of the str dim_type")


class Representation(DataParser):
    """The allowable value or format for Component or Concept"""

    def __init__(self, facets: List[Facet] = None, codelist=None, conceptScheme=None, gdscollector_=None):
        super().__init__(gds_collector_=gdscollector_)
        self.codelist = codelist
        self.concept_scheme = conceptScheme
        self._type = None
        self._facets = []
        if facets is not None:
            for f in facets:
                self.add_facet(f)

    def __eq__(self, other):
        if isinstance(other, Representation):
            return self._codelist == other._codelist and self._conceptScheme == other._conceptScheme \
                   and self._type == other._type
        else:
            return False

    def __str__(self):
        return f'<{self.__class__.__name__} - {self.facets} - {self.type_}>'

    def __unicode__(self):
        return f'<{self.__class__.__name__} - {self.facets} - {self.type_}>'

    def __repr__(self):
        return f'<{self.__class__.__name__} - {self.facets} - {self.type_}>'

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of Representation"""
        return Representation(*args_, **kwargs_)

    @property
    def facets(self):
        """list of Facets found"""
        return self._facets

    @property
    def codelist(self):
        """Reference to the codelist"""
        return self._codelist

    @property
    def concept_scheme(self):
        """Reference to the ConceptScheme (only in MeasureDimension)"""
        return self._conceptScheme

    @codelist.setter
    def codelist(self, value):
        self._codelist = value

    @concept_scheme.setter
    def concept_scheme(self, value):
        self._conceptScheme = value

    @facets.setter
    def facets(self, value):
        self._facets = value

    def add_facet(self, value):
        """Add a facet to the list"""
        self._facets.append(value)

    @property
    def type_(self):
        """Specifies the basic type of the component (String, BigInteger...)"""
        return self._type

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'Enumeration':
            obj_ = EnumerationType._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self.codelist = obj_.codelist
        elif nodeName_ == 'TextFormat' or nodeName_ == 'EnumerationFormat':
            obj_ = FormatType._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._type = obj_.type_
            self.facets = obj_.facets


class EnumerationType(DataParser):
    """Parser of the XML element Enumeration"""

    def __init__(self, codelist=None, gdscollector_=None, **kwargs_):
        super().__init__(gds_collector_=gdscollector_, **kwargs_)
        self._codelist = codelist

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of EnumerationType"""
        return EnumerationType(*args_, **kwargs_)

    @property
    def codelist(self):
        """Reference to the Codelist by its unique ID"""
        return self._codelist

    @codelist.setter
    def codelist(self, value):
        self._codelist = value

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'Ref':
            obj_ = RefBaseType._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            if obj_.package is not None and obj_.package == 'codelist':
                self.codelist = f'{obj_.agencyID}:{obj_.id_}({obj_.version})'


class FormatType(DataParser):
    """Parser of the EnumerationFormat or TextFormat XML element"""

    def __init__(self, facets=None, type_=None, gdscollector_=None, **kwargs_):
        super().__init__(gds_collector_=gdscollector_, **kwargs_)

        if facets is None:
            self._facets = []
        else:
            self._facets = facets

        self._type = type_

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of FormatType"""
        return FormatType(**kwargs_)

    @property
    def type_(self):
        """Specifies the basic type of the component (String, BigInteger...)"""
        return self._type

    @type_.setter
    def type_(self, value):
        self._type = value

    @property
    def facets(self):
        """List of Facet"""
        return self._facets

    @facets.setter
    def facets(self, value):
        if value is None:
            self._facets = []
        elif isinstance(value, list):
            self._facets = value
        else:
            raise TypeError('Value must be a list')

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        value = find_attr_value_('isSequence', node)
        if value is not None and 'isSequence' not in already_processed:
            already_processed.add('isSequence')
            value = self._gds_validate_boolean(value)
            self.facets.append(Facet(facetType='isSequence', facetValue=value))

        value = find_attr_value_('minLength', node)
        if value is not None and 'minLength' not in already_processed:
            already_processed.add('minLength')
            self.facets.append(Facet(facetType='minLength', facetValue=value))

        value = find_attr_value_('maxLength', node)
        if value is not None and 'maxLength' not in already_processed:
            already_processed.add('maxLength')
            self.facets.append(Facet(facetType='maxLength', facetValue=value))

        value = find_attr_value_('minValue', node)
        if value is not None and 'minValue' not in already_processed:
            already_processed.add('minValue')
            value = self._gds_validate_decimal(value)
            self.facets.append(Facet(facetType='minValue', facetValue=value))

        value = find_attr_value_('maxValue', node)
        if value is not None and 'maxValue' not in already_processed:
            already_processed.add('maxValue')
            value = self._gds_validate_decimal(value)
            self.facets.append(Facet(facetType='maxValue', facetValue=value))

        value = find_attr_value_('startValue', node)
        if value is not None and 'startValue' not in already_processed:
            already_processed.add('startValue')
            value = self._gds_validate_decimal(value)
            self.facets.append(Facet(facetType='startValue', facetValue=value))

        value = find_attr_value_('endValue', node)
        if value is not None and 'endValue' not in already_processed:
            already_processed.add('endValue')
            value = self._gds_validate_decimal(value)
            self.facets.append(Facet(facetType='endValue', facetValue=value))

        value = find_attr_value_('interval', node)
        if value is not None and 'interval' not in already_processed:
            already_processed.add('interval')
            value = self._gds_validate_double(value)
            self.facets.append(Facet(facetType='interval', facetValue=value))

        value = find_attr_value_('timeInterval', node)
        if value is not None and 'timeInterval' not in already_processed:
            already_processed.add('timeInterval')
            value = self._gds_validate_duration(value)
            self.facets.append(Facet(facetType='timeInterval', facetValue=value))

        value = find_attr_value_('decimals', node)
        if value is not None and 'decimals' not in already_processed:
            already_processed.add('decimals')
            value = self._gds_validate_integer(value)
            self.facets.append(Facet(facetType='decimals', facetValue=value))

        value = find_attr_value_('pattern', node)
        if value is not None and 'pattern' not in already_processed:
            already_processed.add('pattern')
            self.facets.append(Facet(facetType='pattern', facetValue=value))

        value = find_attr_value_('startTime', node)
        if value is not None and 'startTime' not in already_processed:
            already_processed.add('startTime')
            value = self._gds_validate_date(value)
            self.facets.append(Facet(facetType='startTime', facetValue=value))

        value = find_attr_value_('endTime', node)
        if value is not None and 'endTime' not in already_processed:
            already_processed.add('endTime')
            value = self._gds_validate_date(value)
            self.facets.append(Facet(facetType='endTime', facetValue=value))

        value = find_attr_value_('textType', node)
        if value is not None and 'textType' not in already_processed:
            already_processed.add('textType')
            self.type_ = value
