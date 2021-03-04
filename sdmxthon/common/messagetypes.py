from ..model.base import LocalisedString, InternationalString
from ..utils.data_parser import DataParser
from ..utils.xml_base import find_attr_value_


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

    def __init__(self, code=None, Text: InternationalString = None, gds_collector_=None, **kwargs_):
        super(StatusMessageType, self).__init__(None)
        self.gds_collector_ = gds_collector_
        self._code = code
        self._text = Text

    @staticmethod
    def factory(*args_, **kwargs_):
        return StatusMessageType(*args_, **kwargs_)

    @property
    def text(self):
        if self._text is None:
            return None
        elif isinstance(self._text, InternationalString):
            if len(self._text.items) == 0:
                return None
            elif len(self._text.items) == 1:
                values_view = self._text.items.values()
                value_iterator = iter(values_view)
                first_value = next(value_iterator)
                return first_value['content']
            else:
                return self._text.items
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        self._code = value

    def has_content_(self):
        if self._text:
            return True
        else:
            return False

    def build_attributes(self, node, attrs, already_processed):
        value = find_attr_value_('Code', node)
        if value is not None and 'Code' not in already_processed:
            already_processed.add('Code')
            self._code = value

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Text':
            obj_ = LocalisedString.factory()
            obj_.build(child_, gds_collector_=gds_collector_)
            if self._text is None:
                self._text = InternationalString()
            self._text.addLocalisedString(obj_)


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

    @staticmethod
    def factory(*args_, **kwargs_):
        return CodedStatusMessageType(*args_, **kwargs_)
# end class CodedStatusMessageType
