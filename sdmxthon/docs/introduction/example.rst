This example demonstrates how SDMXthon can be used to produce SDMX
data from a CSV file.

Let's suppose that we have some data stored in a CSV file, which
correspond to a dataflow following the BIS_DER datastructure from the
BIS.

Generate Dataset
________________

We can create a Dataset object in SDMXthon, and load this CSV data
and the related metadata:


.. code:: python

  >>> import sdmxthon
  >>> from sdmxthon.model.dataset import Dataset

  >>> data_instance = Dataset()
  >>> data_instance.read_csv('input_data/input_data.csv')

  >>> metadata = sdmxthon.read_sdmx('https://stats.bis.org/api/v1/datastructure/BIS/BIS_DER/1.0?references=all&detail=full')
  >>> data_instance.structure = metadata.content['DataStructures']['BIS:BIS_DER(1.0)']

Structural validation
______________________

SDMXthon provides a method to do a structural validation of the data
against the metadata:


.. code:: python

  >>> import json

  >>> validation_results = data_instance.semantic_validation()

  >>> print (f'The dataset has {len(validation_results)} errors:\n {[error["Message"] for error in validation_results]}')

.. container:: output stream stdout

  ::

     The dataset has 3 errors:
      ['Missing value in measure OBS_VALUE', 'Missing FREQ', 'Missing OBS_STATUS']


Thus, the dataset is incorrect, because there are some empty values,
and the dimension 'FREQ' and the mandatory attribute 'OBS_STATUS' are
missing. It is possible to use Pandas to correct the dataset:

.. code:: python

  >>> data_instance.data['OBS_VALUE'] = data_instance.data['OBS_VALUE'].fillna(0)
  >>> data_instance.data['FREQ'] = 'H'
  >>> data_instance.data['OBS_STATUS'] = 'A'

  >>> validation_results = data_instance.semantic_validation()
  >>> print (f'The dataset has {len(validation_results)} errors:\n {[error["Message"] for error in validation_results]}')

.. container:: output stream stdout

  ::

     The dataset has 0 errors:
      []

Data Analysis with pandas
__________________________

Let's now suppose that we want to validate that each observation is
within 50% of the observation for the previous period. Again, we can
use Pandas´ capabilities to perform these validations:

.. container:: cell code

   .. code:: python

      #Get list of dimensions excluding TIME_PERIOD:
      >>> dimension_descriptor = data_instance.structure.dimension_descriptor.components
      >>> dimension_list = [key for key in dimension_descriptor]
      >>> dimension_list.remove('TIME_PERIOD')


      # Add a field with the previous value of the series:
      >>> data_instance.data["previous_value"] = data_instance.data.sort_values("TIME_PERIOD").groupby(dimension_list)["OBS_VALUE"].shift(1)


      # Get if value is between the percentage of the previous value:
      >>> data_instance.data["val_result"] = data_instance.data["previous_value"] / data_instance.data["OBS_VALUE"]
      >>> errors = data_instance.data[~data_instance.data["val_result"].between(0.8, 1.2)].dropna()

      #Drop inmaterial observations (previous or current below 1000):
      >>> errors = errors[(errors['previous_value'] > 1000) |  (errors['OBS_VALUE'] > 1000)]

      >>> print(len(data_instance.data))
      >>> print(len(errors))

      >>> errors.to_csv('error.csv')

   .. container:: output stream stdout

      ::

         9914
         1818



SDMXthon provides a method to simply generate an SDMX-ML message from
a Dataset object. The message is generated as a StringIO object, but
it is also possible to set a path to save the data as a file.


.. code:: python

  >>> data_instance.to_xml(outputPath='output_data/output_data.xml')
  >>> print(data_instance.to_xml().getvalue()[:3000])

