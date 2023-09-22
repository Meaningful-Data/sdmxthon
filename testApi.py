# flake8: noqa
from sdmxthon.webservices import webservices, query_builder
import pandas as pd

def create_codelist_dataframe(codelist, concept_name):
    codelist_list = []
    for id, code in codelist.items.items():
        item = {'id': id}
        for lang_code, strings in code.name.items():
            item[f"{concept_name}-{lang_code}"] = strings['content']
            print(item)
        codelist_list.append(item)
    
    return pd.DataFrame(codelist_list)

def generate_insight_dict(metadata_payload):
    result = {}
    codelists = metadata_payload['Codelists']
    structure = metadata_payload['DataStructures']
    if len(structure) !=  1:
        raise Exception('One structure expected')
    structure = list(structure.values())[0]
    for id, component in structure.dimension_descriptor.components.items():
        codelist=component.representation.codelist
        if codelist:
            codelist = create_codelist_dataframe(codelist, component.id)
        result[id] = {'name': component.concept_identity.name, 'codelist': codelist}
    return result


def generate_final_df_and_concepts_name(data, metadata_payload):
    insight_dict = generate_insight_dict(metadata_payload)

    concepts_names = {}
    for code, component in insight_dict.items():
        concepts_names[code] = component['name']
        if component['codelist'] is not None:
            data = data.merge(component['codelist'], left_on=code, right_on='id', how='inner')
            data.drop(columns=['id_x', 'id_y'], inplace=True, errors='ignore')
    data.to_csv('data.csv')
    return data, concepts_names

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

    # ws = webservices.BisWs()
    # dataflow_id = 'WS_CBPOL_D'

    # ws = webservices.EuroStatWs()
    # dataflow_id = 'MAR_QG_QM_EWHD'

    # ws = webservices.EcbWs()
    # dataflow_id = 'AME'
    # ws.get_pandas_with_names(dataflow_id, last_n_observations=1)
    print(ws.get_data_url(dataflow_id, last_n_observations=1))

    # print(ws.get_data_url(dataflow_id, last_n_observations=1))
    # print(ws.get_data_flow_url(dataflow_id, references='descendants'))
    # data = ws.get_data(dataflow_id, last_n_observations=1)
    # print(data.payload)
    # metadata = ws.get_data_flow(dataflow_id, references='descendants')
    # print(metadata.payload)


    
    # print(ilo_ws.get_constraints_url(dataflow_id))

if __name__ == "__main__":
    main()
