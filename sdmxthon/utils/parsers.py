import copy
import logging
from typing import Dict

import numpy as np
from pandas import DataFrame

from SDMXThon.common.references import DataflowReferenceType
from .enums import DatasetType
from ..common.dataSet import DataSet
from ..common.generic import GenericDataStructureType
from ..common.refs import DataflowRefType
from ..data.generic import DataSetType as GenericDataSetType, \
    TimeSeriesDataSetType as GenericTimeSeriesDataSetType, SeriesType, ObsType, TimeValueType
from ..data.generic import ValuesType, ObsOnlyType, ComponentValueType, ObsValueType
from ..message.generic import GenericDataType, StructureSpecificDataType
from ..model.itemScheme import Code, CodeList, Agency, ConceptScheme, Concept
from ..model.structure import DataStructureDefinition, DimensionDescriptor, MeasureDescriptor, \
    AttributeDescriptor, Dimension, Attribute, PrimaryMeasure, TimeDimension
from ..model.structure import Representation
from ..structure.specificbase import DataSetType as StructureDataSetType, ObsType as Observation, \
    SeriesType as Series, TimeSeriesDataSetType as StructureTimeSeriesDataSetType

try:
    from lxml import etree as etree
except ImportError:
    from xml.etree import ElementTree as etree

CapturedNsmap_ = {}
print_warnings = True
SaveElementTreeNode = True

# create logger
logger = logging.getLogger("logger")


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
        return None


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
        return None


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
        elif len(list_related) == 0:
            att.relatedTo = None
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
        else:
            # TODO Missing dimension list on DSD (validate_metadata)
            continue

        # Add Measures
        expression = "./str:DataStructureComponents/str:MeasureList"
        measureElement = element.xpath(expression,
                                       namespaces={
                                           'str': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})
        if len(measureElement) == 1:
            md = MeasureDescriptor(id_=measureElement[0].attrib['id'], uri=measureElement[0].attrib['urn'])

            create_measures_data(dsd=element, measure_descriptor=md, concepts=concepts, codelists=codelists)
            dsd.measureDescriptor = md
        else:
            # TODO Missing measure list on DSD (validate_metadata)
            continue

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
        else:
            # TODO Missing attribute list on DSD (validate_metadata)
            continue

        identifier = id_creator(dsd.maintainer.id, dsd.id, dsd.version)
        dsds[identifier] = dsd
    return dsds


def get_structure_from_dsd(dsd: DataStructureDefinition, dataset: DataSet, datasetType: DatasetType,
                           allDimensions=True):
    structure = GenericDataStructureType()
    structure.original_tag_name_ = "Structure"
    structure.set_ns_def_("message")
    structure.set_structureID(dataset.code)
    if datasetType == DatasetType.StructureDataSet or datasetType == DatasetType.StructureTimeSeriesDataSet:
        structure.set_namespace(dsd.uri)
    else:
        structure.set_namespace(None)
    if allDimensions:
        structure.set_dimensionAtObservation("AllDimensions")
    else:
        structure.set_dimensionAtObservation(dataset.dataset_attributes.get('dimensionAtObservation'))
    structure_usage = DataflowReferenceType()
    structure_usage.original_tag_name_ = "Structure"
    structure_usage.set_ns_def_("common")
    ref = DataflowRefType()
    ref.original_tag_name_ = "Ref"
    ref.set_id(dsd.id)
    ref.set_agencyID(dsd.agencyId)
    ref.set_version(dsd.version)
    ref.set_class("DataStructure")
    structure_usage.set_Ref(ref)
    structure.set_Structure(structure_usage)
    return structure


