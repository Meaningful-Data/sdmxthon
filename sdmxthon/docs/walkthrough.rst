###########
Walkthrough
###########

************
Introduction
************
SDMXthon is an open-source library created for managing SDMX data and metadata with Python.
The library implements the 2.1 version of the SDMX standard

********
Features
********

- Reading and writing SDMX ML
- Data validation
- Metadata validation
    

************
Installation
************

.. code-block:: text

    pip install SDMXthon

************************************
Use of SDMXthon for common use cases
************************************

====================
Reading an SDMX file
====================
SDMXthon has been thought to provide different simple ways to access the information stored in an SDMX file.
It provides an API method to read any type of SDMX file or URL, returning a Message object.

API method to read an SDMX file or URL:

.. code-block:: python

    >>> import sdmxthon
    >>> sdmx_message = sdmxthon.read_sdmx('sdmxFiles/cbd_dsd.sdmx')




The message class has a number of methods to access the information.

SDMX messages may contain data or metadata. In any of the two cases, the content of the message is inside the *payload*
attribute. But it is important to understand the type of message, because the information and access will depend on
whether the message is a data or metadata message. The attribute *type* provides that information:

.. code-block:: python

    >>> sdmx_message.type

    MessageTypeEnum.Metadata


The information in the payload can be obtained by using the payload class attributes. For instance, to access the DSDs contained in the message:

.. code-block:: python

     >>> sdmx_message.payload['DataStructures']

    {'ECB:ECB_CBD2(1.0)': <DataStructureDefinition  - ECB:ECB_CBD2(1.0)>}

But there is also a convenience method to access the information. The *content* attribute returns a dictionary with
the content of the file. The keys of the dictionaries represent the types of object, and the values are lists with
the concrete objects:

.. code-block:: python

    >>> sdmx_message.content

    {
      "Codelists": {
        "ECB:CL_ACTIVITY(1.0)": "<Codelist - ECB:CL_ACTIVITY(1.0)>",
        "ECB:CL_AREA(1.0)": "<Codelist - ECB:CL_AREA(1.0)>",
        "ECB:CL_CB_EXP_TYPE(1.0)": "<Codelist - ECB:CL_CB_EXP_TYPE(1.0)>",
        "ECB:CL_CB_ITEM(1.0)": "<Codelist - ECB:CL_CB_ITEM(1.0)>",
        "ECB:CL_CB_PORTFOLIO(1.0)": "<Codelist - ECB:CL_CB_PORTFOLIO(1.0)>",
        "ECB:CL_CB_REP_FRAMEWRK(1.0)": "<Codelist - ECB:CL_CB_REP_FRAMEWRK(1.0)>",
        "ECB:CL_CB_REP_SECTOR(1.0)": "<Codelist - ECB:CL_CB_REP_SECTOR(1.0)>",
        "ECB:CL_CB_SECTOR_SIZE(1.0)": "<Codelist - ECB:CL_CB_SECTOR_SIZE(1.0)>",
        "ECB:CL_CB_VAL_METHOD(1.0)": "<Codelist - ECB:CL_CB_VAL_METHOD(1.0)>",
        "ECB:CL_CONF_STATUS(1.0)": "<Codelist - ECB:CL_CONF_STATUS(1.0)>",
        "ECB:CL_CURRENCY(1.0)": "<Codelist - ECB:CL_CURRENCY(1.0)>",
        "ECB:CL_DECIMALS(1.0)": "<Codelist - ECB:CL_DECIMALS(1.0)>",
        "ECB:CL_FREQ(1.0)": "<Codelist - ECB:CL_FREQ(1.0)>",
        "ECB:CL_FSENTRY(1.0)": "<Codelist - ECB:CL_FSENTRY(1.0)>",
        "ECB:CL_MATURITY(1.0)": "<Codelist - ECB:CL_MATURITY(1.0)>",
        "ECB:CL_OBS_STATUS(1.0)": "<Codelist - ECB:CL_OBS_STATUS(1.0)>",
        "ECB:CL_ORGANISATION(1.0)": "<Codelist - ECB:CL_ORGANISATION(1.0)>",
        "ECB:CL_SECTOR(1.0)": "<Codelist - ECB:CL_SECTOR(1.0)>",
        "ECB:CL_TIME_COLLECT(1.0)": "<Codelist - ECB:CL_TIME_COLLECT(1.0)>",
        "ECB:CL_UNIT(1.0)": "<Codelist - ECB:CL_UNIT(1.0)>",
        "ECB:CL_UNIT_MULT(1.0)": "<Codelist - ECB:CL_UNIT_MULT(1.0)>"
      },
      "Concepts": {
        "ECB:ECB_CONCEPTS(1.0)": "<ConceptScheme - ECB:ECB_CONCEPTS(1.0)>"
      },
      "DataStructures": {
        "ECB:ECB_CBD2(1.0)": "<DataStructureDefinition  - ECB:ECB_CBD2(1.0)>"
      },
      "OrganisationSchemes": "<AgencyScheme - SDMX:AGENCIES(1.0)>"
    }

