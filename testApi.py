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

    ilo_ws = webservices.IloWs()
    dataflow_id = 'DF_CLD_XCHL_SEX_AGE_STE_NB'
    # data = ilo_ws.get_data(dataflow_id, last_n_observations=1)
    # print(data.payload)
    metadata = ilo_ws.get_data_flow(dataflow_id, references='descendants')
    print(list(metadata.payload['Codelists'].values())[0].items['AGE_YTHADULT'].name)
    # print(ilo_ws.get_constraints_url(dataflow_id))

if __name__ == "__main__":
    main()
