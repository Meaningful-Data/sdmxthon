# """
#     Module to facilitate direct connections to known implementations of SDMX web services.
# """

# # flake8: noqa
# import requests as rq

# from sdmxthon.api.api import read_sdmx
# from sdmxthon.model.definitions import DataFlowDefinition
# from sdmxthon.utils.handlers import split_unique_id


# class SdmxWebServiceConnection:
#     "Base class for all requests"

#     name = None
#     code = None
#     base_url = None

#     data_params = None

#     @property
#     def dataflows_url(self):
#         return self.base_url + "/dataflow/"


#     @classmethod
#     def get_dataflows(cls, params):
#         "Returns all dataflows defined for the agency"
#         for key in params:
#             if key not in cls.dataflows_params:
#                 raise ValueError(f"Invalid parameter {key}")

#         url = cls.dataflows_url.format(**params)
#         message = read_sdmx(url, validate=False)

#         dataflows = message.payload['Dataflows'].values()
#         list_dataflows = []
#         for i in dataflows:
#             name = i.name
#             description = i.description

#             i: DataFlowDefinition
#             info = {'id': i.id,
#                     'unique_id': i.unique_id,
#                     'name': name,
#                     'description': description,
#                     'version': i.version}
#             list_dataflows.append(info)
#         return list_dataflows

#     @classmethod
#     def get_data_url(cls, unique_id, params):
#         """Returns the URL to get the data"""
#         # Implement this method in the child class
#         raise NotImplementedError

#     @classmethod
#     def get_metadata_url(cls, unique_id, params) -> str:
#         """Returns the URL to get the data"""
#         # Implement this method in the child class
#         raise NotImplementedError

#     @classmethod
#     def get_dataflow_data(cls, df_unique_id, params):
#         """Returns data SDMX file from a dataflow id"""
#         url_df = cls.get_data_url(df_unique_id, params)

#         req = rq.get(url_df, timeout=10)
#         if req.status_code != 200:
#             return {"status code": req.status_code, "message": req.text}
#         else:
#             return req.content


#     @classmethod
#     def get_sdmxthon_code(cls, url):
#         "Returns a string with the SDMXThon code to get some data into Pandas"
#         code = f"from sdmxthon import read_sdmx\n" \
#                f"if __name__ == '__main__':\n" \
#                f"\tmessage = read_sdmx('{url}', validate=True)\n" \
#                f"\tprint(message.content)"
#         return code


# START_PERIOD = 'start_period'
# END_PERIOD = 'end_period'
# FIRST_N = 'first_n'
# LAST_N = 'last_n'
# DETAIL = 'detail'
# UPDATED_AFTER = 'updated_after'
# DIMENSION_AT = 'dimension_at_observation'
# REFERENCES = 'references'
# INCLUDE_HISTORY = 'include_history'


# class BisWs(SdmxWebServiceConnection):
#     "Implements the connection to the BIS SDMX web service"

#     name = 'Bank for International Settlements'
#     code = 'BIS'
#     base_url = 'https://stats.bis.org/api/v1'

#     dataflows_params = ['code']
#     dataflows_url = base_url + "/dataflow/{code}/all/latest?references=none&detail=full"

#     data_params = ['key', 'detail']
#     # key='all', detail='full'

#     mapping_params_url = {
#         START_PERIOD: 'startPeriod',
#         END_PERIOD: 'endPeriod',
#         FIRST_N: 'firstNObservations',
#         LAST_N: 'lastNObservations'
#     }

#     @staticmethod
#     def to_bis_id(unique_id):
#         return ','.join(split_unique_id(unique_id))

#     @classmethod
#     def get_data_url(cls, unique_id, params):
#         flow = cls.to_bis_id(unique_id)  # Flow
#         # flow = f"{agency_id},{dataflow_id},{dataflow_version}"
#         if 'key' not in params:
#             params['key'] = 'all'
#         if 'detail' not in params:
#             params['detail'] = 'full'
#         url_df = f"{cls.base_url}/data/{flow}/{params['key']}/all?"
#         for key, value in cls.mapping_params_url.items():
#             if key in params:
#                 url_df = f"{url_df}{value}={params[key]}&"
#         url_df = f"{url_df}detail={params['detail']}"
#         return url_df

#     @classmethod
#     def get_metadata_url(cls, unique_id, params):
#         flow = cls.to_bis_id(unique_id)
#         flow = flow.replace(',', '/')

#         url_md = f"{cls.base_url}/dataflow/{flow}?references=all&detail=full"
#         return url_md


# class EuroStatWs(SdmxWebServiceConnection):
#     name = 'Eurostat'
#     code = 'ESTAT'
#     base_url = 'https://ec.europa.eu/eurostat/api/dissemination'

#     dataflows_params = ['code']
#     dataflows_url = base_url + "/sdmx/2.1/dataflow/{code}/all?detail=referencestubs"

#     mapping_params_url = {
#         START_PERIOD: 'startPeriod',
#         END_PERIOD: 'endPeriod',
#         FIRST_N: 'firstNObservations',
#         LAST_N: 'lastNObservations',
#         DETAIL: 'detail',
#     }

