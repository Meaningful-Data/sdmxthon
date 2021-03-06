###########################
SDMXthon: the pythonic SDMX
###########################

SDMXthon is a library for parsing, validate and write SDMX documents.

Based on Pandas and written in python, it allows the conversion from different data formats, as CSV or JSON,
and inputting the data straight from a Pandas Dataframe.

Main features of the library:

- SDMX to Pandas Dataframe
- SDMX metadata parsing
- Data and metadata validation
- Pandas Dataframe to SDMX
- All SDMX-ML 2.1 formats supported

############
Introduction
############

SDMXthon is designed upon the necessity of a python library that guarantees
the conversion of data to SDMX from many formats and vice versa.

The philosophy to build it was to provide a simple way to parse and access the data and metadata,
perform validations on it, modify the data if necessary using the Pandas infrastructure and
provide an engine to write the SDMX-ML files.

For a quickstart, please head to the :doc:`Walkthrough<./walkthrough>`

*****************
Information Model
*****************

The library is based on the `SDMX Information model
<https://sdmx.org/wp-content/uploads/SDMX_2-1-1_SECTION_2_InformationModel_201108.pdf>`_.
Same names for classes and properties have been used.

***************************************
Access to the main features of SDMXthon
***************************************

All access to parse the SDMX files are in the :doc:`Api package<./packages/api>`

Classes of the library are in the :doc:`Model package<./packages/model>`

********
Packages
********

.. toctree::
   :maxdepth: 2

   walkthrough
   packages/api
   packages/model
   packages/parsers
   validations
   developers

