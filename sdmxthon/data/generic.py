from ..common.references import DataProviderReferenceType
from ..model.base import AnnotableArtefact
from ..utils.data_parser import DataParser
from ..utils.data_parser import Validate_simpletypes_
from ..utils.generateds import datetime_
from ..utils.xml_base import cast, BaseStrType_, find_attr_value_, encode_str_2_3


class BaseValueType(DataParser):
    """BaseValueType is a general structure which contains a reference to a
    data structure definition component and a value for that component. In
    this structure the reference to the component is optional to allow for
    usages where the actual reference might be provided in another
    context.The id_ attribute contains the identifier for the component for
    which a value is being provided.The value attribute contains the
    provided component value."""
    __hash__ = DataParser.__hash__
    subclass = None
    superclass = None

    def __init__(self, idx=None, value=None, gds_collector_=None, **kwargs_):
        super(BaseValueType, self).__init__(gds_collector_, **kwargs_)
        self.gds_collector_ = gds_collector_
        self.gds_element_tree_node_ = None
        self.original_tag_name_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self._id = idx
        self._id_nsprefix_ = None
        self._value = value
        self._value_nsprefix_ = None
        self._namespace_def = 'xmlns:generic="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic"'
        self._namespace_prefix = 'data'
        self._name = 'BaseValueType'

    @staticmethod
    def factory(*args_, **kwargs_):
        return BaseValueType(*args_, **kwargs_)

    @property
    def id_(self):
        return self._id

    @id_.setter
    def id_(self, value):
        self._id = value

    @property
    def value_(self):
        return self._value

    @value_.setter
    def value_(self, value):
        self._value = value

    def build_attributes(self, node, attrs, already_processed):
        value = find_attr_value_('id', node)
        if value is not None and 'id' not in already_processed:
            already_processed.add('id')
            self._id = value
            self.validate_NC_name_id_type(self._id)  # validate dim_type NCNameIDType

        value = find_attr_value_('value', node)
        if value is not None and 'value' not in already_processed:
            already_processed.add('value')
            self._value = value


# end class BaseValueType

class ObsValueType(BaseValueType):
    """ObsValueType is a derivation of the BaseValueType which is used to
    provide an observation value. Since an observation value is always
    associated with the data structure definition primary measure, and the
    identifier for the primary measure is fixed, the component reference
    for this structure is fixed. Note that this means that it is not
    necessary to provide a value in an instance as the fixed value will be
    provided in the post validation information set.The id_ attribute
    contains a fixed reference to the primary measure component of the data
    structure definition."""
    __hash__ = BaseValueType.__hash__
    subclass = None
    superclass = BaseValueType

    def __init__(self, idx=None, value=None, **kwargs_):
        super(ObsValueType, self).__init__(idx, value, **kwargs_)
        self._name = 'ObsValueType'

    @staticmethod
    def factory(*args_, **kwargs_):
        return ObsValueType(*args_, **kwargs_)

    def build_attributes(self, node, attrs, already_processed):
        value = find_attr_value_('id', node)
        if value is not None and 'id' not in already_processed:
            already_processed.add('id')
            self._id = value
            self.validate_NC_name_id_type(self._id)  # validate dim_type NCNameIDType

        value = find_attr_value_('value', node)
        if value is not None and 'value' not in already_processed:
            already_processed.add('value')
            self._value = value


# end class ObsValueType

