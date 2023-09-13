#########
Changelog
#########

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
________________

Initial release.