def parse_obs_generic_from_dsd(data_frame, dsd: DataStructureDefinition):
    obs_attributes_keys = dsd.attributeCodes
    series_list_keys = dsd.dimensionCodes
    list_keys = data_frame.keys()
    observation_list = []
    iterations = len(data_frame)

    logger.debug("Iterations for dataset %s: %d (Generic)" % (dsd.id, iterations))
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

            if aux is np.nan:
                continue

            if element in series_list_keys:
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
                value.set_id("OBS_VALUE")
                value.set_value(aux)
                obs_.set_ObsValue(value)

        obs_.set_ObsKey(obs_key)
        obs_.set_Attributes(obs_attr)
        observation_list.append(obs_)

    return observation_list


def parse_obs_structure_from_dsd(data_frame, dsd: DataStructureDefinition):
    obs_attributes_keys = dsd.attributeCodes
    obs_attributes = {}
    for e in obs_attributes_keys:
        if e not in dsd.datasetAttributeCodes:
            obs_attributes[e] = ''
    series_list_keys = dsd.dimensionCodes
    series_attributes = {}
    for e in series_list_keys:
        series_attributes[e] = ''
    list_keys = data_frame.keys()
    observation_list = []
    iterations = len(data_frame)
    logger.debug("Iterations for dataset %s: %d (Structure)" % (dsd.id, iterations))

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
                if aux is np.nan:
                    continue

                obs_attributes[element] = aux

        if len(series_attributes) > 0:
            series_list_keys = series_attributes.keys()
            for element in series_list_keys:
                if element in list_keys:
                    aux = df[element]
                    if aux == '' or aux is None or aux is np.nan:
                        aux = "N_A"

                    obs_attributes[element] = aux
                else:
                    obs_attributes[element] = 'N_A'

        obs.set_anyAttributes_(obs_attributes.copy())
        series.set_anyAttributes_(series_attributes)
        observation_list.append(obs)

    return observation_list


def parse_series_generic(obs, dsd, dimensionAtObservation):
    count = 0
    series_list = []
    series_key_codes = dsd.dimensionCodes
    attributes_codes = []
    obs_attributes_codes = []
    for record in dsd.attributeDescriptor.components.values():
        if record.relatedTo is not None:
            if isinstance(record.relatedTo, PrimaryMeasure):
                obs_attributes_codes.append(record.id)
            elif isinstance(record.relatedTo, list) and all(isinstance(n, Dimension) for n in record.relatedTo):
                attributes_codes.append(record.id)
    logger.debug("Series to parse from DSD %s: %d (Generic)" % (dsd.id, len(obs)))
    for s in obs:
        count = count + 1
        if 'Data' not in s.keys() or 'Series' not in s.keys():
            # TODO Warning series in position %d couldn´t be parsed. Missing Data or Series
            continue
        series_data = s.get('Series').copy()
        data_frame = s.get('Data').copy()
        list_keys = data_frame.keys()
        iterations = len(data_frame)
        series_ = None
        series_ = SeriesType()
        series_attr = ValuesType()
        series_attr.original_tag_name_ = "Attributes"

        series_key = ValuesType()
        series_key.original_tag_name_ = "SeriesKey"

        for attr in attributes_codes:
            if attr in series_data.keys():
                aux = series_data.get(attr)
                attr_value = ComponentValueType()
                attr_value.original_tag_name_ = "Value"
                attr_value.set_id(attr)
                attr_value.set_value(aux)
                series_attr.add_Value(attr_value)
        series_.set_Attributes(series_attr)

        for key in series_key_codes:
            if key in series_data.keys():
                aux = series_data.get(key)
                key_value = ComponentValueType()
                key_value.original_tag_name_ = "Value"
                key_value.set_id(key)
                key_value.set_value(aux)
                series_key.add_Value(key_value)

        series_.set_SeriesKey(series_key)

        for row in range(iterations):
            obs_ = ObsType()
            obs_.original_tag_name_ = "Obs"
            obs_._namespace_prefix = "generic"
            obs_dim = TimeValueType()
            obs_dim.original_tag_name_ = "ObsDimension"
            obs_dim._namespace_prefix = "generic"
            obs_attr = ValuesType()
            obs_attr.original_tag_name_ = "Attributes"
            df = data_frame.iloc[row, :]
            for element in list_keys:
                aux = df[element]

                if aux is np.nan:
                    continue

                # ObsAttributes
                if element in obs_attributes_codes:
                    attr_value = ComponentValueType()
                    attr_value.original_tag_name_ = "Value"
                    attr_value.set_id(element)
                    attr_value.set_value(aux)
                    obs_attr.add_Value(attr_value)
                # ObsDimension
                elif element == dimensionAtObservation:
                    obs_dim.set_id(element)
                    obs_dim.set_value(aux)
                # ObsValue
                elif element.upper() == "OBS_VALUE":
                    value = ObsValueType()
                    value.original_tag_name_ = "ObsValue"
                    value._namespace_prefix = "generic"
                    value.set_value(aux)
                    obs_.set_ObsValue(value)

            obs_.set_ObsDimension(obs_dim)
            obs_.set_Attributes(obs_attr)
            series_.add_Obs(obs_)
        series_list.append(series_)

    return series_list