class ComponentValueType(BaseValueType):
    """ComponentValueType is a derivation of the BaseValueType which requires
    that the component reference be provided. This is used when the
    identification of the component cannot be inferred from another
    context."""
    __hash__ = BaseValueType.__hash__
    subclass = None
    superclass = BaseValueType

    def __init__(self, id_=None, value=None, gds_collector_=None, **kwargs_):
        super(ComponentValueType, self).__init__(id_, value, gds_collector_, **kwargs_)
        self._name = 'ComponentValueType'
        self._namespace_prefix = 'generic'

    @staticmethod
    def factory(*args_, **kwargs_):
        return ComponentValueType(*args_, **kwargs_)

    def has_content_(self):
        if (
                super(ComponentValueType, self).has_content_()
        ):
            return True
        else:
            return False

    def build_attributes(self, node, attrs, already_processed):
        value = find_attr_value_('id', node)
        if value is not None and 'id' not in already_processed:
            already_processed.add('id')
            self._id = value
            self.validate_NC_name_id_type(self._id)  # validate dim_type NCNameIDType
        value = find_attr_value_('value', node)
        if value is not None and 'value' not in already_processed:
            already_processed.add('value')
            self._value = value
        super(ComponentValueType, self).build_attributes(node, attrs, already_processed)


class ValuesType(DataParser):
    """ValuesType is a general structure which contains a collection of data
    structure definition component values. This dim_type is used to provide
    both key and attribute collection values."""
    __hash__ = DataParser.__hash__
    subclass = None
    superclass = None

    def __init__(self, Value=None, gds_collector_=None, **kwargs_):
        super(ValuesType, self).__init__(gds_collector_, **kwargs_)
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self._namespace_prefix = 'generic'
        self.parent_object_ = kwargs_.get('parent_object_')

        if Value is None:
            self._value = {}
        elif isinstance(Value, dict):
            self._value = Value
        else:
            raise TypeError('Value must be a dict')

        self._value_nsprefix_ = None
        self._namespacedef = 'xmlns:generic="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic"'
        self._namespaceprefix = 'generic'
        self._namespace_prefix = 'generic'
        self._name = 'ValuesType'

    @staticmethod
    def factory(*args_, **kwargs_):
        return ValuesType(*args_, **kwargs_)

    @property
    def value_(self):
        return self._value

    @value_.setter
    def value_(self, value):
        if value is None:
            self._value = {}
        elif isinstance(value, list):
            self._value = value
        else:
            raise TypeError('Value must be a dict')

    def has_content_(self):
        if self._value is not None:
            return True
        else:
            return False

    def export_attributes_as_dict(self, parent_dict: dict, data: list, valid_fields: list):
        for Value_ in self._value:
            Value_.export_attributes_as_dict(parent_dict, )

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Value':
            obj_ = ComponentValueType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._value[obj_.id_] = obj_.value_
            obj_.original_tag_name_ = 'Value'


# end class ValuesType

class GroupType(AnnotableArtefact):
    """GroupType defines a structure which is used to communicate attribute
    values for a group defined in a data structure definition. The group
    can consist of either a subset of the dimensions defined by the data
    structure definition, or an association to an attachment constraint,
    which in turn defines key sets to which attributes can be attached. In
    the case that the group is based on an attachment constraint, only the
    identification of group is provided. It is expected that a system which
    is processing this will relate that identifier to the key sets defined
    in the constraint and apply the values provided for the attributes
    appropriately.The dim_type attribute holds the identifier assigned to the
    group in the data structure definition for which attribute values are
    being provided."""

    def __init__(self, Annotations=None, type_=None, GroupKey=None, Attributes=None, gds_collector_=None):
        super(GroupType, self).__init__(Annotations, gds_collector_)
        self._type_ = cast(None, type_)
        self._type__nsprefix_ = None
        self._group_key = GroupKey
        self._groupKey_nsprefix_ = None
        self._attributes = Attributes
        self._attributes_nsprefix_ = None
        self._namespacedef = 'xmlns:data="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic"'
        self._namespaceprefix = 'data'
        self._name = 'GroupType',

    @staticmethod
    def factory(*args_, **kwargs_):
        return GroupType(*args_, **kwargs_)

    @property
    def group_key(self):
        return self._group_key

    @group_key.setter
    def group_key(self, value):
        self._group_key = value

    @property
    def attributes(self):
        return self._attributes

    @attributes.setter
    def attributes(self, value):
        self._attributes = value

    @property
    def type(self):
        return self._type_

    @type.setter
    def type(self, value):
        self._type_ = value

    def has_content_(self):
        if (
                self._group_key is not None or
                self._attributes is not None or
                super(GroupType, self).has_content_()
        ):
            return True
        else:
            return False

    def build_attributes(self, node, attrs, already_processed):
        value = find_attr_value_('dim_type', node)
        if value is not None and 'dim_type' not in already_processed:
            already_processed.add('dim_type')
            self._type_ = value
            self.validate_id_type(self._type_)  # validate dim_type IDType
        super(GroupType, self).build_attributes(node, attrs, already_processed)

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'GroupKey':
            obj_ = ValuesType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._group_key = obj_
            obj_.original_tagname_ = 'GroupKey'
        elif nodeName_ == 'Attributes':
            obj_ = ValuesType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._attributes = obj_
            obj_.original_tagname_ = 'Attributes'
        super(GroupType, self).build_children(child_, node, nodeName_, True)


