import copy
import logging
from typing import Dict

from SDMXThon.common.generic import GenericDataStructureType
from SDMXThon.common.references import DataflowReferenceType
from SDMXThon.common.refs import DataflowRefType
from SDMXThon.data.generic import DataSetType as GenericDataSetType
from SDMXThon.data.generic import ValuesType, ObsOnlyType, ComponentValueType, ObsValueType
from SDMXThon.message.generic import GenericDataType, StructureSpecificDataType
from SDMXThon.model.itemScheme import Code, CodeList, Agency, ConceptScheme, Concept
from SDMXThon.model.structure import DataStructureDefinition, DimensionDescriptor, MeasureDescriptor, \
    AttributeDescriptor, Dimension, Attribute, PrimaryMeasure, TimeDimension
from SDMXThon.model.structure import Representation
from SDMXThon.structure.specificbase import DataSetType as StructureDataSetType, ObsType as Observation, \
    SeriesType as Series
from SDMXThon.utils.enums import DatasetType

try:
    from lxml import etree as etree_, etree
except ImportError:
    from xml.etree import ElementTree as etree_, etree

CapturedNsmap_ = {}
print_warnings = True
SaveElementTreeNode = True

# create logger
logger = logging.getLogger("logging_tryout2")
logger.setLevel(logging.DEBUG)

"""
def parse(inFileName, silence=False, print_warnings=True):
    global CapturedNsmap_
    gds_collector = GdsCollector_()
    parser = None
    doc = parsexml_(inFileName, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)

    if rootClass is None:
        rootTag = 'GenericData'
        rootClass = GenericDataType

    rootTag = 'GenericData'
    rootClass = GenericDataType
    rootObj = rootClass.factory()
    rootObj.original_tag_name_ = rootTag
    rootObj.build(rootNode, gds_collector_=gds_collector)
    CapturedNsmap_, namespacedefs = get_required_ns_prefix_defs(rootNode)
    rootObj._namespace_def = namespacedefs

    if not SaveElementTreeNode:
        doc = None
        rootNode = None

    if not silence:
        f = open("example.xml", "w")
        f.write('<?xml version="1.0" ' + "encoding='UTF-8'?>\n")
        rootObj.export(f, 0, pretty_print=True, has_parent=False)
        f.close()

    makeWarnings(print_warnings, gds_collector)

    return rootObj


def parseEtree(inFileName, silence=False, print_warnings=True, mapping=None, nsmap=None):
    parser = None
    doc = parsexml_(inFileName, parser)
    gds_collector = GdsCollector_()
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)

    if rootClass is None:
        rootTag = 'GenericData'
        rootClass = GenericDataType

    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    # Enable Python to collect the space used by the DOM.
    if mapping is None:
        mapping = {}

    rootElement = rootObj.to_etree(None, name_=rootTag, mapping_=mapping, nsmap_=nsmap)
    reverse_mapping = rootObj.gds_reverse_node_mapping(mapping)

    if not SaveElementTreeNode:
        doc = None
        rootNode = None

    if not silence:
        content = etree_.tostring(rootElement, encoding="utf-8")
        sys.stdout.write(str(content))
        sys.stdout.write('\n')

    makeWarnings(print_warnings, gds_collector)

    return rootObj, rootElement, mapping, reverse_mapping


def parseString(inString, silence=False, print_warnings=True):
    '''Parse a string, create the object tree, and export it.

    Arguments:
    - inString -- A string.  This XML fragment should not start
      with an XML declaration containing an encoding.
    - silence -- A boolean.  If False, export the object.
    Returns -- The root object in the tree.
    '''
    parser = None
    rootNode = parsexmlstring_(inString, parser)
    gds_collector = GdsCollector_()
    rootTag, rootClass = get_root_tag(rootNode)

    if rootClass is None:
        rootTag = 'GenericData'
        rootClass = GenericDataType

    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)

    if not SaveElementTreeNode:
        rootNode = None

    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(sys.stdout, 0, name_=rootTag,
                       namespacedef_='xmlns:message="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message"')

    if print_warnings and len(gds_collector.get_messages()) > 0:
        separator = ('-' * 50) + '\n'
        sys.stderr.write(separator)
        sys.stderr.write('----- Warnings -- count: {} -----\n'.format(len(gds_collector.get_messages()), ))
        gds_collector.write_messages(sys.stderr)
        sys.stderr.write(separator)

    return rootObj


def parseLiteral(inFileName, silence=False, print_warnings=True):
    parser = None
    doc = parsexml_(inFileName, parser)
    gds_collector = GdsCollector_()
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)

    if rootClass is None:
        rootTag = 'GenericData'
        rootClass = GenericDataType

    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    # Enable Python to collect the space used by the DOM.

    if not SaveElementTreeNode:
        doc = None
        rootNode = None

    if not silence:
        sys.stdout.write('#from smdxthon_lib import *\n\n')
        sys.stdout.write('import smdxthon_lib as model_\n\n')
        sys.stdout.write('xmlObj = model_.rootClass(\n')
        rootObj.exportLiteral(sys.stdout, 0, name_=rootTag)
        sys.stdout.write(')\n')

    makeWarnings(print_warnings, gds_collector)

"""


