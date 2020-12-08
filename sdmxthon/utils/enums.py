try:
    from enum import Enum
    from enum import IntEnum
except ImportError:
    Enum = object


class ActionType(str, Enum):
    """ActionType provides a list of actions, describing the intention of the
    data transmission from the sender's side. Each action provided at the
    data or metadata set level applies to the entire data set for which it
    is given. Note that the actions indicated in the Message Header are
    optional, and used to summarize specific actions indicated with this
    data type for all registry interactions. The "Informational" value is
    used when the message contains information in response to a query,
    rather than being used to invoke a maintenance activity."""
    APPEND = 'Append'  # Append - this is an incremental update for an existing data/metadata set or the provision of new data or documentation (attribute values) formerly absent. If any of the supplied data or metadata is already present, it will not replace that data or metadata. This corresponds to the "Update" value found in version 1.0 of the SDMX Technical Standards.
    REPLACE = 'Replace'  # Replace - data/metadata is to be replaced, and may also include additional data/metadata to be appended. The replacement occurs at the level of the observation - that is, it is not possible to replace an entire series.
    DELETE = 'Delete'  # Delete - data/metadata is to be deleted. Deletion occurs at the lowest level object. For instance, if a delete data message contains a series with no observations, then the entire series will be deleted. If the series contains observations, then only those observations specified will be deleted. The same basic concept applies for attributes. If a series or observation in a delete message contains attributes, then only those attributes will be deleted.
    INFORMATION = 'Information'  # Informational - data/metadata is being exchanged for informational purposes only, and not meant to update a system.


class AnyQueryType(str, Enum):
    """AnyQueryType is a single enumeration of the value "Any" which is meant
    to be used in union with other simple types when a query allows for any
    of the possible values."""
    ANY = 'Any'


class BasicComponentDataType(str, Enum):
    """BasicComponentDataType provides an enumerated list of the types of
    characters allowed in the textType attribute for all non-target object
    components."""
    STRING = 'String'
    ALPHA = 'Alpha'
    ALPHA_NUMERIC = 'AlphaNumeric'
    NUMERIC = 'Numeric'
    BIG_INTEGER = 'BigInteger'
    INTEGER = 'Integer'
    LONG = 'Long'
    SHORT = 'Short'
    DECIMAL = 'Decimal'
    FLOAT = 'Float'
    DOUBLE = 'Double'
    BOOLEAN = 'Boolean'
    _uri = 'URI'
    COUNT = 'Count'
    INCLUSIVE_VALUE_RANGE = 'InclusiveValueRange'
    EXCLUSIVE_VALUE_RANGE = 'ExclusiveValueRange'
    INCREMENTAL = 'Incremental'
    OBSERVATIONAL_TIME_PERIOD = 'ObservationalTimePeriod'
    STANDARD_TIME_PERIOD = 'StandardTimePeriod'
    BASIC_TIME_PERIOD = 'BasicTimePeriod'
    GREGORIAN_TIME_PERIOD = 'GregorianTimePeriod'
    GREGORIAN_YEAR = 'GregorianYear'
    GREGORIAN_YEAR_MONTH = 'GregorianYearMonth'
    GREGORIAN_DAY = 'GregorianDay'
    REPORTING_TIME_PERIOD = 'ReportingTimePeriod'
    REPORTING_YEAR = 'ReportingYear'
    REPORTING_SEMESTER = 'ReportingSemester'
    REPORTING_TRIMESTER = 'ReportingTrimester'
    REPORTING_QUARTER = 'ReportingQuarter'
    REPORTING_MONTH = 'ReportingMonth'
    REPORTING_WEEK = 'ReportingWeek'
    REPORTING_DAY = 'ReportingDay'
    DATE_TIME = 'DateTime'
    TIME_RANGE = 'TimeRange'
    MONTH = 'Month'
    MONTH_DAY = 'MonthDay'
    DAY = 'Day'
    TIME = 'Time'
    DURATION = 'Duration'
    XHTML = 'XHTML'


class CodeDataType(str, Enum):
    """CodeDataType is a restriction of the basic data types that are
    applicable to codes. Although some of the higher level time period
    formats are perimitted, it should be noted that any value which
    contains time (which includes a time zone offset) is not allowable as a
    code identifier."""
    STRING = 'String'
    ALPHA = 'Alpha'
    ALPHA_NUMERIC = 'AlphaNumeric'
    NUMERIC = 'Numeric'
    BIG_INTEGER = 'BigInteger'
    INTEGER = 'Integer'
    LONG = 'Long'
    SHORT = 'Short'
    BOOLEAN = 'Boolean'
    _uri = 'URI'
    COUNT = 'Count'
    INCLUSIVE_VALUE_RANGE = 'InclusiveValueRange'
    EXCLUSIVE_VALUE_RANGE = 'ExclusiveValueRange'
    INCREMENTAL = 'Incremental'
    OBSERVATIONAL_TIME_PERIOD = 'ObservationalTimePeriod'
    STANDARD_TIME_PERIOD = 'StandardTimePeriod'
    BASIC_TIME_PERIOD = 'BasicTimePeriod'
    GREGORIAN_TIME_PERIOD = 'GregorianTimePeriod'
    GREGORIAN_YEAR = 'GregorianYear'
    GREGORIAN_YEAR_MONTH = 'GregorianYearMonth'
    GREGORIAN_DAY = 'GregorianDay'
    REPORTING_TIME_PERIOD = 'ReportingTimePeriod'
    REPORTING_YEAR = 'ReportingYear'
    REPORTING_SEMESTER = 'ReportingSemester'
    REPORTING_TRIMESTER = 'ReportingTrimester'
    REPORTING_QUARTER = 'ReportingQuarter'
    REPORTING_MONTH = 'ReportingMonth'
    REPORTING_WEEK = 'ReportingWeek'
    REPORTING_DAY = 'ReportingDay'
    MONTH = 'Month'
    MONTH_DAY = 'MonthDay'
    DAY = 'Day'
    DURATION = 'Duration'


