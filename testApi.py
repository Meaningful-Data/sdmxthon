# flake8: noqa

import pandas as pd
import requests as rq

from sdmxthon.api.api import get_pandas_df, read_sdmx
from sdmxthon.model.dataset import Dataset
from sdmxthon.model.definitions import DataStructureDefinition, \
    DataFlowDefinition
from sdmxthon.utils.enums import MessageTypeEnum
from sdmxthon.utils.handlers import first_element_dict

data_file1 = "development_files/data_file1.xml"

ds2_file = "development_files/ds2.xml"
ds2_data_file = "development_files/ds2_data.xml"

ds3_file = "development_files/ds3.xml"
ds3_data_file = "development_files/ds3_data.xml"

ds4_file = "development_files/ds4.xml"
ds4_data_file = "development_files/ds4_data.xml"

ds5_file = "development_files/ds5.xml"
ds5_data_file = "development_files/ds5_data.xml"

ds6_file = "development_files/ds6.xml"
ds6_data_file = "development_files/ds6_data.xml"

ds7_file = "development_files/ds7.xml"
ds7_data_file = "development_files/ds7_data.xml"

ds8_file = "development_files/ds8.xml"
ds8_data_file = "development_files/ds8_data.xml"

url_eu_data1 = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/" \
               "EI_BSCO_M$DEFAULTVIEW/?format=sdmx_2.1_structured"

url_eu_ds2 = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/dataflow/ESTAT/TGS00045/1.0?references=descendants&detail=referencepartial&format=sdmx_2.1_generic"
url_eu_ds2_data = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/TGS00045/?format=sdmx_2.1_generic"

url_eu_ds3 = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/dataflow/ESTAT/RAIL_AC_CATVICT/1.0?references=descendants&detail=referencepartial&format=sdmx_2.1_generic"
url_eu_ds3_data = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/RAIL_AC_CATVICT/?format=sdmx_2.1_generic"

url_eu_ds4 = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/dataflow/ESTAT/HRST_ST_NCAT/1.0?references=descendants&detail=referencepartial&format=sdmx_2.1_generic"
url_eu_ds4_data = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/HRST_ST_NCAT/?format=sdmx_2.1_generic"

url_eu_ds5 = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/dataflow/ESTAT/PAT_EP_NTOT/1.0?references=descendants&detail=referencepartial&format=sdmx_2.1_generic"
url_eu_ds5_data = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/PAT_EP_NTOT/?format=sdmx_2.1_generic"

url_eu_ds6 = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/dataflow/ESTAT/SDG_13_20/1.0?references=descendants&detail=referencepartial&format=sdmx_2.1_generic"
url_eu_ds6_data = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/SDG_13_20/?format=sdmx_2.1_generic"

url_bis = "https://stats.bis.org/api/v1/dataflow/BIS/all/latest?references=none&detail=full"


def return_agencies():
    agencies = {'BIS': {'name': 'Bank for International Settlements',
                        'code': 'BIS',
                        'api_base_url': 'https://stats.bis.org/api/v1'
                        },
                'EUROSTAT': {'name': 'Eurostat',
                             'code': 'ESTAT',
                             'api_base_url': 'https://ec.europa.eu/eurostat/api/dissemination'
                             },
                'ECB': {'name': 'European Central Bank',
                        'code': 'ECB',
                        'api_base_url': 'https://sdw-wsrest.ecb.europa.eu'
                        },
                'ILO': {'name': 'International Labour Organization',
                        'code': 'ILO',
                        'api_base_url': 'https://www.ilo.org/sdmx/rest'
                        }
                }
    return agencies


def BIS_return_dataflows(name='BIS'):
    agencies = return_agencies()
    agency_id = agencies[name]['code']

    base_url = agencies[name]['api_base_url']
    version = 'all'
    resource_id = 'all'
    references = 'none'
    detail = 'full'

    url_bis = base_url + '/dataflow/' + agency_id + '/' + resource_id + '/' + version + '?references=' + references + '&detail=' + detail

    message = read_sdmx(url_bis, validate=False)

    dataflows = message.payload['Dataflows'].values()
    list_dataflows = []
    for i in dataflows:
        i: DataFlowDefinition
        info = {'id': i.id,
                'unique_id': i.unique_id,
                'name': i.name,
                'description': i.description,
                'version': i.version}
        list_dataflows.append(info)

    return list_dataflows


