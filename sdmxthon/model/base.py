"""
SDMX Base pacakage.

Please refer to the package in the SDMX Information Model

"""

from datetime import datetime
from typing import List

from lxml import etree

from .utils import (qName, stringSetter, dateSetter, setDateFromString,
                    getDateString, boolSetter, genericSetter)


class LocalisedString(object):
    """LocalisedString class.

        The Localised String supports the representation
        of text in one locale (locale is similar to language but
        includes geographic variations such as Canadian
        French, US English etc.). 

    Attributes:
        label: Label of the string
        locale: The geographic locale of the string
    """

    def __init__(self, locale: str = None, label: str = None):
        """Inits LocalisedString with optional attributes."""

        self.label = label
        self.locale = locale

    @property
    def locale(self):
        return self._locale

    @property
    def label(self):
        return self._label

    @locale.setter
    def locale(self, value):
        self._locale = stringSetter(value)

    @label.setter
    def label(self, value):
        self._label = stringSetter(value)

    @classmethod
    def fromXml(cls, elem: etree._Element):
        """Instantiates the object from lxml element.

        Receives an etree Element and instantiates the localises string

        Args:
            elem: an etree Element of the localised string

        Returns:
            A LocalisedString instance corresponding to the XML

        Raises:
            ValueError if the item is not an etree._Element
        """
        if not isinstance(elem, etree._Element):
            raise ValueError(f"etree._Element object required. {type(elem)} passed")

        locString = cls(label=elem.text, locale=elem.get(qName("xml", "lang")))

        return locString


class InternationalString(object):
    """InternationalString class.

        The International String is a collection of Localised
        Strings and supports the representation of text in
        multiple locales. 

    Attributes:
        localisedStrings: List with all the localised strings belonging to the InternationalString
        localisedStringsDict: Convenience access to the localised strings. Dict[locale:label]

    Index:
        A locale in the index returns the label
    """

    def __init__(self, localisedStrings: List[LocalisedString] = []):
        """Inits InternationalString with optional attributes."""
        self._localisedStrings = []
        self._localisedStringsDict = {}
        for l in localisedStrings:
            self.addLocalisedString(l)

    @property
    def localisedStrings(self):
        return self._localisedStrings

    @property
    def localisedStringsDict(self):
        return self._localisedStringsDict

    def addLocalisedString(self, localisedString: LocalisedString):
        if not isinstance(localisedString, LocalisedString):
            raise TypeError("International strings can only get localised strings as arguments")
        else:
            self._localisedStrings.append(localisedString)
            self._localisedStringsDict[localisedString.locale] = localisedString.label

    @classmethod
    def fromXml(cls, elems: List[etree.Element]):
        if elems != []:
            InternationalString = cls()

            for ls in elems:
                InternationalString.addLocalisedString(LocalisedString.fromXml(ls))

            return InternationalString

    def getLocales(self):
        return set(self._localisedStringsDict.keys())

    def __getitem__(self, key):
        return self._localisedStringsDict[key]

    def __str__(self):
        return str(self._localisedStringsDict)


class Annotation(object):
    def __init__(self, id_: str = None, title: str = None, type_: str = None,
                 url: str = None, text: InternationalString = None):
        self.id = id_
        self.title = title
        self.type = type_
        self.url = url
        self.text = text

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
        self._text = genericSetter(value, InternationalString)


class AnnotableArtefact(object):
    def __init__(self, annotations: List[Annotation] = []):
        self._annotations = []

        if isinstance(annotations, list):
            for a in annotations:
                self.addAnnotation(a)
        else:
            raise TypeError(
                "Annotations passed to Annotable artefacts can only be a list of Annotation objects or a single Annotation")

    @property
    def annotations(self):
        return self._annotations

    def addAnnotation(self, annotation: Annotation):
        if not isinstance(annotation, Annotation):
            raise TypeError("Annotable artefacts can only get annotations as arguments")
        else:
            self._annotations.append(annotation)


class IdentifiableArtefact(AnnotableArtefact):
    def __init__(self, id_: str = None, uri: str = None, annotations: List[Annotation] = []):

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
        self._id = stringSetter(value, "[A-Za-z0-9_@$\-]+")

    @uri.setter
    def uri(self, value):
        self._uri = stringSetter(value)

    @property
    def urn(self):
        try:
            urn = f"urn:sdmx:org.sdmx.infomodel.{self._urnType}.{etree.QName(self._qName).localname}={self.id}"  # TOBECHECKED
        except:
            urn = ""
        return urn


class NameableArtefact(IdentifiableArtefact):
    def __init__(self, id_: str = None, uri: str = None, annotations: List[Annotation] = [],
                 name: str = None, description: str = None):
        super(NameableArtefact, self).__init__(id_=id_, uri=uri, annotations=annotations)

        self.name = name
        self.description = description

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @name.setter
    def name(self, value):
        self._name = value

    @description.setter
    def description(self, value):
        self._description = value


class VersionableArtefact(NameableArtefact):
    def __init__(self, id_: str = None, uri: str = None, annotations: List[Annotation] = [],
                 name: str = None, description: str = None,
                 version: str = "1.0", validFrom: datetime = None, validTo: datetime = None):

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
        self._version = stringSetter(value, pattern="[0-9]+(\.[0-9]+)*")

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

    @property
    def urn(self):
        try:
            urn = f"urn:sdmx:org.sdmx.infomodel.{self._urnType}.{self._qName.split('}')[1]}={self.id}({self.version})"  # TOBECHECKED
        except:
            urn = ""
        return urn


class MaintainableArtefact(VersionableArtefact):
    def __init__(self, id_: str = None, uri: str = None, annotations: List[Annotation] = [],
                 name: str = None, description: str = None,
                 version: str = None, validFrom: datetime = None, validTo: datetime = None,
                 isFinal: bool = False, isExternalReference: bool = False, serviceUrl: str = None,
                 structureUrl: str = None, maintainer=None):

        super(MaintainableArtefact, self).__init__(id_=id_, uri=uri, annotations=annotations,
                                                   name=name, description=description,
                                                   version=version, validFrom=validFrom, validTo=validTo)

        self.isFinal = isFinal
        self.isExternalReference = isExternalReference
        self.serviceUrl = serviceUrl
        self.structureUrl = structureUrl
        self.maintainer = maintainer

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
        if value.__class__.__name__ == "Agency" or value is None:
            self._maintainer = value
        else:
            raise TypeError("The maintainer has to be an instance of Agency")

    @property
    def urn(self):
        try:
            urnType = self._urnType
            tag = etree.QName(self._qName).localname
            agencyId = self.agencyId

            urn = f"urn:sdmx:org.sdmx.infomodel.{urnType}.{tag}={agencyId}:{self.id}({self.version})"  # TOBECHECKED
        except:
            urn = ""
        return urn

    @property
    def agencyId(self):
        return self.maintainer.id if self.maintainer is not None else self._agencyId