class CodeTypeCodelistType(str, Enum):
    """CodeTypeCodelistType provides an enumeration of all code objects."""
    CODE = 'Code'
    HIERARCHICAL_CODE = 'HierarchicalCode'


class CodelistTypeCodelistType(str, Enum):
    """CodelistTypeCodelistType provides an enumeration of all codelist
    objects."""
    CODELIST = 'Codelist'
    HIERARCHICAL_CODELIST = 'HierarchicalCodelist'


class ComponentListTypeCodelistType(str, Enum):
    """ComponentListTypeCodelistType provides an enumeration of all component
    list objects."""
    ATTRIBUTE_DESCRIPTOR = 'AttributeDescriptor'
    DIMENSION_DESCRIPTOR = 'DimensionDescriptor'
    GROUP_DIMENSION_DESCRIPTOR = 'GroupDimensionDescriptor'
    MEASURE_DESCRIPTOR = 'MeasureDescriptor'
    METADATA_TARGET = 'MetadataTarget'
    REPORT_STRUCTURE = 'ReportStructure'


class ComponentTypeCodelistType(str, Enum):
    """ComponentTypeCodelistType provides an enumeration of all component
    objects."""
    ATTRIBUTE = 'Attribute'
    CONSTRAINT_TARGET = 'ConstraintTarget'
    DATA_SET_TARGET = 'DataSetTarget'
    DIMENSION = 'Dimension'
    IDENTIFIABLE_OBJECT_TARGET = 'IdentifiableObjectTarget'
    DIMENSION_DESCRIPTOR_VALUES_TARGET = 'DimensionDescriptorValuesTarget'
    MEASURE_DIMENSION = 'MeasureDimension'
    METADATA_ATTRIBUTE = 'MetadataAttribute'
    PRIMARY_MEASURE = 'PrimaryMeasure'
    REPORTING_YEAR_START_DAY = 'ReportingYearStartDay'
    REPORT_PERIOD_TARGET = 'ReportPeriodTarget'
    TIME_DIMENSION = 'TimeDimension'


class ConcreteMaintainableTypeCodelistType(str, Enum):
    """ConcreteMaintainableTypeCodelistType provides an enumeration of all
    concrete maintainable objects."""
    AGENCY_SCHEME = 'AgencyScheme'
    ATTACHMENT_CONSTRAINT = 'AttachmentConstraint'
    CATEGORISATION = 'Categorisation'
    CATEGORY_SCHEME = 'CategoryScheme'
    CODELIST = 'Codelist'
    CONCEPT_SCHEME = 'ConceptScheme'
    CONTENT_CONSTRAINT = 'ContentConstraint'
    DATAFLOW = 'Dataflow'
    DATA_CONSUMER_SCHEME = 'DataConsumerScheme'
    DATA_PROVIDER_SCHEME = 'DataProviderScheme'
    DATA_STRUCTURE = 'DataStructure'
    HIERARCHICAL_CODELIST = 'HierarchicalCodelist'
    METADATAFLOW = 'Metadataflow'
    METADATA_STRUCTURE = 'MetadataStructure'
    ORGANISATION_UNIT_SCHEME = 'OrganisationUnitScheme'
    PROCESS = 'Process'
    PROVISION_AGREEMENT = 'ProvisionAgreement'
    REPORTING_TAXONOMY = 'ReportingTaxonomy'
    STRUCTURE_SET = 'StructureSet'


class ConstraintTypeCodelistType(str, Enum):
    """ConstraintTypeCodelistType provides an enumeration of all constraint
    objects."""
    ATTACHMENT_CONSTRAINT = 'AttachmentConstraint'
    CONTENT_CONSTRAINT = 'ContentConstraint'


class ConstraintTypeCodelistType4(str, Enum):
    """ConstraintTypeCodelistType defines a list of types for a constraint for
    the purpose of querying."""
    CONSTRAINT = 'Constraint'
    ATTACHMENT_CONSTRAINT = 'AttachmentConstraint'
    CONTENT_CONSTRAINT = 'ContentConstraint'


class ContentConstraintTypeCodeType(str, Enum):
    """ContentConstraintTypeCodeType defines a list of types for a content
    constraint. A content constraint can state which data is present or
    which content is allowed for the constraint attachment."""
    ALLOWED = 'Allowed'  # The constraint contains the allowed values for attachable object.
    ACTUAL = 'Actual'  # The constraints contains the actual data present for the attachable object.


class DataReturnDetailType(str, Enum):
    """DataReturnDetailType contains a set of enumerations that indicate how
    much detail should be returned for a data set."""
    FULL = 'Full'  # The entire data set (including all data, documentation, and annotations) will be returned.
    DATA_ONLY = 'DataOnly'  # Only the observed values and their keys will be returned. Annotations and documentation (i.e. Attributes) and therefore Groups, will be excluded.
    SERIES_KEY_ONLY = 'SeriesKeyOnly'  # Only the series elements and the values for the dimensions will be returned. Annotations, documentation, and observations will be excluded.
    NO_DATA = 'NoData'  # Returns all documentation at the DataSet, Group, and Series level without any Observations (therefore, Observation level documentation is not returned). Annotations are not returned.


