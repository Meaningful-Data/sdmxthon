# flake8: noqa

import pandas as pd

from sdmxthon.api.api import get_pandas_df, read_sdmx
from sdmxthon.model.dataset import Dataset
from sdmxthon.model.definitions import DataStructureDefinition
from sdmxthon.utils.enums import MessageTypeEnum
from sdmxthon.utils.handlers import first_element_dict

data_file1 = "development_files/data_file1.xml"
url_eu = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/" \
         "EI_BSCO_M$DEFAULTVIEW/?format=sdmx_2.1_structured"


def main():
    message = read_sdmx(data_file1, validate=False)

    # print(message.payload['ESTAT:EI_BSCO_M$DEFAULTVIEW(1.0)']
    # .data.to_csv('test.csv', index=False))

    print(message)


if __name__ == "__main__":
    main()
