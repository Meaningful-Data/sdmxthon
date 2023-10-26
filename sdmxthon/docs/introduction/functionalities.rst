SDMX-Message reading
____________________

SDMXthon includes a simple method to read any sdmx file, regardless of
whether it is a data or metadata file. The method can be called on
stored files or urls.

.. code:: python

  >>> import sdmxthon

  >>> message_metadata = sdmxthon.read_sdmx('input_data/bis_otc_outs.xml')
  >>> message_data = sdmxthon.read_sdmx('https://stats.bis.org/api/v1/data/BIS,WS_OTC_DERIV2,1.0/all/all?lastNObservations=3&detail=full')

  >>> print(message_metadata.type)
  >>> print(message_data.type)

.. container:: output stream stdout

  ::

     MessageTypeEnum.Metadata
     MessageTypeEnum.StructureDataSet



The payload of the messages is in an attribute of the message object:

.. code:: python

  print(message_metadata.payload)
  print(message_data.payload)

.. container:: output stream stdout

  ::

     {'OrganisationSchemes': {'SDMX:AGENCIES(1.0)': <AgencyScheme - SDMX:AGENCIES(1.0)>}, 'Codelists': {'BIS:CL_AVAILABILITY(1.0)': <Codelist - CL_AVAILABILITY>, 'BIS:CL_BIS_IF_REF_AREA(1.0)': <Codelist - CL_BIS_IF_REF_AREA>, 'BIS:CL_BIS_UNIT(1.0)': <Codelist - CL_BIS_UNIT>, 'BIS:CL_COLLECTION(1.0)': <Codelist - CL_COLLECTION>, 'BIS:CL_CONF_STATUS(1.0)': <Codelist - CL_CONF_STATUS>, 'BIS:CL_DECIMALS(1.0)': <Codelist - CL_DECIMALS>, 'BIS:CL_DER_BASIS(1.0)': <Codelist - CL_DER_BASIS>, 'BIS:CL_DER_INSTR(1.0)': <Codelist - CL_DER_INSTR>, 'BIS:CL_EX_METHOD(1.0)': <Codelist - CL_EX_METHOD>, 'BIS:CL_FREQ(1.0)': <Codelist - CL_FREQ>, 'BIS:CL_ISSUE_MAT(1.0)': <Codelist - CL_ISSUE_MAT>, 'BIS:CL_MARKET_RISK(1.0)': <Codelist - CL_MARKET_RISK>, 'BIS:CL_OBS_STATUS(1.0)': <Codelist - CL_OBS_STATUS>, 'BIS:CL_OD_TYPE(1.0)': <Codelist - CL_OD_TYPE>, 'BIS:CL_RATING(1.0)': <Codelist - CL_RATING>, 'BIS:CL_SECTOR_CPY(1.0)': <Codelist - CL_SECTOR_CPY>, 'BIS:CL_SECTOR_UDL(1.0)': <Codelist - CL_SECTOR_UDL>, 'BIS:CL_TIME_FORMAT(1.0)': <Codelist - CL_TIME_FORMAT>, 'BIS:CL_UNIT_MULT(1.0)': <Codelist - CL_UNIT_MULT>}, 'Concepts': {'BIS:STANDALONE_CONCEPT_SCHEME(1.0)': <ConceptScheme - BIS:STANDALONE_CONCEPT_SCHEME(1.0)>}, 'DataStructures': {'BIS:BIS_DER(1.0)': <DataStructureDefinition  - BIS:BIS_DER(1.0)>}, 'Dataflows': {'BIS:WS_OTC_DERIV2(1.0)': <DataFlowDefinition - BIS:WS_OTC_DERIV2(1.0)>}, 'Constraints': {'BIS:OTCDO_NA_R(1.0)': <sdmxthon.model.definitions.ContentConstraint object at 0x000001BB3A5CE450>}, 'errors': []}
     {'BIS:WS_OTC_DERIV2(1.0)': <DataSet - No Structure found>}


Data functionalities
____________________

The DataSet object has a series of SDMX-specific attributes. The data
in the dataset are stored as a Pandas Dataframe, in the data
attribute:



.. code:: python

  >>> dataset = message_data.content['BIS:WS_OTC_DERIV2(1.0)']
  >>> dataset.data

.. container:: output execute_result

  ::

       FREQ DER_TYPE DER_INSTR DER_RISK DER_REP_CTY DER_SECTOR_CPY DER_CPC
    0        H        T         W        T          5J              N      5J  ...
    1        H        T         W        T          5J              N      5J  ...
    2        H        T         W        T          5J              N      5J  ...
    3        H        A         T        L          5J              A      5J  ...
    4        H        A         T        L          5J              A      5J  ...
    ...    ...      ...       ...      ...         ...            ...     ...
    14862    H        S         U        T          5J              A      5J  ...
    14863    H        S         U        T          5J              A      5J  ...
    14864    H        A         M        D          5J              B      5J  ...
    14865    H        A         M        D          5J              B      5J  ...
    14866    H        A         M        D          5J              B      5J  ...

    [14867 rows x 20 columns]

The generated data frame has one column for each component of the
data structure of the dataset. This dataset does not have any data
structure attached to it, since it has not been loaded:

