# flake8: noqa
import requests as rq

from sdmxthon.api.api import read_sdmx
from sdmxthon.model.base import InternationalString
from sdmxthon.model.definitions import DataStructureDefinition, \
    DataFlowDefinition
from sdmxthon.utils.handlers import split_unique_id


def format_locale(element: InternationalString):
    if element is None:
        return None

    if isinstance(element, dict):
        return element["en"]["content"]
    return str(element)


class BaseRequest:
    agencies_names = ['Bank for International Settlements', 'Eurostat',
                      'European Central Bank',
                      'International Labour Organization']

    name = None
    code = None
    base_url = None

    dataflows_url = None
    dataflows_params = None

    data_params = None

    @classmethod
    def get_dataflows(cls, params):
        for key in params:
            if key not in cls.dataflows_params:
                raise Exception
        for key in cls.dataflows_params:
            if key not in params:
                raise Exception
        url = cls.dataflows_url.format(**params)
        message = read_sdmx(url, validate=False)

        dataflows = message.payload['Dataflows'].values()
        list_dataflows = []
        for i in dataflows:
            name = format_locale(i.name)
            description = format_locale(i.description)

            i: DataFlowDefinition
            info = {'id': i.id,
                    'unique_id': i.unique_id,
                    'name': name,
                    'description': description,
                    'version': i.version}
            list_dataflows.append(info)
        return list_dataflows

    @classmethod
    def get_data_url(cls, unique_id, params) -> str:
        for key in params:
            if key not in cls.data_params:
                raise Exception

        for key in cls.data_params:
            if key not in params:
                raise Exception
        raise NotImplementedError

    @classmethod
    def get_metadata_url(cls, unique_id, params) -> str:
        raise NotImplementedError

    @classmethod
    def get_dataflow_data(cls, df_unique_id, params):
        url_df = cls.get_data_url(df_unique_id, params)

        req = rq.get(url_df)
        if req.status_code != 200:
            return {"status code": req.status_code, "message": req.text}
        else:
            file = f"development_files/{df_unique_id.replace(':', '-')}_data.xml"
            with open(file, "wb") as fl:
                fl.write(req.content)

        # data = read_sdmx(url_df, validate=False)
        # print(data)


START_PERIOD = 'start_period'
END_PERIOD = 'end_period'
FIRST_N = 'first_n'
LAST_N = 'last_n'
DETAIL = 'detail'
UPDATED_AFTER = 'updated_after'
DIMENSION_AT = 'dimension_at_observation'
REFERENCES = 'references'
INCLUDE_HISTORY = 'include_history'


class BISRequest(BaseRequest):
    name = 'Bank for International Settlements'
    code = 'BIS'
    base_url = 'https://stats.bis.org/api/v1'

    dataflows_params = ['code']
    dataflows_url = base_url + "/dataflow/{code}/all/latest?references=none&detail=full"

    data_params = ['key', 'detail']
    # key='all', detail='full'

    mapping_params_url = {
        START_PERIOD: 'startPeriod',
        END_PERIOD: 'endPeriod',
        FIRST_N: 'firstNObservations',
        LAST_N: 'lastNObservations'
    }

    @staticmethod
    def to_bis_id(unique_id):
        return ','.join(split_unique_id(unique_id))

    @classmethod
    def get_data_url(cls, unique_id, params):
        flow = cls.to_bis_id(unique_id)  # Flow
        # flow = f"{agency_id},{dataflow_id},{dataflow_version}"

        url_df = f"{cls.base_url}/data/{flow}/{params['key']}/all?"
        for key, value in cls.mapping_params_url.items():
            if key in params:
                url_df = f"{url_df}{value}={params[key]}&"
        url_df = f"{url_df}detail={params['detail']}"
        return url_df

    @classmethod
    def get_metadata_url(cls, unique_id, params):
        references = 'none'
        flow = cls.to_bis_id(unique_id)
        flow = flow.replace(',', '/')

        url_md = f"{cls.base_url}/dataflow/{flow}?references=none&detail=full"
        return url_md


class EUROSTATRequest(BaseRequest):
    name = 'Eurostat'
    code = 'ESTAT'
    base_url = 'https://ec.europa.eu/eurostat/api/dissemination'

    dataflows_params = ['code']
    dataflows_url = base_url + "/sdmx/2.1/dataflow/{code}/all?detail=referencestubs"

    mapping_params_url = {
        START_PERIOD: 'startPeriod',
        END_PERIOD: 'endPeriod',
        FIRST_N: 'firstNObservations',
        LAST_N: 'lastNObservations',
        DETAIL: 'detail',
    }

    @staticmethod
    def to_eurostat_id(unique_id):
        agency_id, id_, version = split_unique_id(unique_id)
        return id_, agency_id, version

    @classmethod
    def get_data_url(cls, unique_id, params):
        flow_id, agency_id, version = cls.to_eurostat_id(unique_id)  # Flow

        url_df = f"{cls.base_url}/sdmx/2.1/data/{flow_id}?"
        for key, value in cls.mapping_params_url.items():
            if key in params:
                url_df = f"{url_df}{value}={params[key]}&"
        url_df = url_df[:-1]  # Deletes the last character (?, &)
        return url_df

    @classmethod
    def get_metadata_url(cls, unique_id, params):
        flow_id, agency_id, version = cls.to_eurostat_id(unique_id)

        url_md = f"{cls.base_url}/sdmx/2.1/dataflow/{agency_id}/{flow_id}/{version}"

        return url_md