class DataScopeType(str, Enum):
    """DataScopeType is an enumeration of the possible validity scopes for a
    data set. These scopes indicate the level at which the data is stated
    to be valid."""
    DATA_STRUCTURE = 'DataStructure'  # The data set conforms simply to the data structure definition as it is defined, without regard to any constraints.
    CONSTRAINED_DATA_STRUCTURE = 'ConstrainedDataStructure'  # The data set conforms to the known allowable content constraints applied to the data structure definition.
    DATAFLOW = 'Dataflow'  # The data set conforms to the known allowable content constraints applied to the dataflow.
    PROVISION_AGREEMENT = 'ProvisionAgreement'  # The data set conforms to the known allowable content constraints applied to the provision agreement.


class DataStructureComponentTypeCodelistType(str, Enum):
    """DataStructureComponentTypeCodelistType provides an enumeration of all
    data structure component objects, except for the primary measure."""
    ATTRIBUTE = 'Attribute'
    DIMENSION = 'Dimension'
    MEASURE_DIMENSION = 'MeasureDimension'
    PRIMARY_MEASURE = 'PrimaryMeasure'
    REPORTING_YEAR_START_DAY = 'ReportingYearStartDay'
    TIME_DIMENSION = 'TimeDimension'


class DataType(str, Enum):
    """DataTypeType provides an enumerated list of the types of data formats
    allowed as the for the representation of an object."""
    STRING = 'String'  # A string datatype corresponding to W3C XML Schema's xs:string datatype.
    ALPHA = 'Alpha'  # A string datatype which only allows for the simple aplhabetic charcter set of A-Z, a-z.
    ALPHA_NUMERIC = 'AlphaNumeric'  # A string datatype which only allows for the simple alphabetic character set of A-Z, a-z plus the simple numeric character set of 0-9.
    NUMERIC = 'Numeric'  # A string datatype which only allows for the simple numeric character set of 0-9. This format is not treated as an integer, and therefore can having leading zeros.
    BIG_INTEGER = 'BigInteger'  # An integer datatype corresponding to W3C XML Schema's xs:integer datatype.
    INTEGER = 'Integer'  # An integer datatype corresponding to W3C XML Schema's xs:int datatype.
    LONG = 'Long'  # A numeric datatype corresponding to W3C XML Schema's xs:long datatype.
    SHORT = 'Short'  # A numeric datatype corresponding to W3C XML Schema's xs:short datatype.
    DECIMAL = 'Decimal'  # A numeric datatype corresponding to W3C XML Schema's xs:decimal datatype.
    FLOAT = 'Float'  # A numeric datatype corresponding to W3C XML Schema's xs:float datatype.
    DOUBLE = 'Double'  # A numeric datatype corresponding to W3C XML Schema's xs:double datatype.
    BOOLEAN = 'Boolean'  # A datatype corresponding to W3C XML Schema's xs:boolean datatype.
    _uri = 'URI'  # A datatype corresponding to W3C XML Schema's xs:anyURI datatype.
    COUNT = 'Count'  # A simple incrementing Integer type. The isSequence facet must be set to true, and the interval facet must be set to "1".
    INCLUSIVE_VALUE_RANGE = 'InclusiveValueRange'  # This value indicates that the startValue and endValue attributes provide the inclusive boundaries of a numeric range of type xs:decimal.
    EXCLUSIVE_VALUE_RANGE = 'ExclusiveValueRange'  # This value indicates that the startValue and endValue attributes provide the exclusive boundaries of a numeric range, of type xs:decimal.
    INCREMENTAL = 'Incremental'  # This value indicates that the value increments according to the value provided in the interval facet, and has a true value for the isSequence facet.
    OBSERVATIONAL_TIME_PERIOD = 'ObservationalTimePeriod'  # Observational time periods are the superset of all time periods in SDMX. It is the union of the standard time periods (i.e. Gregorian time periods, the reporting time periods, and date time) and a time range.
    STANDARD_TIME_PERIOD = 'StandardTimePeriod'  # Standard time periods is a superset of distinct time period in SDMX. It is the union of the basic time periods (i.e. the Gregorian time periods and date time) and the reporting time periods.
    BASIC_TIME_PERIOD = 'BasicTimePeriod'  # BasicTimePeriod time periods is a superset of the Gregorian time periods and a date time.
    GREGORIAN_TIME_PERIOD = 'GregorianTimePeriod'  # Gregorian time periods correspond to calendar periods and are represented in ISO-8601 formats. This is the union of the year, year month, and date formats.
    GREGORIAN_YEAR = 'GregorianYear'  # A Gregorian time period corresponding to W3C XML Schema's xs:gYear datatype, which is based on ISO-8601.
    GREGORIAN_YEAR_MONTH = 'GregorianYearMonth'  # A time datatype corresponding to W3C XML Schema's xs:gYearMonth datatype, which is based on ISO-8601.
    GREGORIAN_DAY = 'GregorianDay'  # A time datatype corresponding to W3C XML Schema's xs:date datatype, which is based on ISO-8601.
    REPORTING_TIME_PERIOD = 'ReportingTimePeriod'  # Reporting time periods represent periods of a standard length within a reporting year, where to start of the year (defined as a month and day) must be defined elsewhere or it is assumed to be January 1. This is the union of the reporting year, semester, trimester, quarter, month, week, and day.
    REPORTING_YEAR = 'ReportingYear'  # A reporting year represents a period of 1 year (P1Y) from the start date of the reporting year. This is expressed as using the SDMX specific ReportingYearType.
    REPORTING_SEMESTER = 'ReportingSemester'  # A reporting semester represents a period of 6 months (P6M) from the start date of the reporting year. This is expressed as using the SDMX specific ReportingSemesterType.
    REPORTING_TRIMESTER = 'ReportingTrimester'  # A reporting trimester represents a period of 4 months (P4M) from the start date of the reporting year. This is expressed as using the SDMX specific ReportingTrimesterType.
    REPORTING_QUARTER = 'ReportingQuarter'  # A reporting quarter represents a period of 3 months (P3M) from the start date of the reporting year. This is expressed as using the SDMX specific ReportingQuarterType.
    REPORTING_MONTH = 'ReportingMonth'  # A reporting month represents a period of 1 month (P1M) from the start date of the reporting year. This is expressed as using the SDMX specific ReportingMonthType.
    REPORTING_WEEK = 'ReportingWeek'  # A reporting week represents a period of 7 days (P7D) from the start date of the reporting year. This is expressed as using the SDMX specific ReportingWeekType.
    REPORTING_DAY = 'ReportingDay'  # A reporting day represents a period of 1 day (P1D) from the start date of the reporting year. This is expressed as using the SDMX specific ReportingDayType.
    DATE_TIME = 'DateTime'  # A time datatype corresponding to W3C XML Schema's xs:dateTime datatype.
    TIME_RANGE = 'TimeRange'  # TimeRange defines a time period by providing a distinct start (date or date time) and a duration.
    MONTH = 'Month'  # A time datatype corresponding to W3C XML Schema's xs:gMonth datatype.
    MONTH_DAY = 'MonthDay'  # A time datatype corresponding to W3C XML Schema's xs:gMonthDay datatype.
    DAY = 'Day'  # A time datatype corresponding to W3C XML Schema's xs:gDay datatype.
    TIME = 'Time'  # A time datatype corresponding to W3C XML Schema's xs:time datatype.
    DURATION = 'Duration'  # A time datatype corresponding to W3C XML Schema's xs:duration datatype.
    XHTML = 'XHTML'  # This value indicates that the content of the component can contain XHTML markup.
    KEY_VALUES = 'KeyValues'  # This value indicates that the content of the component will be data key (a set of dimension references and values for the dimensions).
    IDENTIFIABLE_REFERENCE = 'IdentifiableReference'  # This value indicates that the content of the component will be complete reference (either URN or full set of reference fields) to an Identifiable object in the SDMX Information Model.
    DATA_SET_REFERENCE = 'DataSetReference'  # This value indicates that the content of the component will be reference to a data provider, which is actually a formal reference to a data provider and a data set identifier value.
    ATTACHMENT_CONSTRAINT_REFERENCE = 'AttachmentConstraintReference'  # This value indicates that the content of the component will be reference to an attachment constraint, which is actually a combination of a collection of full or partial key values and a reference to a data set or data structure, usage, or provision agreement.


