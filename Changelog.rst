#########
Changelog
#########

2.6.7 (2024-07-26)
------------------
**Added**

**Changes**
  - Accepting .Stat Suite exported data with two datasets with same structure and different action (Replace and Delete), to keep only the Replace data.

**Bugfixes**
  - Fixed bug on OBSVALUE on Generic All Dimensions Reader when OBSVALUE is not present. #62
  - Fixed bug on Organisation Scheme when isPartial is present.


2.6.6 (2024-04-16)
------------------
**Added**

**Changes**
  - Updated VTL mapping from TimePeriod to Time_Period

**Bugfixes**


2.6.5 (2024-04-15)
------------------
**Added**

**Changes**

**Bugfixes**
  - Fixed possible unhandled exceptions in reading ContentConstraints

2.6.4 (2024-03-12)
------------------
**Added**

**Changes**
  - Changed VTL Mapping on ObservationalTimePeriod and StandardTimePeriod to TimePeriod
  - Improved sdmxthon comprehensive example notebook

**Bugfixes**
  - Fixed circular import on webservices and API

2.6.3 (2024-02-23)
------------------
**Added**

**Changes**

**Bugfixes**
  - Fixed bug on writing if Attribute Descriptor is not present
  - Fixed bug on reading Structure Specific datasets with only one record
  - Fixed bug on reading Generic with no Attributes at OBS level

2.6.2 (2024-02-22)
------------------
**Added**
  - Added tons of webservices queries and query builders.

**Changes**

**Bugfixes**
  - Fixed bug on Series writing if Attribute Descriptor is not present (#56)

2.6.1 (2024-01-17)
------------------
**Added**
  - Added flag for use_dataset_id on get_pandas_df

**Changes**

**Bugfixes**


2.6 (2024-01-17)
------------------
**Added**
  - Added compatibility for Group on attributes related to a GroupDimensionDescriptor
  - Added compatibility for SDMX-CSV on get_pandas_df and get_datasets #54
  - Added reading and writing methods for Group in SDMX-ML StructureSpecific data messages

**Changes**

**Bugfixes**
  - Fixed a bug on ActionEnum in DatasetAttributes

2.5.3 (2023-12-22)
------------------
**Added**
  - Added internal enumeration for Action (ActionEnum)

**Changes**
  - Changed description of dataset attributes and added docs for structure_type and unique_id in Dataset.
  - Fixed reading and writing of SDMX-CSV v2 to handle ACTION column. #53
  - Changed link to Changelog in docs.

**Bugfixes**
  - Fixed bug when adding dataset attributes to raise an unhandled exception if not present on keys. #53

2.5.1 (2023-12-21)
------------------
**Added**
  - Added changelog on docs and github link #52
  - Structure submission to FMR from Dataflow and DataStructureDefinition #47
  - Read SDMX to support SDMX-CSV v1 and v2 #45
  - Handling on error messages on SOAP APIs requests
  - Added MessageTypeEnum documentation.

**Changes**
  - Changed description of features in docs.

**Bugfixes**

2.5 (2023-11-10)
----------------
**Added**
  - Added FMR interaction with data validation and metadata submission. Added methods on webservices package.
  - Added SDMXError and SubmissionRequest classes to handle FMR interaction
  - Added to_sdmx_csv() method to Dataset #43
  - Added fmr_validation() method to Dataset #43
  - Added upload_metadata_to_fmr() method to Message #44
  - Added upload_metadata_to_fmr() method to API #44
  - Added webservices documentation #42

**Changes**
  - Changed semantic_validation to structural validation on documentation
  - Changed MessageTypeEnum on StructureSpecific files from Structure to StructureSpecific

**Bugfixes**
  - Fixed bug on Message validate method using old semantic_validation on each Dataset in payload.

2.4 (2023-10-23)
----------------
**Added**

**Changes**
  - Support for DatasetID as key on get_pandas_df and xml_to_csv results

**Bugfixes**

2.3.2 (2023-09-26)
------------------
**Added**
  - Webservices and Data Discovery for OECD (v1 and v2) and UNICEF

**Changes**

**Bugfixes**
  - Fixed bug on ConceptRole on Dimension


2.3.1 (2023-09-15)
------------------
**Added**

**Changes**

**Bugfixes**
 - Fixed webservices URLs and params.

2.3 (2023-09-13)
----------------
**Added**
 - Webservices and data discovery on BIS, ECB, ESTAT, ILO

**Changes**

**Bugfixes**
 - Fixed duplication detection on ItemScheme. It is based now on ID instead of URN.

2.2 (2023-07-04)
----------------
**Added**

**Changes**
 - International String is now based on str instead of object. NameableArtefacts can use str on __init__ method.
 - Changed semantic validation to structure validation. Improved error messages and logic.

**Bugfixes**

2.1 (2023-03-14)
----------------
**Added**

**Changes**
 - Improved structural error management with definitions of common errors.

**Bugfixes**
 - Fixed ID errors on Annotation

2.0 (2023-03-03)
----------------

**Added**
 - Added Webservices to search for datasets and dataflows in ECB, EUROSTAT,
   BIS and ILO using a REST API.

**Changes**
 - Fixed read_xml to allow for more flexibility on structural validation and better error management.

**Bugfixes**
 - Fixed member reading on CubeRegion.

1.3 (2022-31-05)
----------------
**Added**

**Changes**
 - Implemented better understanding of inFile in read_xml.
 - Adapted to_vtl_json() to new format.

**Bugfixes**

1.2 (2021-01-12)
-----------------

**Added**
 - Implemented several formats on validFrom/validTo, as shown on issue #17

**Changes**
 - Redesigned reading process based on xmltodict
 - Implemented custom writing process based on generators. Reduced memory footprint and improved performance and maintainability. Implemented Generic Series writing process.
 - Improved overall performance on semantic validation.
 - Cleanup of old parsers and writing methods. Simplified code for better maintainability.
 - Model changes:
    - Deleted 'dataset' on data retrieval
    - Changed keys of message.content on Metadata Type.

**Bugfixes**

1.1 (2021-01-12)
----------------

Development version (Yanked Release), changes are implemented in 1.2.


1.0.3 (2021-09-30)
------------------

**Added**

**Changes**

**Bugfixes**
 - Fixed bug on Dataflow with constraints parsing.

1.0.2 (2021-07-06)
------------------

**Added**

**Changes**

**Bugfixes**
 - Fixed bug on Generic writing with only one dimension or attribute.

1.0.1 (2021-06-23)
------------------

**Added**

**Changes**
 - Added support for strings in all API methods. Restricted path to os.Pathlike


**Bugfixes**
 - Fixed bug on Series Constraints duplicated rows.

1.0 (2021-05-28)
----------------

Initial release.
