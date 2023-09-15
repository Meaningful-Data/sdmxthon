# flake8: noqa
from sdmxthon.webservices import webservices


def main():
    # bis_ws = webservices.BisWs()
    # # dataflows = bis_ws.get_all_dataflows()
    # # data_flow_id = dataflows[0]['id']
    # data_flow_id = 'WS_CBPOL_D'
    # print(bis_ws.get_data_url(data_flow_id))
    # print(bis_ws.get_dsd_url())
    # print(bis_ws.get_dsd_url(data_flow_id))
    # print(bis_ws.get_dsd_url(resources = data_flow_id, agency_id = 'BIS'))

    ws = webservices.IloWs()
    dataflow_id = 'DF_CLD_XCHL_SEX_AGE_STE_NB'

    ws = webservices.BisWs()
    dataflow_id = 'WS_CBPOL_D'

    ws = webservices.EuroStatWs()
    dataflow_id = 'MAR_QG_QM_EWHD'

    ws = webservices.EcbWs()
    dataflow_id = 'AME'

    # print(ws.get_data_url(dataflow_id, last_n_observations=1))
    # print(ws.get_data_flow_url(dataflow_id, references='descendants'))
    data = ws.get_data(dataflow_id, last_n_observations=1)
    print(data.payload)
    metadata = ws.get_data_flow(dataflow_id, references='descendants')
    print(metadata.payload)


    
    # print(ilo_ws.get_constraints_url(dataflow_id))

if __name__ == "__main__":
    main()
