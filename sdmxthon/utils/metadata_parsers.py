import logging
from typing import Dict

from ..model.dataTypes import FacetType, FacetValueType
from ..model.itemScheme import Code, CodeList, Agency, ConceptScheme, Concept
from ..model.structure import DataStructureDefinition, DimensionDescriptor, MeasureDescriptor, \
    AttributeDescriptor, Dimension, Attribute, PrimaryMeasure, TimeDimension, Facet
from ..model.structure import Representation

try:
    from lxml import etree as etree
except ImportError:
    from xml.etree import ElementTree as etree

CapturedNsmap_ = {}
print_warnings = True
SaveElementTreeNode = True

# create logger
logger = logging.getLogger("logger")


def id_creator(agencyID, id_, version):
    return f"{agencyID}:{id_}({version})"


def get_codelist_model(root):
    expression = "/mes:Structure/mes:Structures/str:Codelists/str:Codelist"
    result = root.xpath(expression,
                        namespaces={'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure',
                                    'mes': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message'})

    if result is not None:
        codelists: Dict = {}
        for element in result:
            cl = CodeList(id_=element.attrib['id'],
                          uri=element.attrib['urn'],
                          isExternalReference=element.attrib['isExternalReference'],
                          maintainer=Agency(id_=element.attrib['agencyID']),
                          isFinal=element.attrib['isFinal'],
                          version=element.attrib['version']
                          )
            expression = "./com:Name/text()"
            name = element.xpath(expression,
                                 namespaces={'com': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common'})
            if len(name) > 0:
                cl.name = name[0]

            expression = "./str:Code"
            codes = element.xpath(expression,
                                  namespaces={'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})
            for code in codes:
                cd = Code(id_=code.attrib['id'], uri=code.attrib['urn'])
                expression = "./com:Name/text()"
                name = code.xpath(expression,
                                  namespaces={'com': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common'})
                if len(name) > 0:
                    cd.name = name[0]

                expression = "./com:Description/text()"
                desc = code.xpath(expression,
                                  namespaces={'com': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common'})
                if len(desc) > 0:
                    cd.description = desc[0]
                cl.append(cd)
            identifier = id_creator(cl.maintainer.id, cl.id, cl.version)

            codelists[identifier] = cl
        return codelists
    else:
        return None


def get_concept_schemes(root, codelists=None):
    list_mx04 = []

    expression = "/mes:Structure/mes:Structures/str:Concepts/str:ConceptScheme"
    result = root.xpath(expression,
                        namespaces={'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure',
                                    'mes': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message'})

    if result is not None:
        schemes: Dict = {}
        for element in result:
            sch = ConceptScheme(id_=element.attrib['id'],
                                uri=element.attrib['urn'],
                                isExternalReference=element.attrib['isExternalReference'],
                                maintainer=Agency(id_=element.attrib['agencyID']),
                                isFinal=element.attrib['isFinal'],
                                version=element.attrib['version']
                                )
            expression = "./com:Name/text()"
            name = element.xpath(expression,
                                 namespaces={'com': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common'})
            if len(name) > 0:
                sch.name = name[0]

            expression = "./str:Concept"
            concepts = element.xpath(expression,
                                     namespaces={'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})
            for concept in concepts:
                cd = Concept(id_=concept.attrib['id'], uri=concept.attrib['urn'])
                expression = "./com:Name/text()"
                name = concept.xpath(expression,
                                     namespaces={'com': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common'})
                if len(name) > 0:
                    cd.name = name[0]

                facets = []

                expression = "./str:CoreRepresentation/child::*"
                representation = concept.xpath(expression,
                                               namespaces={
                                                   'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})
                if len(representation) > 0:
                    cl = None
                    for e in representation:
                        if e.tag == '{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}Enumeration':
                            expression = "./str:CoreRepresentation/str:Enumeration/Ref"
                            rep_data = concept.xpath(expression,
                                                     namespaces={
                                                         'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})
                            if len(rep_data) == 1:
                                attrib = rep_data[0].attrib
                                if attrib['package'] == 'codelist' and attrib['class'] == 'Codelist':
                                    id_ = id_creator(attrib['agencyID'], attrib['id'], attrib['version'])
                                    if codelists is not None and id_ in codelists.keys():
                                        cl = codelists[id_]
                                    else:
                                        list_mx04.append(
                                            f'Codelist {id_} not found for Concept {cd.id}')
                        elif e.tag == '{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}TextFormat':
                            for k, v in dict(e.attrib).items():
                                if k in FacetType:
                                    facets.append(Facet(facetType=k, facetValue=v))
                                elif k in FacetValueType:
                                    facets.append(Facet(facetValueType=k, facetValue=v))
                        elif e.tag == '{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}EnumerationFormat':
                            for k, v in dict(e.attrib).items():
                                if k in FacetType:
                                    facets.append(Facet(facetType=k, facetValue=v))
                                elif k in FacetValueType:
                                    facets.append(Facet(facetValueType=k, facetValue=v))
                        else:
                            # TODO Error in Local Representation
                            print(
                                f'CoreRepresentation for Concept {cd.id} hasn´t been parsed. Implemented elements are '
                                f'Enumeration, Text Format and EnumerationFormat')
                    cd.coreRepresentation = Representation(codeList=cl, facets=facets)
                sch.append(cd)
            identifier = id_creator(sch.maintainer.id, sch.id, sch.version)
            schemes[identifier] = sch

        if len(list_mx04) > 0:
            return schemes, list_mx04
        return schemes, None
    else:
        return None


def extract_ref_data(list_ms03, obj, dsd, ref, concepts):
    attrib_cs = ref[0].attrib
    cs_id = id_creator(attrib_cs['agencyID'], attrib_cs['maintainableParentID'],
                       attrib_cs['maintainableParentVersion'])

    objType = ''

    if isinstance(obj, Dimension):
        objType = 'Dimension'
    elif isinstance(obj, Attribute):
        objType = 'Attribute'
    elif isinstance(obj, PrimaryMeasure):
        objType = 'Measure'

    if cs_id in concepts.keys():
        cs = concepts[cs_id]
        if attrib_cs['id'] in cs.items.keys():
            con = cs.items[attrib_cs['id']]
            if con.coreRepresentation is not None:
                cl = con.coreRepresentation.codeList
            else:
                cl = None
        else:
            cs = None
            con = None
            cl = None
            list_ms03.append(f'Concept {attrib_cs["id"]} not found for {objType} {obj.id} '
                             f'on DSD '
                             f'{id_creator(dsd.attrib["agencyID"], dsd.attrib["id"], dsd.attrib["version"])}')
    else:
        list_ms03.append(f'Concept Scheme {cs_id} not found for {objType} {obj.id} '
                         f'on DSD '
                         f'{id_creator(dsd.attrib["agencyID"], dsd.attrib["id"], dsd.attrib["version"])}')

        cs = None
        con = None
        cl = None

    return cs, con, cl


def override_core_rep(list_ms02, record, dsdid, codelist_list, obj):
    facets = []
    codelist = None
    expression = "./str:LocalRepresentation/child::*"
    representation = record.xpath(expression,
                                  namespaces={
                                      'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})

    if len(representation) > 0:
        for e in representation:
            if e.tag == '{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}Enumeration':
                expression = "./str:LocalRepresentation/str:Enumeration/Ref"
                rep_data = record.xpath(expression,
                                        namespaces={
                                            'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})
                if len(rep_data) == 1:
                    attrib = rep_data[0].attrib
                    if attrib['package'] == 'codelist' and attrib['class'] == 'Codelist':
                        id_ = id_creator(attrib['agencyID'], attrib['id'], attrib['version'])
                        if codelist_list is not None and id_ in codelist_list.keys():
                            codelist = codelist_list[id_]
                        else:
                            if isinstance(obj, Attribute):
                                list_ms02.append(f'Codelist {id_} not found for Attribute {obj.id} in DSD {dsdid}')
                            elif isinstance(obj, PrimaryMeasure):
                                list_ms02.append(f'Codelist {id_} not found for Measure {obj.id} in DSD {dsdid}')
                            elif isinstance(obj, Dimension):
                                list_ms02.append(f'Codelist {id_} not found for Dimension {obj.id} in DSD {dsdid}')
            elif e.tag == '{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}TextFormat':
                for k, v in dict(e.attrib).items():
                    if k in FacetType:
                        facets.append(Facet(facetType=k, facetValue=v))
                    elif k in FacetValueType:
                        facets.append(Facet(facetValueType=k, facetValue=v))
                codelist = None
            elif e.tag == '{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}EnumerationFormat':
                for k, v in dict(e.attrib).items():
                    if k in FacetType:
                        facets.append(Facet(facetType=k, facetValue=v))
                    elif k in FacetValueType:
                        facets.append(Facet(facetValueType=k, facetValue=v))
            else:
                # TODO Error in Local Representation
                print(f'Local Representation for attribute {obj.id} hasn´t been parsed. Implemented elements are '
                      f'Enumeration, Text Format and EnumerationFormat')

    return codelist, facets


def gen_representation(record, concepts, codelists, obj, dsd, list_ms03, list_ms02):
    expression = "./str:ConceptIdentity/Ref"
    ref = record.xpath(expression,
                       namespaces={
                           'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})
    if len(ref) == 1 and concepts is not None:
        cs, con, cl = extract_ref_data(list_ms03, obj, dsd, ref, concepts=concepts)
    else:
        # TODO Error no concept scheme found in DataStructureDefinition (validate_metadata)
        cs = None
        con = None
        cl = None

    expression = "./str:LocalRepresentation"
    local = record.xpath(expression,
                         namespaces={
                             'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})
    facets = []
    if len(local) == 1:

        cl, facets = override_core_rep(list_ms02=list_ms02, record=record,
                                       dsdid=id_creator(dsd.attrib["agencyID"], dsd.attrib["id"],
                                                        dsd.attrib["version"]), codelist_list=codelists, obj=obj)
    else:
        if con is not None and con.coreRepresentation is not None and len(con.coreRepresentation.facets) > 0:
            facets = con.coreRepresentation.facets

    return Representation(codeList=cl, conceptScheme=cs, concept=con, facets=facets)


def get_attribute_relationship(record, measure_descriptor, attribute_descriptor, dimension_descriptor,
                               list_ms04, list_ms05):
    expression = "./str:AttributeRelationship/child::*"
    obj = record.xpath(expression,
                       namespaces={
                           'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})
    related = []
    if len(obj) > 0:
        expression = "./str:AttributeRelationship/str:PrimaryMeasure/Ref"
        meas_data = record.xpath(expression,
                                 namespaces={
                                     'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})
        if len(meas_data) > 0 and measure_descriptor is not None:
            for e in meas_data:
                if e.attrib['id'] in measure_descriptor.components.keys():
                    related.append(measure_descriptor.components.get(e.attrib['id']))
                else:
                    # TODO Measure not found in Measure Descriptor
                    list_ms05.append(f'Primary Measure {e.attrib["id"]} related to attribute '
                                     f'{attribute_descriptor.id} not found')
                    related = None

        elif len(meas_data) == 0 and dimension_descriptor is not None:
            expression = "./str:AttributeRelationship/str:Dimension/Ref"
            dim_data = record.xpath(expression,
                                    namespaces={
                                        'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})
            if len(dim_data) > 0:
                for e in dim_data:
                    if e.attrib['id'] in dimension_descriptor.components.keys():
                        related.append(dimension_descriptor.components.get(e.attrib['id']))
                    else:
                        list_ms04.append(f'Dimension {e.attrib["id"]} related to attribute '
                                         f'{attribute_descriptor.id} not found')
                        related = None

        else:
            # TODO Not found Ref in Attribute Relationship (validate_metadata)
            related = None

    return related


def create_dimension_data(list_ms02: list, list_ms03: list, dsd, dimension_descriptor, concepts, codelists,
                          dim_type='Dimension'):
    if dim_type not in ['Dimension', 'TimeDimension']:
        return None

    # Add Dimensions or TimeDimensions
    expression = "./str:DataStructureComponents/str:DimensionList/str:" + dim_type
    dimensions = dsd.xpath(expression,
                           namespaces={
                               'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})

    # Add Dimensions to Dimension Descriptor
    for record in dimensions:
        if dim_type == 'TimeDimension':
            dim = TimeDimension(id_=record.attrib['id'], uri=record.attrib['urn'],
                                position=record.attrib['position'])
        else:
            dim = Dimension(id_=record.attrib['id'], uri=record.attrib['urn'],
                            position=record.attrib['position'])

        rep = gen_representation(record, concepts, codelists, dim, dsd, list_ms03, list_ms02)
        dim.localRepresentation = rep
        dimension_descriptor.addComponent(dim)

    return dimension_descriptor


def create_attribute_data(list_ms03: list, list_ms04: list, list_ms05: list, list_ms02: list, dsd, attribute_descriptor,
                          concepts,
                          codelists, measure_descriptor: MeasureDescriptor = None,
                          dimension_descriptor: DimensionDescriptor = None):
    expression = "./str:DataStructureComponents/str:AttributeList/str:Attribute"
    attributes = dsd.xpath(expression,
                           namespaces={
                               'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})
    # Add Attributes to Attribute Descriptor
    for record in attributes:
        att = Attribute(id_=record.attrib['id'], uri=record.attrib['urn'],
                        usageStatus=record.attrib['assignmentStatus'])

        # Attribute Relationship

        list_related = get_attribute_relationship(record, measure_descriptor, attribute_descriptor,
                                                  dimension_descriptor,
                                                  list_ms04, list_ms05)

        if len(list_related) == 1:
            att.relatedTo = list_related[0]
        elif len(list_related) == 0 or list_related is None:
            att.relatedTo = None
        else:
            att.relatedTo = list_related

        rep = gen_representation(record, concepts, codelists, att, dsd, list_ms03, list_ms02)
        att.localRepresentation = rep
        attribute_descriptor.addComponent(att)

    return attribute_descriptor


def create_measures_data(dsd, measure_descriptor, concepts, codelists, list_mx02: list, list_ms02: list,
                         list_ms03: list):
    expression = "./str:DataStructureComponents/str:MeasureList/str:PrimaryMeasure"
    measures = dsd.xpath(expression,
                         namespaces={
                             'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})

    if measures is None:
        list_mx02.append(f'DSD {dsd.attrib["id"]} does not have a Primary Measure')
    else:

        # Add Measure to Measure Descriptor
        for record in measures:
            meas = PrimaryMeasure(id_=record.attrib['id'], uri=record.attrib['urn'])

            rep = gen_representation(record, concepts, codelists, meas, dsd, list_ms03, list_ms02)
            meas.localRepresentation = rep
            measure_descriptor.addComponent(meas)

    return measure_descriptor


def get_DSDs(root, concepts=None, codelists=None):
    errors = {}
    list_ms06 = []
    duplicated_dsds = []

    expression = "/mes:Structure/mes:Structures/str:DataStructures/str:DataStructure"
    result = root.xpath(expression,
                        namespaces={'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure',
                                    'mes': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message'})
    if result is None:
        errors['Common'] = {'MS01': 'Not found any DSD in this file'}
        return errors

    dsds: Dict = {}
    for element in result:
        list_ms02 = []
        list_ms03 = []
        list_ms04 = []
        list_ms05 = []
        list_mx01 = []
        list_mx02 = []
        list_mx03 = []
        dsd = DataStructureDefinition(id_=element.attrib['id'],
                                      uri=element.attrib['urn'],
                                      isExternalReference=element.attrib['isExternalReference'],
                                      maintainer=Agency(id_=element.attrib['agencyID']),
                                      isFinal=element.attrib['isFinal'],
                                      version=element.attrib['version']
                                      )
        expression = "./com:Name/text()"
        name = element.xpath(expression,
                             namespaces={'com': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common'})
        if len(name) > 0:
            dsd.name = name[0]

        expression = "./str:DataStructureComponents/str:DimensionList"
        dimensionElement = element.xpath(expression,
                                         namespaces={
                                             'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})

        dd = None

        if len(dimensionElement) == 1:
            dd = DimensionDescriptor(id_=dimensionElement[0].attrib['id'],
                                     uri=dimensionElement[0].attrib['urn'])

            dd = create_dimension_data(list_ms02=list_ms02, list_ms03=list_ms03, dsd=element, dimension_descriptor=dd,
                                       concepts=concepts,
                                       codelists=codelists)
            dd = create_dimension_data(list_ms02=list_ms02, list_ms03=list_ms03, dsd=element, dimension_descriptor=dd,
                                       concepts=concepts,
                                       codelists=codelists, dim_type='TimeDimension')

            if 'TIME_PERIOD' not in dd.components.keys() and dsd.agencyId == 'RBI':
                list_mx03.append(f'Missing TIME_PERIOD as TimeDimension for DSD '
                                 f'{id_creator(dsd.agencyId, dsd.id, dsd.version)}')

            dsd.dimensionDescriptor = dd
        else:
            # TODO Missing dimension list on DSD (validate_metadata)
            list_mx01.append(f'DSD {id_creator(dsd.agencyId, dsd.id, dsd.version)} does not have a DimensionList')

        # Add Measures
        expression = "./str:DataStructureComponents/str:MeasureList"
        measureElement = element.xpath(expression,
                                       namespaces={
                                           'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})

        md = None
        if len(measureElement) == 1:
            md = MeasureDescriptor(id_=measureElement[0].attrib['id'], uri=measureElement[0].attrib['urn'])

            create_measures_data(list_mx02=list_mx02, list_ms03=list_ms03, list_ms02=list_ms02, dsd=element,
                                 measure_descriptor=md,
                                 concepts=concepts, codelists=codelists)

            if 'OBS_VALUE' not in md.components.keys() and dsd.agencyId == 'RBI':
                list_mx03.append(f'Missing OBS_VALUE as PrimaryMeasure for DSD '
                                 f'{id_creator(dsd.agencyId, dsd.id, dsd.version)}')

            dsd.measureDescriptor = md
        else:
            # TODO Missing measure list on DSD (validate_metadata)
            list_mx01.append(f'DSD {id_creator(dsd.agencyId, dsd.id, dsd.version)} does not have a MeasureList')

        # Add Attributes
        expression = "./str:DataStructureComponents/str:AttributeList"
        attributeElement = element.xpath(expression,
                                         namespaces={
                                             'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})
        if len(attributeElement) == 1:
            ad = AttributeDescriptor(id_=attributeElement[0].attrib['id'], uri=attributeElement[0].attrib['urn'])

            if concepts is not None:
                create_attribute_data(list_ms02=list_ms02, list_ms03=list_ms03, list_ms04=list_ms04,
                                      list_ms05=list_ms05, dsd=element,
                                      attribute_descriptor=ad, measure_descriptor=md,
                                      concepts=concepts, codelists=codelists, dimension_descriptor=dd)

            dsd.attributeDescriptor = ad

        identifier = id_creator(dsd.maintainer.id, dsd.id, dsd.version)
        dsd_errors = {}
        if identifier in dsds.keys():
            list_ms06.append(f'DSD {identifier} is not unique')
            duplicated_dsds.append(identifier)
        else:
            if len(list_ms02) > 0:
                dsd_errors['MS02'] = list_ms02
            if len(list_ms03) > 0:
                dsd_errors['MS03'] = list_ms03
            if len(list_ms04) > 0:
                dsd_errors['MS04'] = list_ms04
            if len(list_ms05) > 0:
                dsd_errors['MS05'] = list_ms05
            if len(list_mx01) > 0:
                dsd_errors['MX01'] = list_mx01
            if len(list_mx02) > 0:
                dsd_errors['MX02'] = list_mx02
            if len(list_mx03) > 0:
                dsd_errors['MX03'] = list_mx03

            if len(dsd_errors) > 0:
                errors[identifier] = dsd_errors.copy()
            else:
                dsds[identifier] = dsd

    if len(list_ms06) > 0:
        errors['Common'] = {'MS06': list_ms06}
        for e in duplicated_dsds:
            del dsds[e]

    if len(errors) > 0:
        return dsds, errors
    return dsds, None


def validate_dataset_attributes_from_dsd(dsd, dataset):
    dataset_keys = dsd.datasetAttributeCodes
    attached_keys = dataset.attached_attributes.keys()
    wrong_attributes = {"missing_attributes": [], "spared_attributes": []}

    for key in dataset_keys:
        if key not in attached_keys:
            wrong_attributes.get("missing_attributes").append(key)

    for key in attached_keys:
        if key not in dataset_keys:
            wrong_attributes.get("spared_attributes").append(key)

    return wrong_attributes


def add_elements_to_dict(dict1: dict, dict2: dict, updateElementsFromDict2=True):
    if updateElementsFromDict2:
        dict1.update(dict2)
    else:
        for e in dict2.keys():
            if e not in dict1.keys():
                dict1[e] = dict2[e]

    return dict1


def delete_unused_codelists(codelists: dict, concepts: dict, dsds: dict):
    used_codelists = []
    used_concepts = []

    for e in dsds.values():
        for i in e.attributeDescriptor.components.values():
            if i.localRepresentation.codeList is not None:
                a = i.localRepresentation.codeList
                used_codelists.append(id_creator(a.agencyId, a.id, a.version))
            if i.localRepresentation.concept is not None:
                b = i.localRepresentation.concept.scheme
                used_concepts.append(id_creator(b.agencyId, b.id, b.version))

        for j in e.dimensionDescriptor.components.values():
            if j.localRepresentation.codeList is not None:
                a = j.localRepresentation.codeList
                used_codelists.append(id_creator(a.agencyId, a.id, a.version))
            if j.localRepresentation.concept is not None:
                b = j.localRepresentation.concept.scheme
                used_concepts.append(id_creator(b.agencyId, b.id, b.version))

        for k in e.measureDescriptor.components.values():
            if k.localRepresentation.codeList is not None:
                a = k.localRepresentation.codeList
                used_codelists.append(id_creator(a.agencyId, a.id, a.version))
            if k.localRepresentation.concept is not None:
                b = k.localRepresentation.concept.scheme
                used_concepts.append(id_creator(b.agencyId, b.id, b.version))

    for m in concepts.values():
        for n in m.items.values():
            if n.coreRepresentation is not None:
                if n.coreRepresentation.codeList is not None:
                    a = n.coreRepresentation.codeList
                    used_codelists.append(id_creator(a.agencyId, a.id, a.version))
    updatedCL = codelists.copy()
    updatedCS = concepts.copy()
    for o in codelists.keys():
        if o not in used_codelists:
            updatedCL.pop(o)
            print('Deleted CL key %s' % o)
    for o in concepts.keys():
        if o not in used_concepts:
            updatedCS.pop(o)
            print('Deleted CS key %s' % o)
    return updatedCL, updatedCS


def set_dsds_checked_to_false(dsds: dict):
    for e in dsds.values():
        if e.attributeDescriptor is not None:
            for i in e.attributeDescriptor.components.values():
                if i.localRepresentation.codeList is not None:
                    i.localRepresentation.codeList._checked = False
                if i.localRepresentation.concept is not None:
                    i.localRepresentation.concept.scheme._checked = False
        if e.dimensionDescriptor is not None:
            for j in e.dimensionDescriptor.components.values():
                if j.localRepresentation.codeList is not None:
                    j.localRepresentation.codeList._checked = False
                if j.localRepresentation.concept is not None:
                    j.localRepresentation.concept.scheme._checked = False
        if e.measureDescriptor is not None:
            for k in e.measureDescriptor.components.values():
                if k.localRepresentation.codeList is not None:
                    k.localRepresentation.codeList._checked = False
                if k.localRepresentation.concept is not None:
                    k.localRepresentation.concept.scheme._checked = False


def set_codelists_checked_to_false(codelists: dict):
    for e in codelists.values():
        e._checked = False


def set_concepts_checked_to_false(concepts: dict):
    for e in concepts.values():
        e._checked = False
