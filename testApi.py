# flake8: noqa
from sdmxthon.webservices import webservices


def main():
    bis_ws = webservices.BisWs()
    # dataflows = bis_ws.get_all_dataflows()
    # data_flow_id = dataflows[0]['id']
    data_flow_id = 'WS_CBPOL_D'
    print(bis_ws.get_data_url(data_flow_id))
    print(bis_ws.get_dsd_url())
    print(bis_ws.get_dsd_url(data_flow_id))
    print(bis_ws.get_dsd_url(resources = data_flow_id, agency_id = 'BIS'))

if __name__ == "__main__":
    main()
