###########################
SDMXthon: the pythonic SDMX
###########################

SDMXthon is a library for parsing, validate and write SDMX documents.

Based on Pandas and written in python, it allows the conversion from different data formats, as CSV or JSON,
and inputting the data straight from a Pandas Dataframe.

**Features**

- Reading and writing SDMX-ML and SDMX-CSV
- Pandas connector (SDMX to Pandas, Pandas to SDMX)
- Data validation
- Metadata validation
- Interaction with SDMX APIs and Fusion Metadata Registry

**********
Main links
**********

- Bug Tracker and Enhancements: https://github.com/Meaningful-Data/sdmxthon/issues
- Documentation: https://docs.sdmxthon.meaningfuldata.eu
- Source Code: https://github.com/Meaningful-Data/sdmxthon
- Changelog: https://docs.sdmxthon.meaningfuldata.eu/changelog.html
- PyPi: https://pypi.org/project/sdmxthon/

.. include:: installation.rst

############
Introduction
############

SDMXthon is designed upon the necessity of a python library that guarantees
the conversion of data to SDMX and vice versa, supporting many formats.

The philosophy to build it was to provide a simple way to parse and access the data and metadata,
perform validations on it, modify the data if necessary using the Pandas infrastructure and
provide an engine to write SDMX-ML and SDMX-CSV files.

For a quickstart, please head to the :doc:`Walkthrough<./walkthrough>`

**Main convenience methods**

- Read SDMX files: :doc:`read_sdmx<./packages/api>`
- :class:`.Message` (SDMX Message abstraction)
- :class:`.Dataset` (data handling, validation and writing SDMX-ML and SDMX-CSV files)
- :doc:`Webservices<./webservices>`

*****************
Information Model
*****************

The library is based on the `SDMX Information model
<https://sdmx.org/wp-content/uploads/SDMX_2-1-1_SECTION_2_InformationModel_201108.pdf>`_.
Same names for classes and properties have been used.

***************************************
Access to the main features of SDMXthon
***************************************

Access to the main external methods are in :doc:`API module<./packages/api>`

Classes of the library are in the :doc:`Model package<./packages/model>`


********
Site map
********

.. toctree::
    :maxdepth: 2

    walkthrough
    installation
    packages/api
    packages/model
    packages/parsers
    webservices
    validations
    developers
    changelog