.. code:: python

  >>> print(dataset.structure)

.. container:: output stream stdout

  ::

     None


By assigning a structure to the dataset, it is possible to validate
the data against its structure:

.. code:: python

  >>> dataset.structure = message_metadata.content['DataStructures']['BIS:BIS_DER(1.0)']
  >>> dataset.semantic_validation()

.. container:: output execute_result

  ::

     []


If the dataset has structural errors, the output of the
semantic_validation method is a list of dictionaries with the errors:

.. code:: python

  >>> dataset.data['DER_BASIS'] = 'error'
  >>> dataset.semantic_validation()

.. container:: output execute_result

  ::

     [{'Code': 'SS08',
       'ErrorLevel': 'WARNING',
       'Component': 'DER_BASIS',
       'Type': 'Dimension',
       'Rows': None,
       'Message': 'Value error not compliant with maxLength : 1'},
      {'Code': 'SS04',
       'ErrorLevel': 'CRITICAL',
       'Component': 'DER_BASIS',
       'Type': 'Dimension',
       'Rows': None,
       'Message': 'Wrong value error for dimension DER_BASIS'}]



The list of possible errors can be found in :doc:`Validations Page<../validations>`

From dataset objects it is possible to generate an SDMX v2.1 message,
with any of the different modalities:

.. code-block:: python

    >>> from sdmxthon.utils.enums import MessageTypeEnum
    >>> from datetime import datetime

    >>> dataset.to_xml(
          message_type = MessageTypeEnum.StructureDataSet,
          outputPath = 'structure_dataset_example.xml',
          id_ = 'dataset_id',
          test = 'false',
          prepared = datetime.now(),
          sender = 'MeaningfulData',
          receiver = 'open',
          prettyprint=True
      )

Metadata functionalities
_________________________

SDMXthon provides a simple way to navigate through the metadata.
Using the content method on the Message class and the items method on
each item Scheme we can access to the inner metadata classes.


.. code:: python

    >>> concept_scheme = message_metadata.content['Concepts']['BIS:STANDALONE_CONCEPT_SCHEME(1.0)']
    >>> concept_scheme.items

.. code-block:::: output execute_result

    ::

        {
            'TIME_FORMAT': <Concept - TIME_FORMAT>,
            'ADJUST_CODED': <Concept - ADJUST_CODED>,
            'AGG_EQUN': <Concept - AGG_EQUN>,
            'AVAILABILITY': <Concept - AVAILABILITY>,
            'BIS_BLOCK': <Concept - BIS_BLOCK>,
            'BIS_DOC_DATE': <Concept - BIS_DOC_DATE>,
            'BIS_SUFFIX': <Concept - BIS_SUFFIX>,
            'BIS_TOPIC': <Concept - BIS_TOPIC>,
            'BIS_UNIT': <Concept - BIS_UNIT>,
            'COLPOSTYPE': <Concept - COLPOSTYPE>
        }


Data Structure Definitions can be accessed in a similar way:

.. code:: python

    >>> dsd = message_metadata.content['DataStructures']['BIS:BIS_DER(1.0)']
    >>> dsd.content

.. container:: output execute_result

    ::

        {
        'dimensions': {
            'FREQ': <Dimension - FREQ>,
            'DER_TYPE': <Dimension - DER_TYPE>,
            'DER_INSTR': <Dimension - DER_INSTR>,
            'DER_RISK': <Dimension - DER_RISK>,
            'DER_REP_CTY': <Dimension - DER_REP_CTY>,
            'DER_SECTOR_CPY': <Dimension - DER_SECTOR_CPY>,
            'DER_CPC': <Dimension - DER_CPC>,
            'DER_SECTOR_UDL': <Dimension - DER_SECTOR_UDL>,
            'DER_CURR_LEG1': <Dimension - DER_CURR_LEG1>,
            'DER_CURR_LEG2': <Dimension - DER_CURR_LEG2>,
            'DER_ISSUE_MAT': <Dimension - DER_ISSUE_MAT>,
            'DER_RATING': <Dimension - DER_RATING>,
            'DER_EX_METHOD': <Dimension - DER_EX_METHOD>,
            'DER_BASIS': <Dimension - DER_BASIS>,
            'TIME_PERIOD': <TimeDimension - TIME_PERIOD>},
            'measure': <PrimaryMeasure - OBS_VALUE>,
            'attributes': {'TIME_FORMAT': <Attribute - TIME_FORMAT>,
            'OBS_STATUS': <Attribute - OBS_STATUS>,
            'AVAILABILITY': <Attribute - AVAILABILITY>,
            'COLLECTION': <Attribute - COLLECTION>,
            'DECIMALS': <Attribute - DECIMALS>,
            'UNIT_MEASURE': <Attribute - UNIT_MEASURE>,
            'UNIT_MULT': <Attribute - UNIT_MULT>,
            'OBS_CONF': <Attribute - OBS_CONF>,
            'OBS_PRE_BREAK': <Attribute - OBS_PRE_BREAK>,
            'TITLE_TS': <Attribute - TITLE_TS>
        },
        'groups': <GroupDimensionDescriptor - Sibling>
        }

