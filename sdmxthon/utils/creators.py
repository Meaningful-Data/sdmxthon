from datetime import date

import pandas as pd

from ..common.dataSet import DataSet


def DataSetCreator(dsd, dataset_attributes=None, attached_attributes=None,
                   obs=None):
    if dataset_attributes is None or dataset_attributes == {}:
        dataset_attributes = {"reportingBegin": None,
                              "reportingEnd": None,
                              "dataExtractionDate": date.today(),
                              "validFrom": None,
                              "validTo": None,
                              "publicationYear": None,
                              "publicationPeriod": None,
                              "action": "Replace",
                              "setId": dsd.id,
                              "dimensionAtObservation": "AllDimensions"
                              }

    else:
        check_DA_keys(dataset_attributes, dsd.id)

    if isinstance(obs, pd.DataFrame):
        item = DataSet(structure=dsd,
                       dataset_attributes=dataset_attributes, attached_attributes=attached_attributes,
                       obs=obs)
    elif isinstance(obs, list):
        item = DataSet(structure=dsd,
                       dataset_attributes=dataset_attributes, attached_attributes=attached_attributes,
                       obs=pd.DataFrame(obs))
    else:
        return None

    return item


def check_DA_keys(attributes: dict, code):
    keys = ["reportingBegin", "reportingEnd", "dataExtractionDate", "validFrom", "validTo", "publicationYear",
            "publicationPeriod", "action", "setId", "dimensionAtObservation"]

    for spared_key in attributes.keys():
        if spared_key not in keys:
            attributes.pop(spared_key)

    for k in keys:
        if k not in attributes.keys():
            if k == "dataExtractionDate":
                attributes[k] = date.today()
            elif k == "action":
                attributes[k] = "Replace"
            elif k == "setId":
                attributes[k] = code
            elif k == "dimensionAtObservation":
                attributes[k] = "AllDimensions"
            else:
                attributes[k] = None


def id_creator(agencyID, id_, version):
    return f"{agencyID}:{id_}({version})"
