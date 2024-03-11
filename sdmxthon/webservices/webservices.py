"""
    Module to facilitate direct connections to
    known implementations of SDMX web services.
"""

from abc import ABC

import pandas as pd

from sdmxthon.api.api import read_sdmx
from sdmxthon.model.definitions import DataFlowDefinition
from sdmxthon.parsers.read import read_xml
from sdmxthon.webservices import query_builder


# from sdmxthon.utils.handlers import split_unique_id


class SdmxWebServiceConnection(ABC):
    """
    Base class for all SDMX web service connections.

    Implements the query builder
    :doc:`QueryBuilder <./query_builder>`
    and the methods to get the data from the web service.

    :param AGENCY_ID: The agency id of the web service
    :type AGENCY_ID: str

    :param ENTRY_POINT: The entry point of the web service
    :type ENTRY_POINT: str

    :param WS_IMPLEMENTATION: The query builder implementation
    :type WS_IMPLEMENTATION:
        :doc:`QueryBuilder <./query_builder>`

    """

    AGENCY_ID = None
    ENTRY_POINT = None
    WS_IMPLEMENTATION = None

    def get_all_dataflows(self):
        """
        Queries the API to get the simplified information of all dataflows

        :return: A list of dictionaries with the information of the dataflows
                 (id, unique_id, name, description, version)
        """
        url = (f"{self.ENTRY_POINT}"
               f"{self.WS_IMPLEMENTATION.get_data_flows()}")
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
        Generates the URL to get the dataflow

        :param flow: The id of the dataflow
        :type flow: str

        :param kwargs: The parameters to add to the URL
            (check the documentation of the get_data method in QueryBuilder )
            :py:meth:`~sdmxthon.webservices.query_builder.QueryBuilder.get_data`
        :type kwargs: dict
        """
        url_params = self.WS_IMPLEMENTATION.get_data_flows(resources=flow,
                                                           **kwargs)

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
        url = self.get_dsd_url(**kwargs)
        message = read_sdmx(url, validate=False)
        return message

    def get_data_flow(self, flow, **kwargs):
        """Returns a message with the dataflow"""
        url = self.get_data_flow_url(flow, **kwargs)
        message = read_sdmx(url, validate=False)
        return message

    def get_constraints(self, **kwargs):
        """Returns a message with the constraints"""
        url = self.get_constraints_url(kwargs)
        message = read_sdmx(url, validate=False)
        return message

    def get_pandas_with_names(self, flow, **kwargs):
        """Returns a Pandas DataFrame with the data"""

        def _create_codelist_dataframe(codelist, concept_name):
            codelist_list = []
            for id, code in codelist.items.items():
                item = {'id': id}
                for lang_code, strings in code.name.items():
                    item[f"{concept_name}-{lang_code}"] = strings['content']
                codelist_list.append(item)

            return pd.DataFrame(codelist_list)

        def _generate_insight_dict(metadata_payload):
            result = {}
            structure = metadata_payload['DataStructures']
            if len(structure) != 1:
                raise Exception('One structure expected')
            structure = list(structure.values())[0]
            components = structure.dimension_descriptor.components
            for id_, component in components.items():
                codelist = component.representation.codelist
                if codelist:
                    codelist = _create_codelist_dataframe(codelist,
                                                          component.id)
                result[id_] = {'name': component.concept_identity.name,
                               'codelist': codelist}
            return result

        def _generate_final_df_and_concepts_name(data, metadata_payload):
            insight_dict = _generate_insight_dict(metadata_payload)

            concepts_names = {}
            for code, component in insight_dict.items():
                concepts_names[code] = component['name']
                if component['codelist'] is not None:
                    data = data.merge(component['codelist'], left_on=code,
                                      right_on='id', how='inner')
                    data.drop(columns=['id_x', 'id_y'], inplace=True,
                              errors='ignore')
            data.to_csv('data.csv')
            return data, concepts_names

        metadata = self.get_data_flow(flow, references='descendants')
        message = self.get_data(flow, **kwargs)
        data = list(message.payload.values())[0].data
        result = _generate_final_df_and_concepts_name(data, metadata.payload)
        df = result[0]
        concepts_name = result[1]

        df.to_csv('data.csv')

        return df, concepts_name

    @staticmethod
    def get_sdmxthon_code(url):
        """Returns a string with the SDMXThon code to get
        some data into Pandas"""
        code = f"from sdmxthon import read_sdmx\n" \
               f"if __name__ == '__main__':\n" \
               f"\tmessage = read_sdmx('{url}', validate=True)\n" \
               f"\tprint(message.content)"
        return code


class BisWs(SdmxWebServiceConnection):
    """Implements the connection to the BIS SDMX web service"""
    AGENCY_ID = 'BIS'
    ENTRY_POINT = 'https://stats.bis.org/api/v1'
    WS_IMPLEMENTATION = query_builder.QueryBuilder(query_builder.SdmxWs1p4())


class EuroStatWs(SdmxWebServiceConnection):
    """Implements the connection to the Eurostat SDMX web service"""
    AGENCY_ID = 'ESTAT'
    ENTRY_POINT = 'https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1'
    WS_IMPLEMENTATION = query_builder.QueryBuilder(query_builder.SdmxWs1p4())

    def get_data_url(self, flow, start_period=None,
                     end_period=None, updated_after=None,
                     first_n_observations=None,
                     last_n_observations=None) -> str:
        """EuroStat specific implementation"""

        params = ""
        if start_period:
            initial = "&" if "?" in params else "?"
            params += f"{initial}startPeriod={start_period}"
        if end_period:
            initial = "&" if "?" in params else "?"
            params += f"{initial}endPeriod={end_period}"
        if updated_after:
            initial = "&" if "?" in params else "?"
            params += f"{initial}updatedAfter={updated_after}"
        if first_n_observations:
            initial = "&" if "?" in params else "?"
            params += f"{initial}firstNObservations={first_n_observations}"
        if last_n_observations:
            initial = "&" if "?" in params else "?"
            params += f"{initial}lastNObservations={last_n_observations}"

        return f"{self.ENTRY_POINT}/data/{flow}/" + params

    def get_data_flow_url(self, flow=None, agency_id=None,
                          version=None, references=None) -> str:
        version = version if version else "latest"
        agency_id = agency_id if agency_id else "all"

        references_query = f"?references={references}" if references else ""

        return (f"{self.ENTRY_POINT}/dataflow/{agency_id}/{flow}/{version}" +
                references_query)


class EcbWs(SdmxWebServiceConnection):
    """Implements the connection to the ECB SDMX web service"""
    AGENCY_ID = 'ECB'
    ENTRY_POINT = 'https://data-api.ecb.europa.eu/service'
    WS_IMPLEMENTATION = query_builder.QueryBuilder(query_builder.SdmxWs1p4())


class IloWs(SdmxWebServiceConnection):
    """Implements the connection to the ILO SDMX web service"""
    AGENCY_ID = 'ILO'
    ENTRY_POINT = 'https://www.ilo.org/sdmx/rest'
    WS_IMPLEMENTATION = query_builder.QueryBuilder(query_builder.SdmxWs1p4())


class OecdWs(SdmxWebServiceConnection):
    """Implements the connection to the OECD SDMX web service"""
    AGENCY_ID = 'OECD'
    ENTRY_POINT = 'https://sdmx.oecd.org/public/rest'
    WS_IMPLEMENTATION = query_builder.QueryBuilder(query_builder.SdmxWs1p5())


class OecdWs2(SdmxWebServiceConnection):
    """Implements the connection to the OECD SDMX web service"""
    AGENCY_ID = 'OECD'
    ENTRY_POINT = 'https://sdmx.oecd.org/public/rest/v2'
    WS_IMPLEMENTATION = query_builder.QueryBuilder(query_builder.SdmxWs2p0())

    def get_all_dataflows(self):
        """Not supported by v2, goes to v1"""
        return OecdWs().get_all_dataflows()


class UnicefWs(SdmxWebServiceConnection):
    """Implements the connection to the UNICEF SDMX web service"""
    AGENCY_ID = 'UNICEF'
    ENTRY_POINT = 'https://sdmx.data.unicef.org/ws/public/sdmxapi/rest'
    WS_IMPLEMENTATION = query_builder.QueryBuilder(query_builder.SdmxWs1p5())


class WitsWs(SdmxWebServiceConnection):
    """Implements the connection to the WITS SDMX web service"""
    AGENCY_ID = "WITS"
    ENTRY_POINT = 'http://wits.worldbank.org/API/V1/SDMX/V21/rest'
    WS_IMPLEMENTATION = query_builder.QueryBuilder(query_builder.SdmxWs1p4())


class UnsdWs(SdmxWebServiceConnection):
    """Implements the connection to the UNSD SDMX web service"""
    AGENCY_ID = "UNSD"
    ENTRY_POINT = 'http://data.un.org/WS/rest'
    WS_IMPLEMENTATION = query_builder.QueryBuilder(query_builder.SdmxWs1p5())


class InseeWs(SdmxWebServiceConnection):
    """Implements the connection to the INSEE SDMX web service"""
    AGENCY_ID = "INSEE"
    ENTRY_POINT = 'https://bdm.insee.fr/series/sdmx'
    WS_IMPLEMENTATION = query_builder.QueryBuilder(query_builder.SdmxWs1p5())


class IstatWs(SdmxWebServiceConnection):
    """Implements the connection to the ISTAT SDMX web service"""
    AGENCY_ID = "ISTAT"
    ENTRY_POINT = 'https://esploradati.istat.it/SDMXWS/rest'
    WS_IMPLEMENTATION = query_builder.QueryBuilder(query_builder.SdmxWs1p5())


class AbsWs(SdmxWebServiceConnection):
    """Implements the connection to the ISTAT SDMX web service"""
    AGENCY_ID = "ABS"
    ENTRY_POINT = 'https://api.data.abs.gov.au'
    WS_IMPLEMENTATION = query_builder.QueryBuilder(query_builder.SdmxWs1p5())