def BIS_return_dataflow_data(name='BIS',
                             dataflow_unique_id='BIS:WS_CBPOL_D(1.0)',
                             key='all', start_period=None, end_period=None,
                             first_n_observations=None,
                             last_n_observations=None,
                             detail='full'):
    agencies = return_agencies()

    agencies_names = agencies.keys()
    if name not in agencies_names:
        return {"status code": 404,
                "message": "This agency name does not match with any available agency"}
    agency_id = agencies[name]['code']
    base_url = agencies[name]['api_base_url']

    dataflows = BIS_return_dataflows(name)

    list_dataflows_unique_id = []
    for df in dataflows:
        list_dataflows_unique_id.append(df['unique_id'])

    if dataflow_unique_id not in list_dataflows_unique_id:
        return {"status code": 404,
                "message": "This unique id does not match with any available dataset"}
    else:
        index = list_dataflows_unique_id.index(dataflow_unique_id)

    dataflow = dataflows[index]

    dataflow_version = dataflow['version']
    dataflow_id = dataflow['id']
    flow = agency_id + '%2C' + dataflow_id + '%2C' + dataflow_version
    url_df = base_url + '/data/' + flow + '/' + key + '/all?'
    if start_period is not None:
        url_df = url_df + 'startPeriod=' + start_period + '&'
    if end_period is not None:
        url_df = url_df + 'endPeriod=' + end_period + '&'
    if first_n_observations is not None:
        url_df = url_df + 'firstNObservations=' + first_n_observations + '&'
    if last_n_observations is not None:
        url_df = url_df + 'lastNObservations=' + last_n_observations + '&'

    url_df = url_df + 'detail=' + detail

    req = rq.get(url_df)
    if req.status_code != 200:
        return {"status code": req.status_code, "message":
            req.text.split('<com:Text>')[1].split('</com:Text>')[0]}
    else:
        file = f"development_files/{dataflow_id}_data.xml"
        with open(file, "wb") as fl:
            fl.write(req.content)

    # data = read_sdmx(url_df, validate=False)
    # print(data)


def EUROSTAT_return_dataflows(name='EUROSTAT'):
    agencies = return_agencies()
    agency_id = agencies[name]['code']

    base_url = agencies[name]['api_base_url']
    resource = 'dataflow'
    details = 'allstubs'

    url_estat = base_url + '/sdmx/2.1/' + resource + '/' + agency_id + '/all?detail=' + details

    message = read_sdmx(url_estat, validate=False)
    dataflows = message.payload['Dataflows'].values()
    list_dataflows = []
    for i in dataflows:
        i: DataFlowDefinition
        info = {'id': i.id,
                'unique_id': i.unique_id,
                'name': i.name['en']['content'],
                'description': i.description,
                'version': i.version}
        list_dataflows.append(info)
    return list_dataflows


def EUROSTAT_return_dataflow_data(name='EUROSTAT',
                                  dataflow_unique_id='ESTAT:HLTH_EHIS_SK4E(1.0)',
                                  start_period=None, end_period=None,
                                  first_n_observations=None,
                                  last_n_observations=None,
                                  detail=None):
    agencies = return_agencies()

    agencies_names = agencies.keys()
    if name not in agencies_names:
        return {"status code": 404,
                "message": "This agency name does not match with any available agency"}
    agency_id = agencies[name]['code']
    base_url = agencies[name]['api_base_url']

    dataflows = EUROSTAT_return_dataflows(name)

    list_dataflows_unique_id = []
    for df in dataflows:
        list_dataflows_unique_id.append(df['unique_id'])

    if dataflow_unique_id not in list_dataflows_unique_id:
        return {"status code": 404,
                "message": "This unique id does not match with any available dataset"}
    else:
        index = list_dataflows_unique_id.index(dataflow_unique_id)

    dataflow = dataflows[index]
    dataflow_version = dataflow['version']
    dataflow_id = dataflow['id']
    url_df = base_url + '/sdmx/2.1/data/' + dataflow_id + '?'
    if start_period is not None:
        url_df = url_df + 'startPeriod=' + start_period + '&'
    if end_period is not None:
        url_df = url_df + 'endPeriod=' + end_period + '&'
    if first_n_observations is not None:
        url_df = url_df + 'firstNObservations=' + first_n_observations
    if last_n_observations is not None:
        url_df = url_df + 'lastNObservations=' + last_n_observations + '&'
    if detail is not None:
        url_df = url_df + 'detail=' + detail

    req = rq.get(url_df)
    if req.status_code != 200:
        return {"status code": req.status_code, "message":
            req.text.split('<com:Text>')[1].split('</com:Text>')[0]}
    else:
        file = f"development_files/{dataflow_id}_data.xml"
        with open(file, "wb") as fl:
            fl.write(req.content)

    # data = read_sdmx(url_df, validate=False)
    # print(data)


