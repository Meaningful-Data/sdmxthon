"""Data_Structure contains all parsers for the data in a Structure Specific
Message """

import re as re_

import pandas as pd
from lxml.etree import DocumentInvalid

from sdmxthon.model.base import AnnotableArtefact
from sdmxthon.parsers.data_parser import Validate_simpletypes_
from sdmxthon.parsers.gdscollector import datetime_
from sdmxthon.parsers.references import ReferenceType
from sdmxthon.utils.xml_base import cast, BaseStrType_, find_attr_value_, \
    encode_str_2_3


class ObsType(AnnotableArtefact):
    """ObsType is the abstract dim_type which defines the structure of a
    grouped or un-grouped observation. The observation must be provided a
    key, which is either a value for the dimension which is declared to be
    at the observation level if the observation is grouped, or a full set of
    values for all dimensions in the data structure definition if the
    observation is un-grouped. This key should disambiguate the observation
    within the context in which it is defined (e.g. there should not be
    another observation with the same dimension value in a series). The
    observation can contain an observed value and/or attribute values. Data
    structure definition schemas will drive a dim_type or types based on
    this that is specific to the data structure definition and the variation
    of the format being expressed in the schema. The dimension value(s)
    which make up the key and the attribute values associated with the key
    dimension(s) or the primary measure will be represented with XML
    attributes. This is specified in the content model with the declaration
    of anyAttributes in the "local" namespace. The derived observation
    dim_type will refine this structure so that the attributes are explicit.
    The XML attributes will be given a name based on the attribute's
    identifier. These XML attributes will be unqualified (meaning they do
    not have a namespace associated with them). The dimension XML attribute(
    s) will be required while the attribute XML attributes will be optional.
    To allow for generic processing, it is required that the only
    unqualified XML attributes in the derived observation dim_type be for
    the observation dimension(s) and attributes declared in the data
    structure definition. If additional attributes are required,
    these should be qualified with a namespace so that a generic application
    can easily distinguish them as not being meant to represent a data
    structure definition dimension or attribute. If the data structure
    definition specific schema requires that explicit measures be used (only
    possible when the measure dimension is specified at the observation),
    then there will be types derived for each measure defined by the measure
    dimension. In this case, the types will be specific to each measure,
    which is to say that the representation of the primary measure (i.e. the
    observed value) will be restricted to that which is specified by the
    specific measure. The dim_type attribute is used when the derived format
    requires that explicit measure be used. In this case, the derived
    dim_type based on the measure will fix this value to be the
    identification of the measure concept. This will not be required,
    but since it is fixed it will be available in the post validation
    information set which will allow for generic processing of the data. If
    explicit measures are not used, then the derived dim_type will prohibit
    the use of this attribute.The TIME_PERIOD attribute is an explicit
    attribute for the time dimension. This is declared in the base schema
    since it has a fixed identifier and representation. The derived series
    dim_type will either require or prohibit this attribute, depending on
    whether time is the observation dimension. If the time dimension
    specifies a more specific representation of time the derived dim_type
    will restrict the dim_type definition to the appropriate dim_type.The
    REPORTING_YEAR_START_DAY attribute is an explict attribute for the
    reporting year start day, which provides context to the time dimension
    when its value contains a reporting period (e.g. 2010-Q1). This
    attribute is used to state the month and day that the reporting year
    begins (e.g. --07-01 for July 1st). In the absence of an explicit value
    provided in this attribute, all reporting period values will be assumed
    to be based on a reporting year start day of January 1. This is declared
    in the base schema since it has a fixed identifier and representation.
    The derived observation dim_type may either require or prohibit this
    attribute, depending on whether the data structure declared the
    reporting year start day attribute and if so, the attribute relationship
    and assignment status assigned to it.The OBS_VALUE attribute is an
    explicit attribute for the primary measure, which is intended to hold
    the value for the observation. This is declared in the base schema since
    it has a fixed identifier. This attribute is un-typed, since the
    representation of the observed value can vary widely. """

    def __init__(self, Annotations=None, type_=None, TIME_PERIOD=None,
                 REPORTING_YEAR_START_DAY=None, OBS_VALUE=None,
                 gds_collector_=None, **kwargs_):
        super(ObsType, self).__init__(Annotations, gds_collector_)
        self._type_ = cast(None, type_)
        self._time_period = cast(None, TIME_PERIOD)
        self._reporting_year_start_day = cast(None, REPORTING_YEAR_START_DAY)
        self._obs_value = cast(None, OBS_VALUE)
        self._anyAttributes_ = {}

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of ObsType"""
        return ObsType(*args_, **kwargs_)

    @property
    def type(self):
        """Derived types will restrict this to be a dim_type based on
    the representation of the primary measure. In the case that an explicit
    measure is used, the derived dim_type for a given measure might further
    restrict the dim_type of the primary measure to be more specific to the
    core representation for the measure concept. Note that it is required
    that in the case of multiple measures being used, that the
    representation of the primary measure is broad enough to handle the
    various representations of the measure concepts."""
        return self._type_

    @type.setter
    def type(self, value):
        self._type_ = value

    @property
    def any_attributes(self):
        """Any Attributes contains the attributes at a Dataset Level"""

        return self._anyAttributes_

    @any_attributes.setter
    def any_attributes(self, value):
        self._anyAttributes_ = value

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""

        self._anyAttributes_ = {}
        value = find_attr_value_('dim_type', node)
        if value is not None and 'dim_type' not in already_processed:
            already_processed.add('dim_type')
            self._type_ = value
            self._validate_id_type(self._type_)  # validate dim_type IDType

        for name, value in attrs.items():
            if name not in already_processed:
                self._anyAttributes_[name] = value

        super(ObsType, self)._build_attributes(node, attrs, already_processed)


class GroupType(AnnotableArtefact):
    """GroupType is the abstract dim_type which defines a structure which is
    used to communicate attribute values for a group defined in a data
    structure definition. The group can consist of either a subset of the
    dimensions defined by the data structure definition, or an association
    to an attachment constraint, which in turn defines key sets to which
    attributes can be attached. In the case that the group is based on an
    attachment constraint, only the identification of group is provided. It
    is expected that a system which is processing this will relate that
    identifier to the key sets defined in the constraint and apply the
    values provided for the attributes appropriately. Data structure
    definition schemas will drive types based on this for each group defined
    in the data structure definition. Both the dimension values which make
    up the key (if applicable) and the attribute values associated with the
    group will be represented with XML attributes. This is specified in the
    content model with the declaration of anyAttributes in the "local"
    namespace. The derived group dim_type will refine this structure so that
    the attributes are explicit. The XML attributes will be given a name
    based on the attribute's identifier. These XML attributes will be
    unqualified (meaning they do not have a namespace associated with them).
    The dimension XML attributes will be required while the attribute XML
    attributes will be optional. To allow for generic processing,
    it is required that the only unqualified XML attributes in the derived
    group dim_type be for the group dimensions and attributes declared in
    the data structure definition. If additional attributes are required,
    these should be qualified with a namespace so that a generic application
    can easily distinguish them as not being meant to represent a data
    structure definition dimension or attribute.
    """

    def __init__(self, Annotations=None, type_=None,
                 REPORTING_YEAR_START_DAY=None, gds_collector_=None,
                 **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        super(GroupType, self).__init__(Annotations, **kwargs_)
        self._type_ = cast(None, type_)
        self._reporting_year_start_day = cast(None, REPORTING_YEAR_START_DAY)
        self._anyAttributes_ = {}

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of GroupType"""
        return GroupType(*args_, **kwargs_)

    @property
    def type(self):
        """The dim_type attribute reference the identifier of the group as
        defined in the data structure definition. This is optional,
        but derived group types will provide a fixed value for this so that
        it always available in the post validation information set. This
        allows the group to be processed in a generic manner """
        return self._type_

    @type.setter
    def type(self, value):
        self._type_ = value

    @property
    def reporting_year_start_day(self):
        """The REPORTING_YEAR_START_DAY attribute is an
    explict attribute for the reporting year start day, which provides
    context to the time dimension when its value contains a reporting
    period (e.g. 2010-Q1). This attribute is used to state the month and
    day that the reporting year begins (e.g. --07-01 for July 1st). In the
    absence of an explicit value provided in this attribute, all reporting
    period values will be assumed to be based on a reporting year start day
    of January 1. This is declared in the base schema since it has a fixed
    identifier and representation. The derived group types may either
    require or prohibit this attribute, depending on whether the data
    structure declared the reporting year start day attribute and if so,
    the attribute relationship and assignment status assigned to it."""
        return self._reporting_year_start_day

    @reporting_year_start_day.setter
    def reporting_year_start_day(self, value):
        self._reporting_year_start_day = value

    @property
    def any_attributes(self):
        """Any Attributes contains the attributes at a Group Level"""
        return self._anyAttributes_

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        value = find_attr_value_('dim_type', node)

        if value is not None and 'dim_type' not in already_processed:
            already_processed.add('dim_type')
            self._type_ = value
            self._validate_id_type(self._type_)  # validate dim_type IDType

        value = find_attr_value_('REPORTING_YEAR_START_DAY', node)

        if (value is not None and
                'REPORTING_YEAR_START_DAY' not in already_processed):
            already_processed.add('REPORTING_YEAR_START_DAY')
            self._reporting_year_start_day = value

        self._anyAttributes_ = {}

        for name, value in attrs.items():
            if name not in already_processed:
                self._anyAttributes_[name] = value
        super(GroupType, self)._build_attributes(node, attrs,
                                                 already_processed)


