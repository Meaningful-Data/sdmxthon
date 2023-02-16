import json
from flask import Flask, redirect, request, Response, jsonify
from flask_cors import CORS
from web_services import BISRequest, EUROSTATRequest, ECBRequest, ILORequest

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
        dataflows = x.get_dataflows(params={'code': agency_code})
    except Exception as e:
        return Response(str(e), status=500)
    return Response(json.dumps(dataflows, indent=2), status=200)


# url to redirect to specific dataflow data
@app.route('/dataflows/data/url/<agency_code>/<unique_id>', methods=['GET'])
def get_dataflow_data_url(agency_code, unique_id):
    params = request.args.to_dict()
    if agency_code not in agencies.keys():
        return Response('Agency name not allowed', status=400)
    try:
        x = agencies[agency_code]
        data_url_str = x.get_data_url(unique_id=unique_id,
                                      params=params)
        return jsonify(data_url_str)
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
        return jsonify(metadata_url_str)
    except Exception as e:
        return Response(str(e), status=500)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
