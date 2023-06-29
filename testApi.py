# flake8: noqa
import json
from sdmxthon.WebServices import sdmx_requests

def main():
    
    # EXAMPLES
    x = sdmx_requests.BISRequest()
    dataflows = x.get_dataflows()
    print(json.dumps(dataflows, indent=2))


if __name__ == "__main__":
    main()
