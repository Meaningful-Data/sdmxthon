import copy

from SDMXThon.common.annotations import AnnotableType
from SDMXThon.common.references import DataProviderReferenceType
from SDMXThon.utils.data_parser import DataParser
from SDMXThon.utils.data_parser import Validate_simpletypes_
from SDMXThon.utils.generateds import datetime_
from SDMXThon.utils.xml_base import _cast, BaseStrType_, quote_attrib, find_attr_value_, encode_str_2_3


class BaseValueType(DataParser):
    """BaseValueType is a general structure which contains a reference to a
    data structure definition component and a value for that component. In
    this structure the reference to the component is optional to allow for
    usages where the actual reference might be provided in another
    context.The id attribute contains the identifier for the component for
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

    def factory(*args_, **kwargs_):
        return BaseValueType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_id(self):
        return self._id

    def set_id(self, idx):
        self._id = idx

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = value

    def export_attributes(self, outfile, level, already_processed, namespace_prefix_='', name_='BaseValueType'):
        if self._id is not None and 'id' not in already_processed:
            already_processed.add('id')
            outfile.write(' id=%s' % (quote_attrib(self._id),))

        if self._value is not None and 'value' not in already_processed:
            already_processed.add('value')
            outfile.write(
                ' value=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self._value), input_name='value')),))

    def export_attributes_as_dict(self, parent_dict: dict, data: list, valid_fields: list):
        if self._id is not None and self._id in valid_fields and self._value is not None:
            parent_dict.update({self._id: self._value})

    def build_attributes(self, node, attrs, already_processed):
        value = find_attr_value_('id', node)
        if value is not None and 'id' not in already_processed:
            already_processed.add('id')
            self._id = value
            self.validate_NC_name_id_type(self._id)  # validate type NCNameIDType

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
    provided in the post validation information set.The id attribute
    contains a fixed reference to the primary measure component of the data
    structure definition."""
    __hash__ = BaseValueType.__hash__
    subclass = None
    superclass = BaseValueType

    def __init__(self, idx=None, value=None, gds_collector_=None, **kwargs_):
        super(ObsValueType, self).__init__(id, value, **kwargs_)
        self._name = 'ObsValueType'

    def factory(*args_, **kwargs_):
        return ObsValueType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_id(self):
        return self._id

    def set_id(self, idx):
        self._id = idx

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = value

    def export_attributes(self, outfile, level, already_processed, namespace_prefix_='', name_='ObsValueType'):
        if self._id != "OBS_VALUE" and 'id' not in already_processed and self._id is not None:
            already_processed.add('id')
            outfile.write(' id=%s' % (quote_attrib(self._id),))

        if self._value is not None and 'value' not in already_processed and self._value is not None:
            already_processed.add('value')
            outfile.write(
                ' value=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self._value), input_name='value')),))

    def export_attributes_as_dict(self, parent_dict: dict, data: list, valid_fields: list):
        if self._id is not None and self._id in valid_fields and self._value is not None:
            parent_dict.update({self._id: self._value})
        elif self._id is None and "OBS_VALUE" in valid_fields and self._value is not None:
            parent_dict.update({"OBS_VALUE": self._value})

    def build_attributes(self, node, attrs, already_processed):
        value = find_attr_value_('id', node)
        if value is not None and 'id' not in already_processed:
            already_processed.add('id')
            self._id = value
            self.validate_NC_name_id_type(self._id)  # validate type NCNameIDType

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

    def __init__(self, id=None, value=None, gds_collector_=None, **kwargs_):
        super(ComponentValueType, self).__init__(id, value, gds_collector_, **kwargs_)
        self._name = 'ComponentValueType'
        self._namespace_prefix = 'generic'

    def factory(*args_, **kwargs_):
        return ComponentValueType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_id(self):
        return self._id

    def set_id(self, id):
        self._id = id

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = value

    def has_content_(self):
        if (
                super(ComponentValueType, self).has_content_()
        ):
            return True
        else:
            return False

    def export_attributes(self, outfile, level, already_processed, namespace_prefix_='', name_='ComponentValueType'):
        super(ComponentValueType, self).export_attributes(outfile, level, already_processed, namespace_prefix_,
                                                          name_='ComponentValueType')
        if self._id is not None and 'id' not in already_processed:
            already_processed.add('id')
            outfile.write(' id=%s' % (quote_attrib(self._id),))
        if self._value is not None and 'value' not in already_processed:
            already_processed.add('value')
            outfile.write(
                ' value=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self._value), input_name='value')),))

    def build_attributes(self, node, attrs, already_processed):
        value = find_attr_value_('id', node)
        if value is not None and 'id' not in already_processed:
            already_processed.add('id')
            self._id = value
            self.validate_NC_name_id_type(self._id)  # validate type NCNameIDType
        value = find_attr_value_('value', node)
        if value is not None and 'value' not in already_processed:
            already_processed.add('value')
            self._value = value
        super(ComponentValueType, self).build_attributes(node, attrs, already_processed)


class ValuesType(DataParser):
    """ValuesType is a general structure which contains a collection of data
    structure definition component values. This type is used to provide
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
            self.Value = []
        else:
            self.Value = Value

        self.Value_nsprefix_ = None
        self._namespacedef = 'xmlns:generic="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic"'
        self._namespaceprefix = 'generic'
        self._namespace_prefix = 'generic'
        self._name = 'ValuesType'

    def factory(*args_, **kwargs_):
        return ValuesType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_Value(self):
        return self.Value

    def set_Value(self, Value):
        self.Value = Value

    def add_Value(self, value):
        self.Value.append(value)

    def insert_Value_at(self, index, value):
        self.Value.insert(index, value)

    def replace_Value_at(self, index, value):
        self.Value[index] = value

    def has_content_(self):
        if (
                self.Value is not None
        ):
            return True
        else:
            return False

    def export_attributes_as_dict(self, parent_dict: dict, data: list, valid_fields: list):
        for Value_ in self.Value:
            Value_.export_attributes_as_dict(parent_dict, data, valid_fields)

    def export_children(self, outfile, level, pretty_print=True, has_parent=True, **kwargs):
        for Value_ in self.Value:
            Value_.export(outfile, level, pretty_print=pretty_print, has_parent=has_parent)

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Value':
            obj_ = ComponentValueType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Value.append(obj_)
            obj_.original_tag_name_ = 'Value'


# end class ValuesType

class GroupType(AnnotableType):
    """GroupType defines a structure which is used to communicate attribute
    values for a group defined in a data structure definition. The group
    can consist of either a subset of the dimensions defined by the data
    structure definition, or an association to an attachment constraint,
    which in turn defines key sets to which attributes can be attached. In
    the case that the group is based on an attachment constraint, only the
    identification of group is provided. It is expected that a system which
    is processing this will relate that identifier to the key sets defined
    in the constraint and apply the values provided for the attributes
    appropriately.The type attribute holds the identifier assigned to the
    group in the data structure definition for which attribute values are
    being provided."""
    __hash__ = AnnotableType.__hash__
    subclass = None
    superclass = AnnotableType

    def __init__(self, Annotations=None, type_=None, GroupKey=None, Attributes=None, gds_collector_=None, **kwargs_):
        super(GroupType, self).__init__(Annotations, gds_collector_, **kwargs_)
        self._type_ = _cast(None, type_)
        self._type__nsprefix_ = None
        self.GroupKey = GroupKey
        self.GroupKey_nsprefix_ = None
        self._Attributes = Attributes
        self._Attributes_nsprefix_ = None
        self._namespacedef = 'xmlns:data="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic"'
        self._namespaceprefix = 'data'
        self._name = 'GroupType',

    def factory(*args_, **kwargs_):
        return GroupType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_GroupKey(self):
        return self.GroupKey

    def set_GroupKey(self, GroupKey):
        self.GroupKey = GroupKey

    def get_Attributes(self):
        return self._Attributes

    def set_Attributes(self, Attributes):
        self._Attributes = Attributes

    def get_type(self):
        return self._type_

    def set_type(self, type_):
        self._type_ = type_

    def has_content_(self):
        if (
                self.GroupKey is not None or
                self._Attributes is not None or
                super(GroupType, self).has_content_()
        ):
            return True
        else:
            return False

    def export_attributes(self, outfile, level, already_processed, namespace_prefix_='', name_='GroupType'):
        if self._type_ is not None and 'type_' not in already_processed:
            already_processed.add('type_')
            outfile.write(' type=%s' % (quote_attrib(self._type_),))

    def export_attributes_as_dict(self, parent_dict: dict, data: list, valid_fields: list):
        if self.GroupKey is not None:
            self.GroupKey.export_attributes_as_dict(parent_dict, data, valid_fields)
        if self._Attributes is not None:
            self._Attributes.export_attributes_as_dict(parent_dict, data, valid_fields)

    def export_children(self, outfile, level, pretty_print=True, has_parent=True, **kwargs):
        if self.GroupKey is not None:
            self.GroupKey.export(outfile, level, pretty_print=pretty_print, has_parent=has_parent)
        if self._Attributes is not None:
            self._Attributes.export(outfile, level, pretty_print=pretty_print, has_parent=has_parent)

    def build_attributes(self, node, attrs, already_processed):
        value = find_attr_value_('type', node)
        if value is not None and 'type' not in already_processed:
            already_processed.add('type')
            self._type_ = value
            self.validate_id_type(self._type_)  # validate type IDType
        super(GroupType, self).build_attributes(node, attrs, already_processed)

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'GroupKey':
            obj_ = ValuesType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.GroupKey = obj_
            obj_.original_tagname_ = 'GroupKey'
        elif nodeName_ == 'Attributes':
            obj_ = ValuesType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._Attributes = obj_
            obj_.original_tagname_ = 'Attributes'
        super(GroupType, self).build_children(child_, node, nodeName_, True)


# end class GroupType


class SeriesType(AnnotableType):
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
    __hash__ = AnnotableType.__hash__
    subclass = None
    superclass = AnnotableType

    def __init__(self, Annotations=None, SeriesKey=None, Attributes=None, Obs=None, gds_collector_=None, **kwargs_):
        super(SeriesType, self).__init__(Annotations, gds_collector_, **kwargs_)
        self.SeriesKey = SeriesKey
        self.SeriesKey_nsprefix_ = None
        self._Attributes = Attributes
        self._Attributes_nsprefix_ = None
        if Obs is None:
            self._obs = []
        else:
            self._obs = Obs
        self._obs_nsprefix_ = None
        self._namespacedef = 'xmlns:data="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic"'
        self._namespaceprefix = 'data'
        self._name = 'SeriesType'

    def factory(*args_, **kwargs_):
        return SeriesType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_SeriesKey(self):
        return self.SeriesKey

    def set_SeriesKey(self, SeriesKey):
        self.SeriesKey = SeriesKey

    def get_Attributes(self):
        return self._Attributes

    def set_Attributes(self, Attributes):
        self._Attributes = Attributes

    def get_Obs(self):
        return self._obs

    def set_Obs(self, Obs):
        self._obs = Obs

    def add_Obs(self, value):
        self._obs.append(value)

    def insert_Obs_at(self, index, value):
        self._obs.insert(index, value)

    def replace_Obs_at(self, index, value):
        self._obs[index] = value

    def has_content_(self):
        if (
                self.SeriesKey is not None or
                self._Attributes is not None or
                self._obs or
                super(SeriesType, self).has_content_()
        ):
            return True
        else:
            return False

    def export_attributes_as_dict(self, parent_dict: dict, data: list, valid_fields: list):
        if self.SeriesKey is not None:
            self.SeriesKey.export_attributes_as_dict(parent_dict, data, valid_fields)

        if self._Attributes is not None:
            self._Attributes.export_attributes_as_dict(parent_dict, data, valid_fields)

        for Obs_ in self._obs:
            parent_data = copy.deepcopy(parent_dict)
            Obs_.export_attributes_as_dict(parent_data, data, valid_fields)
            data.append(parent_data)

    def export_children(self, outfile, level, pretty_print=True, has_parent=True, **kwargs):
        super(SeriesType, self).export_children(outfile, level, pretty_print=pretty_print)
        if self.SeriesKey is not None:
            self.SeriesKey.export(outfile, level, pretty_print=pretty_print, has_parent=has_parent)

        if self._Attributes is not None:
            self._Attributes.export(outfile, level, pretty_print=pretty_print, has_parent=has_parent)

        for Obs_ in self._obs:
            Obs_.export(outfile, level, pretty_print=pretty_print, has_parent=has_parent)

    def build_attributes(self, node, attrs, already_processed):
        super(SeriesType, self).build_attributes(node, attrs, already_processed)

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'SeriesKey':
            obj_ = ValuesType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.SeriesKey = obj_
            obj_.original_tagname_ = 'SeriesKey'
        elif nodeName_ == 'Attributes':
            obj_ = ValuesType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._Attributes = obj_
            obj_.original_tagname_ = 'Attributes'
        elif nodeName_ == 'Obs':
            obj_ = ObsType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._obs.append(obj_)
            obj_.original_tagname_ = 'Obs'
        super(SeriesType, self).build_children(child_, node, nodeName_, True)


# end class SeriesType


class ObsOnlyType(AnnotableType):
    """ObsOnlyType defines the structure for an un-grouped observation. Unlike
    a group observation, an un-grouped must provided a full set of values
    for every dimension declared in the data structure definition. The
    observation can contain an observed value and/or a collection of
    attribute values."""
    __hash__ = AnnotableType.__hash__
    subclass = None
    superclass = AnnotableType

    def __init__(self, Annotations=None, ObsKey=None, ObsValue=None, Attributes=None, gds_collector_=None, **kwargs_):
        super(ObsOnlyType, self).__init__(Annotations, gds_collector_, **kwargs_)
        self.ObsKey = ObsKey
        self.ObsKey_nsprefix_ = None
        self.ObsValue = ObsValue
        self.ObsValue_nsprefix_ = None
        self._Attributes = Attributes
        self._Attributes_nsprefix_ = None
        self._namespacedef = 'xmlns:generic="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic"'
        self._namespace_prefix = 'generic'
        self._name = 'ObsOnlyType'

    def factory(*args_, **kwargs_):
        return ObsOnlyType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_ObsKey(self):
        return self.ObsKey

    def set_ObsKey(self, ObsKey):
        self.ObsKey = ObsKey

    def get_ObsValue(self):
        return self.ObsValue

    def set_ObsValue(self, ObsValue):
        self.ObsValue = ObsValue

    def get_Attributes(self):
        return self._Attributes

    def set_Attributes(self, Attributes):
        self._Attributes = Attributes

    def has_content_(self):
        if (
                self.ObsKey is not None or
                self.ObsValue is not None or
                self._Attributes is not None or
                super(ObsOnlyType, self).has_content_()
        ):
            return True
        else:
            return False

    def export_attributes_as_dict(self, parent_dict: dict, data: list, valid_fields: list):
        if self.ObsKey is not None and self.ObsKey.has_content_():
            self.ObsKey.export_attributes_as_dict(parent_dict, data, valid_fields)

        if self.ObsValue is not None:
            self.ObsValue.export_attributes_as_dict(parent_dict, data, valid_fields)

        if self._Attributes is not None and self._Attributes.has_content_():
            self._Attributes.export_attributes_as_dict(parent_dict, data, valid_fields)

    def export_attributes(self, outfile, level, already_processed, namespace_prefix_='', name_='ObsOnlyType'):
        super(ObsOnlyType, self).export_attributes(outfile, level, already_processed, namespace_prefix_,
                                                   name_='ObsOnlyType')

    def export_children(self, outfile, level, pretty_print=True, has_parent=True, **kwargs):
        if self.ObsKey is not None and self.ObsKey.has_content_():
            self.ObsKey.export(outfile, level, pretty_print=pretty_print, has_parent=has_parent)

        if self.ObsValue is not None:
            self.ObsValue.export(outfile, level, pretty_print=pretty_print, has_parent=has_parent)

        if self._Attributes is not None and self._Attributes.has_content_():
            self._Attributes.export(outfile, level, pretty_print=pretty_print, has_parent=has_parent)

    def build_attributes(self, node, attrs, already_processed):
        super(ObsOnlyType, self).build_attributes(node, attrs, already_processed)

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'ObsKey':
            obj_ = ValuesType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ObsKey = obj_

            obj_.original_tagname_ = 'ObsKey'
        elif nodeName_ == 'ObsValue':
            obj_ = ObsValueType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ObsValue = obj_
            obj_.original_tag_name_ = 'ObsValue'

        elif nodeName_ == 'Attributes':
            obj_ = ValuesType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._Attributes = obj_
            obj_.original_tagname_ = 'Attributes'

        super(ObsOnlyType, self).build_children(child_, node, nodeName_, True)


# end class ObsOnlyType

class ObsType(AnnotableType):
    """ObsType defines the structure of a grouped observation. The observation
    must be provided a value for the dimension which is declared to be at
    the observation level for this data set. This dimension value should
    disambiguate the observation within the series in which it is defined
    (i.e. there should not be another observation with the same dimension
    value). The observation can contain an observed value and/or attribute
    values."""
    __hash__ = AnnotableType.__hash__
    subclass = None
    superclass = AnnotableType

    def __init__(self, Annotations=None, ObsDimension=None, ObsValue=None, Attributes=None, gds_collector_=None,
                 **kwargs_):
        super(ObsType, self).__init__(Annotations, gds_collector_, **kwargs_)
        self.ObsDimension = ObsDimension
        self.ObsDimension_nsprefix_ = None
        self.ObsValue = ObsValue
        self.ObsValue_nsprefix_ = None
        self._Attributes = Attributes
        self._Attributes_nsprefix_ = None
        self._name = 'ObsType'
        self._namespacedef = 'xmlns:data="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic"'
        self._namespaceprefix = 'data'
        self.original_tagname_ = 'Obs'

    def factory(*args_, **kwargs_):
        return ObsType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_ObsDimension(self):
        return self.ObsDimension

    def set_ObsDimension(self, ObsDimension):
        self.ObsDimension = ObsDimension

    def get_ObsValue(self):
        return self.ObsValue

    def set_ObsValue(self, ObsValue):
        self.ObsValue = ObsValue

    def get_Attributes(self):
        return self._Attributes

    def set_Attributes(self, Attributes):
        self._Attributes = Attributes

    def has_content_(self):
        if (
                self.ObsDimension is not None or
                self.ObsValue is not None or
                self._Attributes is not None or
                super(ObsType, self).has_content_()
        ):
            return True
        else:
            return False

    def export_attributes(self, outfile, level, already_processed, namespace_prefix_='', name_='ObsType'):
        super(ObsType, self).export_attributes(outfile, level, already_processed, namespace_prefix_, name_='ObsType')

    def export_children(self, outfile, level, pretty_print=True, has_parent=True, **kwargs):
        super(ObsType, self).export_children(outfile, level, pretty_print=pretty_print)

        if self.ObsDimension is not None:
            self.ObsDimension.export(outfile, level, pretty_print=pretty_print, has_parent=has_parent)

        if self.ObsValue is not None:
            self.ObsValue.export(outfile, level, pretty_print=pretty_print, has_parent=has_parent)

        if self._Attributes is not None:
            self._Attributes.export(outfile, level, pretty_print=pretty_print, has_parent=has_parent)

    def build_attributes(self, node, attrs, already_processed):
        super(ObsType, self).build_attributes(node, attrs, already_processed)

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'ObsDimension':
            obj_ = BaseValueType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ObsDimension = obj_
            obj_.original_tag_name_ = 'ObsDimension'

        elif nodeName_ == 'ObsValue':
            obj_ = ObsValueType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ObsValue = obj_
            obj_.original_tag_name_ = 'ObsValue'

        elif nodeName_ == 'Attributes':
            obj_ = ValuesType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._Attributes = obj_
            obj_.original_tagname_ = 'Attributes'

        super(ObsType, self).build_children(child_, node, nodeName_, True)


# end class ObsType

class DataSetType(AnnotableType):
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
    __hash__ = AnnotableType.__hash__
    subclass = None
    superclass = AnnotableType

    def __init__(self, Annotations=None, structureRef=None, setID=None, action=None, reportingBeginDate=None,
                 reportingEndDate=None, validFromDate=None, validToDate=None, publicationYear=None,
                 publicationPeriod=None, DataProvider=None, Attributes=None, Group=None, Series=None, Obs=None,
                 gds_collector_=None, **kwargs_):
        super(DataSetType, self).__init__(Annotations, gds_collector_, **kwargs_)
        self._structureRef = _cast(None, structureRef)
        self._structureRef_nsprefix_ = None
        self._setID = _cast(None, setID)
        self._setID_nsprefix_ = None
        self._action = _cast(None, action)
        self._action_nsprefix_ = None
        self._reportingBeginDate = _cast(None, reportingBeginDate)
        self._reportingBeginDate_nsprefix_ = None
        self._reportingEndDate = _cast(None, reportingEndDate)
        self._reportingEndDate_nsprefix_ = None
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
        self._publicationYear = _cast(None, publicationYear)
        self._publicationYear_nsprefix_ = None
        self._publicationPeriod = _cast(None, publicationPeriod)
        self._publicationPeriod_nsprefix_ = None
        self._dataProvider = DataProvider
        self._dataProvider_nsprefix_ = None
        self._Attributes = Attributes
        self._Attributes_nsprefix_ = None
        if Group is None:
            self._group = []
        else:
            self._group = Group
        self._group_nsprefix_ = None
        if Series is None:
            self._Series = []
        else:
            self._Series = Series
        self._Series_nsprefix_ = None
        if Obs is None:
            self._obs = []
        else:
            self._obs = Obs
        self._obs_nsprefix_ = None

        self._namespacedef = 'xmlns:message="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message"'
        self._namespace_prefix = 'message'
        self._name = 'DataSetType'
        self.original_tagname_ = 'DataSet'

    def factory(*args_, **kwargs_):
        return DataSetType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_DataProvider(self):
        return self._dataProvider

    def set_DataProvider(self, DataProvider):
        self._dataProvider = DataProvider

    def get_Attributes(self):
        return self._Attributes

    def set_Attributes(self, Attributes):
        self._Attributes = Attributes

    def get_Group(self):
        return self._group

    def set_Group(self, Group):
        self._group = Group

    def add_Group(self, value):
        self._group.append(value)

    def insert_Group_at(self, index, value):
        self._group.insert(index, value)

    def replace_Group_at(self, index, value):
        self._group[index] = value

    def get_Series(self):
        return self._Series

    def set_Series(self, Series):
        self._Series = Series

    def add_Series(self, value):
        self._Series.append(value)

    def insert_Series_at(self, index, value):
        self._Series.insert(index, value)

    def replace_Series_at(self, index, value):
        self._Series[index] = value

    def get_Obs(self):
        return self._obs

    def set_Obs(self, Obs):
        self._obs = Obs

    def add_Obs(self, value):
        self._obs.append(value)

    def insert_Obs_at(self, index, value):
        self._obs.insert(index, value)

    def replace_Obs_at(self, index, value):
        self._obs[index] = value

    def get_structureRef(self):
        return self._structureRef

    def set_structureRef(self, structureRef):
        self._structureRef = structureRef

    def get_setID(self):
        return self._setID

    def set_setID(self, setID):
        self._setID = setID

    def get_action(self):
        return self._action

    def set_action(self, action):
        self._action = action

    def get_reportingBeginDate(self):
        return self._reportingBeginDate

    def set_reportingBeginDate(self, reportingBeginDate):
        self._reportingBeginDate = reportingBeginDate

    def get_reportingEndDate(self):
        return self._reportingEndDate

    def set_reportingEndDate(self, reportingEndDate):
        self._reportingEndDate = reportingEndDate

    def get_validFromDate(self):
        return self._validFromDate

    def set_validFromDate(self, validFromDate):
        self._validFromDate = validFromDate

    def get_validToDate(self):
        return self._validToDate

    def set_validToDate(self, validToDate):
        self._validToDate = validToDate

    def get_publicationYear(self):
        return self._publicationYear

    def set_publicationYear(self, publicationYear):
        self._publicationYear = publicationYear

    def get_publicationPeriod(self):
        return self._publicationPeriod

    def set_publicationPeriod(self, publicationPeriod):
        self._publicationPeriod = publicationPeriod

    def validate_ActionType(self, value):
        # Validate type common:ActionType, a restriction on xs:NMTOKEN.
        result = True
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value,
                                                                                                  "lineno": lineno, })
                return False
            value = value
            enumerations = ['Append', 'Replace', 'Delete', 'Information']
            if value not in enumerations:
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on ActionType' % {
                        "value": encode_str_2_3(value), "lineno": lineno})
                result = False
        return result

    def has_content_(self):
        if (
                self._dataProvider is not None or
                self._Attributes is not None or
                self._group or
                self._Series or
                self._obs or
                super(DataSetType, self).has_content_()
        ):
            return True
        else:
            return False

    def export_attributes(self, outfile, level, already_processed, namespace_prefix_='', name_='DataSetType'):
        super(DataSetType, self).export_attributes(outfile, level, already_processed, namespace_prefix_,
                                                   name_='DataSetType')

        if self._structureRef is not None and 'structureRef' not in already_processed:
            already_processed.add('structureRef')
            outfile.write(' structureRef=%s' % (
                self.gds_encode(self.gds_format_string(quote_attrib(self._structureRef), input_name='structureRef')),))

        if self._setID is not None and 'setID' not in already_processed:
            already_processed.add('setID')
            outfile.write(' setID=%s' % (quote_attrib(self._setID),))

        if self._action is not None and 'action' not in already_processed:
            already_processed.add('action')
            outfile.write(' action=%s' % (
                self.gds_encode(self.gds_format_string(quote_attrib(self._action), input_name='action')),))

        if self._reportingBeginDate is not None and 'reportingBeginDate' not in already_processed:
            already_processed.add('reportingBeginDate')
            outfile.write(' reportingBeginDate=%s' % (quote_attrib(self._reportingBeginDate),))

        if self._reportingEndDate is not None and 'reportingEndDate' not in already_processed:
            already_processed.add('reportingEndDate')
            outfile.write(' reportingEndDate=%s' % (quote_attrib(self._reportingEndDate),))

        if self._validFromDate is not None and 'validFromDate' not in already_processed:
            already_processed.add('validFromDate')
            outfile.write(
                ' validFromDate="%s"' % self.gds_format_datetime(self._validFromDate, input_name='validFromDate'))

        if self._validToDate is not None and 'validToDate' not in already_processed:
            already_processed.add('validToDate')
            outfile.write(' validToDate="%s"' % self.gds_format_datetime(self._validToDate, input_name='validToDate'))

        if self._publicationYear is not None and 'publicationYear' not in already_processed:
            already_processed.add('publicationYear')
            outfile.write(' publicationYear=%s' % (self.gds_encode(
                self.gds_format_string(quote_attrib(self._publicationYear), input_name='publicationYear')),))

        if self._publicationPeriod is not None and 'publicationPeriod' not in already_processed:
            already_processed.add('publicationPeriod')
            outfile.write(' publicationPeriod=%s' % (quote_attrib(self._publicationPeriod),))

    def export_attributes_as_dict(self, parent_dict: dict, data: list, valid_fields: list):
        if self._structureRef is not None and 'DSDID' in valid_fields:
            parent_dict.update({'DSDID': self._structureRef})

        if self._setID is not None and 'setID' in valid_fields:
            parent_dict.update({'setID': self._setID})

        if self._action is not None and 'action' in valid_fields:
            parent_dict.update({'action': self._action})

        if self._reportingBeginDate is not None and 'reportingBeginDate' in valid_fields:
            parent_dict.update({'reportingBeginDate': self._reportingBeginDate})

        if self._reportingEndDate is not None and 'reportingEndDate' in valid_fields:
            parent_dict.update({'reportingEndDate': self._reportingEndDate})

        if self._validFromDate is not None and 'validFromDate' in valid_fields:
            parent_dict.update({'validFromDate': self._validFromDate})

        if self._validToDate is not None and 'validToDate' in valid_fields:
            parent_dict.update({'validToDate': self._validToDate})

        if self._publicationYear is not None and 'publicationYear' in valid_fields:
            parent_dict.update({'publicationYear': self._publicationYear})

        if self._publicationPeriod is not None and 'publicationPeriod' in valid_fields:
            parent_dict.update({'publicationPeriod': self._publicationPeriod})

        if self._dataProvider is not None:
            parent_data = copy.deepcopy(parent_dict)
            self._dataProvider.export_attributes_as_dict(parent_dict, data, valid_fields)
            data.append(parent_data)

        if self._Attributes is not None:
            self._Attributes.export_attributes_as_dict(parent_dict, data, valid_fields)

        for Group_ in self._group:
            parent_data = copy.deepcopy(parent_dict)
            Group_.export_attributes_as_dict(parent_data, data, valid_fields)
            data.append(parent_data)

        for Series_ in self._Series:
            parent_data = copy.deepcopy(parent_dict)
            Series_.export_attributes_as_dict(parent_data, data, valid_fields)
            data.append(parent_data)

        for Obs_ in self._obs:
            parent_data = copy.deepcopy(parent_dict)
            Obs_.export_attributes_as_dict(parent_data, data, valid_fields)
            data.append(parent_data)

    def export_children(self, outfile, level, pretty_print=True, has_parent=True, **kwargs):
        if self._dataProvider is not None:
            self._dataProvider.export(outfile, level, pretty_print=pretty_print, has_parent=has_parent)

        if self._Attributes is not None:
            self._Attributes.export(outfile, level, pretty_print=pretty_print, has_parent=has_parent)

        for Group_ in self._group:
            Group_.export(outfile, level, pretty_print=pretty_print, has_parent=has_parent)

        for Series_ in self._Series:
            Series_.export(outfile, level, pretty_print=pretty_print, has_parent=has_parent)

        for Obs_ in self._obs:
            Obs_.export(outfile, level, pretty_print=pretty_print, has_parent=has_parent)

    def build_attributes(self, node, attrs, already_processed):
        value = find_attr_value_('structureRef', node)

        if value is not None and 'structureRef' not in already_processed:
            already_processed.add('structureRef')
            self._structureRef = value

        value = find_attr_value_('setID', node)

        if value is not None and 'setID' not in already_processed:
            already_processed.add('setID')
            self._setID = value
            self.validate_id_type(self._setID)  # validate type IDType

        value = find_attr_value_('action', node)

        if value is not None and 'action' not in already_processed:
            already_processed.add('action')
            self._action = value
            self.validate_ActionType(self._action)  # validate type ActionType

        value = find_attr_value_('reportingBeginDate', node)

        if value is not None and 'reportingBeginDate' not in already_processed:
            already_processed.add('reportingBeginDate')
            self._reportingBeginDate = value
            self.validate_BasicTimePeriodType(self._reportingBeginDate)  # validate type BasicTimePeriodType

        value = find_attr_value_('reportingEndDate', node)

        if value is not None and 'reportingEndDate' not in already_processed:
            already_processed.add('reportingEndDate')
            self._reportingEndDate = value
            self.validate_BasicTimePeriodType(self._reportingEndDate)  # validate type BasicTimePeriodType

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
                self._publicationPeriod)  # validate type ObservationalTimePeriodType

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
            self._Series.append(obj_)
            obj_.original_tagname_ = 'Series'
        elif nodeName_ == 'Obs':
            obj_ = ObsOnlyType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._obs.append(obj_)
            obj_.original_tagname_ = 'Obs'
        super(DataSetType, self).build_children(child_, node, nodeName_, True)
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
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = DataSetType

    def __init__(self, Annotations=None, structureRef=None, setID=None, action=None, reportingBeginDate=None,
                 reportingEndDate=None, validFromDate=None, validToDate=None, publicationYear=None,
                 publicationPeriod=None, DataProvider=None, Attributes=None, Group=None, Series=None, Obs=None,
                 gds_collector_=None, **kwargs_):
        super(TimeSeriesDataSetType, self).__init__(Annotations, structureRef, setID, action, reportingBeginDate,
                 reportingEndDate, validFromDate, validToDate, publicationYear,
                 publicationPeriod, DataProvider, Attributes, Group, Series, Obs,
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

    def __init__(self, idx=None, value=None, gds_collector_=None, **kwargs_):
        super(TimeSeriesType, self).__init__(idx, value, gds_collector_, **kwargs_)

    def export_attributes(self, outfile, level, already_processed, namespace_prefix_='', name_='TimeValueType'):
        if self.id != "TIME_PERIOD" and 'id' not in already_processed:
            already_processed.add('id')
            outfile.write(' id=%s' % (quote_attrib(self.id), ))

        if self.value is not None and 'value' not in already_processed:
            already_processed.add('value')
            outfile.write(' value=%s' % (quote_attrib(self.value), ))