def ECB_return_dataflows(name='ECB'):
    agencies = return_agencies()
    agency_id = agencies[name]['code']

    base_url = agencies[name]['api_base_url']
    version = 'all'
    resource_id = 'all'
    references = 'none'
    detail = 'full'

    url_bis = base_url + '/service/dataflow/' + agency_id + '/' + resource_id + '/' + version + '?references=' + references + '&detail=' + detail

    message = read_sdmx(url_bis, validate=False)

    dataflows = message.payload['Dataflows'].values()
    list_dataflows = []
    for i in dataflows:
        i: DataFlowDefinition
        info = {'id': i.id,
                'unique_id': i.unique_id,
                'name': i.name,
                'description': i.description,
                'version': i.version}
        list_dataflows.append(info)

    return list_dataflows


def ECB_return_dataflow_data(name='ECB',
                             dataflow_unique_id='ESTAT:HLTH_EHIS_SK4E(1.0)',
                             start_period=None, end_period=None,
                             updated_after=None,
                             first_n_observations=None,
                             last_n_observations=None,
                             dimension_at_observation=None,
                             detail='full',
                             key='all',
                             provider_ref='all',
                             references=None):
    agencies = return_agencies()

    agencies_names = agencies.keys()
    if name not in agencies_names:
        return {"status code": 404,
                "message": "This agency name does not match with any available agency"}
    agency_id = agencies[name]['code']
    base_url = agencies[name]['api_base_url']

    dataflows = ECB_return_dataflows(name)

    list_dataflows_unique_id = []
    for df in dataflows:
        list_dataflows_unique_id.append(df['unique_id'])

    if dataflow_unique_id not in list_dataflows_unique_id:
        return {"status code": 404,
                "message": "This unique id does not match with any available dataset"}
    else:
        index = list_dataflows_unique_id.index(dataflow_unique_id)

    dataflow = dataflows[index]
    dataflow_version = dataflow['version']
    dataflow_id = dataflow['id']
    url_df = base_url + '/service/data/' + agency_id + ',' + dataflow_id + ',' + dataflow_version + '/' + key + '/' + provider_ref + '?'
    # agency_id and dataflow_id could be 'all' and dataflow_version could be 'all' and 'latest'
    if start_period is not None:
        url_df = url_df + 'startPeriod=' + start_period + '&'
    if end_period is not None:
        url_df = url_df + 'endPeriod=' + end_period + '&'
    if updated_after is not None:
        url_df = url_df + 'updatedAfter=' + updated_after + '&'
    if first_n_observations is not None:
        url_df = url_df + 'firstNObservations=' + first_n_observations + '&'
    if last_n_observations is not None:
        url_df = url_df + 'lastNObservations=' + last_n_observations + '&'
    if dimension_at_observation is not None:
        url_df = url_df + 'dimensionAtObservation=' + dimension_at_observation + '&'
    if references is not None:
        url_df = url_df + 'references=' + detail
    url_df = url_df + 'detail=' + detail

    req = rq.get(url_df)
    if req.status_code != 200:
        return {"status code": req.status_code, "message":
            req.text.split('<com:Text>')[1].split('</com:Text>')[0]}
    else:
        file = f"development_files/{dataflow_id}_data.xml"
        with open(file, "wb") as fl:
            fl.write(req.content)

    # data = read_sdmx(url_df, validate=False)
    # print(data)


def ILO_return_dataflows(name='ILO'):
    agencies = return_agencies()
    agency_id = agencies[name]['code']

    base_url = agencies[name]['api_base_url']
    version = 'all'
    resource_id = 'all'
    references = 'none'
    detail = 'full'

    url_bis = base_url + '/dataflow/' + agency_id + '/' + resource_id + '/' + version + '?references=' + references + '&detail=' + detail

    message = read_sdmx(url_bis, validate=False)
    print(message)

    dataflows = message.payload['Dataflows'].values()
    list_dataflows = []
    for i in dataflows:
        i: DataFlowDefinition
        info = {'id': i.id,
                'unique_id': i.unique_id,
                'name': i.name,
                'description': i.description,
                'version': i.version}
        list_dataflows.append(info)

    return list_dataflows