def parse_series_structure(obs, dsd, dimensionAtObservation):
    count = 0
    series_list = []
    series_key_codes = dsd.dimensionCodes
    attributes_codes = []
    obs_attributes_codes = []
    for record in dsd.attributeDescriptor.components.values():
        if record.relatedTo is not None:
            if isinstance(record.relatedTo, PrimaryMeasure):
                obs_attributes_codes.append(record.id)
            if isinstance(record.relatedTo, list) and all(isinstance(n, Dimension) for n in record.relatedTo):
                attributes_codes.append(record.id)

    for s in obs:
        count = count + 1
        if 'Data' not in s.keys() or 'Series' not in s.keys():
            # TODO Warning series in position %d couldn´t be parsed. Missing Data or Series
            continue
        series_data = s.get('Series')
        data_frame = s.get('Data')

        series = Series()
        series.set_anyAttributes_(series_data)

        list_keys = data_frame.keys()
        observation_list = []
        iterations = len(data_frame)
        logger.debug("Iterations for dataset %s: %d (Structure)" % (dsd.id, iterations))

        for row in range(iterations):

            obs = Observation()
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

            obs_attributes = {}
            for element in obs_attributes_codes:
                if element in df.keys():
                    aux = df[element]
                    if aux is np.nan:
                        continue

                    obs_attributes[element] = aux

            if len(series_key_codes) > 0:
                for element in series_key_codes:
                    if element in list_keys:
                        aux = df[element]

                        obs_attributes[element] = aux

            obs.set_anyAttributes_(obs_attributes.copy())
            series.add_Obs(obs)
        series_list.append(series)
    return series_list