class DimensionEumerationSchemeTypeCodelistType(str, Enum):
    """DimensionEumerationSchemeTypeCodelistType provides an enumeration of all
    item schemes which are allowable as the representation of a data
    structure definition component."""
    CODELIST = 'Codelist'
    CONCEPT_SCHEME = 'ConceptScheme'


class DimensionTypeCodelistType(str, Enum):
    """DimensionTypeCodelistType provides an enumeration of all dimension
    objects."""
    DIMENSION = 'Dimension'
    MEASURE_DIMENSION = 'MeasureDimension'
    TIME_DIMENSION = 'TimeDimension'


class DimensionTypeType(str, Enum):
    """DimensionTypeType enumerates the sub-classes of a dimension."""
    DIMENSION = 'Dimension'  # An ordinary dimension.
    MEASURE_DIMENSION = 'MeasureDimension'  # A measure dimension.
    TIME_DIMENSION = 'TimeDimension'  # The time dimension.


class InputOutputTypeCodeType(str, Enum):
    """InputOutputTypeCodeType enumerates the role an object plays in a process
    step."""
    INPUT = 'Input'  # Input - referenced object is an input to the process step.
    OUTPUT = 'Output'  # Output - referenced object is an output to the process step.
    ANY = 'Any'  # Any - referenced object is either an input or an output to the process step.


class ItemSchemePackageTypeCodelistType(str, Enum):
    """ItemSchemePackageTypeCodelistType provides an enumeration of all SDMX
    packages which contain item schemes."""
    BASE = 'base'
    CODELIST = 'codelist'
    CATEGORYSCHEME = 'categoryscheme'
    CONCEPTSCHEME = 'conceptscheme'


class ItemSchemeTypeCodelistType(str, Enum):
    """ItemSchemeTypeCodelistType provides an enumeration of all item scheme
    objects."""
    AGENCY_SCHEME = 'AgencyScheme'
    CATEGORY_SCHEME = 'CategoryScheme'
    CODELIST = 'Codelist'
    CONCEPT_SCHEME = 'ConceptScheme'
    DATA_CONSUMER_SCHEME = 'DataConsumerScheme'
    DATA_PROVIDER_SCHEME = 'DataProviderScheme'
    ORGANISATION_UNIT_SCHEME = 'OrganisationUnitScheme'
    REPORTING_TAXONOMY = 'ReportingTaxonomy'


class ItemTypeCodelistType(str, Enum):
    """ItemTypeCodelistType provides an enumeration of all item objects."""
    AGENCY = 'Agency'
    CATEGORY = 'Category'
    CODE = 'Code'
    CONCEPT = 'Concept'
    DATA_CONSUMER = 'DataConsumer'
    DATA_PROVIDER = 'DataProvider'
    ORGANISATION_UNIT = 'OrganisationUnit'
    REPORTING_CATEGORY = 'ReportingCategory'