class SeriesType(AnnotableArtefact):
    """SeriesType is the abstract dim_type which defines a structure which
    is used to group a collection of observations which have a key in
    common. The key for a series is every dimension defined in the data
    structure definition, save the dimension declared to be at the
    observation level for this data set. In addition to observations,
    values can be provided for attributes which are associated with the
    dimensions which make up this series key (so long as the attributes do
    not specify a group attachment or also have an relationship with the
    observation dimension). It is possible for the series to contain only
    observations or only attribute values, or both. Data structure
    definition schemas will drive a dim_type based on this that is specific
    to the data structure definition and the variation of the format being
    expressed in the schema. Both the dimension values which make up the key
    and the attribute values associated with the key dimensions will be
    represented with XML attributes. This is specified in the content model
    with the declaration of anyAttributes in the "local" namespace. The
    derived series dim_type will refine this structure so that the
    attributes are explicit. The XML attributes will be given a name based
    on the attribute's identifier. These XML attributes will be unqualified
    (meaning they do not have a namespace associated with them). The
    dimension XML attributes will be required while the attribute XML
    attributes will be optional. To allow for generic processing,
    it is required that the only unqualified XML attributes in the derived
    group dim_type be for the series dimensions and attributes declared in
    the data structure definition. If additional attributes are required,
    these should be qualified with a namespace so that a generic application
    can easily distinguish them as not being meant to represent a data
    structure definition dimension or attribute. The TIME_PERIOD attribute
    is an explict attribute for the time dimension. This is declared in the
    base schema since it has a fixed identifier and representation. The
    derived series dim_type will either require or prohibit this attribute,
    depending on whether time is the observation dimension. If the time
    dimension specifies a more specific representation of time the derived
    dim_type will restrict the dim_type definition to the appropriate
    dim_type.The REPORTING_YEAR_START_DAY attribute is an explict attribute
    for the reporting year start day, which provides context to the time
    dimension when its value contains a reporting period (e.g. 2010-Q1).
    This attribute is used to state the month and day that the reporting
    year begins (e.g. --07-01 for July 1st). In the absence of an explicit
    value provided in this attribute, all reporting period values will be
    assumed to be based on a reporting year start day of January 1. This is
    declared in the base schema since it has a fixed identifier and
    representation. The derived series dim_type may either require or
    prohibit this attribute, depending on whether the data structure
    declared the reporting year start day attribute and if so, the attribute
    relationship and assignment status assigned to it. """

    def __init__(self, Annotations=None, TIME_PERIOD=None,
                 REPORTING_YEAR_START_DAY=None, Obs=None,
                 gds_collector_=None):

        super(SeriesType, self).__init__(Annotations, gds_collector_)
        self._time_period = TIME_PERIOD
        self._reporting_year_start_day = REPORTING_YEAR_START_DAY

        if Obs is None:
            self._obs = []
        else:
            self._obs = Obs

        self._obs_nsprefix_ = None
        self._anyAttributes_ = {}

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of SeriesType"""
        return SeriesType(*args_, **kwargs_)

    @property
    def obs(self):
        """Observations in a Series"""
        return self._obs

    @obs.setter
    def obs(self, value):
        if value is None:
            self._obs = []
        elif isinstance(value, list):
            self._obs = value
        else:
            raise TypeError('Obs must be a list')

    @property
    def any_attributes(self):
        """Any Attributes contains the attributes at a Series Level"""
        return self._anyAttributes_

    @any_attributes.setter
    def any_attributes(self, value):
        self._anyAttributes_ = value

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        self._anyAttributes_ = dict(attrs)

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False,
                        gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'Obs':
            any_attributes = dict(child_.attrib)
            if 'dim_type' in any_attributes.keys():
                del any_attributes['dim_type']
            self._anyAttributes_.update(any_attributes)
            self.obs.append(self._anyAttributes_.copy())
        elif nodeName_ == 'Annotations':
            super(SeriesType, self)._build_children(child_, node, nodeName_,
                                                    True)
        else:
            raise DocumentInvalid(
                f"Element {nodeName_} not expected, line {node.sourceline}")


class DataSetType(AnnotableArtefact):
    """DataSetType is the abstract dim_type which defines the base structure
    for any data structure definition specific data set. A derived data set
    dim_type will be created that is specific to a data structure definition
    and the details of the organisation of the data (i.e. which dimension is
    the observation dimension and whether explicit measures should be used).
    Data is organised into either a collection of series (grouped
    observations) or a collection of un-grouped observations. The derived
    data set dim_type will restrict this choice to be either grouped or un-
    grouped observations. If this dimension is "AllDimensions" then the
    derived data set dim_type must consist of a collection of un-grouped
    observations; otherwise the data set will contain a collection of series
    with the observations in the series disambiguated by the specified
    dimension at the observation level. This data set is capable of
    containing data (observed values) and/or documentation (attribute
    values) and can be used for incremental updates and deletions (i.e. only
    the relevant updates or deletes are exchanged). It is assumed that each
    series or un-grouped observation will be distinct in its purpose. For
    example, if series contains both data and documentation, it assumed that
    each series will have a unique key. If the series contains only data or
    only documentation, then it is possible that another series with the
    same key might exist, but with not with the same purpose (i.e. to
    provide data or documentation) as the first series. This base dim_type
    is designed such that derived types can be processed in a generic
    manner; it assures that data structure definition specific data will
    have a consistent structure. The group, series, and observation elements
    are unqualified, meaning that they are not qualified with a namespace in
    an instance. This means that in the derived data set types, the elements
    will always be the same, regardless of the target namespace of the
    schemas which defines these derived types. This allows for consistent
    processing of the structure without regard to what the namespace might
    be for the data structure definition specific schema. The data set can
    contain values for attributes which do not have an attribute
    relationship with any data structure definition components. These
    attribute values will exist in XML attributes in this element based on
    this dim_type (DataSet). This is specified in the content model with the
    declaration of anyAttributes in the "local" namespace. The derived data
    set dim_type will refine this structure so that the attributes are
    explicit. The XML attributes will be given a name based on the
    attribute's identifier. These XML attributes will be unqualified (
    meaning they do not have a namespace associated with them). To allow for
    generic processing, it is required that the only unqualified XML
    attributes in the derived data set dim_type (outside of the standard
    data set attributes) be for attributes declared in the data structure
    definition. If additional attributes are required, these should be
    qualified with a namespace so that a generic application can easily
    distinguish them as not being meant to represent a data structure
    definition attribute. The derived data set dim_type may either require
    or prohibit this attribute, depending on whether the data structure
    declared the reporting year start day attribute and if so, the attribute
    relationship and assignment status assigned to it. """

    def __init__(self, Annotations=None, REPORTING_YEAR_START_DAY=None,
                 structureRef=None, setID=None, action=None,
                 reportingBeginDate=None, reportingEndDate=None,
                 validFromDate=None, validToDate=None,
                 publicationYear=None, publicationPeriod=None,
                 DataProvider=None, Group=None, Data=None,
                 gds_collector_=None, **kwargs_):
        super(DataSetType, self).__init__(Annotations, gds_collector_)
        self._reporting_year_start_day = cast(None, REPORTING_YEAR_START_DAY)
        self._structureRef = structureRef
        self._setID = setID
        self._action = action
        self._reportingBeginDate = reportingBeginDate
        self._reportingEndDate = reportingEndDate

        if isinstance(validFromDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(validFromDate,
                                                     '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = validFromDate

        self._validFromDate = initvalue_

        if isinstance(validToDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(validToDate,
                                                     '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = validToDate

        self._validToDate = initvalue_
        self._publicationYear = cast(None, publicationYear)
        self._publicationPeriod = cast(None, publicationPeriod)
        self._dataProvider = DataProvider
        self._dataScope = None

        if Group is None:
            self._group = []
        else:
            self._group = Group

        if Data is None:
            self._data = []
        else:
            self._data = Data

        self._anyAttributes_ = {}

        self._dataframe = None

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of DataSetType"""
        return DataSetType(*args_, **kwargs_)

    @property
    def dataProvider(self):
        """DataProvider contains a reference to the provider for the data
        set. """
        return self._dataProvider

    @dataProvider.setter
    def dataProvider(self, value):
        self._dataProvider = value

    @property
    def group(self):
        """Group contains a references to a defined group in the data
        structure definition along with its key (if necessary) and values
        for the attributes which are associated with the group. """
        return self._group

    @group.setter
    def group(self, value):
        if value is None:
            self._group = []
        elif isinstance(value, list):
            self._group = value
        else:
            raise TypeError('Group must be a list')

    @property
    def data(self):
        """Data refers to the series or observations included in the Dataset"""
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    @property
    def dataframe(self):
        return self._dataframe

    @property
    def reporting_year_start_day(self):
        """ The REPORTING_YEAR_START_DAY attribute is an explict attribute
        for the reporting year start day, which provides context to the time
        dimension when its value contains a reporting period (e.g. 2010-Q1).
        This attribute is used to state the month and day that the reporting
        year begins (e.g. --07-01 for July 1st). In the absence of an
        explicit value provided in this attribute, all reporting period
        values will be assumed to be based on a reporting year start day of
        January 1. This is declared in the base schema since it has a fixed
        identifier and representation. """
        return self._reporting_year_start_day

    @reporting_year_start_day.setter
    def reporting_year_start_day(self, value):
        self._reporting_year_start_day = value

    @property
    def structureRef(self):
        """StructureRef is the reference to the structure located in the
        Header """
        return self._structureRef

    @structureRef.setter
    def structureRef(self, value):
        self._structureRef = value

    @property
    def setID(self):
        """The setID provides an identification of the data or metadata set"""
        return self._setID

    @setID.setter
    def setID(self, value):
        self._setID = value

    @property
    def action(self):
        """The action attribute indicates whether the file is appending,
        replacing, or deleting. """
        return self._action

    @action.setter
    def action(self, value):
        self._action = value

    @property
    def reporting_begin_date(self):
        """The reporting_begin_date indicates the inclusive start time
        of the data reported in the data or metadata set."""
        return self._reportingBeginDate

    @reporting_begin_date.setter
    def reporting_begin_date(self, value):
        self._reportingBeginDate = value

    @property
    def reporting_end_date(self):
        """The reporting_end_date indicates the inclusive end time
        of the data reported in the data or metadata set."""
        return self._reportingEndDate

    @reporting_end_date.setter
    def reporting_end_date(self, value):
        self._reportingEndDate = value

    @property
    def valid_from_date(self):
        """The validFromDate indicates the inclusive start time indicating
        the validity of the information in the data or metadata set. """
        return self._validFromDate

    @valid_from_date.setter
    def valid_from_date(self, value):
        self._validFromDate = value

    @property
    def valid_to_date(self):
        """The validToDate indicates the inclusive end time indicating the
        validity of the information in the data or metadata set. """
        return self._validToDate

    @valid_to_date.setter
    def valid_to_date(self, value):
        self._validToDate = value

    @property
    def publication_year(self):
        """The publicationYear holds the ISO 8601 four-digit year."""
        return self._publicationYear

    @publication_year.setter
    def publication_year(self, value):
        self._publicationYear = value

    @property
    def publication_period(self):
        """The publicationPeriod specifies the period of publication of the
        data or metadata in terms of whatever provisioning agreements might
        be in force (i.e., "Q1 2005" if that is the time of publication for
        a data set published on a quarterly basis). """
        return self._publicationPeriod

    @publication_period.setter
    def publication_period(self, value):
        self._publicationPeriod = value

    @property
    def dataScope(self):
        return self._dataScope

    @property
    def any_attributes(self):
        """Any Attributes contains the attributes at a Dataset Level"""
        return self._anyAttributes_

    @any_attributes.setter
    def any_attributes(self, value):
        self._anyAttributes_ = value

    def _validate_action_type(self, value):
        """Validate dim_type common:ActionType, a restriction on xs:NMTOKEN."""
        result = True

        if (value is not None and Validate_simpletypes_ and
                self.gds_collector_ is not None):
            if not isinstance(value, str):
                lineno = self._gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{value}": {lineno} is not of the '
                    f'correct base simple dim_type (str)')
                return False

            value = value
            enumerations = ['Append', 'Replace', 'Delete', 'Information']

            if value not in enumerations:
                lineno = self._gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{encode_str_2_3(value)}": {lineno} does not match'
                    f' xsd enumeration restriction on ActionType')
                result = False
        return result

    def _validate_BasicTimePeriodType(self, value):
        """Validate dim_type common:BasicTimePeriodType, a restriction on
        None. """
        pass

    def _validate_ObservationalTimePeriodType(self, value):
        """Validate dim_type common:ObservationalTimePeriodType,
        a restriction on None. """
        pass

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        self._anyAttributes_ = {}
        tag_pattern_ = re_.compile(r'({.*})?(.*)')

        for name, value in attrs.items():
            real_name = tag_pattern_.match(name).groups()[-1]
            if real_name not in already_processed:
                if real_name == "dim_type":
                    real_name = "xsi:dim_type"
                self._anyAttributes_[real_name] = value

        value = find_attr_value_('REPORTING_YEAR_START_DAY',
                                 self._anyAttributes_)

        if (value is not None and 'REPORTING_YEAR_START_DAY'
                not in already_processed):
            already_processed.add('REPORTING_YEAR_START_DAY')
            self.reporting_year_start_day = value

        value = find_attr_value_('structureRef', self._anyAttributes_)

        if value is not None and 'structureRef' not in already_processed:
            already_processed.add('structureRef')
            self.structureRef = value

        value = find_attr_value_('setID', self._anyAttributes_)

        if value is not None and 'setID' not in already_processed:
            already_processed.add('setID')
            self.setID = value
            self._validate_id_type(self._setID)  # validate dim_type IDType

        value = find_attr_value_('action', self._anyAttributes_)

        if value is not None and 'action' not in already_processed:
            already_processed.add('action')
            self.action = value
            self._validate_action_type(
                self._action)  # validate dim_type ActionType

        value = find_attr_value_('reportingBeginDate', self._anyAttributes_)

        if value is not None and 'reportingBeginDate' not in already_processed:
            already_processed.add('reportingBeginDate')
            self.reporting_begin_date = value
            self._validate_BasicTimePeriodType(
                self._reportingBeginDate)

        value = find_attr_value_('reportingEndDate', self._anyAttributes_)

        if value is not None and 'reportingEndDate' not in already_processed:
            already_processed.add('reportingEndDate')
            self.reporting_end_date = value
            self._validate_BasicTimePeriodType(
                self._reportingEndDate)

        value = find_attr_value_('validFromDate', self._anyAttributes_)

        if value is not None and 'validFromDate' not in already_processed:
            already_processed.add('validFromDate')
            try:
                self.valid_from_date = self._gds_parse_datetime(value)
            except ValueError as exp:
                raise ValueError(
                    'Bad date-time attribute (validFromDate): %s' % exp)

        value = find_attr_value_('validToDate', self._anyAttributes_)

        if value is not None and 'validToDate' not in already_processed:
            already_processed.add('validToDate')
            try:
                self.valid_to_date = self._gds_parse_datetime(value)
            except ValueError as exp:
                raise ValueError(
                    'Bad date-time attribute (validToDate): %s' % exp)

        value = find_attr_value_('publicationYear', self._anyAttributes_)

        if value is not None and 'publicationYear' not in already_processed:
            already_processed.add('publicationYear')
            self.publication_year = value

        value = find_attr_value_('publicationPeriod', self._anyAttributes_)

        if value is not None and 'publicationPeriod' not in already_processed:
            already_processed.add('publicationPeriod')
            self.publication_period = value
            self._validate_ObservationalTimePeriodType(self._publicationPeriod)

        value = find_attr_value_('dataScope', self._anyAttributes_)

        if value is not None and 'dataScope' not in already_processed:
            already_processed.add('dataScope')
            self._dataScope = value

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False,
                        gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'DataProvider':
            obj_ = ReferenceType._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._dataProvider = obj_
        elif nodeName_ == 'Group':
            obj_ = GroupType._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._group.append(obj_)
        elif nodeName_ == 'Series':
            obj_ = SeriesType._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self.data += obj_.obs
        elif nodeName_ == 'Obs':
            any_attributes = dict(child_.attrib)
            if 'dim_type' in any_attributes.keys():
                del any_attributes['dim_type']
            self.data.append(any_attributes)
        elif nodeName_ == 'Annotations':
            super(DataSetType, self)._build_children(child_, node,
                                                     nodeName_, True)
        else:
            raise DocumentInvalid(
                f"Element {nodeName_} not expected, line {node.sourceline}")

        if len(self.data) >= 50000:
            if self.dataframe is not None:
                self._dataframe = pd.concat([self._dataframe,
                                             pd.DataFrame(self.data)],
                                            ignore_index=True)
            else:
                self._dataframe = pd.DataFrame(self.data)
            self.data = []
