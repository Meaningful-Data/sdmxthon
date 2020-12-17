import copy
from datetime import datetime
from urllib.request import urlopen

import numpy as np
from lxml import etree

from .metadata_parsers import get_codelist_model, get_concept_schemes, get_DSDs
from ..common.generic import GenericDataStructureType
from ..common.references import DataflowReferenceType
from ..common.refs import DataflowRefType
from ..data.generic import DataSetType as GenericDataSetType, \
    SeriesType, ObsType, TimeValueType
from ..data.generic import ValuesType, ComponentValueType, ObsOnlyType, ObsValueType
from ..message.generic import PartyType, SenderType, \
    StructureSpecificTimeSeriesDataHeaderType, GenericTimeSeriesDataHeaderType, StructureSpecificDataHeaderType, \
    GenericDataHeaderType
from ..model.structure import DataStructureDefinition, PrimaryMeasure, Dimension
from ..structure.specificbase import DataSetType as StructureDataSetType, ObsType as Observation, \
    SeriesType as Series
from ..utils.enums import DatasetType


def getMetadata(pathToMetadata) -> dict:
    if isinstance(pathToMetadata, str) and 'http' in pathToMetadata:
        res = urlopen(pathToMetadata)
        root = etree.parse(res)
    else:
        root = etree.parse(pathToMetadata)

    codelists = get_codelist_model(root)
    concepts = get_concept_schemes(root, codelists)
    return get_DSDs(root, concepts, codelists)


def get_structure_from_dsd(dsd: DataStructureDefinition, dataset, datasetType: DatasetType,
                           allDimensions=True):
    structure = GenericDataStructureType()
    structure.original_tag_name_ = "Structure"
    structure.set_ns_def_("messageXML")
    structure.set_structureID(dataset.structure.id)
    if datasetType == DatasetType.StructureDataSet or datasetType == DatasetType.StructureTimeSeriesDataSet:
        structure.set_namespace(dsd.uri)
    else:
        structure.set_namespace(None)
    if allDimensions:
        structure.set_dimensionAtObservation("AllDimensions")
    else:
        structure.set_dimensionAtObservation(dataset.datasetAttributes.get('dimensionAtObservation'))
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