class LateBoundVersionType(str, Enum):
    """LateBoundVersionType is a single value code list, used to include the
    '*' character - indicating that the latest version of an object is
    required."""
    _ = '*'  # Indicates that the latest version of an object is requested.


class MaintainableReturnDetailType(str, Enum):
    """MaintainableReturnDetailType contains a sub set of the enumerations
    defined in the ReturnDetailType. Enumerations relating specifically to
    item schemes are not included"""
    STUB = 'Stub'
    COMPLETE_STUB = 'CompleteStub'
    FULL = 'Full'


class MaintainableTypeCodelistType(str, Enum):
    """MaintainableTypeCodelistType provides an enumeration of all maintainable
    objects."""
    ANY = 'Any'
    AGENCY_SCHEME = 'AgencyScheme'
    ATTACHMENT_CONSTRAINT = 'AttachmentConstraint'
    CATEGORISATION = 'Categorisation'
    CATEGORY_SCHEME = 'CategoryScheme'
    CODELIST = 'Codelist'
    CONCEPT_SCHEME = 'ConceptScheme'
    CONSTRAINT = 'Constraint'
    CONTENT_CONSTRAINT = 'ContentConstraint'
    DATAFLOW = 'Dataflow'
    DATA_CONSUMER_SCHEME = 'DataConsumerScheme'
    DATA_PROVIDER_SCHEME = 'DataProviderScheme'
    DATA_STRUCTURE = 'DataStructure'
    HIERARCHICAL_CODELIST = 'HierarchicalCodelist'
    METADATAFLOW = 'Metadataflow'
    METADATA_STRUCTURE = 'MetadataStructure'
    ORGANISATION_SCHEME = 'OrganisationScheme'
    ORGANISATION_UNIT_SCHEME = 'OrganisationUnitScheme'
    PROCESS = 'Process'
    PROVISION_AGREEMENT = 'ProvisionAgreement'
    REPORTING_TAXONOMY = 'ReportingTaxonomy'
    STRUCTURE_SET = 'StructureSet'


class MappedObjectTypeCodelistType(str, Enum):
    """MappedObjectTypeCodelistType is a restriction of the
    MaintainableTypeCodelistType which contains only the object types which
    can be mapped in a structure set."""
    AGENCY_SCHEME = 'AgencyScheme'
    CATEGORY_SCHEME = 'CategoryScheme'
    CODELIST = 'Codelist'
    CONCEPT_SCHEME = 'ConceptScheme'
    DATAFLOW = 'Dataflow'
    DATA_CONSUMER_SCHEME = 'DataConsumerScheme'
    DATA_PROVIDER_SCHEME = 'DataProviderScheme'
    DATA_STRUCTURE = 'DataStructure'
    HIERARCHICAL_CODELIST = 'HierarchicalCodelist'
    METADATAFLOW = 'Metadataflow'
    METADATA_STRUCTURE = 'MetadataStructure'
    ORGANISATION_UNIT_SCHEME = 'OrganisationUnitScheme'
    REPORTING_TAXONOMY = 'ReportingTaxonomy'


class MetadataStructureComponentTypeCodelistType(str, Enum):
    """MetadataStructureComponentTypeCodelistType provides an enumeration of
    all metadata structure component objects."""
    CONSTRAINT_TARGET = 'ConstraintTarget'
    DATA_SET_TARGET = 'DataSetTarget'
    IDENTIFIABLE_OBJECT_TARGET = 'IdentifiableObjectTarget'
    DIMENSION_DESCRIPTOR_VALUES_TARGET = 'DimensionDescriptorValuesTarget'
    METADATA_ATTRIBUTE = 'MetadataAttribute'
    REPORT_PERIOD_TARGET = 'ReportPeriodTarget'


