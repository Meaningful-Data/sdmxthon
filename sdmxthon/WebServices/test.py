# flake8: noqa
import random

import requests


def describe_GET_agencies_info():
    def get():
        response = requests.get('http://127.0.0.1:5000/agencies')
        return response

    def it_return_agencies_info():
        response = get()
        assert response.status_code == 200
        assert response.json() == [
            {"name": "Bank for International Settlements", "code": "BIS",
             "api_base_url": "https://stats.bis.org/api/v1"},
            {"name": "European Central Bank", "code": "ECB",
             "api_base_url": "https://sdw-wsrest.ecb.europa.eu"},
            {"name": "Eurostat", "code": "ESTAT",
             "api_base_url": "https://ec.europa.eu/eurostat/api/dissemination"},
            {"name": "International Labour Organization", "code": "ILO",
             "api_base_url": "https://www.ilo.org/sdmx/rest"}]


AGENCIES_CODES = ["BIS", "ESTAT", "ECB", "ILO"]


def describe_GET_dataflows():
    def get(agency_code):
        url = f'http://127.0.0.1:5000/dataflows/{agency_code}'
        response = requests.get(url)
        return response

    def context_available_agency():
        def it_return_agencies_info():
            agency_code = random.choice(AGENCIES_CODES)
            response = get(agency_code)
            assert response.status_code == 200
            assert response.json()[0].keys() == ["id", "unique_id",
                                                 "name", "description",
                                                 "version"]

    def context_not_available_agency():
        def it_respond_with_error_message():
            response = get("other_agency")
            assert response.status_code == 400
            assert response.json() == "Agency name not allowed"


DATA_PARAMS = {"BIS": {"key": "all", "detail": "full"},
               "ECB": {"key": "all", "detail": "full",
                       "provider_ref": "all"},
               "ESTAT": "",
               "ILO": {"key": "all", "detail": "full",
                       "include_history": "false"}}
UNIQUE_ID = {"BIS": "BIS:WS_CBPOL_D(1.0)",
             "ECB": "ECB:AME(1.0)",
             "ESTAT": "ESTAT:MED_MA6(1.0)",
             "ILO": "ILO:DF_CLD_TPOP_SEX_AGE_GEO_NB(1.0)"}


def describe_GET_dataflows_data():
    def get(agency_code, unique_id, params):
        url = f'http://127.0.0.1:5000/dataflows/data/url/{agency_code}/{unique_id}'
        if params != "":
            response = requests.get(url, params=params)
        else:
            response = requests.get(url)
        return response

    def context_available_params():
        def it_return_dataflow_data_url():
            agency_code = random.choice(AGENCIES_CODES)
            response = get(agency_code=agency_code,
                           unique_id=UNIQUE_ID[agency_code],
                           params=DATA_PARAMS[agency_code])
            assert response.status_code == 200
            assert len(response.json()) >= 1

    def context_not_available_agency():
        def it_respond_with_error_message():
            response = get(agency_code="other_agency", unique_id="unique_id",
                           params="")
            assert response.status_code == 400
            assert response.json() == "Agency name not allowed"

    def context_not_available_params():
        def it_respond_with_error_message():
            agency_code = random.choice(AGENCIES_CODES)
            response = get(agency_code=agency_code,
                           unique_id=UNIQUE_ID[agency_code],
                           params={"other_param": "other_param"})
            assert response.status_code == 500


def describe_GET_dataflows_metadata():
    def get(agency_code, unique_id):
        url = 'http://127.0.0.1:5000/dataflows/url/{agency_code}/{unique_id}'.format(
            agency_code=agency_code, unique_id=unique_id)
        response = requests.get(url)
        return response

    def context_available_params():
        def it_return_dataflow_metadata_url():
            agency_code = random.choice(AGENCIES_CODES)
            response = get(agency_code=agency_code,
                           unique_id=UNIQUE_ID[agency_code])
            assert response.status_code == 200
            assert len(response.json()) >= 1

    def context_not_available_agency():
        def it_respond_with_error_message():
            response = get(agency_code="other_agency", unique_id="unique_id")
            assert response.status_code == 400
            assert response.json() == "Agency name not allowed"


def describe_GET_dataflows_code():
    def get(params):
        url = 'http://127.0.0.1:5000/dataflows/code?'
        for key in params:
            url = f"{url}{key}={params[key]}&"
        url = url[:-1]
        response = requests.get(url)
        return response

    def context_too_much_parameters():
        def it_respond_with_error_message():
            url = "https://stats.bis.org/api/v1/data/BIS,WS_CBPOL_D,1.0/all/all?detail=full"
            params = {'url': url, 'other_parameter': 'other_parameter'}
            response = get(params)
            assert response.status_code == 400
            assert response.json() == "Too much parameters, insert only url parameter"

    def context_missing_url_parameter():
        def it_respond_with_error_message():
            params = {'other_parameter': 'other_parameter'}
            response = get(params)
            assert response.status_code == 400
            assert response.json() == "Invalid parameters, insert url parameter"

    def context_empty_url():
        def it_respond_with_error_message():
            params = {'url': ''}
            response = get(params)
            assert response.status_code == 400
            assert response.json() == 'Empty url is not allowed'

    def context_invalid_url():
        def it_return_code():
            url = "invalid_url"
            params = {'url': url}
            response = get(params)
            assert response.status_code == 400
            assert response.json() == f"{url} is not a valid url"

    def context_valid_url():
        def it_return_code():
            url = "https://stats.bis.org/api/v1/data/BIS,WS_CBPOL_D,1.0/all/all?detail=full"
            params = {'url': url}
            response = get(params)
            assert response.status_code == 200
            assert response.json() == f"""from sdmxthon import read_sdmx<br/>
                                      if __name__ == 'main':<br/>
                                      &emsp;&emsp;message = read_sdmx('{url}', validate=True)<br/>
                                      &emsp;&emsp;print(message.content)"""