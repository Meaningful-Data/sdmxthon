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
        url_params = self.WS_IMPLEMENTATION.get_data_flows(resources=flow, **kwargs)

        return f"{self.ENTRY_POINT}{url_params}"

    def get_data_url(self, flow, **kwargs) -> str:
        """Returns the URL to get the data"""
        url_params = self.WS_IMPLEMENTATION.get_data(flow, **kwargs)
        return f"{self.ENTRY_POINT}{url_params}"

    def get_dsd_url(self, resources=None, **kwargs) -> str:
        """Returns the URL to get the data"""
        url_params = self.WS_IMPLEMENTATION.get_dsds(resources=resources,
                                                     **kwargs)
        return f"{self.ENTRY_POINT}{url_params}"

    def get_constraints_url(self, flow, **kwargs) -> str:
        """Returns the URL to get the constraints"""
        return (f"{self.ENTRY_POINT}"
                f"{self.WS_IMPLEMENTATION.get_constraints(flow, **kwargs)}")


    def get_data(self, flow, **kwargs):
        """Returns a message with the data"""
        url = self.get_data_url(flow, **kwargs)
        message = read_sdmx(url, validate=False)
        return message

    def get_dsd(self, **kwargs):
        """Returns a message with the dsd"""
        url = self.get_dsd_url(kwargs)
        message = read_sdmx(url, validate=False)
        return message

    def get_data_flow(self, flow, **kwargs):
        "Returns a message with the dataflow"
        url = self.get_data_flow_url(flow, **kwargs)
        message = read_sdmx(url, validate=False)
        return message

    def get_constraints(self, **kwargs):
        """Returns a message with the constraints"""
        url = self.get_constraints_url(kwargs)
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
    ENTRY_POINT = 'https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1'
    WS_IMPLEMENTATION = query_builder.QueryBuilder(query_builder.SdmxWs1p4())

    def get_data_url(self, flow, start_period=None,
        end_period=None, updated_after=None, first_n_observations=None,
        last_n_observations=None,) -> str:
        "EuroStat specific implementation"

        start_period_query = f"?startPeriod={start_period}" if start_period else ""
        end_period_query = f"?endPeriod={end_period}" if end_period else ""
        updated_after_query = f"?updatedAfter={updated_after}" if updated_after else ""
        first_n_observations_query = f"?firstNObservations={first_n_observations}" \
            if first_n_observations else ""
        last_n_observations_query = f"?lastNObservations={last_n_observations}" \
            if last_n_observations else ""

        return f"{self.ENTRY_POINT}/data/{flow}/" + start_period_query +\
            end_period_query + updated_after_query + first_n_observations_query +\
            last_n_observations_query

    def get_data_flow_url(self, flow=None, agency_id=None,
                       version=None, references=None) -> str:

        version = version if version else "latest"
        agency_id = agency_id if agency_id else "all"

        references_query = f"?references={references}" if references else ""

        return f"{self.ENTRY_POINT}/dataflow/{agency_id}/{flow}/{version}" + references_query


class EcbWs(SdmxWebServiceConnection):
    "Implements the connection to the ECB SDMX web service"
    AGENCY_ID = 'ECB'
    ENTRY_POINT = 'https://data-api.ecb.europa.eu/service'
    WS_IMPLEMENTATION = query_builder.QueryBuilder(query_builder.SdmxWs1p4())


class IloWs(SdmxWebServiceConnection):
    "Implements the connection to the ILO SDMX web service"
    AGENCY_ID = 'ILO'
    ENTRY_POINT = 'https://www.ilo.org/sdmx/rest'
    WS_IMPLEMENTATION = query_builder.QueryBuilder(query_builder.SdmxWs1p4())


# class OecdWs(SdmxWebServiceConnection):
#     "Implements the connection to the ILO SDMX web service"
#     AGENCY_ID = 'OECD'
#     ENTRY_POINT = 'https://stats.oecd.org/restsdmx/sdmx.ashx/GetData/'
#     WS_IMPLEMENTATION = None

#     def get_data_url(self, flow, start_period=None,
#         end_period=None, updated_after=None, first_n_observations=None,
#         last_n_observations=None,) -> str:
#         "EuroStat specific implementation"

#         start_period_query = f"?startPeriod={start_period}" if start_period else ""
#         end_period_query = f"?endPeriod={end_period}" if end_period else ""
#         updated_after_query = f"?updatedAfter={updated_after}" if updated_after else ""
#         first_n_observations_query = f"?firstNObservations={first_n_observations}" \
#             if first_n_observations else ""
#         last_n_observations_query = f"?lastNObservations={last_n_observations}" \
#             if last_n_observations else ""

#         return f"{self.ENTRY_POINT}/data/{flow}/" + start_period_query +\
#             end_period_query + updated_after_query + first_n_observations_query +\
#             last_n_observations_query

#     def get_data_flow_url(self, flow=None, agency_id=None,
#                        version=None, references=None) -> str:

#         version = version if version else "latest"
#         agency_id = agency_id if agency_id else "all"

#         references_query = f"?references={references}" if references else ""

#         return f"{self.ENTRY_POINT}/dataflow/{agency_id}/{flow}/{version}" + references_query