def parse_series_generic(data, dsd, dimensionAtObservation):
    series_list = []
    series_key_codes = dsd.dimensionCodes
    attributes_codes = []
    obs_attributes_codes = []
    for record in dsd.attributeDescriptor.components.values():
        if record.relatedTo is not None:
            if isinstance(record.relatedTo, PrimaryMeasure):
                obs_attributes_codes.append(record.id)
            elif isinstance(record.relatedTo, list) and all(isinstance(n, Dimension) for n in record.relatedTo):
                if record.id in data.keys():
                    attributes_codes.append(record.id)

    all_codes = series_key_codes + attributes_codes

    iterations = len(data)
    series_dict = {}

    for row in range(iterations):

        df = data.iloc[row, :]
        series_key_data = df.loc[all_codes]
        obs_dict = {}

        obs_dict['OBS_VALUE'] = df['OBS_VALUE']
        obs_dict[dimensionAtObservation] = df[dimensionAtObservation]
        for element in obs_attributes_codes:
            if element in df.keys():
                aux = df[element]
                if aux is np.nan:
                    continue

                obs_dict[element] = aux
        row_data = ':'.join(map(str, series_key_data.values.tolist()))
        if row_data in series_dict.keys():
            series_dict[row_data].get('Data').append(obs_dict)
        else:
            series_dict[row_data] = {'Key': series_key_data, 'Data': [obs_dict]}

    del data

    for i in series_dict.values():
        series_ = SeriesType()
        series_attr = ValuesType()
        series_attr.original_tag_name_ = "Attributes"

        series_key = ValuesType()
        series_key.original_tag_name_ = "SeriesKey"

        key = i.get('Key').to_dict()
        data = i.get('Data')

        for attr in attributes_codes:
            if attr in key.keys():
                aux = key.get(attr)
                attr_value = ComponentValueType()
                attr_value.original_tag_name_ = "Value"
                attr_value.set_id(attr)
                attr_value.set_value(aux)
                series_attr.add_Value(attr_value)
        series_.set_Attributes(series_attr)

        for k in series_key_codes:
            if k in key.keys():
                aux = key.get(k)
                key_value = ComponentValueType()
                key_value.original_tag_name_ = "Value"
                key_value.set_id(k)
                key_value.set_value(aux)
                series_key.add_Value(key_value)

        series_.set_SeriesKey(series_key)

        for obs_data in data:
            obs_ = ObsType()
            obs_.original_tag_name_ = "Obs"
            obs_._namespace_prefix = "generic"
            obs_dim = TimeValueType()
            obs_dim.original_tag_name_ = "ObsDimension"
            obs_dim._namespace_prefix = "generic"
            obs_attr = ValuesType()
            obs_attr.original_tag_name_ = "Attributes"

            for key_data, value_data in obs_data.items():
                # ObsAttributes
                if key_data in obs_attributes_codes:
                    attr_value = ComponentValueType()
                    attr_value.original_tag_name_ = "Value"
                    attr_value.set_id(key_data)
                    attr_value.set_value(value_data)
                    obs_attr.add_Value(attr_value)
                # ObsDimension
                elif key_data == dimensionAtObservation:
                    obs_dim.set_id(key_data)
                    obs_dim.set_value(value_data)
                # ObsValue
                elif key_data.upper() == "OBS_VALUE":
                    value = ObsValueType()
                    value.original_tag_name_ = "ObsValue"
                    value._namespace_prefix = "generic"
                    value.set_value(value_data)
                    obs_.set_ObsValue(value)

            obs_.set_ObsDimension(obs_dim)
            obs_.set_Attributes(obs_attr)
            series_.add_Obs(obs_)
        series_list.append(series_)

    return series_list


def parse_series_structure(data, dsd, dimensionAtObservation):
    series_list = []
    series_key_codes = dsd.dimensionCodes
    series_key_codes.remove(dimensionAtObservation)
    obs_attributes_codes = []
    for record in dsd.attributeDescriptor.components.values():
        if record.relatedTo is not None:
            if isinstance(record.relatedTo, PrimaryMeasure):
                obs_attributes_codes.append(record.id)
            if isinstance(record.relatedTo, list) and all(isinstance(n, Dimension) for n in record.relatedTo):
                if record.id in data.keys():
                    series_key_codes.append(record.id)

    iterations = len(data)
    series_dict = {}

    for row in range(iterations):

        df = data.iloc[row, :]
        series_key_data = df.loc[series_key_codes]
        obs_dict = {}

        obs_dict['OBS_VALUE'] = df['OBS_VALUE']
        obs_dict[dimensionAtObservation] = df[dimensionAtObservation]
        for element in obs_attributes_codes:
            if element in df.keys():
                aux = df[element]
                if aux is np.nan:
                    continue

                obs_dict[element] = aux
        row_data = ':'.join(map(str, series_key_data.values.tolist()))
        if row_data in series_dict.keys():
            series_dict[row_data].get('Data').append(obs_dict)
        else:
            series_dict[row_data] = {'Key': series_key_data, 'Data': [obs_dict]}

    del data

    for i in series_dict.values():
        series = Series()
        data = i.get('Data')
        key = i.get('Key').to_dict()
        series.set_anyAttributes_(key)
        for obs_data in data:

            obs = Observation()
            if 'OBS_VALUE' in obs_data.keys():
                obs_value = obs_data.get('OBS_VALUE')
                obs.set_OBS_VALUE(obs_value)
                obs_data.pop('OBS_VALUE')

            obs.set_anyAttributes_(obs_data.copy())
            series.add_Obs(obs)
        series_list.append(series)
    return series_list