The input to the read_sdmx method can be a file or an URL. An example with a URL:

.. code-block:: python

     sdmx_data_message = sdmxthon.read_sdmx('http://ec.europa.eu/eurostat/SDMX/diss-web/rest/data/nama_10_gdp/.CLV10_MEUR.B1GQ.BE/?startperiod=2005&endPeriod=2011')


==============
SDMX data
==============

--------------------------------------------
Converting SDMX data into Pandas Data Frames
--------------------------------------------

When reading a data file with the read_sdmx method, metadata are not provided. With this, it is possible to access the
data in pandas, but other actions require loading the metadata (see next section).
SDMXthon is prepared to dealing with SDMX files containing more than one dataset. Therefore, the content attribute,
in the case of data, contains a dictionary where the keys are the id of the Dataset and the values are the
Datasets objects:

.. code-block:: python

     >>> sdmx_data_message = sdmxthon.read_sdmx('http://ec.europa.eu/eurostat/SDMX/diss-web/rest/data/nama_10_gdp/.CLV10_MEUR.B1GQ.BE/?startperiod=2005&endPeriod=2011')
     >>> sdmx_data_message.content

     {'ESTAT_DSD_nama_10_gdp_1_0': <DataSet - No Structure found>}

A Dataset object has a series of SDMX-specific attributes (see reference for complete list). The data in the dataset are stored as a Pandas Dataframe, in the *data* attribute:

.. code-block:: python

     >>> sdmx_data_message.content['ESTAT_DSD_nama_10_gdp_1_0'].data

      NA_ITEM        UNIT GEO FREQ TIME_PERIOD OBS_VALUE
    0    B1GQ  CLV10_MEUR  BE    A        2011  369293.6
    1    B1GQ  CLV10_MEUR  BE    A        2010  363140.1
    2    B1GQ  CLV10_MEUR  BE    A        2009  353028.3
    3    B1GQ  CLV10_MEUR  BE    A        2008  360309.3
    4    B1GQ  CLV10_MEUR  BE    A        2007  358706.1
    5    B1GQ  CLV10_MEUR  BE    A        2006  345984.7
    6    B1GQ  CLV10_MEUR  BE    A        2005  337373.7


