from SDMXThon.common.annotations import TextType
from SDMXThon.utils.data_parser import DataParser
from SDMXThon.utils.xml_base import _cast, quote_attrib, find_attr_value_


class StatusMessageType(DataParser):
    """StatusMessageType describes the structure of an error or warning
    message. A message contains the text of the message, as well as an
    optional language indicator and an optional _code.The _code attribute
    holds an optional _code identifying the underlying error that generated
    the message. This should be used if parallel language descriptions of
    the error are supplied, to distinguish which of the multiple error
    messages are for the same underlying error."""
    __hash__ = DataParser.__hash__
    subclass = None
    superclass = None

    def __init__(self, code=None, Text=None, gds_collector_=None, **kwargs_):
        super(StatusMessageType, self).__init__(None, None, gds_collector_)
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self._code = _cast(None, code)
        self._code_nsprefix_ = None
        if Text is None:
            self._text = []
        else:
            self._text = Text
        self.Text_nsprefix_ = None
        self._namespacedef = 'xmlns:common="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common"'
        self._namespaceprefix = "common"
        self._name = 'StatusMessageType'

    def factory(*args_, **kwargs_):
        return StatusMessageType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_Text(self):
        return self._text

    def set_Text(self, Text):
        self._text = Text

    def add_Text(self, value):
        self._text.append(value)

    def insert_Text_at(self, index, value):
        self._text.insert(index, value)

    def replace_Text_at(self, index, value):
        self._text[index] = value

    def get_code(self):
        return self._code

    def set_code(self, code):
        self._code = code

    def has_content_(self):
        if (
                self._text
        ):
            return True
        else:
            return False

    def export_attributes(self, outfile, level, already_processed, namespace_prefix_='', name_='StatusMessageType'):
        if self._code is not None and 'Code' not in already_processed:
            already_processed.add('Code')
            outfile.write(
                'Code=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self._code), input_name='Code')),))

    def export_attributes_as_dict(self, parent_dict: dict, data: list, valid_fields: list):
        pass

    def export_children(self, outfile, level, pretty_print=True, has_parent=True):
        for Text_ in self._text:
            Text_.export(outfile, level, pretty_print=pretty_print, has_parent=has_parent)

    def build_attributes(self, node, attrs, already_processed):
        value = find_attr_value_('Code', node)
        if value is not None and 'Code' not in already_processed:
            already_processed.add('Code')
            self._code = value

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Text':
            class_obj_ = self.get_class_obj_(child_, TextType)
            obj_ = class_obj_.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._text.append(obj_)
            obj_.original_tag_name_ = 'Text'


# end class StatusMessageType


class CodedStatusMessageType(StatusMessageType):
    """CodedStatusMessageType describes the structure of an error or warning
    message which required a _code."""
    __hash__ = DataParser.__hash__
    subclass = None
    superclass = StatusMessageType

    def __init__(self, code=None, Text=None, gds_collector_=None, **kwargs_):
        super(CodedStatusMessageType, self).__init__(code, Text, gds_collector_, **kwargs_)
        self._name = 'CodedStatusMessageType'

    def factory(*args_, **kwargs_):
        return CodedStatusMessageType(*args_, **kwargs_)

    factory = staticmethod(factory)
# end class CodedStatusMessageType
