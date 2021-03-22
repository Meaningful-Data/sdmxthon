"""
SDMX Base package.

Please refer to the package in the SDMX Information Model

"""

from datetime import datetime
from typing import List

from SDMXThon.parsers.data_parser import DataParser
from SDMXThon.utils.mappings import Locale_Codes, commonAbbr
from SDMXThon.utils.xml_base import find_attr_value_
from .utils import stringSetter, boolSetter


class LocalisedString(DataParser):
    """The Localised String supports the representation
       of text in one locale (locale is similar to language but
       includes geographic variations such as Canadian
       French, US English etc.).
    """

    def __init__(self, locale: str = None, label: str = None, content: str = None, gds_collector=None):
        """Inits LocalisedString with optional attributes."""

        super().__init__(gds_collector)
        self.label = label
        self._locale = locale
        self._content = content

    def __eq__(self, other):
        if isinstance(other, LocalisedString):
            return self._locale == other._locale and self._content == other._content and self._label == other._label
        else:
            return False

    @staticmethod
    def _factory(*args):
        """Factory Method of LocalisedString"""
        return LocalisedString(*args)

    @property
    def locale(self):
        """Locale is the name of the country. Obtained from the
        `ISO 639-1 code <https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes>`_"""
        return self._locale

    @locale.setter
    def locale(self, value):
        self._locale = stringSetter(value)

    @property
    def label(self):
        """Label present in attribute lang of the XML namespace. Uses an ISO 639-1 code to specify the country"""
        return self._label

    @label.setter
    def label(self, value):
        self._label = stringSetter(value)

    @property
    def content(self):
        """Added attribute to the Information Model to specify the string itself"""
        return self._content

    @content.setter
    def content(self, value):
        self._content = stringSetter(value)

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        value = find_attr_value_('{http://www.w3.org/XML/1998/namespace}lang', node)
        if value is not None and 'lang' not in already_processed:
            already_processed.add('lang')
            self._label = value
            if value in Locale_Codes.keys():
                self._locale = Locale_Codes[value]
            else:
                raise ValueError(f'{value} is not in ISO 639-1 Codes')
        if node.text.strip() not in ['', '\n']:
            self._content = " ".join(node.text.split())


class InternationalString(object):
    """The International String is a collection of Localised
       Strings and supports the representation of text in
       multiple locales.
    """

    def __init__(self, localisedStrings: List[LocalisedString] = None):
        """Inits InternationalString with optional attributes."""

        if localisedStrings is None:
            self._items = {}
        else:
            for record in localisedStrings:
                self.addLocalisedString(record)

    def __eq__(self, other):
        if isinstance(other, InternationalString):
            return self._items == other._items
        else:
            return False

    @property
    def items(self):
        """Items of the InternationalString"""
        return self._items

    def addLocalisedString(self, localisedString: LocalisedString):
        """Adds a localisedString to the International String"""
        if not isinstance(localisedString, LocalisedString):
            raise TypeError("International strings can only get localised strings as arguments")
        else:
            self._items[localisedString.label] = {'locale': localisedString.locale,
                                                  'content': localisedString.content}

    def getLabels(self):
        """Gets the labels of the items present in the International String"""
        return set(self._items.keys())

    def __getitem__(self, key):
        return self._items[key]

    def __str__(self):
        return str(self._items)

    def _to_XML(self, name, prettyprint):

        if prettyprint:
            child1 = '\t'
        else:
            child1 = ''

        outfile = []
        if len(self._items) > 0:
            for label, v in self._items.items():
                outfile.append(f'{child1}<{name} xml:lang="{label}">{v["content"].replace("&", "&amp;")}</{name}>')

        return outfile