class ObjectTypeCodelistType(str, Enum):
    """ObjectTypeCodelistType provides an enumeration of all objects outside of
    the base infomration model class. This includes some abstract object
    types such as Organsiation and Constraint."""
    ANY = 'Any'
    AGENCY = 'Agency'
    AGENCY_SCHEME = 'AgencyScheme'
    ATTACHMENT_CONSTRAINT = 'AttachmentConstraint'
    ATTRIBUTE = 'Attribute'
    ATTRIBUTE_DESCRIPTOR = 'AttributeDescriptor'
    CATEGORISATION = 'Categorisation'
    CATEGORY = 'Category'
    CATEGORY_SCHEME_MAP = 'CategorySchemeMap'
    CATEGORY_SCHEME = 'CategoryScheme'
    CODE = 'Code'
    CODE_MAP = 'CodeMap'
    CODELIST = 'Codelist'
    CODELIST_MAP = 'CodelistMap'
    COMPONENT_MAP = 'ComponentMap'
    CONCEPT = 'Concept'
    CONCEPT_MAP = 'ConceptMap'
    CONCEPT_SCHEME = 'ConceptScheme'
    CONCEPT_SCHEME_MAP = 'ConceptSchemeMap'
    CONSTRAINT = 'Constraint'
    CONSTRAINT_TARGET = 'ConstraintTarget'
    CONTENT_CONSTRAINT = 'ContentConstraint'
    DATAFLOW = 'Dataflow'
    DATA_CONSUMER = 'DataConsumer'
    DATA_CONSUMER_SCHEME = 'DataConsumerScheme'
    DATA_PROVIDER = 'DataProvider'
    DATA_PROVIDER_SCHEME = 'DataProviderScheme'
    DATA_SET_TARGET = 'DataSetTarget'
    DATA_STRUCTURE = 'DataStructure'
    DIMENSION = 'Dimension'
    DIMENSION_DESCRIPTOR = 'DimensionDescriptor'
    DIMENSION_DESCRIPTOR_VALUES_TARGET = 'DimensionDescriptorValuesTarget'
    GROUP_DIMENSION_DESCRIPTOR = 'GroupDimensionDescriptor'
    HIERARCHICAL_CODE = 'HierarchicalCode'
    HIERARCHICAL_CODELIST = 'HierarchicalCodelist'
    HIERARCHY = 'Hierarchy'
    HYBRID_CODELIST_MAP = 'HybridCodelistMap'
    HYBRID_CODE_MAP = 'HybridCodeMap'
    IDENTIFIABLE_OBJECT_TARGET = 'IdentifiableObjectTarget'
    LEVEL = 'Level'
    MEASURE_DESCRIPTOR = 'MeasureDescriptor'
    MEASURE_DIMENSION = 'MeasureDimension'
    METADATAFLOW = 'Metadataflow'
    METADATA_ATTRIBUTE = 'MetadataAttribute'
    METADATA_SET = 'MetadataSet'
    METADATA_STRUCTURE = 'MetadataStructure'
    METADATA_TARGET = 'MetadataTarget'
    ORGANISATION = 'Organisation'
    ORGANISATION_MAP = 'OrganisationMap'
    ORGANISATION_SCHEME = 'OrganisationScheme'
    ORGANISATION_SCHEME_MAP = 'OrganisationSchemeMap'
    ORGANISATION_UNIT = 'OrganisationUnit'
    ORGANISATION_UNIT_SCHEME = 'OrganisationUnitScheme'
    PRIMARY_MEASURE = 'PrimaryMeasure'
    PROCESS = 'Process'
    PROCESS_STEP = 'ProcessStep'
    PROVISION_AGREEMENT = 'ProvisionAgreement'
    REPORTING_CATEGORY = 'ReportingCategory'
    REPORTING_CATEGORY_MAP = 'ReportingCategoryMap'
    REPORTING_TAXONOMY = 'ReportingTaxonomy'
    REPORTING_TAXONOMY_MAP = 'ReportingTaxonomyMap'
    REPORTING_YEAR_START_DAY = 'ReportingYearStartDay'
    REPORT_PERIOD_TARGET = 'ReportPeriodTarget'
    REPORT_STRUCTURE = 'ReportStructure'
    STRUCTURE_MAP = 'StructureMap'
    STRUCTURE_SET = 'StructureSet'
    TIME_DIMENSION = 'TimeDimension'
    TRANSITION = 'Transition'


class ObsDimensionsCodeType(str, Enum):
    """ObsDimensionsCodeType is an enumeration containing the values
    "TimeDimension" and "AllDimensions" """
    ALL_DIMENSIONS = 'AllDimensions'  # AllDimensions notes that the cross sectional format shall be flat; that is all dimensions should be contained at the observation level.
    _time_period = 'TIME_PERIOD'  # TIME_PERIOD refers to the fixed identifier for the time dimension.


class ObservationActionCodeType(str, Enum):
    """ObservationActionCodeType enumerates the type of observations to be
    returned."""
    ACTIVE = 'Active'  # Active observations, regardless of when they were added or updated will be returned.
    ADDED = 'Added'  # Only newly added observations will be returned.
    UPDATED = 'Updated'  # Only updated observations will be returned.
    DELETED = 'Deleted'  # Only deleted observations will be returned.


class OrganisationSchemeTypeCodeType(str, Enum):
    """OrganisationSchemeTypeCodeType enumerates the possible types of
    organisation schemes that can be queried for."""
    ORGANISATION_SCHEME = 'OrganisationScheme'
    AGENCY_SCHEME = 'AgencyScheme'
    DATA_CONSUMER_SCHEME = 'DataConsumerScheme'
    DATA_PROVIDER_SCHEME = 'DataProviderScheme'
    ORGANISATION_UNIT_SCHEME = 'OrganisationUnitScheme'


class OrganisationSchemeTypeCodelistType(str, Enum):
    """OrganisationSchemeTypeCodelistType provides an enumeration of all
    organisation scheme objects."""
    AGENCY_SCHEME = 'AgencyScheme'
    DATA_CONSUMER_SCHEME = 'DataConsumerScheme'
    DATA_PROVIDER_SCHEME = 'DataProviderScheme'
    ORGANISATION_UNIT_SCHEME = 'OrganisationUnitScheme'


class OrganisationTypeCodelistType(str, Enum):
    """OrganisationTypeCodelistType provides an enumeration of all organisation
    objects."""
    AGENCY = 'Agency'
    DATA_CONSUMER = 'DataConsumer'
    DATA_PROVIDER = 'DataProvider'
    ORGANISATION_UNIT = 'OrganisationUnit'


class PackageTypeCodelistType(str, Enum):
    """PackageTypeCodelistType provides an enumeration of all SDMX package
    names."""
    BASE = 'base'
    DATASTRUCTURE = 'datastructure'
    METADATASTRUCTURE = 'metadatastructure'
    PROCESS = 'process'
    REGISTRY = 'registry'
    MAPPING = 'mapping'
    CODELIST = 'codelist'
    CATEGORYSCHEME = 'categoryscheme'
    CONCEPTSCHEME = 'conceptscheme'


class QueryTypeType(str, Enum):
    """QueryType provides an enumeration of values which specify the objects in
    the result-set for a registry query."""
    DATA_SETS = 'DataSets'  # Only references data sets should be returned.
    METADATA_SETS = 'MetadataSets'  # Only references to metadata sets should be returned.
    ALL_SETS = 'AllSets'  # References to both data sets and metadata sets should be returned.