def get_all_obs_attributes(root):
    find_dataset_attr = "/str:Structure/str:Structures/mes:DataStructures/mes:DataStructure/mes:AttributeList"
    record = root.xpath(find_dataset_attr,
                        namespaces={'mes': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure',
                                    'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message'},
                        smart_string=False)
    attribute_list = []

    if len(record) > 0:
        aux = []
        attributes = record[0]
        find_attr_obs_value = "./mes:Attribute[./mes:AttributeRelationship/mes:PrimaryMeasure/Ref/@id='OBS_VALUE" \
                              "']/mes:ConceptIdentity/Ref/@id "
        result = attributes.xpath(find_attr_obs_value,
                                  namespaces={'mes': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure',
                                              'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message'}
                                  )
        aux.extend(result)
        attribute_list = list(set(aux))

    return attribute_list


def get_all_series_attributes(root):
    expression = "/str:Structure/str:Structures/mes:DataStructures/mes:DataStructure/mes:DataStructureComponents/mes:DimensionList/mes:Dimension/@id"
    record = root.xpath(expression,
                        namespaces={'mes': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure',
                                    'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message'})
    attribute_list = []

    if len(record) > 0:
        aux = []
        aux.extend(record)
        attribute_list = list(set(aux))

    return attribute_list


def get_all_dataset_attributes(root):
    find_dataset_attr = "/str:Structure/str:Structures/mes:DataStructures/mes:DataStructure/mes:AttributeList"
    record = root.xpath(find_dataset_attr,
                        namespaces={'mes': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure',
                                    'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message'})
    attribute_list = []

    if len(record) > 0:
        aux = []
        attributes = record[0]
        find_attr_obs_value = "./mes:Attribute[count(./*/mes:None) > 0]/mes:ConceptIdentity/Ref/@id"
        result = attributes.xpath(find_attr_obs_value,
                                  namespaces={'mes': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure',
                                              'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message'})
        aux.extend(result)
        attribute_list = list(set(aux))

    return attribute_list


def get_obs_attributes(root, dataset_id):
    find_dataset_attr = "/str:Structure/str:Structures/mes:DataStructures/mes:DataStructure[@id=$name]/mes:DataStructureComponents/mes:AttributeList/mes:Attribute[./mes:AttributeRelationship/mes:PrimaryMeasure/Ref/@id='OBS_VALUE']/mes:ConceptIdentity/Ref/@id"
    record = root.xpath(find_dataset_attr, name=dataset_id,
                        namespaces={'mes': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure',
                                    'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message'},
                        smart_string=False)

    attribute_list = {}
    for record_ in record:
        attribute_list[record_] = ''

    return attribute_list


