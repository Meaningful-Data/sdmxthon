# flake8: noqa
from sdmxthon.model.itemScheme import Codelist, Code, Agency
from sdmxthon.model.message import Message
from sdmxthon.utils.enums import MessageTypeEnum

if __name__ == '__main__':
    agency = Agency(id_='SDMX', name='SDMX')
    # Create a codelist
    codelist = Codelist(id_='CL_TEST', maintainer=agency, version='1.0',
                        name='Codelist_1')
    code = Code(id_='CODE1', name='Code_1')
    codelist.append(code)

    code_2 = Code(id_='CODE2', name='Code_2')
    codelist.append(code_2)
    # Create a message
    message = Message(
        message_type=MessageTypeEnum.Metadata,
        payload=
        {
            'Codelists': {'mData:CL_TEST(1.0)': codelist}}
    )

    io_buf = message.to_xml()
    print(io_buf)