class Annotation(DataParser):
    """Additional descriptive information attached to an object"""

    def __init__(self, id_: str = None, title: str = None, type_: str = None,
                 url: str = None, text: InternationalString = None, gds_collector=None):
        super(Annotation, self).__init__(gds_collector_=gds_collector)
        self.id = id_
        self.title = title
        self.type = type_
        self.url = url
        self.text = text

    def __eq__(self, other):
        if isinstance(other, Annotation):
            return self._id == other._id and self._title == other._title and self._type == other._type \
                   and self._url == other._url and self._text == other._text

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of Annotation"""
        return Annotation(*args_, **kwargs_)

    @property
    def id(self):
        """Identifier for the Annotation. It can be used to disambiguate one Annotation from another
            where there are several Annotations for the same annotated object."""
        return self._id

    @property
    def title(self):
        """A title used to identify an annotation."""
        return self._title

    @property
    def type(self):
        """Specifies how the annotation is to be processed"""
        return self._type

    @property
    def url(self):
        """A link to external descriptive text"""
        return self._url

    @property
    def text(self):
        """An International String provides the multilingual text content of the annotation via this role"""
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

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        value = find_attr_value_('id', node)

        if value is not None and 'id' not in already_processed:
            already_processed.add('id')
            self._id = value

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the attributes present in the XML element"""
        if nodeName_ == 'AnnotationTitle':
            value_ = child_.text
            value_ = self._gds_parse_string(value_)
            value_ = self._gds_validate_string(value_)
            self._title = value_
        elif nodeName_ == 'AnnotationType':
            value_ = child_.text
            value_ = self._gds_parse_string(value_)
            value_ = self._gds_validate_string(value_)
            self._type = value_
        elif nodeName_ == 'AnnotationURL':
            value_ = child_.text
            value_ = self._gds_parse_string(value_)
            value_ = self._gds_validate_string(value_)
            self._url = value_.strip()
        elif nodeName_ == 'AnnotationText':
            obj_ = LocalisedString._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            if self._text is None:
                self._text = InternationalString()
            self._text.addLocalisedString(obj_)


