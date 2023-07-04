import json

import validators
from flask import Flask, Response, request
from flask_cors import CORS

from .sdmx_requests import BISRequest, BaseRequest, ECBRequest, \
    EUROSTATRequest, ILORequest

app = Flask(__name__)
CORS(app)

agencies = {'BIS': BISRequest, 'ECB': ECBRequest,
            'ESTAT': EUROSTATRequest, 'ILO': ILORequest}


# url to provide agencies information (name, code and base url)
@app.route('/agencies', methods=['GET'])
def get_agencies_info():
    agencies_info = []
    for i in agencies.values():
        info = {'name': i.name,
                'code': i.code,
                'api_base_url': i.base_url}
        agencies_info.append(info)
    try:
        return Response(json.dumps(agencies_info, indent=2), status=200)
    except Exception as e:
        return Response(str(e), status=500)


# url to provide available dataflows for every agency
@app.route('/dataflows/<agency_code>', methods=['GET'])
def get_dataflows(agency_code):
    if agency_code not in agencies.keys():
        return Response('Agency name not allowed', status=400)
    try:
        x = agencies[agency_code]
        dataflows = x.get_dataflows(params={'agency_code': agency_code})
    except Exception as e:
        return Response(str(e), status=500)
    return Response(json.dumps(dataflows, indent=2), status=200)


# url to redirect to specific dataflow data
@app.route('/dataflows/data/url/<agency_code>/<unique_id>', methods=['GET'])
def get_data_url(agency_code, unique_id):
    params = request.args.to_dict()
    if agency_code not in agencies.keys():
        return Response('Agency name not allowed', status=400)
    try:
        x = agencies[agency_code]
        url_str = x.get_data_url(unique_id=unique_id,
                                 params=params)
        return url_str, 200
    except Exception as e:
        return Response(str(e), status=500)


@app.route('/dataflows/url/<agency_code>/<unique_id>', methods=['GET'])
def get_dataflow_metadata_url(agency_code, unique_id):
    params = request.args.to_dict()
    if agency_code not in agencies.keys():
        return Response('Agency name not allowed', status=400)
    try:
        x = agencies[agency_code]
        metadata_url_str = x.get_metadata_url(unique_id=unique_id,
                                              params=params)
        return metadata_url_str, 200
    except Exception as e:
        return Response(str(e), status=500)


@app.route('/dataflows/code', methods=['GET'])
def get_code_url():
    params = request.args.to_dict()
    print(params.keys())
    if len(params.keys()) > 1:
        return Response("Too many parameters, insert only url parameter",
                        status=400)
    if 'url' not in params.keys():
        return Response("Invalid parameters, insert url parameter", status=400)
    url = params['url']
    if f"{url}" == '':
        return Response('Empty url is not allowed', status=400)
    if not validators.url(f"{url}"):
        return Response(f"{url} is not a valid url", status=400)
    try:
        x = BaseRequest()
        code_str = x.get_sdmxthon_code(url=url)
        return code_str
    except Exception as e:
        return Response(str(e), status=500)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