class RangeOperatorType(str, Enum):
    """RangeOperatorType provides an enumeration of range operators to be
    applied to an ordered value."""
    GREATER_THAN_OR_EQUAL = 'greaterThanOrEqual'  # (>=) - value must be greater than or equal to the value supplied.
    LESS_THAN_OR_EQUAL = 'lessThanOrEqual'  # (<=) - value must be less than or equal to the value supplied.
    GREATER_THAN = 'greaterThan'  # (>) - value must be greater than the value supplied.
    LESS_THAN = 'lessThan'  # (<) - value must be less than the value supplied.


class SeverityCodeType(str, Enum):
    ERROR = 'Error'  # Error indicates the status message coresponds to an error.
    WARNING = 'Warning'  # Warning indicates that the status message corresponds to a warning.
    INFORMATION = 'Information'  # Information indicates that the status message corresponds to an informational message.


class SimpleCodeDataType(str, Enum):
    """SimpleCodeDataType restricts SimpleDataType to specify the allowable
    data types for a simple code. The possible values are simply Alpha,
    AlphaNumeric, or Numeric."""
    ALPHA = 'Alpha'
    ALPHA_NUMERIC = 'AlphaNumeric'
    NUMERIC = 'Numeric'


class SimpleDataType(str, Enum):
    """SimpleDataType restricts BasicComponentDataType to specify the allowable
    data types for a data structure definition component. The XHTML
    representation is removed as a possible type."""
    STRING = 'String'
    ALPHA = 'Alpha'
    ALPHA_NUMERIC = 'AlphaNumeric'
    NUMERIC = 'Numeric'
    BIG_INTEGER = 'BigInteger'
    INTEGER = 'Integer'
    LONG = 'Long'
    SHORT = 'Short'
    DECIMAL = 'Decimal'
    FLOAT = 'Float'
    DOUBLE = 'Double'
    BOOLEAN = 'Boolean'
    _uri = 'URI'
    COUNT = 'Count'
    INCLUSIVE_VALUE_RANGE = 'InclusiveValueRange'
    EXCLUSIVE_VALUE_RANGE = 'ExclusiveValueRange'
    INCREMENTAL = 'Incremental'
    OBSERVATIONAL_TIME_PERIOD = 'ObservationalTimePeriod'
    STANDARD_TIME_PERIOD = 'StandardTimePeriod'
    BASIC_TIME_PERIOD = 'BasicTimePeriod'
    GREGORIAN_TIME_PERIOD = 'GregorianTimePeriod'
    GREGORIAN_YEAR = 'GregorianYear'
    GREGORIAN_YEAR_MONTH = 'GregorianYearMonth'
    GREGORIAN_DAY = 'GregorianDay'
    REPORTING_TIME_PERIOD = 'ReportingTimePeriod'
    REPORTING_YEAR = 'ReportingYear'
    REPORTING_SEMESTER = 'ReportingSemester'
    REPORTING_TRIMESTER = 'ReportingTrimester'
    REPORTING_QUARTER = 'ReportingQuarter'
    REPORTING_MONTH = 'ReportingMonth'
    REPORTING_WEEK = 'ReportingWeek'
    REPORTING_DAY = 'ReportingDay'
    DATE_TIME = 'DateTime'
    TIME_RANGE = 'TimeRange'
    MONTH = 'Month'
    MONTH_DAY = 'MonthDay'
    DAY = 'Day'
    TIME = 'Time'
    DURATION = 'Duration'


class SimpleOperatorType(str, Enum):
    """SimpleOperatorType provides an enumeration of simple operators to be
    applied to any value."""
    NOT_EQUAL = 'notEqual'  # (!=) - value must not be equal to the value supplied.
    EQUAL = 'equal'  # (=) - value must be exactly equal to the value supplied.


class SourceTargetType(str, Enum):
    """SourceTargetType is an enumeration to indicate whether an object is the
    source, target, or either of the two options."""
    ANY = 'Any'
    SOURCE = 'Source'
    TARGET = 'Target'


class StatusType(str, Enum):
    """StatusType provides an enumeration of values that detail the status of
    queries or requests."""
    SUCCESS = 'Success'  # Query or request successful.
    WARNING = 'Warning'  # Query or request successful, but with warnings.
    FAILURE = 'Failure'  # Query or request not successful.


class StructureOrUsageTypeCodelistType(str, Enum):
    """StructureOrUsageTypeCodelistType provides an enumeration all structure
    and structure usage objects"""
    DATAFLOW = 'Dataflow'
    DATA_STRUCTURE = 'DataStructure'
    METADATAFLOW = 'Metadataflow'
    METADATA_STRUCTURE = 'MetadataStructure'


class StructurePackageTypeCodelistType(str, Enum):
    """StructurePackageTypeCodelistType provides an enumeration of all SDMX
    packages which contain structure and structure usages."""
    DATASTRUCTURE = 'datastructure'
    METADATASTRUCTURE = 'metadatastructure'


class StructureReturnDetailType(str, Enum):
    """StructureReturnDetailType contains a set of enumerations that indicate
    how much detail should be returned for an object."""
    STUB = 'Stub'  # Only the identification information and name should be returned.
    COMPLETE_STUB = 'CompleteStub'  # Identification information, name, description, and annotations should be returned.
    FULL = 'Full'  # The entire detail of the object should be returned.
    MATCHED_ITEMS = 'MatchedItems'  # For an item scheme, only the items matching the item where parameters will be returned. In the case that items are hierarchical, the entire hierarchy leading to the matched item will have to be returned.
    CASCADED_MATCHED_ITEMS = 'CascadedMatchedItems'  # For an item scheme, only the items matching the item where parameters, and their hierarchical child items will be returned. In the case that items are hierarchical, the entire hierarchy leading to the matched item will have to be returned.


