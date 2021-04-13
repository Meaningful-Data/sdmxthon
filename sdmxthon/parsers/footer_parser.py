"""
    Footer_parser file define the classes for parsing the footer of a Message
"""

from SDMXThon.parsers.status_message import CodedStatusMessageType
from SDMXThon.utils.xml_base import find_attr_value_
from .data_parser import DataParser, Validate_simpletypes_


class FooterType(DataParser):
    """FooterType describes the structure of a message footer. The footer is
    used to convey any error, information, or warning messages. This is to
    be used when the message has payload, but also needs to communicate
    additional information. If an error occurs and no payload is generated,
    an Error message should be returned."""

    def __init__(self, Message=None, gds_collector_=None):
        super(FooterType, self).__init__(gds_collector_)
        self.gds_collector_ = gds_collector_
        if Message is None:
            self._message = []
        else:
            self._message = Message
        self._message_nsprefix_ = None

    @staticmethod
    def _factory(*args_, **kwargs_):
        """Factory Method of FooterType"""
        return FooterType(*args_, **kwargs_)

    @property
    def message(self):
        """Message at the footer"""
        return self._message

    @message.setter
    def message(self, value):
        if value is None:
            self._message = []
        elif isinstance(value, list):
            self._message = value
        else:
            raise TypeError('Message must be a list')

    def _build_children(self, child_, node, nodeName_, fromsubclass_=False,
                        gds_collector_=None):
        """Builds the childs of the XML element"""
        if nodeName_ == 'Message':
            obj_ = FooterMessageType._factory()
            obj_._build(child_, gds_collector_=gds_collector_)
            self._message.append(obj_)


# end class FooterType

class FooterMessageType(CodedStatusMessageType):
    """FooterMessageType defines the structure of a message that is contained
    in the footer of a message. It is a status message that have a severity
    code of Error, Information, or Warning added to it."""
    __hash__ = DataParser.__hash__
    subclass = None
    superclass = CodedStatusMessageType

    def __init__(self, code=None, Text=None, severity=None,
                 gds_collector_=None, **kwargs_):
        super(FooterMessageType, self).__init__(code, Text, gds_collector_,
                                                **kwargs_)
        self._severity = severity

    @staticmethod
    def _factory(*args_, **kwargs_):

        """Factory Method of FooterMessageType"""
        return FooterMessageType(*args_, **kwargs_)

    @property
    def severity(self):
        """Severity code (Error, Information or Warning)"""
        return self._severity

    @severity.setter
    def severity(self, value):
        if self._validate_SeverityCodeType(value):
            self._severity = value

    def _validate_SeverityCodeType(self, value):
        """Validate dim_type SeverityCodeType, a restriction on xs:string."""
        result = True
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self._gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{value}": {lineno} is not of the correct '
                    f'base simple dim_type (str)')
                return False
            value = value
            enumerations = ['Error', 'Warning', 'Information']
            if value not in enumerations:
                lineno = self._gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    f'Value "{value}": {lineno} does not match xsd '
                    f'enumeration restriction')
                result = False
        return result

    def _build_attributes(self, node, attrs, already_processed):
        """Builds the attributes present in the XML element"""
        value = find_attr_value_('severity', node)
        if value is not None and 'severity' not in already_processed:
            already_processed.add('severity')
            self.severity = value
            self._validate_SeverityCodeType(self.severity)
        super(FooterMessageType, self)._build_attributes(node, attrs,
                                                         already_processed)
# end class FooterMessageType