def get_series_attributes(root, dataset_id):
    expression = "/str:Structure/str:Structures/mes:DataStructures/mes:DataStructure[@id=$name]/mes:DataStructureComponents/mes:DimensionList/mes:Dimension/@id"
    record = root.xpath(expression, name=dataset_id,
                        namespaces={'mes': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure',
                                    'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message'})
    attribute_list = {}

    if len(record) > 0:
        for record_ in record:
            attribute_list[record_] = ''

    # TIME_PERIOD Fix
    expression = "/str:Structure/str:Structures/mes:DataStructures/mes:DataStructure[@id=$name]/mes:DataStructureComponents/mes:DimensionList/mes:TimeDimension/@id"
    record = root.xpath(expression, name=dataset_id,
                        namespaces={'mes': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure',
                                    'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message'})

    if len(record) > 0:
        for record_ in record:
            attribute_list[record_] = ''

    return attribute_list


def get_dataset_attributes(root, dataset_id):
    find_dataset_attr = "/str:Structure/str:Structures/mes:DataStructures/mes:DataStructure[@id=$name]/mes:DataStructureComponents/mes:AttributeList/mes:Attribute[count(./mes:AttributeRelationship/mes:None) > 0]/mes:ConceptIdentity/Ref/@id"
    record = root.xpath(find_dataset_attr, name=dataset_id,
                        namespaces={'mes': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure',
                                    'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message'})
    attribute_list = {}

    for result_ in record:
        attribute_list[result_] = ''

    return attribute_list


def get_codelist(root):
    expression = "/str:Structure/str:Structures/mes:Codelists/mes:Codelist"
    result = root.xpath(expression,
                        namespaces={'mes': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure',
                                    'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message'})

    codelist_ids = {}
    if result is not None:
        for result_ in result:
            expression = "./mes:Code/@id"
            enums = result_.xpath(expression,
                                  namespaces={'mes': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure',
                                              'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message'})

            codelist_ids[result_.attrib['id']] = enums

    return codelist_ids


def id_creator(agencyID, id, version):
    return f"{agencyID}:{id}({version})"


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
        return []