class StructureTypeCodelistType(str, Enum):
    """StructureTypeCodelistType provides an enumeration all structure
    objects"""
    DATA_STRUCTURE = 'DataStructure'
    METADATA_STRUCTURE = 'MetadataStructure'


class StructureUsageTypeCodelistType(str, Enum):
    """StructureUsageTypeCodelistType provides an enumeration all structure
    usage objects"""
    DATAFLOW = 'Dataflow'
    METADATAFLOW = 'Metadataflow'


class TargetObjectDataType(str, Enum):
    """TargetObjectDataType restricts DataType to specify the allowable data
    types for representing a target object value."""
    KEY_VALUES = 'KeyValues'
    IDENTIFIABLE_REFERENCE = 'IdentifiableReference'
    DATA_SET_REFERENCE = 'DataSetReference'
    ATTACHMENT_CONSTRAINT_REFERENCE = 'AttachmentConstraintReference'


class TargetObjectTypeCodelistType(str, Enum):
    """TargetObjectTypeCodelistType provides an enumeration of all target
    object objects."""
    CONSTRAINT_TARGET = 'ConstraintTarget'
    DATA_SET_TARGET = 'DataSetTarget'
    IDENTIFIABLE_OBJECT_TARGET = 'IdentifiableObjectTarget'
    DIMENSION_DESCRIPTOR_VALUES_TARGET = 'DimensionDescriptorValuesTarget'
    REPORT_PERIOD_TARGET = 'ReportPeriodTarget'


class TextSearchOperatorType(str, Enum):
    """TextSearchOperatorType provides an enumeration of text search
    operators."""
    CONTAINS = 'contains'  # The text being searched must contain the supplied text.
    STARTS_WITH = 'startsWith'  # The text being searched must start with the supplied text.
    ENDS_WITH = 'endsWith'  # The text being searched must end with the supplied text.
    DOES_NOT_CONTAIN = 'doesNotContain'  # The text being searched cannot contain the supplied text.
    DOES_NOT_START_WITH = 'doesNotStartWith'  # The text being searched cannot start with the supplied text.
    DOES_NOT_END_WITH = 'doesNotEndWith'  # The text being searched cannot end with the supplied text.


class TimeDataType(str, Enum):
    """TimeDataType restricts SimpleDataType to specify the allowable data
    types for representing a time value."""
    OBSERVATIONAL_TIME_PERIOD = 'ObservationalTimePeriod'
    STANDARD_TIME_PERIOD = 'StandardTimePeriod'
    BASIC_TIME_PERIOD = 'BasicTimePeriod'
    GREGORIAN_TIME_PERIOD = 'GregorianTimePeriod'
    GREGORIAN_YEAR = 'GregorianYear'
    GREGORIAN_YEAR_MONTH = 'GregorianYearMonth'
    GREGORIAN_DAY = 'GregorianDay'
    REPORTING_TIME_PERIOD = 'ReportingTimePeriod'
    REPORTING_YEAR = 'ReportingYear'
    REPORTING_SEMESTER = 'ReportingSemester'
    REPORTING_TRIMESTER = 'ReportingTrimester'
    REPORTING_QUARTER = 'ReportingQuarter'
    REPORTING_MONTH = 'ReportingMonth'
    REPORTING_WEEK = 'ReportingWeek'
    REPORTING_DAY = 'ReportingDay'
    DATE_TIME = 'DateTime'
    TIME_RANGE = 'TimeRange'


class TimeOperatorType(str, Enum):
    """TimeOperatorType derives from the OrderedOperatorType to remove the
    notEqual operator."""
    EQUAL = 'equal'
    GREATER_THAN_OR_EQUAL = 'greaterThanOrEqual'
    LESS_THAN_OR_EQUAL = 'lessThanOrEqual'
    GREATER_THAN = 'greaterThan'
    LESS_THAN = 'lessThan'


class ToValueTypeType(str, Enum):
    """ToValueTypeType provides an enumeration of available text-equivalents
    for translation of coded values into textual formats."""
    VALUE = 'Value'  # Code or other tokenized value, as provided in the representation scheme.
    NAME = 'Name'  # The human-readable name of the Value, as provided in the representation scheme.
    DESCRIPTION = 'Description'  # The human-readable description of the Value, as provided in the representation scheme.


class UnboundedCodeType(str, Enum):
    """UnboundedCodeType provides single textual value of "unbounded", for use
    in OccurentType."""
    UNBOUNDED = 'unbounded'  # Object has no upper limit on occurrences.


class UsageStatusType(str, Enum):
    """UsageStatusType provides a list of enumerated types for indicating
    whether reporting a given attribute is mandatory or conditional."""
    MANDATORY = 'Mandatory'  # Reporting the associated attribute is mandatory - a value must be supplied.
    CONDITIONAL = 'Conditional'  # Reporting the associated attribute is not mandatory - a value may be supplied, but is not required.


class WildCardValueType(str, Enum):
    """WildCardValueType is a single value code list, used to include the '%'
    character - indicating that an entire field is wild carded."""
    _ = '%'  # Indicates a wild card value.


class DatasetType(IntEnum):
    GenericDataSet = 1
    StructureDataSet = 2
    GenericTimeSeriesDataSet = 3
    StructureTimeSeriesDataSet = 4