#     @staticmethod
#     def to_eurostat_id(unique_id):
#         agency_id, id_, version = split_unique_id(unique_id)
#         return id_

#     @classmethod
#     def get_data_url(cls, unique_id, params):
#         flow_id = cls.to_eurostat_id(unique_id)  # Flow

#         url_df = f"{cls.base_url}/sdmx/2.1/data/{flow_id}/?"
#         for key, value in cls.mapping_params_url.items():
#             if key in params:
#                 url_df = f"{url_df}{value}={params[key]}&"
#         url_df = url_df[:-1]  # Deletes the last character (?, &)
#         return url_df

#     @classmethod
#     def get_metadata_url(cls, unique_id, params):
#         flow_id, agency_id, version = cls.to_eurostat_id(unique_id)

#         url_md = f"{cls.base_url}/sdmx/2.1/dataflow/{agency_id}/{flow_id}/{version}"

#         return url_md


# class EcbWs(SdmxWebServiceConnection):
#     name = 'European Central Bank'
#     code = 'ECB'
#     base_url = 'https://sdw-wsrest.ecb.europa.eu'

#     dataflows_params = ['code']
#     dataflows_url = base_url + "/service/dataflow/{code}/all/latest?references=none&detail=full"

#     data_params = ['key', 'detail', 'provider_ref']
#     # key='all', detail='full', provider_ref='all'

#     mapping_params_url = {
#         START_PERIOD: 'startPeriod',
#         END_PERIOD: 'endPeriod',
#         FIRST_N: 'firstNObservations',
#         LAST_N: 'lastNObservations',
#         UPDATED_AFTER: 'updatedAfter',
#         DIMENSION_AT: 'dimensionAtObservation',
#         # Only TIME_PERIOD and AllDimensions are supported values for the dimensionAtObservation parameter
#         REFERENCES: 'references',
#     }

#     @staticmethod
#     def to_ecb_id(unique_id):
#         return ','.join(split_unique_id(unique_id))

#     @classmethod
#     def get_data_url(cls, unique_id, params):
#         flow = cls.to_ecb_id(unique_id)  # Flow
#         # flow = f"{agency_id},{dataflow_id},{dataflow_version}"
#         if 'key' not in params:
#             params['key'] = 'all'
#         if 'detail' not in params:
#             params['detail'] = 'full'
#         if 'provider_ref' not in params:
#             params['provider_ref'] = 'all'
#         url_df = f"{cls.base_url}/service/data/{flow}/{params['key']}/{params['provider_ref']}?"
#         for key, value in cls.mapping_params_url.items():
#             if key in params:
#                 url_df = f"{url_df}{value}={params[key]}&"
#         url_df = f"{url_df}detail={params['detail']}"
#         return url_df

#     @classmethod
#     def get_metadata_url(cls, unique_id, params):
#         flow = cls.to_ecb_id(unique_id)  # Flow
#         # flow = f"{agency_id},{dataflow_id},{dataflow_version}"
#         agency_id, flow_id, version = flow.split(',')

#         url_md = f"{cls.base_url}/service/dataflow/{agency_id}/{flow_id}/{version}?references=all&detail=full"
#         return url_md


# class IloWs(SdmxWebServiceConnection):
#     name = 'International Labour Organization'
#     code = 'ILO'
#     base_url = 'https://www.ilo.org/sdmx/rest'

#     dataflows_params = ['code']

#     dataflows_url = base_url + "/dataflow/{code}/all/latest?references=none&detail=full"

#     data_params = ['key', 'detail']
#     # key='all', detail='full', include_history='false'

#     mapping_params_url = {
#         START_PERIOD: 'startPeriod',
#         END_PERIOD: 'endPeriod',
#         FIRST_N: 'firstNObservations',
#         LAST_N: 'lastNObservations',
#         UPDATED_AFTER: 'updatedAfter',
#         DIMENSION_AT: 'dimensionAtObservation',
#         # Only TIME_PERIOD and AllDimensions are supported values for the dimensionAtObservation parameter
#         INCLUDE_HISTORY: 'includeHistory',
#     }

#     @staticmethod
#     def to_ilo_id(unique_id):
#         agency_id, id_, version = split_unique_id(unique_id)
#         return agency_id, id_, version

#     @classmethod
#     def get_data_url(cls, unique_id, params):
#         agency_id, flow_id, version = cls.to_ilo_id(unique_id)  # Flow
#         # flow = f"{agency_id},{dataflow_id},{dataflow_version}"
#         if 'key' not in params:
#             params['key'] = 'all'
#         if 'detail' not in params:
#             params['detail'] = 'full'
#         url_df = f"{cls.base_url}/data/{flow_id}/{params['key']}/{agency_id}?"
#         for key, value in cls.mapping_params_url.items():
#             if key in params:
#                 url_df = f"{url_df}{value}={params[key]}&"
#         url_df = f"{url_df}detail={params['detail']}"
#         return url_df

#     @classmethod
#     def get_metadata_url(cls, unique_id, params):
#         agency_id, flow_id, version = cls.to_ilo_id(unique_id)

#         url_md = f"{cls.base_url}/dataflow/{agency_id}/{flow_id}/{version}?references=all&detail=full"
#         return url_md