def ILO_return_dataflow_data(name='ILO',
                             dataflow_unique_id='ILO:DF_CLD_TPOP_SEX_AGE_GEO_NB(1.0)',
                             key='all', start_period=None, end_period=None,
                             first_n_observations=None,
                             last_n_observations=None,
                             dimension_at_observation=None,
                             updated_after=None,
                             include_history='false',
                             detail='full'):
    agencies = return_agencies()
    print(agencies)
    agencies_names = agencies.keys()
    if name not in agencies_names:
        return {"status code": 404,
                "message": "This agency name does not match with any available agency"}
    agency_id = agencies[name]['code']
    base_url = agencies[name]['api_base_url']

    dataflows = ILO_return_dataflows(name)

    list_dataflows_unique_id = []
    for df in dataflows:
        list_dataflows_unique_id.append(df['unique_id'])

    if dataflow_unique_id not in list_dataflows_unique_id:
        return {"status code": 404,
                "message": "This unique id does not match with any available dataset"}
    else:
        index = list_dataflows_unique_id.index(dataflow_unique_id)

    dataflow = dataflows[index]

    dataflow_version = dataflow['version']
    dataflow_id = dataflow['id']

    url_df = base_url + '/data/' + dataflow_id + '/' + key + '/' + agency_id + '?'
    if start_period is not None:
        url_df = url_df + 'startPeriod=' + start_period + '&'
    if end_period is not None:
        url_df = url_df + 'endPeriod=' + end_period + '&'
    if first_n_observations is not None:
        url_df = url_df + 'firstNObservations=' + first_n_observations + '&'
    if last_n_observations is not None:
        url_df = url_df + 'lastNObservations=' + last_n_observations + '&'
    if dimension_at_observation is not None:
        url_df = url_df + 'dimensionAtObservation=' + dimension_at_observation + '&'
    if updated_after is not None:
        url_df = url_df + 'updatedAfter=' + updated_after + '&'
    if include_history != 'false':
        url_df = url_df + 'includeHistory=' + include_history + '&'

    url_df = url_df + 'detail=' + detail

    req = rq.get(url_df)
    if req.status_code != 200:
        return {"status code": req.status_code, "message":
            req.text.split('<com:Text>')[1].split('</com:Text>')[0]}
    else:
        file = f"development_files/{dataflow_id}_data.xml"
        with open(file, "wb") as fl:
            fl.write(req.content)

    # data = read_sdmx(url_df, validate=False)
    # print(data)


def main():
    ## EXAMPLES
    # message = read_sdmx(data_file1, validate=False)

    # print(message.payload['ESTAT:EI_BSCO_M$DEFAULTVIEW(1.0)']
    # .data.to_csv('test.csv', index=False))

    # Para devolver agencias
    # message_def = return_agencies()

    # Para listar los dataflows de cada agencia
    # message_def = BIS_return_dataflows(name='BIS')
    # message_def = EUROSTAT_return_dataflows(name='EUROSTAT')
    # message_def = ECB_return_dataflows(name='ECB')
    # message_def = ILO_return_dataflows(name='ILO')

    # Para devolver data de un dataflow en concreto
    # message_def = BIS_return_dataflow_data(name='BIS',
    #                                        dataflow_unique_id='BIS:WS_CBPOL_D(1.0)',
    #                                        first_n_observations='10')

    # message_def = EUROSTAT_return_dataflow_data(name='EUROSTAT',
    #                                             dataflow_unique_id='ESTAT:HLTH_EHIS_SK4E(1.0)',
    #                                             first_n_observations='1')

    # message_def = ECB_return_dataflow_data(name='ECB',
    #                                        dataflow_unique_id='ECB:AME(1.0)',
    #                                        first_n_observations='1')

    message_def = ILO_return_dataflow_data(name='ILO',
                                           dataflow_unique_id='ILO:DF_CLD_TPOP_SEX_AGE_GEO_NB(1.0)')

    print(message_def)


if __name__ == "__main__":
    main()