class ECBRequest(BaseRequest):
    name = 'European Central Bank'
    code = 'ECB'
    base_url = 'https://sdw-wsrest.ecb.europa.eu'

    dataflows_params = ['code']
    dataflows_url = base_url + "/service/dataflow/{code}/all/latest?references=none&detail=full"

    data_params = ['key', 'detail', 'provider_ref']
    # key='all', detail='full', provider_ref='all'

    mapping_params_url = {
        START_PERIOD: 'startPeriod',
        END_PERIOD: 'endPeriod',
        FIRST_N: 'firstNObservations',
        LAST_N: 'lastNObservations',
        UPDATED_AFTER: 'updatedAfter',
        DIMENSION_AT: 'dimensionAtObservation',
        # Only TIME_PERIOD and AllDimensions are supported values for the dimensionAtObservation parameter
        REFERENCES: 'references',
    }

    @staticmethod
    def to_ecb_id(unique_id):
        return ','.join(split_unique_id(unique_id))

    @classmethod
    def get_data_url(cls, unique_id, params):
        flow = cls.to_ecb_id(unique_id)  # Flow
        # flow = f"{agency_id},{dataflow_id},{dataflow_version}"

        url_df = f"{cls.base_url}/service/data/{flow}/{params['key']}/{params['provider_ref']}?"
        for key, value in cls.mapping_params_url.items():
            if key in params:
                url_df = f"{url_df}{value}={params[key]}&"
        url_df = f"{url_df}detail={params['detail']}"
        return url_df

    @classmethod
    def get_metadata_url(cls, unique_id, params):
        flow = cls.to_ecb_id(unique_id)  # Flow
        # flow = f"{agency_id},{dataflow_id},{dataflow_version}"
        agency_id, flow_id, version = flow.split(',')

        url_md = f"{cls.base_url}/service/dataflow/{agency_id}/{flow_id}/{version}?references=none&detail=full"
        return url_md


class ILORequest(BaseRequest):
    name = 'International Labour Organization'
    code = 'ILO'
    base_url = 'https://www.ilo.org/sdmx/rest'

    dataflows_params = ['code']

    dataflows_url = base_url + "/dataflow/{code}/all/latest?references=none&detail=full"

    data_params = ['key', 'detail']
    # key='all', detail='full', include_history='false'

    mapping_params_url = {
        START_PERIOD: 'startPeriod',
        END_PERIOD: 'endPeriod',
        FIRST_N: 'firstNObservations',
        LAST_N: 'lastNObservations',
        UPDATED_AFTER: 'updatedAfter',
        DIMENSION_AT: 'dimensionAtObservation',
        # Only TIME_PERIOD and AllDimensions are supported values for the dimensionAtObservation parameter
        INCLUDE_HISTORY: 'includeHistory',
    }

    @staticmethod
    def to_ilo_id(unique_id):
        agency_id, id_, version = split_unique_id(unique_id)
        return id_, agency_id, version

    @classmethod
    def get_data_url(cls, unique_id, params):
        flow_id, agency_id, version = cls.to_ilo_id(unique_id)  # Flow
        # flow = f"{agency_id},{dataflow_id},{dataflow_version}"

        url_df = f"{cls.base_url}/data/{flow_id}/{params['key']}/{agency_id}?"
        for key, value in cls.mapping_params_url.items():
            if key in params:
                url_df = f"{url_df}{value}={params[key]}&"
        url_df = f"{url_df}detail={params['detail']}"
        return url_df

    @classmethod
    def get_metadata_url(cls, unique_id, params):
        flow_id, agency_id, version = cls.to_ilo_id(unique_id)

        url_md = f"{cls.base_url}/dataflow/{agency_id}/{flow_id}/{version}?references=none&detail=full"
        return url_md


def main():
    ## EXAMPLES
    # Elección de la agencia
    x = ECBRequest()

    # Para listar los dataflows de cada agencia
    # message_def = x.get_dataflows(params={'code': 'ECB'})

    # Para devolver la url de los datos de un dataflow en concreto
    # url_str = x.get_data_url(unique_id='ECB:AME(1.0)', params={'key': 'all', 'detail': 'full', 'provider_ref': 'all', DIMENSION_AT: 2020, UPDATED_AFTER: 2020})

    # Para devolver datos de un dataflow en concreto
    message_def = x.get_dataflow_data(df_unique_id='ECB:AME(1.0)',
                                      params={'key': 'all', 'detail': 'full',
                                              'provider_ref': 'all',
                                              DIMENSION_AT: 'TIME_PERIOD',
                                              UPDATED_AFTER: 2020})
    print(message_def)


if __name__ == "__main__":
    main()