.. container:: output stream stdout

  ::

     <?xml version="1.0" encoding="UTF-8"?>
     <mes:StructureSpecificData xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:mes="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message" xmlns:ss="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/structurespecific" xmlns:ns1="urn:sdmx:org.sdmx.infomodel.datastructure.DataStructure=BIS:BIS_DER(1.0):ObsLevelDim:AllDimensions" xmlns:com="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common" xsi:schemaLocation="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message https://registry.sdmx.org/schemas/v2_1/SDMXMessage.xsd">
        <mes:Header>
            <mes:ID>test</mes:ID>
            <mes:Test>true</mes:Test>
            <mes:Prepared>2023-03-24T09:41:39</mes:Prepared>
            <mes:Sender id="Unknown"/>
            <mes:Receiver id="Not_supplied"/>
            <mes:Structure structureID="BIS_DER" namespace="urn:sdmx:org.sdmx.infomodel.datastructure.DataStructure=BIS:BIS_DER(1.0)" dimensionAtObservation="AllDimensions">
                <com:Structure>
                    <Ref agencyID="BIS" id="BIS_DER" version="1.0" class="DataStructure"/>
                </com:Structure>
            </mes:Structure>
            <mes:Source xml:lang="en">SDMXthon</mes:Source>
        </mes:Header>
        <mes:DataSet ss:structureRef="BIS_DER" xsi:type="ns1:DataSetType" ss:dataScope="DataStructure" action="Replace">
            <Obs DER_TYPE="T" DER_INSTR="W" DER_RISK="T" DER_REP_CTY="5J" DER_SECTOR_CPY="N" DER_CPC="5J" DER_SECTOR_UDL="A" DER_CURR_LEG1="TO1" DER_CURR_LEG2="TO1" DER_ISSUE_MAT="A" DER_RATING="B" DER_EX_METHOD="3" DER_BASIS="A" AVAILABILITY="K" COLLECTION="S" TIME_PERIOD="2021-S2" OBS_VALUE="12381.0" FREQ="H" OBS_STATUS="A" previous_value="" val_result="" />
            <Obs DER_TYPE="T" DER_INSTR="W" DER_RISK="T" DER_REP_CTY="5J" DER_SECTOR_CPY="N" DER_CPC="5J" DER_SECTOR_UDL="A" DER_CURR_LEG1="TO1" DER_CURR_LEG2="TO1" DER_ISSUE_MAT="A" DER_RATING="B" DER_EX_METHOD="3" DER_BASIS="A" AVAILABILITY="K" COLLECTION="S" TIME_PERIOD="2022-S1" OBS_VALUE="10363.0" FREQ="H" OBS_STATUS="A" previous_value="12381.0" val_result="1.1947312554279648" />
            <Obs DER_TYPE="A" DER_INSTR="T" DER_RISK="L" DER_REP_CTY="5J" DER_SECTOR_CPY="A" DER_CPC="5J" DER_SECTOR_UDL="A" DER_CURR_LEG1="TO1" DER_CURR_LEG2="TO1" DER_ISSUE_MAT="A" DER_RATING="A" DER_EX_METHOD="3" DER_BASIS="A" AVAILABILITY="K" COLLECTION="S" TIME_PERIOD="2021-S2" OBS_VALUE="97640.002" FREQ="H" OBS_STATUS="A" previous_value="" val_result="" />
            <Obs DER_TYPE="A" DER_INSTR="T" DER_RISK="L" DER_REP_CTY="5J" DER_SECTOR_CPY="A" DER_CPC="5J" DER_SECTOR_UDL="A" DER_CURR_LEG1="TO1" DER_CURR_LEG2="TO1" DER_ISSUE_MAT="A" DER_RATING="A" DER_EX_METHOD="3" DER_BASIS="A" AVAILABILITY="K" COLLECTION="S" TIME_PERIOD="2022-S1" OBS_VALUE="122347.497" FREQ="H" OBS_STATUS="A" previous_value="97640.002" val_result="0.7980547570989539" />
            <Obs DER_TYPE="A" DER_INSTR="V" DER_RISK="T" DER_REP_CTY="5J" DER_SECTOR_CPY="M" DER_CPC="5J" DER_SECTOR_UDL="A" DER_CURR_LEG1="TO1" DER_CURR_LEG2="TO1" DER_ISSUE_MAT="A" DER_RATING="B" DER_EX_METHOD="3" DER_BASIS="C" AVAILABILITY="K" COLLECTION="S" TIME_PERIOD="2021-S2" OBS_VALUE=
        ...

We can also make use of the FMR web service to validate the generated
data:

.. code:: python

    >>> import requests

    >>> url = "http://127.0.0.1:8080/ws/public/data/load"
    >>> files = {'uploadFile': open('output_data/output_data.xml','rb')}

    >>> validate_request = requests.post(url, files=files)

    >>> print(validate_request.text)

    {"Success":true,"uid":"78e280ca-aeab-4c1b-b932-f6b177f46f2b"}



.. code:: python

    >>> import time

    >>> url = "http://127.0.0.1:8080/ws/public/data/loadStatus"
    >>> uid =  json.loads(validate_request.text)['uid']

    >>> time.sleep(3) # Wait for the validation to finish

    >>> result_request = requests.get(f'{url}?uid={uid}')

    >>> result = json.loads(result_request.text)

    >>> print(result['Datasets'][0]['ValidationReport'][:2])

    [
      {
        "Type": "MandatoryAttributes",
        "Errors": [
          {
            "ErrorCode": "REG-201-051",
            "Message": "Missing mandatory attribute 'DECIMALS'",
            "Dataset": 0,
            "ComponentId": "DECIMALS",
            "Position": "Dataset"
          },
          {
            "ErrorCode": "REG-201-051",
            "Message": "Missing mandatory attribute 'UNIT_MEASURE'",
            "Dataset": 0,
            "ComponentId": "UNIT_MEASURE",
            "Position": "Dataset"
          },
          {
            "ErrorCode": "REG-201-051",
            "Message": "Missing mandatory attribute 'UNIT_MULT'",
            "Dataset": 0,
            "ComponentId": "UNIT_MULT",
            "Position": "Dataset"
          }
        ]
      },
      {
        "Type": "FormatSpecific",
        "Errors": [
          {
            "ErrorCode": "-",
            "Message": "Unexpected attribute 'previous_value' for element 'StructureSpecificData/DataSet/Obs'",
            "Dataset": 0,
            "Position": "Dataset"
          },
          {
            "ErrorCode": "-",
            "Message": "Unexpected attribute 'val_result' for element 'StructureSpecificData/DataSet/Obs'",
            "Dataset": 0,
            "Position": "Dataset"
          }
        ]
      }
    ]








