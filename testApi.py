# flake8: noqa
import sdmxthon

def main():
    message_data = sdmxthon.read_sdmx('https://stats.bis.org/api/v1/data/BIS,WS_OTC_DERIV2,1.0/all/all?lastNObservations=3&detail=full')
    dataset = message_data.content['BIS:WS_OTC_DERIV2(1.0)']
    # dataset.structure = sdmxthon.read_sdmx('https://stats.bis.org/api/v1/dataflow/BIS/WS_OTC_DERIV2/1.0?references=all&detail=full').content['DataStructures']['BIS:BIS_DER(1.0)']
    print(dataset.structural_validation())


if __name__ == "__main__":
    main()