def get_concept_schemes(root, codelists=None):
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

                expression = "./str:CoreRepresentation/str:Enumeration/Ref"
                cr = concept.xpath(expression,
                                   namespaces={'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})
                if len(cr) == 1:
                    attrib = cr[0].attrib
                    if attrib['package'] == 'codelist' and attrib['class'] == 'Codelist':
                        id_ = id_creator(attrib['agencyID'], attrib['id'], attrib['version'])
                        if codelists is not None:
                            if id_ not in codelists.keys():
                                # TODO Codelist not found in list
                                print(id_)
                            else:
                                cd.coreRepresentation = Representation(codeList=codelists[id_])
                sch.append(cd)
            identifier = id_creator(sch.maintainer.id, sch.id, sch.version)
            schemes[identifier] = sch
        return schemes
    else:
        return []


def create_dimension_data(dsd, dimension_descriptor, concepts, codelists, dim_type='Dimension'):
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

        expression = "./str:ConceptIdentity/Ref"
        ref = record.xpath(expression,
                           namespaces={
                               'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})
        if len(ref) == 1 and concepts is not None:
            attrib_cs = ref[0].attrib
            cs_id = id_creator(attrib_cs['agencyID'], attrib_cs['maintainableParentID'],
                               attrib_cs['maintainableParentVersion'])
            if cs_id in concepts.keys():
                cs = concepts[cs_id]
                con = cs.items[attrib_cs['id']]
            else:
                # TODO Error message no concept scheme in scheme list (validate_metadata)
                cs = None
                con = None
        else:
            # TODO Error message no concept scheme found in DataStructureDefinition (validate_metadata)
            cs = None
            con = None
        expression = "./str:LocalRepresentation/str:Enumeration/Ref"
        ref = record.xpath(expression,
                           namespaces={
                               'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})
        if len(ref) == 1 and codelists is not None:
            attrib_cl = ref[0].attrib
            cl_id = id_creator(attrib_cl['agencyID'], attrib_cl['id'],
                               attrib_cl['version'])
            if cl_id in codelists.keys():
                cl = codelists[cl_id]
            else:
                # TODO Error message no codelist found in codelist list (validate_metadata)
                cl = None
        else:
            # TODO Error message no codelist found in DataStructureDefinition (validate_metadata)
            cl = None
        rep = Representation(codeList=cl, conceptScheme=cs, concept=con)
        dim.localRepresentation = rep
        dimension_descriptor.addComponent(dim)

    return dimension_descriptor


def extract_ref_data(ref, concepts):
    attrib_cs = ref[0].attrib
    cs_id = id_creator(attrib_cs['agencyID'], attrib_cs['maintainableParentID'],
                       attrib_cs['maintainableParentVersion'])
    if cs_id in concepts.keys():
        cs = concepts[cs_id]
        con = cs.items[attrib_cs['id']]
        if con.coreRepresentation is not None:
            cl = con.coreRepresentation.codeList
        else:
            cl = None
    else:
        # TODO Error message no concept scheme in scheme list (validate_metadata)
        cs = None
        con = None
        cl = None

    return cs, con, cl


def override_core_rep(record, codelist, codelist_list, object):
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
                        if codelist_list is not None:
                            codelist = codelist_list[id_]
            elif e.tag == '{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}TextFormat':
                codelist = None
            elif e.tag != '{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}EnumerationFormat':
                # TODO Error in Local Representation
                print('Local Representation for attribute %s hasn´t been parsed' % object.id)

    return codelist


def create_attribute_data(dsd, attribute_descriptor, concepts, codelists, measure_descriptor: MeasureDescriptor = None,
                          dimension_descriptor: DimensionDescriptor = None):
    expression = "./str:DataStructureComponents/str:AttributeList/str:Attribute"
    attributes = dsd.xpath(expression,
                           namespaces={
                               'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})
    # Add Attributes to Attribute Descriptor
    for record in attributes:
        att = Attribute(id_=record.attrib['id'], uri=record.attrib['urn'],
                        usageStatus=record.attrib['assignmentStatus'])
        expression = "./str:ConceptIdentity/Ref"
        ref = record.xpath(expression,
                           namespaces={
                               'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})
        if len(ref) == 1 and concepts is not None:
            cs, con, cl = extract_ref_data(ref, concepts=concepts)
        else:
            # TODO Error message no concept scheme found in DataStructureDefinition (validate_metadata)
            cs = None
            con = None
            cl = None

        # Local representation overrides CoreRepresentation
        cl = override_core_rep(record=record, codelist=cl, codelist_list=codelists, object=att)

        # Attribute Relationship

        expression = "./str:AttributeRelationship/child::*"
        obj = record.xpath(expression,
                           namespaces={
                               'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})
        list_related = []
        if len(obj) > 0:
            expression = "./str:AttributeRelationship/str:PrimaryMeasure/Ref"
            meas_data = record.xpath(expression,
                                     namespaces={
                                         'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})
            if len(meas_data) > 0 and measure_descriptor is not None:
                for e in meas_data:
                    if e.attrib['id'] in measure_descriptor.components.keys():
                        list_related.append(measure_descriptor.components.get(e.attrib['id']))
                    else:
                        # TODO Measure not found in Measure Descriptor
                        att.relatedTo = None


            elif len(meas_data) == 0 and dimension_descriptor is not None:
                expression = "./str:AttributeRelationship/str:Dimension/Ref"
                dim_data = record.xpath(expression,
                                        namespaces={
                                            'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})
                if len(dim_data) > 0:
                    for e in dim_data:
                        if e.attrib['id'] in dimension_descriptor.components.keys():
                            list_related.append(dimension_descriptor.components.get(e.attrib['id']))
                        else:
                            # TODO Dimension not found in Dimension Descriptor
                            att.relatedTo = None

            else:
                # TODO Not found Ref in Attribute Relationship (validate_metadata)
                att.relatedTo = None
                print('Ref not found in attribute %s' % att.id)

        if len(list_related) == 1:
            att.relatedTo = list_related[0]
        else:
            att.relatedTo = list_related

        rep = Representation(conceptScheme=cs, concept=con, codeList=cl)
        att.localRepresentation = rep
        attribute_descriptor.addComponent(att)

    return attribute_descriptor


def create_measures_data(dsd, measure_descriptor, concepts, codelists):
    expression = "./str:DataStructureComponents/str:MeasureList/str:PrimaryMeasure"
    measures = dsd.xpath(expression,
                         namespaces={
                             'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})
    # Add Measure to Measure Descriptor
    for record in measures:
        meas = PrimaryMeasure(id_=record.attrib['id'], uri=record.attrib['urn'])
        expression = "./str:ConceptIdentity/Ref"
        ref = record.xpath(expression,
                           namespaces={
                               'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})
        if len(ref) == 1 and concepts is not None:
            attrib_cs = ref[0].attrib
            cs_id = id_creator(attrib_cs['agencyID'], attrib_cs['maintainableParentID'],
                               attrib_cs['maintainableParentVersion'])
            if cs_id in concepts.keys():
                cs = concepts[cs_id]
                con = cs.items[attrib_cs['id']]
                if con.coreRepresentation is not None:
                    cl = con.coreRepresentation.codeList
                else:
                    cl = None
            else:
                # TODO Error message no concept scheme in scheme list (validate_metadata)
                cs = None
                con = None
                cl = None
        else:
            # TODO Error message no concept scheme found in DataStructureDefinition (validate_metadata)
            cs = None
            con = None
            cl = None

        # Local representation overrides CoreRepresentation
        cl = override_core_rep(record=record, codelist=cl, codelist_list=codelists, object=meas)

        rep = Representation(conceptScheme=cs, concept=con, codeList=cl)
        meas.localRepresentation = rep
        measure_descriptor.addComponent(meas)

    return measure_descriptor


def get_DSDs(root, concepts=None, codelists=None):
    expression = "/mes:Structure/mes:Structures/str:DataStructures/str:DataStructure"
    result = root.xpath(expression,
                        namespaces={'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure',
                                    'mes': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message'})
    if result is None:
        return None

    dsds: Dict = {}
    for element in result:
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
        if len(dimensionElement) == 1:
            dd = DimensionDescriptor(id_=dimensionElement[0].attrib['id'],
                                     uri=dimensionElement[0].attrib['urn'])

            dd = create_dimension_data(dsd=element, dimension_descriptor=dd, concepts=concepts,
                                       codelists=codelists)
            dd = create_dimension_data(dsd=element, dimension_descriptor=dd, concepts=concepts,
                                       codelists=codelists, dim_type='TimeDimension')

            dsd.dimensionDescriptor = dd

        # Add Measures
        expression = "./str:DataStructureComponents/str:MeasureList"
        measureElement = element.xpath(expression,
                                       namespaces={
                                           'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})
        if len(measureElement) == 1:
            md = MeasureDescriptor(id_=measureElement[0].attrib['id'], uri=measureElement[0].attrib['urn'])

            create_measures_data(dsd=element, measure_descriptor=md, concepts=concepts, codelists=codelists)
            dsd.measureDescriptor = md

        # Add Attributes
        expression = "./str:DataStructureComponents/str:AttributeList"
        attributeElement = element.xpath(expression,
                                         namespaces={
                                             'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})
        if len(attributeElement) == 1:
            ad = AttributeDescriptor(id_=attributeElement[0].attrib['id'], uri=attributeElement[0].attrib['urn'])

            if concepts is not None:
                ad = create_attribute_data(dsd=element, attribute_descriptor=ad, measure_descriptor=md,
                                           concepts=concepts, codelists=codelists, dimension_descriptor=dd)

            dsd.attributeDescriptor = ad

        identifier = id_creator(dsd.maintainer.id, dsd.id, dsd.version)
        dsds[identifier] = dsd
    return dsds


def get_attr_enums(root, dataset_id):
    expression = "/str:Structure/str:Structures/mes:DataStructures/mes:DataStructure[@id=$name]/mes:DataStructureComponents//*[count(./mes:LocalRepresentation/mes:Enumeration) > 0]/@id"
    result = root.xpath(expression, name=dataset_id,
                        namespaces={'mes': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure',
                                    'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message'})

    codelist_ids = {}
    if result is not None:
        for result_ in result:
            expression = "/str:Structure/str:Structures/mes:DataStructures/mes:DataStructure[@id=$name]/mes:DataStructureComponents//*[@id=$subname]/mes:LocalRepresentation/mes:Enumeration/Ref/@id"
            enum = root.xpath(expression, name=dataset_id, subname=result_,
                              namespaces={'mes': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure',
                                          'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message'})

            codelist_ids[result_] = enum[0]

    return codelist_ids


def is_enum(attr_name: str, attr_enums: dict):
    value = None
    if attr_name in attr_enums:
        value = attr_enums[attr_name]

    return value


def is_valid_enum_value(enum_name: str, enum_value: str, codelist: dict):
    valid_value = False

    if enum_name is not None:
        if enum_name in codelist:
            values = codelist[enum_name]
            if enum_value in values:
                valid_value = True

    return valid_value


def get_node_data_structure(root, id):
    expression = "/str:Structure/str:Structures/mes:DataStructures/mes:DataStructure[@id=$name]"
    record = root.xpath(expression, name=id,
                        namespaces={'mes': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure',
                                    'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message'})

    return record


def get_agency_id(root):
    expression = "/str:Structure/str:Structures/mes:Codelists/mes:Codelist[@agencyID != ''][1]/@agencyID"
    record = root.xpath(expression,
                        namespaces={'mes': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure',
                                    'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message'})

    if len(record) is 0:
        return None
    else:
        return record[0]


def get_urn_header(root, datasets_ids):
    dataset_namespaces = "\n"
    for id in datasets_ids:
        expression = "/str:Structure/str:Structures/mes:DataStructures/mes:DataStructure[@id=$name]/@urn"
        record = root.xpath(expression, name=id,
                            namespaces={'mes': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure',
                                        'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message'})
        dataset_namespaces += 'xmlns:' + id + '="' + record[0] + ':ObsLevelDim:AllDimensions"\n'

    return dataset_namespaces


def get_structure(root, dataset_id, agency_id):
    expression = "/str:Structure/str:Structures/mes:DataStructures/mes:DataStructure[@id=$name]/@urn"
    record = root.xpath(expression, name=dataset_id,
                        namespaces={'mes': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure',
                                    'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message'})
    urn_aux = record[0]
    urn = urn_aux + ':ObsLevelDim:AllDimensions'
    aux = urn_aux.split("(", 1)[1]
    version = aux.split(")", 1)[0]
    structure = GenericDataStructureType()
    structure.original_tag_name_ = "Structure"
    structure.set_ns_def_("message")
    structure.set_structureID(dataset_id)
    structure.set_namespace(urn)
    structure.set_dimensionAtObservation("AllDimensions")
    structure_usage = DataflowReferenceType()
    structure_usage.original_tag_name_ = "Structure"
    structure_usage.set_ns_def_("common")
    ref = DataflowRefType()
    ref.original_tag_name_ = "Ref"
    ref.set_id(dataset_id)
    ref.set_agencyID(agency_id)
    ref.set_version(version)
    ref.set_class("DataStructure")
    structure_usage.set_Ref(ref)
    structure.set_Structure(structure_usage)
    return structure


def get_version(root, dataset_id):
    expression = "/str:Structure/str:Structures/mes:DataStructures/mes:DataStructure[@id=$name]/@urn"
    record = root.xpath(expression, name=dataset_id,
                        namespaces={'mes': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure',
                                    'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message'})
    if (len(record) > 0):
        urn_aux = record[0]
        aux = urn_aux.split("(", 1)[1]
        version = aux.split(")", 1)[0]
    else:
        version = "1.0"
    return version


def parse_obs_generic(data_frame, root, structure_ref, validate_data=False):
    obs_attributes_keys = get_obs_attributes(root, structure_ref).keys()
    series_list_keys = list(get_series_attributes(root, structure_ref).keys())
    list_keys = data_frame.keys()
    observation_list = []
    iterations = len(data_frame)

    if validate_data:
        attr_enums = get_attr_enums(root, structure_ref).keys()
        codelist = get_codelist(root)

    logger.debug("Iterations for dataset %s: %d (Generic)" % (structure_ref, iterations))
    for row in range(iterations):
        obs_ = ObsOnlyType()
        obs_.original_tag_name_ = "Obs"
        obs_key = ValuesType()
        obs_key.original_tag_name_ = "ObsKey"
        obs_attr = ValuesType()
        obs_attr.original_tag_name_ = "Attributes"
        df = data_frame.iloc[row, :]
        for element in list_keys:
            aux = df[element]

            if element in series_list_keys:
                if (aux != '' or aux is not None) and validate_data:
                    if element in attr_enums and not validate_observation_value(aux, element, codelist, structure_ref):
                        return None
                elif aux == '' or aux is None:
                    aux = "N_A"

                attr_value = ComponentValueType()
                attr_value.original_tag_name_ = "Value"
                attr_value.set_id(element)
                attr_value.set_value(aux)
                obs_key.add_Value(attr_value)
            elif element in obs_attributes_keys and element.upper() != "OBS_VALUE":
                attr_value = ComponentValueType()
                attr_value.original_tag_name_ = "Value"
                attr_value.set_id(element)
                attr_value.set_value(aux)
                obs_attr.add_Value(attr_value)
            elif element.upper() == "OBS_VALUE":
                value = ObsValueType()
                value.original_tag_name_ = "ObsValue"
                value._namespace_prefix = "generic"
                value.set_value(aux)
                obs_.set_ObsValue(value)

        obs_.set_ObsKey(obs_key)
        obs_.set_Attributes(obs_attr)
        observation_list.append(obs_)

    return observation_list


def parse_obs_structure(data_frame, root, structure_ref, validate_data=False):
    obs_attributes = get_obs_attributes(root, structure_ref)
    series_attributes = get_series_attributes(root, structure_ref)
    list_keys = data_frame.keys()
    observation_list = []
    iterations = len(data_frame)
    logger.debug("Iterations for dataset %s: %d (Structure)" % (structure_ref, iterations))

    if validate_data:
        attr_enums = get_attr_enums(root, structure_ref).keys()
        codelist = get_codelist(root)

    for row in range(iterations):

        obs = Observation()
        series = Series()
        df = data_frame.iloc[row, :]

        if 'OBS_VALUE' in list_keys:
            obs_value = df['OBS_VALUE']
            obs.set_OBS_VALUE(obs_value)

        if 'TIME_PERIOD' in list_keys:
            obs_time_period = df['TIME_PERIOD']
            obs.set_TIME_PERIOD(obs_time_period)

        if 'REPORTING_YEAR_START_DAY' in list_keys:
            obs_reporting_year_start_day = df['REPORTING_YEAR_START_DAY']
            obs.set_REPORTING_YEAR_START_DAY(obs_reporting_year_start_day)

        obs_list_keys = obs_attributes.keys()

        for element in obs_list_keys:
            if element in df.keys():
                aux = df[element]
                if (aux != '' or aux is not None) and validate_data:
                    if element in attr_enums and not validate_observation_value(aux, element, codelist, structure_ref):
                        return None
                elif aux == '' or aux is None:
                    aux = "N_A"

                obs_attributes[element] = aux

        if len(series_attributes) > 0:
            series_list_keys = series_attributes.keys()
            for element in series_list_keys:
                if element in list_keys:
                    aux = df[element]
                    if aux == '' or aux is None:
                        aux = "N_A"

                    obs_attributes[element] = aux
                else:
                    obs_attributes[element] = 'N_A'

            # do = id_data.reindex(columns=series_list_keys)

        obs.set_anyAttributes_(obs_attributes.copy())
        series.set_anyAttributes_(series_attributes)
        observation_list.append(obs)

    return observation_list


def generate_message(dataset_list, path_to_metadata, header, dataset_type, validate_data=False):
    message = None
    all_dataset_valid = True
    root = etree.parse(path_to_metadata)
    structures = []

    if dataset_type == DatasetType.GenericDataSet:
        message = GenericDataType()
    elif dataset_type == DatasetType.StructureDataSet:
        message = StructureSpecificDataType()

    for element in dataset_list:
        data_set = None
        obs_list = None
        if validate_data:
            wrong_attributes = validate_dataset_attributes(root, element)
            if len(wrong_attributes.get("missing_attributes")) > 0 or len(
                    wrong_attributes.get("spared_attributes")) > 0:
                all_dataset_valid = False
                break

        dataset_attr = ValuesType()
        dataset_attr.original_tag_name_ = "Attributes"
        if dataset_type == DatasetType.GenericDataSet:
            data_set = GenericDataSetType()
            obs_list = parse_obs_generic(element.obs, root, element.code, validate_data)
            if obs_list == None:
                return None
            for key, value in element.attached_attributes.items():
                attr_value = ComponentValueType()
                attr_value.original_tag_name_ = "Value"
                attr_value.set_id(key)
                attr_value.set_value(value)
                dataset_attr.add_Value(attr_value)
                data_set.set_Attributes(dataset_attr)

        elif dataset_type == DatasetType.StructureDataSet:
            data_set = StructureDataSetType()
            obs_list = parse_obs_structure(element.obs, root, element.code, validate_data)
            if obs_list == None:
                return None
            dataset_attr = copy.deepcopy(element.attached_attributes)
            dataset_attr['xsi:dim_type'] = element.code + ":DataSet"
            data_set.set_anyAttributes_(dataset_attr)

        data_set._obs = obs_list

        # StructureRef
        data_set.set_structureRef(element.code)

        # DatasetAttributes
        data_set.set_reportingBeginDate(element.dataset_attributes.get('reportingBegin'))
        data_set.set_reportingEndDate(element.dataset_attributes.get('reportingEnd'))
        data_set.set_validFromDate(element.dataset_attributes.get('validFrom'))
        data_set.set_validToDate(element.dataset_attributes.get('validTo'))
        data_set.set_publicationYear(element.dataset_attributes.get('publicationYear'))
        data_set.set_publicationPeriod(element.dataset_attributes.get('publicationPeriod'))
        data_set.set_setID(element.code)
        data_set.set_action(element.dataset_attributes.get('action'))

        structure = get_structure(root, element.code, element.agencyID)
        structure.set_dimensionAtObservation(element.dataset_attributes.get('dimensionAtObservation'))

        if dataset_type == DatasetType.GenericDataSet:
            structure.set_namespace(None)

        structures.append(structure)
        message.add_DataSet(data_set)

    if validate_data and not all_dataset_valid:
        return None
    header.set_Structure(structures)
    message.set_Header(header)

    return message


def validate_dataset_attributes(root, dataset):
    dataset_attributes = get_dataset_attributes(root, dataset.code)
    attached_attributes = dataset.attached_attributes
    dataset_keys = dataset_attributes.keys()
    attached_keys = attached_attributes.keys()
    wrong_attributes = {"missing_attributes": [], "spared_attributes": []}

    for key in dataset_keys:
        if key not in attached_keys:
            wrong_attributes.get("missing_attributes").append(key)

    for key in attached_keys:
        if key not in dataset_keys:
            wrong_attributes.get("spared_attributes").append(key)

    return wrong_attributes


def validate_observation_value(value, attribute, codelist, setID):
    validate = True

    if not is_valid_enum_value("CL_" + attribute, value, codelist):
        validate = False
        print('Invalid value %s in column %s for dataset %s' % (value, attribute, setID))

    return validate


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
