"""
SDMX Base package.

Please refer to the package in the SDMX Information Model

"""

from datetime import datetime
from typing import List

from .utils import stringSetter, dateSetter, setDateFromString, getDateString, boolSetter
from ..utils.data_parser import DataParser
from ..utils.mappings import Locale_Codes
from ..utils.xml_base import find_attr_value_


class LocalisedString(DataParser):
    """LocalisedString class.

        The Localised String supports the representation
        of text in one locale (locale is similar to language but
        includes geographic variations such as Canadian
        French, US English etc.). 

    Attributes:
        label: Label of the string
        locale: The geographic locale of the string
    """

    def __init__(self, locale: str = None, label: str = None, content: str = None, gds_collector=None):
        """Inits LocalisedString with optional attributes."""

        super().__init__(gds_collector)
        self.label = label
        self._locale = locale
        self._content = content

    @staticmethod
    def factory():
        return LocalisedString()

    @property
    def locale(self):
        return self._locale

    @locale.setter
    def locale(self, value):
        self._locale = stringSetter(value)

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = stringSetter(value)

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = stringSetter(value)

    def build_attributes(self, node, attrs, already_processed):
        value = find_attr_value_('{http://www.w3.org/XML/1998/namespace}lang', node)
        if value is not None and 'lang' not in already_processed:
            already_processed.add('lang')
            self._label = value
            if value in Locale_Codes.keys():
                self._locale = Locale_Codes[value]
            else:
                raise ValueError(f'{value} is not in ISO 639-1 Codes')
        if node.text.strip() not in ['', '\n']:
            self._content = node.text

    def build_children(self, child, node, node_name_, gds_collector_):
        pass


class InternationalString(object):
    """InternationalString class.

        The International String is a collection of Localised
        Strings and supports the representation of text in
        multiple locales. 

    Attributes:
        localisedStrings: List with all the localised strings belonging to the InternationalString
        localisedStrings Dict: Convenience access to the localised strings. Dict[locale:label]

    Index:
        A locale in the index returns the label
    """

    def __init__(self, localisedStrings: List[LocalisedString] = None):
        """Inits InternationalString with optional attributes."""

        if localisedStrings is None:
            self._items = {}
        else:
            for record in localisedStrings:
                self.addLocalisedString(record)

    @property
    def items(self):
        return self._items

    def addLocalisedString(self, localisedString: LocalisedString):
        if not isinstance(localisedString, LocalisedString):
            raise TypeError("International strings can only get localised strings as arguments")
        else:
            self._items[localisedString.label] = {'locale': localisedString.locale,
                                                  'content': localisedString.content}

    def getLocales(self):
        return set(self._items.keys())

    def __getitem__(self, key):
        return self._items[key]

    def __str__(self):
        return str(self._items)


