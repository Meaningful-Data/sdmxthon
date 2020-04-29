from .abstract import NameableArtefact, MaintainableArtefact

class ItemScheme(MaintainableArtefact):
    # def __init___(self, url=None, id=None, annotations=[], version=None, validFrom=None, validTo=None,
    #                 final=None, isExternalReference=None, serviceUrl=None, structureUrl=None, isPartial=None, agency=None, items=[]):
    #     super().__init__(url, id, annotations, version, validFrom, validTo, 
    #                                     final, isExternalReference, serviceUrl, structureUrl, agency)

    def __init__(self):
        self._items=[]
        
        self._name=None
        self._description=None
        
        self.final=None
        self.isExternalReference=None
        self.serviceUrl=None
        self.structureUrl=None

        
        ####### DIRTY! Because I'm not able to do a right initialisation...
        if self.__class__.__name__=="ConceptScheme":        
            self._itemType="Concept"
            self._urnType="conceptscheme"
            self._qName="{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}ConceptScheme"

        if self.__class__.__name__=="CodeList":        
            self._itemType="Code"
            self._urnType="codelist"
            self._qName="{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}Codelist"

        #Why is it not initing from Maintainable, but only from Identifiable?
        super().__init__()
        # for i in items:
        #     self.addItem(i)

    @property
    def items(self):
        return self._items
    

    def addItem(self, value):
        if value is None:
            pass
        elif value.__class__.__name__==self._itemType:
            self._items.append(value)
        else:
            raise TypeError("The object has to be of the type {}".format(self._itemType.__class__.__name__))

    def toXml(self):
        xml=super().toXml()
        for i in self.items:
            xml.append(i.toXml())
        return xml


class Item(NameableArtefact):
    def __init__(self, url=None, id=None,  annotations=[], itemScheme=None, parent=None):
        self.parent=parent
       
        self._schemeType=None
        self._scheme=[]
        self.scheme=itemScheme
        
        self._name=None
        self._description=None
        
        super().__init__(url, id, annotations)

    @property
    def urn(self):
        return "urn:sdmx:org.sdmx.infomodel.{}.{}={}.{}".format(self._urnType, self._qName.split("}")[1], self.parent.urn.split("=")[1], self.id) 


    @property
    def scheme(self):
        return self._scheme
    
    @scheme.setter
    def scheme(self,value):
        if value is None:
            pass
        elif str(type(value))==self._schemeType:
            self._scheme=value
        else:
            raise TypeError("The scheme object has to be of the type {}".format(self._schemeType.__name__))

    @property
    def parent(self):
        return self._parent

    @parent.setter 
    def parent(self, value):
        if value==None:
            self._parent=None
        else:
        # elif value.__class__.__name__==self._schemeType:
            self._parent=value
        # else:
        #     raise TypeError("The parent of an Item has to be an Item scheme object")

class ConceptScheme(ItemScheme):
    def __init___(self):

        self._itemType="Concept"
        self._urnType="conceptscheme"
        self._qName="{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}ConceptScheme"

        super().__init__()

class CodeList(ItemScheme):
    def __init___(self, url=None, id=None, annotations=[], version=None, validFrom=None, validTo=None,
                final=None, isExternalReference=None, serviceUrl=None, structureUrl=None, isPartial=None,agency=None, items=[]):
        super().__init__(url, id, annotations, version, validFrom, validTo, 
                                    final, isExternalReference, serviceUrl, structureUrl, isPartial, agency, items)


        self._itemType="Code"
        self._urnType="codelist"
        self._qName="{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}Codelist"

class AgencyList(ItemScheme):
    # def __init___(self, url=None, id=None, annotations=[], version=None, validFrom=None, validTo=None,
    #             final=None, isExternalReference=None, serviceUrl=None, structureUrl=None, isPartial=None, agency=None, items=[]):
    #     super().__init__(url, id, annotations, version, validFrom, validTo, 
    #                                 final, isExternalReference, serviceUrl, structureUrl, isPartial, agency, items)

    def __init__(self):

        self._itemType="Agency" 
        self._urnType="base"
        self._qName="{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}AgencyScheme"
        super().__init__()


class Concept(Item):
    def __init__(self, url=None, id=None, annotations=[], itemScheme=None, parent=None):
        self._schemeType="ConceptScheme"
        self._urnType="conceptscheme"
        self._qName="{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}Concept"

        super().__init__(url=url, id=id, annotations=annotations, itemScheme=itemScheme, parent=parent)

class Code(Item):
    def __init__(self, url=None, id=None, annotations=[], itemScheme=None, parent=None):
        self._schemeType="CodeList"
        self._urnType="codelist"
        self._qName="{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}Code"

        super().__init__(url, id, annotations, itemScheme, parent)

class Agency(Item):
    def __init__(self, url=None, id=None, annotations=[], itemScheme=None, parent=None):
        self._schemeType="AgencyList"
        self._urnType="base"
        self._qName="{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}Agency"

        super().__init__(url=url, id=id, annotations=annotations, itemScheme=itemScheme, parent=parent)
