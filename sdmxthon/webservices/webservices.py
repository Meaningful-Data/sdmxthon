"""
    Module to facilitate direct connections to
    known implementations of SDMX web services.
"""

from abc import ABC

from sdmxthon.api.api import read_sdmx
from sdmxthon.model.definitions import DataFlowDefinition
from sdmxthon.parsers.read import read_xml
from sdmxthon.webservices import query_builder


# from sdmxthon.utils.handlers import split_unique_id


class SdmxWebServiceConnection(ABC):
    "Base class for all requests"

    AGENCY_ID = None
    ENTRY_POINT = None
    WS_IMPLEMENTATION = None

    def get_all_dataflows(self):
        """Returns a list of all dataflows"""
        url = (f"{self.ENTRY_POINT}"
               f"{self.WS_IMPLEMENTATION.get_data_flows(self.AGENCY_ID)}")
        message = read_xml(url, validate=False)
        dataflows = message['Dataflows'].values()
        list_dataflows = []
        for i in dataflows:
            name = i.name
            description = i.description

            i: DataFlowDefinition
            info = {'id': i.id,
                    'unique_id': i.unique_id,
                    'name': name,
                    'description': description,
                    'version': i.version}
            list_dataflows.append(info)
        return list_dataflows

    def get_data_flow_url(self, flow, **kwargs) -> str:
        """
        Returns the URL to get one or many dataflows
        """
        url_params = self.WS_IMPLEMENTATION.get_data(flow, kwargs)

        return f"{self.ENTRY_POINT}{url_params}"

    def get_data_url(self, flow, **kwargs) -> str:
        """Returns the URL to get the data"""
        url_params = self.WS_IMPLEMENTATION.get_data(flow, kwargs)
        return f"{self.ENTRY_POINT}{url_params}"

    def get_dsd_url(self, resources=None, **kwargs) -> str:
        """Returns the URL to get the data"""
        url_params = self.WS_IMPLEMENTATION.get_dsds(resources=resources,
                                                     **kwargs)
        return f"{self.ENTRY_POINT}{url_params}"

    def get_data(self, **kwargs):
        """Returns a message with the data"""
        url = self.get_data_url(kwargs)
        message = read_sdmx(url, validate=False)
        return message

    def get_dsd(self, **kwargs):
        """Returns a message with the dsd"""
        url = self.get_dsd_url(kwargs)
        message = read_sdmx(url, validate=False)
        return message

    def get_dataflow(self, **kwargs):
        "Returns a message with the dataflow"
        url = self.get_data_flow_url(kwargs)
        message = read_sdmx(url, validate=False)
        return message

    @staticmethod
    def get_sdmxthon_code(url):
        "Returns a string with the SDMXThon code to get some data into Pandas"
        code = f"from sdmxthon import read_sdmx\n" \
               f"if __name__ == '__main__':\n" \
               f"\tmessage = read_sdmx('{url}', validate=True)\n" \
               f"\tprint(message.content)"
        return code


class BisWs(SdmxWebServiceConnection):
    "Implements the connection to the BIS SDMX web service"
    AGENCY_ID = 'BIS'
    ENTRY_POINT = 'https://stats.bis.org/api/v1'
    WS_IMPLEMENTATION = query_builder.QueryBuilder(query_builder.SdmxWs1p4())


class EuroStatWs(SdmxWebServiceConnection):
    "Implements the connection to the Eurostat SDMX web service"
    AGENCY_ID = 'ESTAT'
    ENTRY_POINT = 'https://ec.europa.eu/eurostat/api/dissemination'
    WS_IMPLEMENTATION = query_builder.QueryBuilder(query_builder.SdmxWs1p4())


class EcbWs(SdmxWebServiceConnection):
    "Implements the connection to the ECB SDMX web service"
    AGENCY_ID = 'ECB'
    ENTRY_POINT = 'https://sdw-wsrest.ecb.europa.eu'
    WS_IMPLEMENTATION = query_builder.QueryBuilder(query_builder.SdmxWs1p4())


class IloWs(SdmxWebServiceConnection):
    "Implements the connection to the ILO SDMX web service"
    AGENCY_ID = 'ILO'
    ENTRY_POINT = 'https://www.ilo.org/sdmx/rest'
    WS_IMPLEMENTATION = query_builder.QueryBuilder(query_builder.SdmxWs1p4())
