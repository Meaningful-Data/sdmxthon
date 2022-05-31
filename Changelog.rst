#########
Changelog
#########

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