def generate_message(dataset_list, dsd_dict, header, dataset_type):
    message = None
    structures = []

    if dataset_type == DatasetType.GenericDataSet or dataset_type == DatasetType.GenericTimeSeriesDataSet:
        message = GenericDataType()
    elif dataset_type == DatasetType.StructureDataSet or dataset_type == DatasetType.StructureTimeSeriesDataSet:
        message = StructureSpecificDataType()

    for element in dataset_list:
        dsd: DataStructureDefinition = dsd_dict[
            id_creator(element.agencyID, element.dataset_attributes.get('setId'), element.version)]

        if element.dataset_attributes.get('dimensionAtObservation') != 'AllDimensions':
            if dataset_type == DatasetType.GenericTimeSeriesDataSet or dataset_type == DatasetType.StructureTimeSeriesDataSet:
                allDimensions = False
            else:
                # TODO Warning dataset_type is not TimeSeries but dimensionAtObservation is not AllDimensions
                continue
        else:
            if dataset_type == DatasetType.GenericDataSet or dataset_type == DatasetType.StructureDataSet:
                allDimensions = True
            else:
                # TODO Warning dataset_type is TimeSeries but dimensionAtObservation is AllDimensions
                continue
        dataset_attr = ValuesType()
        dataset_attr.original_tag_name_ = "Attributes"
        if allDimensions:
            if dataset_type == DatasetType.GenericDataSet:
                data_set = GenericDataSetType()
                obs_list = parse_obs_generic_from_dsd(element.obs, dsd)
                if obs_list == None:
                    # TODO Warning dataset %s couldn´t be parsed
                    continue
                for key, value in element.attached_attributes.items():
                    attr_value = ComponentValueType()
                    attr_value.original_tag_name_ = "Value"
                    attr_value.set_id(key)
                    attr_value.set_value(value)
                    dataset_attr.add_Value(attr_value)
                    data_set.set_Attributes(dataset_attr)

            else:
                data_set = StructureDataSetType()
                obs_list = parse_obs_structure_from_dsd(element.obs, dsd)
                if obs_list == None:
                    # TODO Warning dataset %s couldn´t be parsed
                    continue
                dataset_attr = copy.deepcopy(element.attached_attributes)
                dataset_attr['xsi:type'] = element.code + ":DataSet"
                data_set.set_anyAttributes_(dataset_attr)

            data_set._obs = obs_list

        else:
            if dataset_type == DatasetType.GenericTimeSeriesDataSet:
                data_set = GenericTimeSeriesDataSetType()
                series_list = parse_series_generic(element.obs, dsd,
                                                   element.dataset_attributes.get('dimensionAtObservation'))
                if series_list == None:
                    # TODO Warning dataset %s couldn´t be parsed
                    continue
                for key, value in element.attached_attributes.items():
                    attr_value = ComponentValueType()
                    attr_value.original_tag_name_ = "Value"
                    attr_value.set_id(key)
                    attr_value.set_value(value)
                    dataset_attr.add_Value(attr_value)
                    data_set.set_Attributes(dataset_attr)

            else:
                data_set = StructureTimeSeriesDataSetType()
                series_list = parse_series_structure(element.obs, dsd,
                                                     element.dataset_attributes.get('dimensionAtObservation'))
                if series_list == None:
                    # TODO Warning dataset %s couldn´t be parsed
                    continue
                dataset_attr = copy.deepcopy(element.attached_attributes)
                dataset_attr['xsi:type'] = element.code + ":DataSet"
                data_set.set_anyAttributes_(dataset_attr)

            data_set.set_Series(series_list)

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

        structure = get_structure_from_dsd(dsd, element, dataset_type, allDimensions=allDimensions)

        structures.append(structure)
        message.add_DataSet(data_set)

    header.set_Structure(structures)
    message.set_Header(header)

    return message


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


def validate_observation_value_from_dsd(value, key, dsd):
    # Getting the codelist from that element
    codelist = dsd.dimensionDescriptor.components[key].localRepresentation.codeList

    if codelist is None:
        return True
    else:
        return value in codelist.items.keys()


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


def get_codelist_values(dsd: DataStructureDefinition) -> dict:
    data = {}

    for element in dsd.dimensionDescriptor.components.values():
        if element.localRepresentation.codeList is not None:
            data[element.id] = element.localRepresentation.codeList.items.keys()

    for record in dsd.attributeDescriptor.components.values():
        if record.localRepresentation.codeList is not None:
            data[record.id] = record.localRepresentation.codeList.items.keys()

    return data


def get_mandatory_attributes(dsd: DataStructureDefinition) -> list:
    data = []

    for record in dsd.attributeDescriptor.components.values():
        if record.relatedTo is not None:
            if isinstance(record.relatedTo, list) and all(isinstance(n, Dimension) for n in record.relatedTo):
                data.append(record.id)

    return data


