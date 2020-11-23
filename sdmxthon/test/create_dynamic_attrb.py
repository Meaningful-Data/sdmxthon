'''
Created on 17 jul. 2020

@author: ruben
'''
from lxml import etree


def ObsAttributes():
    expression = "//*//mes:DataStructure[@id=$name]//mes:AttributeList[//mes:Attribute[//*//Ref[@id='OBS_VALUE']]]//mes:Attribute//mes:ConceptIdentity//Ref//@id"
    root = etree.parse("RBI_Import/HICPAP_2020-02-26T09-03-16.xml")
    record = root.xpath(expression, name='HICPAP',
                        namespaces={'mes': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})
    attribute_list = {}
    for record_ in record:
        attribute_list[record_] = ''
    print("Obs Attributes: ")
    print(attribute_list)


def SeriesAttributes():
    expression = "//*//mes:DataStructure[@id=$name]//*//mes:Dimension//@id"
    root = etree.parse("RBI_Import/HICPAP_2020-02-26T09-03-16.xml")
    record = root.xpath(expression, name='HICPAP',
                        namespaces={'mes': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})
    attribute_list = {}
    for record_ in record:
        attribute_list[record_] = ''
    print("Series Attributes: ")
    print(attribute_list)


def DataSetAttributes():
    expression = '//*//mes:DataStructure[@id=$name]//mes:AttributeList[count(//*//mes:None) > 0]//mes:Attribute//mes:ConceptIdentity//Ref//@id'
    root = etree.parse("RBI_Import/HICPAP_2020-02-26T09-03-16.xml")
    record = root.xpath(expression, name='HICPAP',
                        namespaces={'mes': 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure'})
    attribute_list = {}
    for record_ in record:
        attribute_list[record_] = ''
    print("DataSet Attributes: ")
    print(attribute_list)


def main():
    ObsAttributes()
    SeriesAttributes()
    DataSetAttributes()


if __name__ == '__main__':
    main()
