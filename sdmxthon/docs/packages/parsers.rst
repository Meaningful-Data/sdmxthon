###############
Parsers Package
###############

The `parsers` package is a set of files used for reading, validating and
writing the :doc:`model<./model>` classes.

.. warning::

    All methods and classes of this package are for internal use of the \
    library. No third party application should use them as they are all \
    connected to the :doc:`model<./model>` classes

*************
Reading files
*************

Reading files are used to read the SDMX files and parse its information.

.. important::

    The methods for reading and writing the metadata are triggered from the \
    parsers but can be found on each :doc:`model<./model>` class.

=============
Data generic
=============

Data generic file contains a set of classes to parse the SDMX Generic file
format.

============
Data parser
============

Data parser contains the superclass for all parsing classes. Parsing is based
on the Factory design pattern with slight modifications for XML files:

* Build attributes: parses the attributes for each XML element
* Build children: parses the child of each XML element, calling the proper factory method

===============
Message parsers
===============

Message parsers contains the classes to parse the XML elements in a Message.
It also includes some classes for parsing the metadata XML elements, which call
the relevant model classes.

===============
Payload parsers
===============

Payload parsers contains the classes to parse the structures of a header
in a data message

====
Read
====

Read contains the methods to convert the data parser classes to the model
classes (:doc:`Message<./model/message>`, :doc:`Dataset<./model/dataset>` and `Pandas Dataframe \
<https://pandas.pydata.org/pandas-docs/stable/reference/api/ \
pandas.DataFrame.html>`_)


==========
References
==========

References contains the classes to parse the XML elements that references
a SDMX object from another.

*****************
Validations files
*****************


=================
Data validations
=================

Data validations file includes functions for validating data in a Dataset.
Please refer to the :doc:`Validations Page<../validations>` for more details.

=====================
Metadata validations
=====================

Metadata validations includes methods to check if the referenced objects are
in the same file at parsing.

*********************
Writing SDMX-ML files
*********************

The writer file includes all methods to write the data or metadata
to a SDMX-ML file.

It uses the MessageTypeEnum enumeration to select the format we would like to have, Generic or StructureSpecific
for data and Structure file for Metadata. This can be modified in :attr:`.Message.type` or using this enum in the
:meth:`.Dataset.to_xml` method.

.. autoclass:: sdmxthon.utils.enums.MessageTypeEnum
    :members:
    :show-inheritance:
    :undoc-members:

You may also write SDMX-CSV files using the :meth:`.Dataset.to_sdmx_csv` method.
