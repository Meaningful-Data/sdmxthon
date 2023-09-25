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
    #
    ws = webservices.BisWs()
    dataflow_id = 'WS_CBPOL_D'
    #
    ws = webservices.EuroStatWs()
    dataflow_id = 'MAR_QG_QM_EWHD'

    ws = webservices.EcbWs()
    dataflow_id = 'AME'

    ws = webservices.OecdWs()
    dataflow_id = 'DSD_EARNINGS@AV_AN_WAGE'
    # dsd_id = 'DSD_DEBT_TRANS_DDOWN'
    agency_id = 'OECD.ELS.SAE'
    # agency_id = 'OECD.DAF'
    version = '1.0'
    unique_id = 'OECD.ELS.SAE,DSD_EARNINGS@AV_AN_WAGE,1.0'

    # print(ws.get_data_url(dataflow_id, last_n_observations=1))
    # print(ws.get_data_flow(dataflow_id, references='descendants').content)
    # data = ws.get_data(dataflow_id, provider=agency_id, version=version,
    #                    last_n_observations=1)
    data = ws.get_dsd(resources=f"{agency_id}")
    print(data.content)

    # metadata = ws.get_data_flow(dataflow_id, references='descendants')
    # print(metadata.payload)

    # message = read_sdmx('http://wits.worldbank.org/API/V1/SDMX/V21/rest/dataflow/wbg_wits/').content
    # print(message)
    
    # print(ilo_ws.get_constraints_url(dataflow_id))


if __name__ == "__main__":
    main()
