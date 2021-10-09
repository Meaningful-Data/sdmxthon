# Common
HEADER = 'Header'
DATASET = 'DataSet'
SERIES = 'Series'
OBS = 'Obs'
AGENCY_ID = 'agencyID'
ID = 'id'
VERSION = 'version'

# Structure Specific
STRSPE = 'StructureSpecificData'
GENERIC = 'GenericData'
SERIESKEY = 'SeriesKey'
ATTRIBUTES = 'Attributes'
VALUE = 'Value'
OBS_DIM = 'ObsDimension'
OBSVALUE = 'ObsValue'
OBSKEY = 'ObsKey'
# Header
STRREF = 'structureRef'
STRUCTURE = 'Structure'
STRID = 'structureID'
DIM_OBS = 'dimensionAtObservation'
ALL_DIM = "AllDimensions"
REF = 'Ref'

# Structures
# Common
NAME = 'Name'
DESC = 'Description'
LANG = 'lang'
XML_TEXT = '#text'
# General
ANNOTATIONS = 'Annotations'
STRUCTURES = 'Structures'
ORGS = 'OrganisationSchemes'
AGENCIES = 'AgencyScheme'
CODELISTS = 'Codelists'
CONCEPTS = 'Concepts'
DSDS = 'DataStructures'
DATAFLOWS = 'DataFlows'

# Individual
AGENCY = 'Agency'
CL = 'Codelist'
CODE = 'Code'
CS = 'ConceptScheme'
CON = 'Concept'
DSD = 'DataStructure'

# DSD components
DSD_COMPS = 'DataStructureComponents'
CON_ID = 'ConceptIdentity'
# Dimension
DIM_LIST = 'DimensionList'
DIM_LIST_LOW = 'dimension_list'
DIM = 'Dimension'
TIME_DIM = 'TimeDimension'
# Attribute
ATT_LIST = 'AttributeList'
ATT_LIST_LOW = 'attribute_list'
ATT = 'Attribute'
ATT_REL = 'AttributeRelationship'
# Measure
ME_LIST = 'MeasureList'
ME_LIST_LOW = 'measure_list'
MEASURE = 'Measure'
GROUP = 'Group'
GROUP_DIM = 'GroupDimension'
DIM_REF = 'DimensionReference'

# Annotation
ANNOTATION = 'Annotation'
ANNOTATION_TITLE = 'AnnotationTitle'
ANNOTATION_TYPE = 'AnnotationType'
ANNOTATION_TEXT = 'AnnotationText'

TITLE = 'title'
TYPE = 'title'
TEXT = 'text'

# Representation
CORE_REP = 'CoreRepresentation'
CORE_REP_LOW = 'core_representation'
LOCAL_REP = 'LocalRepresentation'
LOCAL_REP_LOW = 'local_representation'
ENUM = 'Enumeration'
ENUM_FORMAT = 'EnumerationFormat'
TEXT_FORMAT = 'TextFormat'

# Facets
FACETS = 'facets'
TEXT_TYPE = 'textType'
TEXT_TYPE_LOW = 'text_type'

# Contact
CONTACT = 'Contact'
DEPARTMENT = 'Department'
ROLE = 'Role'
URI = 'URI'
EMAIL = 'Email'
X400 = 'X400'
TELEPHONE = 'Telephone'
FAX = 'Fax'

# Extras
MAINTAINER = 'maintainer'
XMLNS = 'xmlns'
COMPS = 'components'

# Schemas
pathToSchema = 'schemas/SDMXMessage.xsd'
schema_root = 'http://www.sdmx.org/resources/sdmxml/schemas/v2_1/'
namespaces = {
    schema_root + 'message': None,
    schema_root + 'common': None,
    schema_root + 'structure': None,
    'http://www.w3.org/2001/XMLSchema-instance': 'xsi',
    'http://www.w3.org/XML/1998/namespace': None,
    schema_root + 'data/structurespecific': None,
    schema_root + 'data/generic': None}

# To exclude from attached_attributes
exc_attributes = [STRREF, 'action', 'dataScope', 'xsi:type', SERIES, OBS]
