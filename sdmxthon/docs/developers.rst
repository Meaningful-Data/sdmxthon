################
Developers Guide
################

This guide has been created to help developers to build applications using the
library as an engine, or contribute to the library through our `GitHub`.
Unless specified, all files that are referred in this guide belong to the
Parsers package. No data is modified in the validations or the writing process.

************
Code styling
************

Code has been adapted to PEP8 style guidelines with maximum 80 columns. It
allows the developers to easily navigate through the code and check the
documentation at the same time.

*********************************
3rd party applications connection
*********************************

Any external applications should use the API methods and the classes defined in
the Model package. All methods starting with a _ defined in those classes
are intended to be used by the processes defined below and should NOT be used
by any 3rd party application as they may produce unwanted results.


***********************
High level architecture
***********************

SDMXthon provides three main features:
    - Reading an SDMX-ML file
    - Validate its content
    - Write the content to a SDMX-ML file

The library is divided in 4 main packages: API, Model, Parsers and Utils.
These packages are connected with each other via several methods depending on
the operations we want to make.

=======
Reading
=======

All reading methods are triggered by the API methods, depending on the
parameters and the desired output they will be suitable for any specific case,
as defined in the API Package.

There are 3 elements that are common to all SDMX-ML files: the Header, the
data or metadata XML elements and their attributes. All headers are parsed via
the :doc:`Header<./packages/model/header>` class, defined in the Model Package. The XML elements and its
attributes are parsed with the build_children and the build_attributes methods
of DataParser and its implementations in each class.

Depending on the content of each XML file, we will go through different classes
to parse it through these two methods.

`DIAGRAMS FOR PARSING METHODS`

===========
Validations
===========

For more details of the errors triggered by the library please refer to the
:doc:`Validations<./validations>`

Data validations processes can be found in the data_validations.py file.
These methods are triggered by the semantic_validation method in the Dataset
class in the Model package.

Metadata validations processes can be found in the metadata_validations file.
These processes are only triggered when the metadata is parsed, as the setters
in each Model class related to metadata should prevent any misbehaviour
if used correctly.

Structural validations is performed on XML files prior to its parsing if the
validate parameter on each API method is set to True.

=======
Writing
=======

The writing processes can be triggered from a Dataset or a Message, by using
the write process. The processes can be found in the write.py file.

To perform the data writing from a Pandas Dataframe to an SDMX file, we found
that best approach was to adapt the to_csv() method to write SDMX-ML files
(XML format), without modifying the Pandas package. It allows a chunking process
to write large files without a huge impact on memory.

The metadata writing process has been implemented in a similar way to the
Reading process, by going through each class in a specific order to be
compliant with the XML Schemas. The methods used are the parse_XML and the
to_XML, depending on each class. Due to the library structure, this method can
only be triggered from the Message class.