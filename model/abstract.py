"""
    SDMX Information Model (SDMX-IM).

    This module implements the base structures in the SDMX IM
"""


from datetime import date, datetime
from lxml import etree
from typing import List, Dict

class LocalisedString(object):
    def __init__(self, locale:str, label:str):
        if not isinstance(label,str):
            raise TypeError("Label should be a string")
        if not isinstance(locale,str):
            raise TypeError("Locale should be a string")
        self.label=label
        self.locale=locale
    
    def __str__(self):
        return f"{self.locale} - {self.label}"

class InternationalString(object):
    """
        SDMX-IM InternationalString.
    """

    def __init__(self, localisedStrings: list = []):
        self._localisedStrings=[]
        self._localisedStringsDict = {}
        for l in localisedStrings:
            self.addLocalisedString(l)

    @property
    def localisedStrings(self):
        return self._localisedStrings
    
    def addLocalisedString(self, localisedString:LocalisedString):
        if not isinstance(localisedString,LocalisedString):
            raise TypeError("International strings can only get localised strings as arguments")
        else:
            self._localisedStrings.append(localisedString)
            self._localisedStringsDict[localisedString.locale] = localisedString.label
    
    def getLocalisedString(self, locale: str):
        if locale in self._localisedStringsDict:
            return self._localisedStringsDict[locale]
        else:
            return ""
    
    def getLocales(self):
        return set(self._localisedStringsDict.keys())

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
        self._id = str(value)

    @title.setter 
    def title(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("Title should be a string")
        else:
            self._title = value

    @type.setter 
    def type(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("Type should be a string")
        else:
            self._type = value

    @url.setter 
    def url(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("URL should be a string")
        else:
            self._url = value
    
    @text.setter 
    def text(self, value):
        if not isinstance(value, InternationalString) and value is not None:
            raise TypeError("Text should be a LocalisedString")
        else:
            self._text = value

class AnnotableArtefact(object):
    def __init__(self, annotations: List[Annotation] = []):
        self._annotations=[]

        if isinstance(annotations, list):    
            for a in annotations:
                self.addAnnotation(a)
        else:
            raise TypeError("Annotations passed to Annotable artefacts can only be a list of Annotation objects or a single Annotation")
    
    @property
    def annotations(self):
        return self._annotations

    def addAnnotation(self, annotation: Annotation):
        if not isinstance(annotation, Annotation):
            raise TypeError("Annotable artefacts can only get annotations as arguments")
        else:
            self._annotations.append(annotation)

class IdentifiableArtefact(AnnotableArtefact):
    def __init__(self, id_: str = None, uri: str = None, annotations:  List[Annotation] = []):

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
        self._id = str(value)
    
    @uri.setter
    def uri(self, value):
        if isinstance(value, str) or value is None:
            self._uri = value
        else:
            raise ValueError("The uri has to be a string")
    
    @property
    def urn(self):
        try:
            urn = f"urn:sdmx:org.sdmx.infomodel.{self._urnType}.{self._qName.split('}')[1]}={self.id}" #TOBECHECKED
        except:
            urn = ""
        return urn

    def toXml(self):
        if hasattr(self, '_qName'):
            xml=etree.Element(self._qName)
            xml.attrib["urn"]=self.urn
            xml.attrib["id"]=self.id

            return xml
        else:
            raise AttributeError("XML cannot be generated because the identifiable object does not have a qName")

class NameableArtefact(IdentifiableArtefact):
    def __init__(self, id_: str = None, uri: str = None, annotations: List[Annotation] = [], 
                    name: InternationalString = None, description: InternationalString = None):
        
        super(NameableArtefact, self).__init__(id_ = id_, uri = uri, annotations= annotations)
                
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
        if not isinstance(value, InternationalString) and value is not None:
            raise TypeError("Name should be a LocalisedString")
        else:
            self._name = value

    @description.setter
    def description(self, value):
        if not isinstance(value, InternationalString) and value is not None:
            raise TypeError("Descritpion should be a LocalisedString")
        else:
            self._description = value

    def toXml(self):
        xml = super(IdentifiableArtefact, self).toXml()

        if self.name is not None and self.name.localisedStrings!=[]:
            for l in self.name.localisedStrings:
                nameXml=etree.Element("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common}Name")
                nameXml.attrib["{http://www.w3.org/XML/1998/namespace}lang"] =l.locale
                nameXml.text=l.label
                xml.append(nameXml)
        elif self.name.localisedStrings==[]:
            nameXml=etree.Element("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common}Name")
            nameXml.attrib["{http://www.w3.org/XML/1998/namespace}lang"] ="en"
            nameXml.text="Default name"
            xml.append(nameXml)

        if self.description is not None:
            for l in self.description.localisedStrings:
                descriptionXml=etree.Element("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common}Description")
                descriptionXml.attrib["{http://www.w3.org/XML/1998/namespace}lang"] =l.locale
                descriptionXml.text=l.label
                xml.append(descriptionXml)
        
        return xml

class VersionableArtefact(NameableArtefact):
    def __init__(self, id_: str = None, uri: str = None, annotations: List[Annotation] = [], 
                    name: InternationalString = None, description: InternationalString = None,
                    version: str = None, validFrom: datetime = None, validTo: datetime= None):

        super(VersionableArtefact, self).__init__(id_ = id_, uri = uri, annotations= annotations,
                                                  name = name, description = description)
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
        self._version = str(value)

    @validFrom.setter 
    def validFrom(self, value):
        if isinstance(value, datetime) or value is None:
            self._validFrom=value
        else:
            raise TypeError("valid from has to be a date or datetime object")
    
    @validTo.setter 
    def validTo(self, value):
        if isinstance(value, datetime) or value is None:
            self._validTo=value
        else:
            raise TypeError("valid to has to be a date or datetime object")

    def setValidFromString(self, date: str, format_: str = "%Y-%m-%d"):
        try:
            self._validFrom = datetime.strptime(date, format_)
        except:
            raise ValueError(f"Wrong date string format. The format {format_} should be followed")
    
    def setValidToString(self, date: str, format_: str = "%Y-%m-%d"):
        try:
            self._validTo = datetime.strptime(date, format_)
        except:
            raise ValueError(f"Wrong date string format. The format {format_} should be followed")

    def getValidFromString(self,  format_: str = "%Y-%m-%d"):
        if self.validFrom is None:
            return ""
        else:
            return datetime.strftime(self.validFrom, format_)

    def getValidToString(self,  format_: str = "%Y-%m-%d"):
        if self.validTo is None:
            return ""
        else:
            return datetime.strftime(self.validTo, format_)

    @property   
    def urn(self):
        try:
            urn = f"urn:sdmx:org.sdmx.infomodel.{self._urnType}.{self._qName.split('}')[1]}={self.id}({self.version})" #TOBECHECKED
        except:
            urn = ""
        return urn

    def toXml(self):
        xml=super().toXml()
        xml.attrib["version"]=self.version

        return xml

class Agency(NameableArtefact):
    pass

class MaintainableArtefact(VersionableArtefact):
    def __init__(self, id_: str = None, uri: str = None, annotations: List[Annotation] = [], 
                name: InternationalString = None, description: InternationalString = None,
                version: str = None, validFrom: datetime = None, validTo: datetime= None,
                isFinal: bool = None, isExternalReference: bool = None, serviceUrl: str = None, 
                    structureUrl: str = None, agency: Agency = None):

        super(MaintainableArtefact, self).__init__(id_ = id_, uri = uri, annotations= annotations,
                                                name = name, description = description,
                                                version = version, validFrom = validFrom, validTo = validTo)

        self.isFinal = isFinal
        self.isExternalReference = isExternalReference
        self.serviceUrl = serviceUrl
        self.structureUrl = structureUrl
        self.agency = agency

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
    def agency(self):
        return self._agency

    @isFinal.setter
    def isFinal(self, value):
        if isinstance(value, bool) or value is None:
            self._isFinal = value
        else:
            raise ValueError("The attribute isFinal should be of the bool type")

    @isExternalReference.setter
    def isExternalReference(self, value):
        if isinstance(value, bool) or value is None:
            self._isExternalReference = value
        else:
            raise ValueError("The attribute isExternalReference should be of the bool type")

    @serviceUrl.setter
    def serviceUrl(self, value):
        if isinstance(value, str) or value is None:
            self._serviceUrl = value
        else:
            raise ValueError("The attribute serviceUrl should be of the str type")
    
    @structureUrl.setter
    def structureUrl(self, value):
        if isinstance(value, str) or value is None:
            self._structureUrl = value
        else:
            raise ValueError("The attribute structureUrl should be of the str type")

    @agency.setter #TOBECHECKED. HOW TO IMPORT IT FROM ANOTHER MODULE?
    def agency(self, value):
        if isinstance(value, Agency) or value is None:
            self._agency = value
        else:
            raise TypeError("The agency has to be an instance of Agency")

    @property   
    def urn(self):
        try:
            urn = f"urn:sdmx:org.sdmx.infomodel.{self._urnType}.{self._qName.split('}')[1]}={self.agency.id}:{self.id}({self.version})" #TOBECHECKED
        except:
            urn = ""
        return urn

    def toXml(self):
        xml=super().toXml()
        if self.__class__.__name__=="AgencyList":
            xml.attrib["agencyID"]="SDMX"   
        else:
            xml.attrib["agencyID"]=self.agency.id
        xml.attrib["isExternalReference"]="false" if self.isExternalReference != True else "true"
        xml.attrib["isFinal"]="false" if self.final != True else "true"

        return xml