# end class GroupType


class SeriesType(AnnotableArtefact):
    """SeriesType defines a structure which is used to group a collection of
    observations which have a key in common. The key for a series is every
    dimension defined in the data structure definition, save the dimension
    declared to be at the observation level for this data set. In addition
    to observations, values can be provided for attributes which are
    associated with the dimensions which make up this series key (so long
    as the attributes do not specify a group attachment or also have an
    relationship with the observation dimension). It is possible for the
    series to contain only observations or only attribute values, or
    both."""

    def __init__(self, Annotations=None, SeriesKey=None, Attributes=None, Obs=None, gds_collector_=None, **kwargs_):
        super(SeriesType, self).__init__(Annotations, gds_collector_)
        self._seriesKey = SeriesKey
        self._attributes = Attributes
        if Obs is None:
            self._obs = []
        else:
            self._obs = Obs
        self._value = {}

    @staticmethod
    def factory(*args_, **kwargs_):
        return SeriesType(*args_, **kwargs_)

    @property
    def value_(self):
        return self._value

    @value_.setter
    def value_(self, value):
        self._value = value

    def has_content_(self):
        if (
                self._seriesKey is not None or
                self._attributes is not None or
                self._obs or
                super(SeriesType, self).has_content_()
        ):
            return True
        else:
            return False

    def build_attributes(self, node, attrs, already_processed):
        super(SeriesType, self).build_attributes(node, attrs, already_processed)

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'SeriesKey':
            obj_ = ValuesType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            if len(self.value_) == 0:
                self._value = obj_.value_
            else:
                self._value.update(obj_.value_)
            self._seriesKey = obj_

        elif nodeName_ == 'Attributes':
            obj_ = ValuesType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._value.update(obj_.value_)
            obj_.original_tagname_ = 'Attributes'
        elif nodeName_ == 'Obs':
            obj_ = ObsType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._value.update(obj_.value_)
        super(SeriesType, self).build_children(child_, node, nodeName_, True)


# end class SeriesType


