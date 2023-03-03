# flake8: noqa

from sdmxthon.api.api import read_sdmx

data_file1 = "development_files/data_file1.xml"
url_eu = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/" \
         "EI_BSCO_M$DEFAULTVIEW/?format=sdmx_2.1_structured"
url_ecb = "https://sdw-wsrest.ecb.europa.eu/service/dataflow/ECB/IVF/1.0?references=all&detail=full"


def main():
    message = read_sdmx(url_ecb, validate=False)

    # print(message.payload['ESTAT:EI_BSCO_M$DEFAULTVIEW(1.0)']
    # .data.to_csv('test.csv', index=False))

    print(message)


if __name__ == "__main__":
    main()