---------------------------------------------------------------
Using SDMXthon for validating data and generating SDMX messages
---------------------------------------------------------------
SDMXthon can be used for validating data against SDMX data, and also for generating SDMX ML messages. In order to do that, *DataSets* need to have, on top of the data as a Pandas DataFrame, their metadata associated (a DSD in the *structure* attribute or a Data Flow in the *dataflow* attribute.

SDMXthon provides an API method to read data and the related metadata:

.. code-block:: python

     >>> sdmx_data = sdmxthon.get_datasets(
            path_to_data='https://sdw-wsrest.ecb.europa.eu/service/data/EXR/M.USD.EUR.SP00.A',
            path_to_metadata='https://sdw-wsrest.ecb.europa.eu/service/datastructure/ECB/ECB_EXR1/1.0?references=children')

This method returns a DataSet object, which contains the related DSD in the *structure* property and the data, as Pandas Data Frame, in the *data* attribute:

.. code-block:: python

     >>> sdmx_data.structure

    <DataStructureDefinition  - ECB:ECB_EXR1(1.0)>

.. code-block:: python

     >>> sdmx_data.data

        FREQ CURRENCY CURRENCY_DENOM  ... TIME_PERIOD          OBS_VALUE OBS_STATUS
    0      M      USD            EUR  ...     1999-01            1.16078          A
    1      M      USD            EUR  ...     1999-02           1.120765          A
    2      M      USD            EUR  ...     1999-03  1.088295652173913          A
    3      M      USD            EUR  ...     1999-04  1.070440909090909          A
    4      M      USD            EUR  ...     1999-05  1.062809523809524          A
    ...
    262    M      USD            EUR  ...     2020-11  1.183790476190476          A
    263    M      USD            EUR  ...     2020-12  1.216972727272728          A
    264    M      USD            EUR  ...     2021-01           1.217085          A
    265    M      USD            EUR  ...     2021-02            1.20979          A
    266    M      USD            EUR  ...     2021-03  1.189908695652174          A

    [267 rows x 16 columns]

With this information it is possible to manipulate and validate the data and to create an SDMX 2.1 XML message. For instance, we can modify the data in the previous example:

.. code-block:: python

     >>> sdmx_data.data['CURRENCY'] = 'currency'

In this case, we have changed the value of the dimension 'Currency' for all the observations, assigning the value 'currency'.

We can now proceed to validate the Data Set:

.. code-block:: python

     >>> sdmx_data.semantic_validation()

    [
        {'Code': 'SS08', 'ErrorLevel': 'WARNING', 'Component': 'CURRENCY', 'Type': 'Dimension', 'Rows': None, 'Message': 'Value currency not compliant with maxLength : 3'},
        {'Code': 'SS04', 'ErrorLevel': 'CRITICAL', 'Component': 'CURRENCY', 'Type': 'Dimension', 'Rows': None, 'Message': 'Wrong value currency for dimension CURRENCY'}
    ]

In this case we are getting an error, because the value 'currency' is not a Code of the CL_CURRENCY Codelist. The list of validations included in SDMXthon is provided in the following file: . The validations have a type, which can take two values: 'Critical' or 'Warning'. Warning errors do not prevent from generating XML files, although they have errors. Critical errors do not allow to generate XML files.

Data Set objects include the method *to_xml* to create an XML IO string object:

.. code-block:: python

     >>> sdmx_data.to_xml()

    _io.StringIO object

================
SDMX metadata
================

-----------
Navigation
-----------

SDMXthon provides a simple way to navigate through the metadata. Using the
content method on the Message class and the items method on each item
Scheme we can access to the inner metadata classes.

.. code-block:: python

    >>> concept_scheme = message.content['Concepts']["ECB:ECB_CONCEPTS(1.0)"]
    >>> concept_scheme.items

    {
     'ACCOUNT_ENTRY': <Concept - ACCOUNT_ENTRY>,
     'ADJU_DETAIL': <Concept - ADJU_DETAIL>,
     'ADJUST_DETAIL': <Concept - ADJUST_DETAIL>,
     ......
    }

Regarding the DataStructureDefinition, we can access in a similar way:

.. code-block:: python

    >>> dsd = message.content['DataStructures']['ECB:ECB_CBD2(1.0)']
    >>> dsd.content

    {'dimensions': {
      'FREQ': <Dimension - FREQ>,
      'REF_AREA': <Dimension - REF_AREA>,
      'COUNT_AREA': <Dimension - COUNT_AREA>,
      ....
      },
     'measure': <PrimaryMeasure - OBS_VALUE>,
     'attributes': {
      'TIME_FORMAT': <Attribute - TIME_FORMAT>,
      'OBS_STATUS': <Attribute - OBS_STATUS>,
      'CONF_STATUS': <Attribute - CONF_STATUS>,
      ....
      }
    }


----------------------------------
Accessing representation elements
----------------------------------

Each element has its own dedicated class as shown in the
:doc:`Model package<./packages/model>`.

To access the :doc:`Representation<./packages/model/representation>`,  there is
a convenience method which calls the effective representation of an element:

.. code-block:: python

    >>> freq = dsd.content['dimensions']['FREQ']
    >>> freq.representation

We can also access its local representation and the core representation in its
concept identity:

.. code-block:: python

    >>> freq.concept_identity

    <Concept - FREQ>

    >>> freq.concept_identity.core_representation

    None

    >>> freq.local_representation.codelist

    <Codelist - CL_FREQ>

As all elements are internally referenced, we can access also its items:

.. code-block:: python

    >>> freq.local_representation.codelist.items

    {
     'A': <Code - A>,
     'B': <Code - B>,
     'D': <Code - D>,
     'E': <Code - E>,
     'H': <Code - H>,
     'M': <Code - M>,
     'N': <Code - N>,
     'Q': <Code - Q>,
     'S': <Code - S>,
     'W': <Code - W>
    }