class AnnotationsType(DataParser):
    """Parser of the XML element Annotations"""

    def __init__(self, gds_collector_=None):
        super().__init__(gds_collector_)
        self._annotations = []

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of AnnotationsType"""
        return AnnotationsType(*args_, **kwargs_)

    @property
    def annotations(self):
        """The annotations included in the XML element Annotations"""
        return self._annotations

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'Annotation':
            obj_ = Annotation._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._annotations.append(obj_)


class AnnotableArtefact(DataParser):
    """Superclass of all artefacts. Contains the list of annotations."""

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

    def __eq__(self, other):
        if isinstance(other, AnnotableArtefact):
            return self._annotations == other._annotations

    @property
    def annotations(self):
        """List of the annotations of the element"""
        return self._annotations

    def addAnnotation(self, annotation: Annotation):
        """Method to add an annotation to the list"""
        if not isinstance(annotation, Annotation):
            raise TypeError("Annotable artefacts can only get annotations as arguments")
        else:
            self._annotations.append(annotation)

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'Annotations':
            obj_ = AnnotationsType._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._annotations = obj_.annotations

    def _to_XML(self, prettyprint):

        if prettyprint:
            child1 = '\t'
            child2 = '\t\t'
        else:
            child1 = child2 = ''
        if len(self.annotations) > 0:
            outfile = [f'<{commonAbbr}:Annotations>']
            for e in self.annotations:
                if e.id is None:
                    outfile.append(f'{child1}<{commonAbbr}:Annotation>')
                else:
                    outfile.append(f'{child1}<{commonAbbr}:Annotation id="{e.id}">')

                if e.title is not None and e.title != '':
                    outfile.append(f'{child2}<{commonAbbr}:AnnotationTitle>{e.title.replace("&", "&amp;")}'
                                   f'</{commonAbbr}:AnnotationTitle>')

                if e.type is not None and e.type != '':
                    outfile.append(f'{child2}<{commonAbbr}:AnnotationType>{e.type.replace("&", "&amp;")}'
                                   f'</{commonAbbr}:AnnotationType>')

                if e.url is not None and e.url != '':
                    outfile.append(f'{child2}<{commonAbbr}:AnnotationURL>{e.url.replace("&", "&amp;")}'
                                   f'</{commonAbbr}:AnnotationURL>')

                if e.text is not None:
                    outfile += [child1 + i for i in e._text._to_XML(f"{commonAbbr}:AnnotationText", prettyprint)]
                outfile.append(f'{child1}</{commonAbbr}:Annotation>')
            outfile.append(f'</{commonAbbr}:Annotations>')
            return outfile
        else:
            return None


class IdentifiableArtefact(AnnotableArtefact):
    """Provides identity to all derived classes. It also provides annotations to derived classes
       because it is a subclass of AnnotableArtefact.
    """

    def __init__(self, id_: str = None, uri: str = None, urn: str = None, annotations: List[Annotation] = None):

        super(IdentifiableArtefact, self).__init__(annotations=annotations)

        self.id = id_
        self.uri = uri
        self.urn = urn

    def __eq__(self, other):
        if isinstance(other, IdentifiableArtefact):
            return super(IdentifiableArtefact, self).__eq__(other) and self._id == other._id \
                   and self._uri == other._uri and self._urn == other._urn
        else:
            return False

    @property
    def id(self):
        """The unique identifier of the object."""
        return self._id

    @property
    def uri(self):
        """Universal resource identifier that may or may not be resolvable."""
        return self._uri

    @property
    def urn(self):
        """Universal resource name – this is for use in registries: all registered objects have a urn."""
        return self._urn

    @id.setter
    def id(self, value):
        self._id = value

    @uri.setter
    def uri(self, value):
        self._uri = value

    @urn.setter
    def urn(self, value):
        self._urn = value

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        value = find_attr_value_('id', node)
        if value is not None and 'id' not in already_processed:
            already_processed.add('id')
            self.id = value

        value = find_attr_value_('uri', node)
        if value is not None and 'uri' not in already_processed:
            already_processed.add('uri')
            self.uri = value

        value = find_attr_value_('urn', node)
        if value is not None and 'urn' not in already_processed:
            already_processed.add('urn')
            self.urn = value

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        super(IdentifiableArtefact, self)._build_children(child_, node, nodeName_, fromsubclass_, gds_collector_)

    def _to_XML(self, prettyprint) -> dict:

        attributes = ''

        if self.id is not None:
            attributes += f' id="{self.id}"'

        if self.uri is not None:
            attributes += f' uri="{self.uri}"'

        if self.urn is not None:
            attributes += f' urn="{self.urn}"'

        outfile = {'Annotations': super(IdentifiableArtefact, self)._to_XML(prettyprint), 'Attributes': attributes}

        return outfile


class NameableArtefact(IdentifiableArtefact):
    """Provides a Name and Description to all derived classes in addition to identification and annotations."""

    def __init__(self, id_: str = None, uri: str = None, urn=None, annotations: List[Annotation] = None,
                 name: InternationalString = None, description: InternationalString = None):
        super(NameableArtefact, self).__init__(id_=id_, uri=uri, urn=urn, annotations=annotations)

        self._name = name
        self._description = description

    def __eq__(self, other):
        if isinstance(other, NameableArtefact):
            return super(NameableArtefact, self).__eq__(other) and self._name == other._name \
                   and self._description == other._description
        else:
            return False

    @property
    def name(self):
        """A multi-lingual name is provided by this role via the International String class """
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
        """A multi-lingual description is provided by this role via the International String class."""
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

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(NameableArtefact, self)._build_attributes(node, attrs, already_processed)

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        super(NameableArtefact, self)._build_children(child_, node, nodeName_, fromsubclass_, gds_collector_)
        if nodeName_ == 'Name':
            obj_ = LocalisedString._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            if self._name is None:
                self._name = InternationalString()
            self._name.addLocalisedString(obj_)
        elif nodeName_ == 'Description':
            obj_ = LocalisedString._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            if self._description is None:
                self._description = InternationalString()
            self._description.addLocalisedString(obj_)

    def _to_XML(self, prettyprint) -> dict:
        outfile = super(NameableArtefact, self)._to_XML(prettyprint)

        if self.name is not None:
            outfile['Name'] = self._name._to_XML(f'{commonAbbr}:Name', prettyprint)

        if self._description is not None:
            outfile['Description'] = self._description._to_XML(f'{commonAbbr}:Description', prettyprint)

        return outfile


class VersionableArtefact(NameableArtefact):
    """Provides versioning information for all derived objects"""

    def __init__(self, id_: str, uri: str = None, urn=None, annotations: List[Annotation] = None,
                 name: str = None, description: str = None,
                 version: str = "1.0", validFrom: datetime = None, validTo: datetime = None):

        super(VersionableArtefact, self).__init__(id_=id_, uri=uri, urn=urn, annotations=annotations, name=name,
                                                  description=description)
        self.version = version
        self.validFrom = validFrom
        self.validTo = validTo

    def __eq__(self, other):
        if isinstance(other, VersionableArtefact):
            return super(VersionableArtefact, self).__eq__(other) and self._version == other._version \
                   and self._validFrom == other._validFrom and self._validTo == other._validTo
        else:
            return False

    @property
    def version(self):
        """A version string following an agreed convention"""
        return self._version

    @property
    def validFrom(self):
        """Date from which the version is valid"""
        return self._validFrom

    @property
    def validTo(self):
        """Date from which version is superseded"""
        return self._validTo

    @version.setter
    def version(self, value):
        self._version = stringSetter(value, pattern="[0-9]+(.[0-9]+)*")

    @validFrom.setter
    def validFrom(self, value):
        # self._validFrom = setDateFromString(value, "%Y-%m-%d")
        self._validFrom = value

    @validTo.setter
    def validTo(self, value):
        # self._validTo = setDateFromString(value, "%Y-%m-%d")
        self._validTo = value

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(VersionableArtefact, self)._build_attributes(node, attrs, already_processed)

        value = find_attr_value_('version', node)
        if value is not None and 'version' not in already_processed:
            already_processed.add('version')
            # TODO Validate version
            self.version = value

        value = find_attr_value_('validFrom', node)
        if value is not None and 'validFrom' not in already_processed:
            already_processed.add('validFrom')
            self.validFrom = value

        value = find_attr_value_('validTo', node)
        if value is not None and 'validTo' not in already_processed:
            already_processed.add('validTo')
            self.validTo = value

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        super(VersionableArtefact, self)._build_children(child_, node, nodeName_, fromsubclass_, gds_collector_)

    def _to_XML(self, prettyprint) -> dict:
        outfile = super(VersionableArtefact, self)._to_XML(prettyprint)

        if self.version is not None:
            outfile['Attributes'] += f' version="{self.version}"'

        if self.validFrom is not None:
            outfile['Attributes'] += f' validFrom="{self.validFrom}"'

        if self.validTo is not None:
            outfile['Attributes'] += f' validTo="{self.validTo}"'

        return outfile


class MaintainableArtefact(VersionableArtefact):
    """An abstract class to group together primary structural metadata artefacts
       that are maintained by an Agency."""

    def __init__(self, id_: str = None, uri: str = None, urn=None, annotations: List[Annotation] = None,
                 name: str = None, description: str = None,
                 version: str = None, validFrom: datetime = None, validTo: datetime = None,
                 isFinal: bool = False, isExternalReference: bool = False, serviceUrl: str = None,
                 structureUrl: str = None, maintainer=None):
        super(MaintainableArtefact, self).__init__(id_=id_, uri=uri, urn=urn, annotations=annotations,
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

    def __eq__(self, other):
        if isinstance(other, MaintainableArtefact):
            return super(MaintainableArtefact, self).__eq__(other) and self._isFinal == other._isFinal \
                   and self._isExternalReference == other._isExternalReference \
                   and self._serviceUrl == other._serviceUrl \
                   and self._structureUrl == other._structureUrl \
                   and self._maintainer == other._maintainer
        else:
            return False

    @property
    def unique_id(self):
        """Provides the unique id in the shape of AgencyID:ID(version)"""
        if isinstance(self.maintainer, str):
            return f'{self.maintainer}:{self.id}({self.version})'
        else:
            return f'{self.maintainer.id}:{self.id}({self.version})'

    @property
    def isFinal(self):
        """Defines whether a maintained artefact is draft or final"""
        return self._isFinal

    @property
    def isExternalReference(self):
        """If set to “true” it indicates that the content of the object is held externally."""
        return self._isExternalReference

    @property
    def serviceUrl(self):
        """The URL of an SDMX compliant web service from which the external object can be retrieved."""
        return self._serviceUrl

    @property
    def structureUrl(self):
        """The URL of an SDMX-ML document containing the external object."""
        return self._structureUrl

    @property
    def maintainer(self):
        """Association to the Maintenance Agency responsible for maintaining the artefact."""
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
        """Extracts the agencyID from the maintainer"""
        if self.maintainer is not None:
            if isinstance(self.maintainer, str):
                return self.maintainer
            else:
                return self.maintainer.id
        else:
            return None

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        super(MaintainableArtefact, self)._build_attributes(node, attrs, already_processed)

        value = find_attr_value_('agencyID', node)
        if value is not None and 'agencyID' not in already_processed:
            already_processed.add('agencyID')
            self.maintainer = value

        value = find_attr_value_('isExternalReference', node)
        if value is not None and 'isExternalReference' not in already_processed:
            already_processed.add('isExternalReference')
            value = self._gds_parse_boolean(value)
            self.isExternalReference = value

        value = find_attr_value_('isFinal', node)
        if value is not None and 'isFinal' not in already_processed:
            already_processed.add('isFinal')
            value = self._gds_parse_boolean(value)
            self.isFinal = value

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        """Builds the childs of the XML element"""
        super(MaintainableArtefact, self)._build_children(child_, node, nodeName_, fromsubclass_, gds_collector_)

    def _to_XML(self, prettyprint):
        outfile = super(MaintainableArtefact, self)._to_XML(prettyprint)

        if self.isExternalReference is not None:
            outfile['Attributes'] += f' isExternalReference="{str(self.isExternalReference).lower()}"'

        if self.isFinal is not None:
            outfile['Attributes'] += f' isFinal="{str(self.isFinal).lower()}"'

        if self.maintainer is not None:
            if isinstance(self.maintainer, str):
                outfile['Attributes'] += f' agencyID="{self.maintainer}"'
            else:
                outfile['Attributes'] += f' agencyID="{self.maintainer.id}"'

        return outfile