class AnnotationType(DataParser):
    """_annotationType provides for non-documentation notes and annotations to
    be embedded in data and structure messages. It provides optional fields
    for providing a title, a dim_type description, a URI, and the text of the
    annotation.The id_ attribute provides a non-standard identification of
    an annotation. It can be used to disambiguate annotations."""
    __hash__ = DataParser.__hash__
    subclass = None
    superclass = None

    def __init__(self, idx=None, annotation_title=None, annotation_type_member=None, annotation_URL=None,
                 annotation_text: InternationalString = None, gds_collector_=None):
        super(AnnotationType, self).__init__(gds_collector_)
        self.gds_collector_ = gds_collector_
        self._id = idx
        self._annotationTitle = annotation_title
        self._annotationType = annotation_type_member
        self._annotationURL = annotation_URL
        self._annotationText = annotation_text

    @staticmethod
    def factory(*args_, **kwargs_):
        return AnnotationType(*args_, **kwargs_)

    @property
    def annotation_title(self):
        return self._annotationTitle

    @annotation_title.setter
    def annotation_title(self, value):
        self._annotationTitle = value

    @property
    def annotation_type(self):
        return self._annotationType

    @annotation_type.setter
    def annotation_type(self, value):
        self._annotationType = value

    @property
    def annotation_url(self):
        return self._annotationURL

    @annotation_url.setter
    def annotation_url(self, value):
        self._annotationURL = value

    @property
    def annotation_text(self):
        if self._annotationText is None:
            return None
        elif isinstance(self._annotationText, InternationalString):
            if len(self._annotationText.items) == 0:
                return None
            elif len(self._annotationText.items) == 1:
                values_view = self._annotationText.items.values()
                value_iterator = iter(values_view)
                first_value = next(value_iterator)
                return first_value['content']
            else:
                return self._annotationText.items
        return self._annotationText

    @annotation_text.setter
    def annotation_text(self, value):
        self._annotationText = value

    @property
    def id_(self):
        return self._id

    def has_content_(self):
        if (
                self._annotationTitle is not None or
                self._annotationType is not None or
                self._annotationURL is not None or
                self._annotationText
        ):
            return True
        else:
            return False

    def build_attributes(self, node, attrs, already_processed):
        value = find_attr_value_('id', node)

        if value is not None and 'id' not in already_processed:
            already_processed.add('id')
            self._id = value

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'AnnotationTitle':
            value_ = child_.text
            value_ = self.gds_parse_string(value_)
            value_ = self.gds_validate_string(value_)
            self._annotationTitle = value_
        elif nodeName_ == 'AnnotationType':
            value_ = child_.text
            value_ = self.gds_parse_string(value_)
            value_ = self.gds_validate_string(value_)
            self._annotationType = value_
        elif nodeName_ == 'AnnotationURL':
            value_ = child_.text
            value_ = self.gds_parse_string(value_)
            value_ = self.gds_validate_string(value_)
            self._annotationURL = value_
        elif nodeName_ == 'AnnotationText':
            obj_ = LocalisedString.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            if self._annotationText is None:
                self._annotationText = InternationalString()
            self._annotationText.addLocalisedString(obj_)


class Annotation(DataParser):
    def __init__(self, id_: str = None, title: str = None, type_: str = None,
                 url: str = None, text: InternationalString = None, gds_collector=None):
        super(Annotation, self).__init__(gds_collector_=gds_collector)
        self.id = id_
        self.title = title
        self.type = type_
        self.url = url
        self.text = text

    @staticmethod
    def factory(*args_, **kwargs_):
        return Annotation(*args_, **kwargs_)

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def type(self):
        return self._type

    @property
    def url(self):
        return self._url

    @property
    def text(self):
        return self._text

    @id.setter
    def id(self, value):
        self._id = stringSetter(value)

    @title.setter
    def title(self, value):
        self._title = stringSetter(value)

    @type.setter
    def type(self, value):
        self._type = stringSetter(value)

    @url.setter
    def url(self, value):
        self._url = stringSetter(value)

    @text.setter
    def text(self, value):
        self._text = value

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Annotation':
            obj_ = AnnotationType.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self.text = obj_.annotation_text
            self.title = obj_.annotation_title
            self.type = obj_.annotation_type
            self.url = obj_.annotation_url


class AnnotableArtefact(DataParser):
    def __init__(self, annotations: List[Annotation] = None, gds_collector=None):

        super().__init__(gds_collector_=gds_collector)
        self._annotations = []

        if isinstance(annotations, list):
            for a in annotations:
                self.addAnnotation(a)
        elif annotations is None:
            self._annotations = []
        else:
            raise TypeError("Annotations passed to Annotable artefacts can only be a list of Annotation objects "
                            "or a single Annotation")

    @property
    def annotations(self):
        return self._annotations

    def addAnnotation(self, annotation: Annotation):
        if not isinstance(annotation, Annotation):
            raise TypeError("Annotable artefacts can only get annotations as arguments")
        else:
            self._annotations.append(annotation)

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Annotations':
            obj_ = Annotation.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            self.addAnnotation(obj_)


