'''
Created on 17 jul. 2020

@author: ruben
'''
from SDMXThon.common.generic import GenericDataStructureType
from SDMXThon.data.generic import DataSetType, ObsOnlyType, ValuesType, ComponentValueType, ObsValueType
from SDMXThon.message.generic import GenericDataType, GenericDataHeaderType, SenderType, PartyType
from SDMXThon.utils.xml_base import GdsCollector_


def main():
    message = GenericDataType()

    sender = SenderType()
    sender.set_id('Unknown')

    receiver = PartyType()
    receiver.set_id('not_supplied')

    structure_1 = GenericDataStructureType()
    structure_1.set_structureID('ASSETS_EX_LNA_SLR')
    structure_1.set_dimensionAtObservation('AllDimensions')

    structure_2 = GenericDataStructureType()
    structure_2.set_structureID('123456')
    structure_2.set_dimensionAtObservation('AllDimensions')

    structures = [structure_1, structure_2]

    header = GenericDataHeaderType()
    header.set_ID('new_test')
    header.set_Test(header.gds_format_boolean(False))
    header.set_Prepared(header.gds_parse_datetime('2020-07-07T12:00:00.000'))
    header.set_Sender(sender)
    header.add_Receiver(receiver)
    header.set_Structure(structures)
    header.original_tagname_ = "Header"

    message.set_Header(header)

    value_1 = ComponentValueType()
    value_1.set_id("FREQ")
    value_1.set_value("Q")
    value_1.original_tag_name_ = "Value"

    value_2 = ComponentValueType()
    value_2.set_id("DEPENDENCY_TYPE")
    value_2.set_value("INDEPENDENT")
    value_2.original_tag_name_ = "Value"

    value_3 = ComponentValueType()
    value_3.set_id("AUDST")
    value_3.set_value("AUDITED")
    value_3.original_tag_name_ = "Value"

    values = [value_1, value_2, value_3]

    attributes = ValuesType()
    attributes.set_Value(values)
    attributes.original_tagname_ = "Attributes"

    obsValue = ObsValueType()
    obsValue.set_id("HOLA")
    obsValue.set_value("1234")
    obsValue.original_tag_name_ = "ObsValue"

    obs_1 = ObsOnlyType()
    obs_1.set_ObsKey(attributes)
    obs_1.set_ObsValue(obsValue)
    obs_1.set_Attributes(attributes)
    obs_1.original_tagname_ = "Obs"

    obs_2 = ObsOnlyType()
    obs_2.set_ObsKey(attributes)
    obs_2.set_ObsValue(obsValue)
    obs_2.set_Attributes(attributes)
    obs_2.original_tagname_ = "Obs"

    obs = [obs_1, obs_2]

    dataset_1 = DataSetType()
    dataset_1.set_action("Replace")
    dataset_1.set_structureRef("ASSETS_EX_LNA_SLR")
    dataset_1.set_validFromDate(dataset_1.gds_parse_datetime("2020-07-07T12:00:00"))
    dataset_1.set_Attributes(attributes)
    dataset_1.set_Obs(obs)
    dataset_1.original_tagname_ = 'DataSet'

    dataset_2 = DataSetType()
    dataset_2.set_action("Append")
    dataset_2.set_structureRef("123456")
    dataset_2.set_validFromDate(dataset_2.gds_parse_datetime("2020-07-07T12:00:00"))
    dataset_2.set_Attributes(attributes)
    dataset_2.set_Obs(obs)
    dataset_2.original_tagname_ = 'DataSet'

    datasets = [dataset_1, dataset_2]

    message.set_DataSet(datasets)

    gds_collector = GdsCollector_
    message.gds_collector_ = gds_collector
    f = open("RBI_Export/create.xml", "w")
    f.write('<?xml version="1.0" ' + "encoding='UTF-8'?>\n")
    message.export(f, 0, pretty_print=True, has_parent=False)
    f.close()


if __name__ == '__main__':
    main()