class ObsOnlyType(AnnotableArtefact):
    """ObsOnlyType defines the structure for an un-grouped observation. Unlike
    a group observation, an un-grouped must provided a full set of values
    for every dimension declared in the data structure definition. The
    observation can contain an observed value and/or a collection of
    attribute values."""

    def __init__(self, Annotations=None, ObsKey=None, ObsValue=None, Attributes=None, gds_collector_=None):
        super(ObsOnlyType, self).__init__(Annotations, gds_collector_)
        self._obsKey = ObsKey
        self._obsValue = ObsValue
        self._attributes = Attributes
        self._value = {}

    @staticmethod
    def factory(*args_, **kwargs_):
        return ObsOnlyType(*args_, **kwargs_)

    @property
    def value_(self):
        return self._value

    @value_.setter
    def value_(self, value):
        self._value = value

    def has_content_(self):
        if (
                self._obsKey is not None or
                self._obsValue is not None or
                self._attributes is not None or
                super(ObsOnlyType, self).has_content_()
        ):
            return True
        else:
            return False

    def export_attributes_as_dict(self, parent_dict: dict, data: list, valid_fields: list):
        if self._obsKey is not None and self._obsKey.has_content_():
            self._obsKey.export_attributes_as_dict(parent_dict, )

        if self._obsValue is not None:
            self._obsValue.export_attributes_as_dict(parent_dict, )

        if self._attributes is not None and self._attributes.has_content_():
            self._attributes.export_attributes_as_dict(parent_dict, )

    def build_attributes(self, node, attrs, already_processed):
        super(ObsOnlyType, self).build_attributes(node, attrs, already_processed)

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'ObsKey':
            obj_ = ValuesType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            if len(self.value_) == 0:
                self._value = obj_.value_
            else:
                self._value.update(obj_.value_)

        elif nodeName_ == 'ObsValue':
            obj_ = ObsValueType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._value['OBS_VALUE'] = obj_.value_

        elif nodeName_ == 'Attributes':
            obj_ = ValuesType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            if len(self.value_) == 0:
                self._value = obj_.value_
            else:
                self._value.update(obj_.value_)

        super(ObsOnlyType, self).build_children(child_, node, nodeName_, True)


# end class ObsOnlyType

class ObsType(AnnotableArtefact):
    """ObsType defines the structure of a grouped observation. The observation
    must be provided a value for the dimension which is declared to be at
    the observation level for this data set. This dimension value should
    disambiguate the observation within the series in which it is defined
    (i.e. there should not be another observation with the same dimension
    value). The observation can contain an observed value and/or attribute
    values."""

    def __init__(self, Annotations=None, ObsDimension=None, ObsValue=None, Attributes=None, gds_collector_=None):
        super(ObsType, self).__init__(Annotations, gds_collector_)
        self._obsDimension = ObsDimension
        self._obsDimension_nsprefix_ = None
        self._obsValue = ObsValue
        self._obsValue_nsprefix_ = None
        self._attributes = Attributes
        self._attributes_nsprefix_ = None
        self._name = 'ObsType'
        self._namespacedef = 'xmlns:generic="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic"'
        self._namespaceprefix = 'generic'
        self.original_tagname_ = 'Obs'
        self._value = {}

    @staticmethod
    def factory(*args_, **kwargs_):
        return ObsType(*args_, **kwargs_)

    @property
    def obsDimension(self):
        return self._obsDimension

    @obsDimension.setter
    def obsDimension(self, value):
        self._obsDimension = value

    @property
    def obsValue(self):
        return self._obsValue

    @obsValue.setter
    def obsValue(self, value):
        self._obsValue = value

    @property
    def attributes(self):
        return self._attributes

    @attributes.setter
    def attributes(self, value):
        self._attributes = value

    @property
    def value_(self):
        return self._value

    @value_.setter
    def value_(self, value):
        self._value = value

    def has_content_(self):
        if (
                self.obsDimension is not None or
                self.obsValue is not None or
                self.attributes is not None or
                super(ObsType, self).has_content_()
        ):
            return True
        else:
            return False

    def build_attributes(self, node, attrs, already_processed):
        super(ObsType, self).build_attributes(node, attrs, already_processed)

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'ObsDimension':
            obj_ = BaseValueType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.value_['ObsDimension'] = obj_.value_

        elif nodeName_ == 'ObsValue':
            obj_ = ObsValueType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.value_['OBS_VALUE'] = obj_.value_

        elif nodeName_ == 'Attributes':
            obj_ = ValuesType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.value_.update(obj_.value_)

        super(ObsType, self).build_children(child_, node, nodeName_, True)


# end class ObsType

def validate_BasicTimePeriodType():
    # TODO Anything to validate here??? (BasicTimePeriod)
    pass