def validate_obs(data: DataFrame, dsd: DataStructureDefinition, validation_list, mandatory_attributes: list = None):
    if 'OBS_VALUE' not in data.keys():
        validation_list.append('SS02: Missing OBS_VALUE for dataset %s' % dsd.id)

    if mandatory_attributes is None:
        mandatory_attributes = get_mandatory_attributes(dsd)

    codelist_values: dict = get_codelist_values(dsd)

    iterations = len(data)

    for i in dsd.dimensionCodes:
        if i not in data.keys():
            validation_list.append('SS01: Missing dimension %s on dataset %s' % (i, dsd.id))

    for j in mandatory_attributes:
        if j not in data.keys():
            validation_list.append('SS03: Missing attribute %s on dataset %s' % (j, dsd.id))

    for k in data.keys():
        df = data[k]
        if k not in dsd.dimensionCodes and k not in dsd.attributeCodes:
            continue
        for row in range(iterations):
            aux = df[row]

            if aux == np.nan:
                row_data = ':'.join(map(str, data.loc[row, :].values.tolist()))
                if k in mandatory_attributes:
                    validation_list.append(
                        'SS06: Missing value for attribute %s on row %s for dataset %s' % (k, row_data, dsd.id))
                elif k in dsd.attributeCodes:
                    validation_list.append(
                        'SS04: Missing value for attribute %s on row %s for dataset %s' % (k, row_data, dsd.id))
                elif k == 'OBS_VALUE':
                    validation_list.append(
                        'SS02: Missing value for OBS_VALUE on row %s for dataset %s' % (row_data, dsd.id))
                else:
                    validation_list.append(
                        'SS05: Missing value for dimension %s on row %s for dataset %s' % (k, row_data, dsd.id))

            elif k in codelist_values.keys() and aux not in codelist_values[k]:
                row_data = ':'.join(map(str, data.loc[row, :].values.tolist()))
                if k in mandatory_attributes:
                    validation_list.append('SS06: Wrong value "%s" for attribute %s on row %s for dataset %s' %
                                           (aux, k, row_data, dsd.id))
                elif k in dsd.attributeCodes:
                    validation_list.append('SS04: Wrong value "%s" for attribute %s on row %s for dataset %s' %
                                           (aux, k, row_data, dsd.id))
                else:
                    validation_list.append('SS05: Wrong value "%s" for dimension %s on row %s for dataset %s' %
                                           (aux, k, row_data, dsd.id))


def validate_series(obs: dict, dsd: DataStructureDefinition, validation_list):
    if 'Series' not in obs.keys():
        raise ValueError('Missing Series in obs for dataset %s' % dsd.id)

    if 'Data' not in obs.keys():
        raise ValueError('Missing Data in obs for dataset %s' % dsd.id)

    if not isinstance(obs.get('Data'), DataFrame):
        raise ValueError('Data of obs for dataset %s is not a pandas DataFrame', dsd.id)

    codelist_values = get_codelist_values(dsd)

    series = obs.get('Series')

    mandatory_attributes = get_mandatory_attributes(dsd)

    for i in dsd.dimensionCodes:
        if i not in series.keys():
            validation_list.append('SS01: Missing dimension %s on dataset %s' % (i, dsd.id))

    for j in mandatory_attributes:
        if j not in series.keys():
            validation_list.append('SS03: Missing attribute %s on dataset %s' % (j, dsd.id))

    for key, value in series.items():
        if key not in codelist_values.keys():
            continue
        if value not in codelist_values[key]:
            if key in mandatory_attributes:
                validation_list.append('SS06: Wrong value "%s" for attribute %s on Series for dataset %s' %
                                       (value, key, dsd.id))
            elif key in dsd.attributeCodes:
                validation_list.append('SS04: Wrong value "%s" for attribute %s on Series for dataset %s' %
                                       (value, key, dsd.id))
            else:
                validation_list.append('SS05: Wrong value "%s" for dimension %s on Series for dataset %s' %
                                       (value, key, dsd.id))

    validate_obs(obs.get('Data'), dsd, validation_list, mandatory_attributes)