def defaultHeader(d_Type):
    if d_Type == DatasetType.GenericDataSet:
        header = GenericDataHeaderType()
    elif d_Type == DatasetType.StructureDataSet:
        header = StructureSpecificDataHeaderType()
    elif d_Type == DatasetType.GenericTimeSeriesDataSet:
        header = GenericTimeSeriesDataHeaderType()
    elif d_Type == DatasetType.StructureTimeSeriesDataSet:
        header = StructureSpecificTimeSeriesDataHeaderType()
    else:
        raise ValueError('Invalid Dataset type')

    header.set_ID('test')
    header.set_Test(True)
    header.set_Prepared(datetime.now())

    sender = SenderType()
    sender.set_id('Unknown')

    receiver = PartyType()
    receiver.set_id('Not_supplied')

    header.set_Sender(sender)
    header.add_Receiver(receiver)

    return header


def generateDataSetXML(dataset, dataset_type: DatasetType = DatasetType.GenericDataSet):
    dsd = dataset.structure

    allDimensions = dataset.datasetAttributes.get('dimensionAtObservation') == 'AllDimensions'

    dataset_attr = ValuesType()
    dataset_attr.original_tag_name_ = "Attributes"
    if allDimensions:
        if dataset_type == DatasetType.GenericDataSet:
            data_set = GenericDataSetType()
            obs_list = parse_obs_generic_from_dsd(dataset.data, dsd)

            for key, value in dataset.attachedAttributes.items():
                attr_value = ComponentValueType()
                attr_value.original_tag_name_ = "Value"
                attr_value.set_id(key)
                attr_value.set_value(value)
                dataset_attr.add_Value(attr_value)
                data_set.set_Attributes(dataset_attr)

        else:
            data_set = StructureDataSetType()
            obs_list = parse_obs_structure_from_dsd(dataset.data, dsd)
            dataset_attr = copy.deepcopy(dataset.attachedAttributes)
            dataset_attr['xsi:type'] = dataset.structure.id + ":DataSet"
            data_set.set_anyAttributes_(dataset_attr)

        data_set._obs = obs_list

    else:
        dimObs = dataset.datasetAttributes.get('dimensionAtObservation')
        if dataset_type == DatasetType.GenericDataSet:
            data_set = GenericDataSetType()
            series_list = parse_series_generic(dataset.data, dsd, dimObs)
            for key, value in dataset.attachedAttributes.items():
                attr_value = ComponentValueType()
                attr_value.original_tag_name_ = "Value"
                attr_value.set_id(key)
                attr_value.set_value(value)
                dataset_attr.add_Value(attr_value)
                data_set.set_Attributes(dataset_attr)
        else:
            data_set = StructureDataSetType()
            series_list = parse_series_structure(dataset.data, dsd,
                                                 dataset.datasetAttributes.get('dimensionAtObservation'))
            dataset_attr = copy.deepcopy(dataset.attachedAttributes)
            dataset_attr['xsi:type'] = dataset.structure.id + ":DataSet"
            data_set.set_anyAttributes_(dataset_attr)

        data_set.set_Series(series_list)

    # StructureRef
    data_set.set_structureRef(dataset.structure.id)

    # DatasetAttributes
    data_set.set_reportingBeginDate(dataset.datasetAttributes.get('reportingBegin'))
    data_set.set_reportingEndDate(dataset.datasetAttributes.get('reportingEnd'))
    data_set.set_validFromDate(dataset.datasetAttributes.get('validFrom'))
    data_set.set_validToDate(dataset.datasetAttributes.get('validTo'))
    data_set.set_publicationYear(dataset.datasetAttributes.get('publicationYear'))
    data_set.set_publicationPeriod(dataset.datasetAttributes.get('publicationPeriod'))
    data_set.set_setID(dataset.structure.id)
    data_set.set_action(dataset.datasetAttributes.get('action'))

    return data_set