class DataSetType(AnnotableArtefact):
    """DataSetType defines the structure of the generic data set. Data is
    organised into either a collection of series (grouped observations) or
    a collection of un-grouped observations. The organisation used is
    dependent on the structure specification in the header of the data
    message (which is referenced via the structureRef attribute). The
    structure specification states which data occurs at the observation
    level. If this dimension is "AllDimensions" then the data set must
    consist of a collection of un-grouped observations; otherwise the data
    set will contain a collection of series with the observations in the
    series disambiguated by the specified dimension at the observation
    level. This data set is capable of containing data (observed values)
    and/or documentation (attribute values). It is assumed that each series
    or un-grouped observation will be distinct in its purpose. For example,
    if series contains both data and documentation, it assumed that each
    series will have a unique key. If the series contains only data or only
    documentation, then it is possible that another series with the same
    key might exist, but with not with the same purpose (i.e. to provide
    data or documentation) as the first series."""

    def __init__(self, Annotations=None, structureRef=None, setID=None, action=None, reportingBeginDate=None,
                 reportingEndDate=None, validFromDate=None, validToDate=None, publicationYear=None,
                 publicationPeriod=None, DataProvider=None, Attributes=None, Group=None, Data=None,
                 gds_collector_=None, **kwargs_):
        super(DataSetType, self).__init__(Annotations, gds_collector_)
        self._structureRef = cast(None, structureRef)
        self._structureRef_nsprefix_ = None
        self._setID = cast(None, setID)
        self._action = cast(None, action)
        self._reportingBeginDate = cast(None, reportingBeginDate)
        self._reportingEndDate = cast(None, reportingEndDate)
        if isinstance(validFromDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(validFromDate, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = validFromDate
        self._validFromDate = initvalue_
        if isinstance(validToDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(validToDate, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = validToDate
        self._validToDate = initvalue_
        self._publicationYear = cast(None, publicationYear)
        self._publicationPeriod = cast(None, publicationPeriod)
        self._dataProvider = DataProvider
        self._Attributes = Attributes
        if Data is None:
            self._data = []
        else:
            self._data = Data
        if Group is None:
            self._group = []
        else:
            self._group = Group
        self._group_nsprefix_ = None
        self._namespacedef = 'xmlns:message="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message"'
        self._namespace_prefix = 'message'
        self._name = 'DataSetType'
        self.original_tagname_ = 'DataSet'

    @staticmethod
    def factory(*args_, **kwargs_):
        return DataSetType(*args_, **kwargs_)

    @property
    def DataProvider(self):
        return self._dataProvider

    @DataProvider.setter
    def DataProvider(self, value):
        self._dataProvider = value

    @property
    def Attributes(self):
        return self._Attributes

    @Attributes.setter
    def Attributes(self, value):
        self._Attributes = value

    @property
    def Group(self):
        return self._group

    @Group.setter
    def Group(self, value):
        if value is None:
            self._group = []
        elif isinstance(value, list):
            self._group = value
        else:
            raise TypeError('Group must be a list')

    def add_Group(self, value):
        self._group.append(value)

    def insert_Group_at(self, index, value):
        self._group.insert(index, value)

    def replace_Group_at(self, index, value):
        self._group[index] = value

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    @property
    def structureRef(self):
        return self._structureRef

    @structureRef.setter
    def structureRef(self, value):
        self._structureRef = value

    @property
    def setID(self):
        return self._setID

    @setID.setter
    def setID(self, value):
        self._setID = value

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, value):
        self._action = value

    @property
    def reportingBeginDate(self):
        return self._reportingBeginDate

    @reportingBeginDate.setter
    def reportingBeginDate(self, value):
        self._reportingBeginDate = value

    @property
    def reportingEndDate(self):
        return self._reportingEndDate

    @reportingEndDate.setter
    def reportingEndDate(self, value):
        self._reportingEndDate = value

    @property
    def validFromDate(self):
        return self._validFromDate

    @validFromDate.setter
    def validFromDate(self, value):
        self._validFromDate = value

    @property
    def validToDate(self):
        return self._validToDate

    @validToDate.setter
    def validToDate(self, value):
        self._validToDate = value

    @property
    def publicationYear(self):
        return self._publicationYear

    @publicationYear.setter
    def publicationYear(self, value):
        self._publicationYear = value

    @property
    def publicationPeriod(self):
        return self._publicationPeriod

    @publicationPeriod.setter
    def publicationPeriod(self, value):
        self._publicationPeriod = value

    def validate_ActionType(self, value):
        # Validate dim_type common:ActionType, a restriction on xs:NMTOKEN.
        result = True
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{value}": {lineno} is not of the correct base simple dim_type (str)')
                return False
            value = value
            enumerations = ['Append', 'Replace', 'Delete', 'Information']
            if value not in enumerations:
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(f'Value "{encode_str_2_3(value)}"{lineno} '
                                                f'does not match xsd enumeration restriction on ActionType')
                result = False
        return result

    def has_content_(self):
        if (
                self._dataProvider is not None or
                self._Attributes is not None or
                self._group or
                self._data or
                super(DataSetType, self).has_content_()
        ):
            return True
        else:
            return False

    def build_attributes(self, node, attrs, already_processed):
        value = find_attr_value_('structureRef', node)

        if value is not None and 'structureRef' not in already_processed:
            already_processed.add('structureRef')
            self._structureRef = value

        value = find_attr_value_('setID', node)

        if value is not None and 'setID' not in already_processed:
            already_processed.add('setID')
            self._setID = value
            self.validate_id_type(self._setID)  # validate dim_type IDType

        value = find_attr_value_('action', node)

        if value is not None and 'action' not in already_processed:
            already_processed.add('action')
            self._action = value
            self.validate_ActionType(self._action)  # validate dim_type ActionType

        value = find_attr_value_('reportingBeginDate', node)

        if value is not None and 'reportingBeginDate' not in already_processed:
            already_processed.add('reportingBeginDate')
            self._reportingBeginDate = value

        value = find_attr_value_('reportingEndDate', node)

        if value is not None and 'reportingEndDate' not in already_processed:
            already_processed.add('reportingEndDate')
            self._reportingEndDate = value
            # Validate reporting end date

        value = find_attr_value_('validFromDate', node)

        if value is not None and 'validFromDate' not in already_processed:
            already_processed.add('validFromDate')
            try:
                self._validFromDate = self.gds_parse_datetime(value)
            except ValueError as exp:
                raise ValueError('Bad date-time attribute (validFromDate): %s' % exp)

        value = find_attr_value_('validToDate', node)

        if value is not None and 'validToDate' not in already_processed:
            already_processed.add('validToDate')
            try:
                self._validToDate = self.gds_parse_datetime(value)
            except ValueError as exp:
                raise ValueError('Bad date-time attribute (validToDate): %s' % exp)

        value = find_attr_value_('publicationYear', node)

        if value is not None and 'publicationYear' not in already_processed:
            already_processed.add('publicationYear')
            self._publicationYear = value

        value = find_attr_value_('publicationPeriod', node)
        if value is not None and 'publicationPeriod' not in already_processed:
            already_processed.add('publicationPeriod')
            self._publicationPeriod = value
            self.validate_ObservationalTimePeriodType(
                self._publicationPeriod)  # validate dim_type ObservationalTimePeriodType

        super(DataSetType, self).build_attributes(node, attrs, already_processed)

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'DataProvider':
            obj_ = DataProviderReferenceType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._dataProvider = obj_
            obj_.original_tag_name_ = 'DataProvider'
        elif nodeName_ == 'Attributes':
            obj_ = ValuesType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._Attributes = obj_
            obj_.original_tagname_ = 'Attributes'
        elif nodeName_ == 'Group':
            obj_ = GroupType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._group.append(obj_)
            obj_.original_tagname_ = 'Group'
        elif nodeName_ == 'Series':
            obj_ = SeriesType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._data.append(obj_.value_)
            obj_.original_tagname_ = 'Series'
        elif nodeName_ == 'Obs':
            obj_ = ObsOnlyType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._data.append(obj_.value_)
            obj_.original_tagname_ = 'Obs'
        super(DataSetType, self).build_children(child_, node, nodeName_, True)

    def validate_ObservationalTimePeriodType(self, date):
        # TODO Anything to validate here??? (Observational Time Period)
        pass


# end class DataSetType


class TimeSeriesDataSetType(DataSetType):
    """TimeSeriesDataSetType is a derivation of the base DataSetType of the
    generic format the restricts the data set to only allow for grouped
    observations where the dimension at the observation level is the time
    dimension of the data structure definition. This means that unlike the
    base data set structure, there can be no un-grouped observations.
    Because this derivation is achieved using restriction, data sets
    conforming to this type will inherently conform to the base data set
    structure as well. In fact, data structured here will be identical to
    data in the base data set when the time dimension is the observation
    dimension. This means that the data contained in this structure can be
    processed in exactly the same manner as the base structure."""
    __hash__ = DataSetType.__hash__
    subclass = None
    superclass = DataSetType

    def __init__(self, Annotations=None, structureRef=None, setID=None, action=None, reportingBeginDate=None,
                 reportingEndDate=None, validFromDate=None, validToDate=None, publicationYear=None,
                 publicationPeriod=None, DataProvider=None, Attributes=None, Group=None,
                 gds_collector_=None, **kwargs_):
        super(TimeSeriesDataSetType, self).__init__(Annotations, structureRef, setID, action, reportingBeginDate,
                                                    reportingEndDate, validFromDate, validToDate, publicationYear,
                                                    publicationPeriod, DataProvider, Attributes, Group,
                                                    gds_collector_, **kwargs_)


class TimeSeriesType(SeriesType):
    """TimeSeriesType defines a structure which is used to group a collection
    of observations which have a key in common, organised by time. The key
    for a series is every dimension defined in the data structure
    definition, save the time dimension. In addition to observations,
    values can be provided for attributes which are associated with the
    dimensions which make up this series key (so long as the attributes do
    not specify a group attachment or also have an relationship with the
    time dimension). It is possible for the series to contain only
    observations or only attribute values, or both."""
    __hash__ = SeriesType.__hash__
    subclass = None
    superclass = SeriesType

    def __init__(self, Annotations=None, SeriesKey=None, Attributes=None, Obs=None, gds_collector_=None, **kwargs_):
        super(TimeSeriesType, self).__init__(Annotations, SeriesKey, Attributes, Obs, gds_collector_, **kwargs_)


class TimeSeriesObsType(ObsType):
    """TimeSeriesObsType defines the structure of a time series observation.
    The observation must be provided a value for the time dimension. This
    time value should disambiguate the observation within the series in
    which it is defined (i.e. there should not be another observation with
    the same time value). The observation can contain an observed value
    and/or attribute values."""
    __hash__ = ObsType.__hash__
    subclass = None
    superclass = ObsType


class TimeValueType(BaseValueType):
    """TimeValueType is a derivation of the BaseValueType which is used to
    provide a value for the time dimension. Since the identifier for the
    time dimension is fixed, the component reference for this structure is
    fixed. Note that this means that it is not necessary to provide a value
    in an instance as the fixed value will be provided in the post
    validation information set."""
    __hash__ = BaseValueType.__hash__
    subclass = None
    superclass = BaseValueType

    def __init__(self, idx=None, value=None, **kwargs_):
        super(TimeValueType, self).__init__(idx, value, None, **kwargs_)