class IdentifiableArtefact(AnnotableArtefact):
    _qName = None
    _urnType = None

    def __init__(self, id_: str = None, uri: str = None, annotations: List[Annotation] = None):
        if annotations is None:
            annotations = []

        super(IdentifiableArtefact, self).__init__(annotations=annotations)

        self.id = id_
        self.uri = uri

    @property
    def id(self):
        return self._id

    @property
    def uri(self):
        return self._uri

    @id.setter
    def id(self, value):
        self._id = stringSetter(value, "[A-Za-z0-9_@$-]+")

    @uri.setter
    def uri(self, value):
        self._uri = stringSetter(value)

    def build_attributes(self, node, attrs, already_processed):
        value = find_attr_value_('id', node)
        if value is not None and 'id' not in already_processed:
            already_processed.add('id')
            self.id = value

        value = find_attr_value_('urn', node)
        if value is not None and 'urn' not in already_processed:
            already_processed.add('urn')
            self.uri = value

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        super(IdentifiableArtefact, self).build_children(child_, node, nodeName_, fromsubclass_, gds_collector_)


class NameableArtefact(IdentifiableArtefact):
    def __init__(self, id_: str = None, uri: str = None, annotations: List[Annotation] = None,
                 name: InternationalString = None, description: InternationalString = None):
        if annotations is None:
            annotations = []

        super(NameableArtefact, self).__init__(id_=id_, uri=uri, annotations=annotations)

        self._name = name
        self._description = description

    @property
    def name(self):
        if self._name is None:
            return None
        elif isinstance(self._name, InternationalString):
            if len(self._name.items) == 0:
                return None
            elif len(self._name.items) == 1:
                values_view = self._name.items.values()
                value_iterator = iter(values_view)
                first_value = next(value_iterator)
                return first_value['content']
            else:
                return self._name.items
        return self._name

    @property
    def description(self):
        if self._description is None:
            return None
        elif isinstance(self._description, InternationalString):
            if len(self._description.items) == 0:
                return None
            elif len(self._description.items) == 1:
                values_view = self._description.items.values()
                value_iterator = iter(values_view)
                first_value = next(value_iterator)
                return first_value['content']
            else:
                return self._description.items
        return self._description

    @name.setter
    def name(self, value):
        self._name = value

    @description.setter
    def description(self, value):
        self._description = value

    def build_attributes(self, node, attrs, already_processed):
        super(NameableArtefact, self).build_attributes(node, attrs, already_processed)

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        super(NameableArtefact, self).build_children(child_, node, nodeName_, fromsubclass_, gds_collector_)
        if nodeName_ == 'Name':
            obj_ = LocalisedString.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            if self._name is None:
                self._name = InternationalString()
            self._name.addLocalisedString(obj_)
        elif nodeName_ == 'Description':
            obj_ = LocalisedString.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            if self._description is None:
                self._description = InternationalString()
            self._description.addLocalisedString(obj_)


class VersionableArtefact(NameableArtefact):
    def __init__(self, id_: str, uri: str = None, annotations: List[Annotation] = None,
                 name: str = None, description: str = None,
                 version: str = "1.0", validFrom: datetime = None, validTo: datetime = None):
        if annotations is None:
            annotations = []

        super(VersionableArtefact, self).__init__(id_=id_, uri=uri, annotations=annotations,
                                                  name=name, description=description)
        self.version = version
        self.validFrom = validFrom
        self.validTo = validTo

    @property
    def version(self):
        return self._version

    @property
    def validFrom(self):
        return self._validFrom

    @property
    def validTo(self):
        return self._validTo

    @version.setter
    def version(self, value):
        self._version = stringSetter(value, pattern="[0-9]+(.[0-9]+)*")

    @validFrom.setter
    def validFrom(self, value):
        self._validFrom = dateSetter(value)

    @validTo.setter
    def validTo(self, value):
        self._validTo = dateSetter(value)

    def setValidFromString(self, date: str, format_: str = "%Y-%m-%d"):
        self._validFrom = setDateFromString(date, format_)

    def setValidToString(self, date: str, format_: str = "%Y-%m-%d"):
        self._validTo = setDateFromString(date, format_)

    def getValidFromString(self, format_: str = "%Y-%m-%d"):
        return getDateString(self.validFrom, format_)

    def getValidToString(self, format_: str = "%Y-%m-%d"):
        return getDateString(self.validTo, format_)

    def build_attributes(self, node, attrs, already_processed):
        super(VersionableArtefact, self).build_attributes(node, attrs, already_processed)

        value = find_attr_value_('version', node)
        if value is not None and 'version' not in already_processed:
            already_processed.add('version')
            # TODO Validate version
            self.version = value

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        super(VersionableArtefact, self).build_children(child_, node, nodeName_, fromsubclass_, gds_collector_)


