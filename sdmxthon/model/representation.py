from typing import List

from sdmxthon.model.utils import FacetType, string_setter, FacetValueType


class Facet:
    """Defines the format for the content of the Component when reported in
    a data or metadata set. """

    def __init__(self, facetType: str = None, facetValue: str = None,
                 facetValueType: str = None):
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
        """A specific content type which is constrained by the FacetType
        enumeration """
        return self._facetType

    @property
    def facet_value(self):
        """The value of the Facet"""
        return self._facetValue

    @property
    def facet_value_type(self):
        """The format of the value of a Component when reported in a data or
        metadata set. This is constrained by the FacetValueType enumeration.
        """
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
                raise ValueError(
                    f"The facet value dim_type {value} is not recognised")
        else:
            raise ValueError(
                "Facet value dim_type should be of the str dim_type")


class Representation(object):
    """The allowable value or format for Component or Concept"""

    def __init__(self, facets: List[Facet] = None, codelist=None,
                 concept_scheme=None, text_type=None):
        self.codelist = codelist
        self.concept_scheme = concept_scheme
        self._type = text_type
        self._facets = []
        if facets is not None:
            for f in facets:
                self.add_facet(f)

    def __eq__(self, other):
        if isinstance(other, Representation):
            return (self._codelist == other._codelist and
                    self._conceptScheme == other._conceptScheme and
                    self._type == other._type)
        else:
            return False

    def __str__(self):
        return f'<{self.__class__.__name__} - {self.facets} - {self.type_}>'

    def __unicode__(self):
        return f'<{self.__class__.__name__} - {self.facets} - {self.type_}>'

    def __repr__(self):
        return f'<{self.__class__.__name__} - {self.facets} - {self.type_}>'

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
