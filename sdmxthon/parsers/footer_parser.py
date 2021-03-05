from .data_parser import DataParser, Validate_simpletypes_
from ..model.status_message import CodedStatusMessageType
from ..utils.xml_base import find_attr_value_


class FooterType(DataParser):
    """FooterType describes the structure of a message footer. The footer is
    used to convey any error, information, or warning messages. This is to
    be used when the message has payload, but also needs to communicate
    additional information. If an error occurs and no payload is generated,
    an Error message should be returned."""
    __hash__ = DataParser.__hash__
    subclass = None
    superclass = None

    def __init__(self, Message=None, gds_collector_=None, **kwargs_):
        super(FooterType, self).__init__(gds_collector_)
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if Message is None:
            self._message = []
        else:
            self._message = Message
        self._message_nsprefix_ = None

    @staticmethod
    def factory(*args_, **kwargs_):
        return FooterType(*args_, **kwargs_)

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        if value is None:
            self._message = []
        elif isinstance(value, list):
            self._message = value
        else:
            raise TypeError('Message must be a list')

    def add_Message(self, value):
        self._message.append(value)

    def insert_Message_at(self, index, value):
        self._message.insert(index, value)

    def replace_Message_at(self, index, value):
        self._message[index] = value

    def has_content_(self):
        if (
                self._message
        ):
            return True
        else:
            return False

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Message':
            obj_ = FooterMessageType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._message.append(obj_)
            obj_.original_tagname_ = 'Message'


# end class FooterType

class FooterMessageType(CodedStatusMessageType):
    """FooterMessageType defines the structure of a message that is contained
    in the footer of a message. It is a status message that have a severity
    code of Error, Information, or Warning added to it."""
    __hash__ = DataParser.__hash__
    subclass = None
    superclass = CodedStatusMessageType

    def __init__(self, code=None, Text=None, severity=None, gds_collector_=None, **kwargs_):
        super(FooterMessageType, self).__init__(code, Text, gds_collector_, **kwargs_)
        self._severity = severity

    @staticmethod
    def factory(*args_, **kwargs_):
        return FooterMessageType(*args_, **kwargs_)

    @property
    def severity(self):
        return self._severity

    @severity.setter
    def severity(self, value):
        self._severity = value

    def validate_SeverityCodeType(self, value):
        # Validate dim_type SeverityCodeType, a restriction on xs:string.
        result = True
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{value}": {lineno} is not of the correct base simple dim_type (str)')
                return False
            value = value
            enumerations = ['Error', 'Warning', 'Information']
            if value not in enumerations:
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{value}": {lineno} does not match xsd enumeration restriction')
                result = False
        return result

    def export_attributes_as_dict(self, parent_dict: dict, data: list, valid_fields: list):
        pass

    def build_attributes(self, node, attrs, already_processed):
        value = find_attr_value_('severity', node)
        if value is not None and 'severity' not in already_processed:
            already_processed.add('severity')
            self.severity = value
            self.validate_SeverityCodeType(self.severity)
        super(FooterMessageType, self).build_attributes(node, attrs, already_processed)
# end class FooterMessageType