class MaintainableArtefact(VersionableArtefact):
    def __init__(self, id_: str = None, uri: str = None, annotations: List[Annotation] = None,
                 name: str = None, description: str = None,
                 version: str = None, validFrom: datetime = None, validTo: datetime = None,
                 isFinal: bool = False, isExternalReference: bool = False, serviceUrl: str = None,
                 structureUrl: str = None, maintainer=None):
        if annotations is None:
            annotations = []
        super(MaintainableArtefact, self).__init__(id_=id_, uri=uri, annotations=annotations,
                                                   name=name, description=description,
                                                   version=version, validFrom=validFrom, validTo=validTo)

        self.isFinal = isFinal
        self.isExternalReference = isExternalReference
        self.serviceUrl = serviceUrl
        self.structureUrl = structureUrl
        self.maintainer = maintainer
        if id_ is not None and maintainer is not None and version is not None:
            self._unique_id = f'{maintainer.id}:{id_}({version})'
        else:
            self._unique_id = None

    @property
    def unique_id(self):

        if isinstance(self.maintainer, str):
            return f'{self.maintainer}:{self.id}({self.version})'
        else:
            return f'{self.maintainer.id}:{self.id}({self.version})'

    @property
    def isFinal(self):
        return self._isFinal

    @property
    def isExternalReference(self):
        return self._isExternalReference

    @property
    def serviceUrl(self):
        return self._serviceUrl

    @property
    def structureUrl(self):
        return self._structureUrl

    @property
    def maintainer(self):
        return self._maintainer

    @isFinal.setter
    def isFinal(self, value):
        self._isFinal = boolSetter(value)

    @isExternalReference.setter
    def isExternalReference(self, value):
        self._isExternalReference = boolSetter(value)

    @serviceUrl.setter
    def serviceUrl(self, value):
        self._serviceUrl = stringSetter(value)

    @structureUrl.setter
    def structureUrl(self, value):
        self._structureUrl = stringSetter(value)

    @maintainer.setter
    def maintainer(self, value):
        self._maintainer = value

    @property
    def agencyID(self):
        if self.maintainer is not None:
            if isinstance(self.maintainer, str):
                return self.maintainer
            else:
                return self.maintainer.id
        else:
            return None

    def build_attributes(self, node, attrs, already_processed):

        super(MaintainableArtefact, self).build_attributes(node, attrs, already_processed)

        value = find_attr_value_('agencyID', node)
        if value is not None and 'agencyID' not in already_processed:
            already_processed.add('agencyID')
            self.maintainer = value

        value = find_attr_value_('isExternalReference', node)
        if value is not None and 'isExternalReference' not in already_processed:
            already_processed.add('isExternalReference')
            value = self.gds_parse_boolean(value)
            self.isExternalReference = value

        value = find_attr_value_('isFinal', node)
        if value is not None and 'isFinal' not in already_processed:
            already_processed.add('isFinal')
            value = self.gds_parse_boolean(value)
            self.isFinal = value

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        super(MaintainableArtefact, self).build_children(child_, node, nodeName_, fromsubclass_, gds_collector_)
