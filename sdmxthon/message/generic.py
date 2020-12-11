from .footer import FooterType
from ..common.annotations import TextType
from ..common.generic import GenericDataStructureType
from ..common.references import DataProviderReferenceType, DataStructureReferenceType
from ..data.generic import DataSetType as GenericDataSet, TimeSeriesDataSetType as GenericTimeSeriesDataSet
from ..structure.specificbase import DataSetType as StructureDataSet, \
    TimeSeriesDataSetType as StructureTimeSeriesDataSet

from ..utils.data_parser import DataParser, UseCapturedNS_, Validate_simpletypes_
from ..utils.generateds import datetime_
from ..utils.mappings import ClassToPrefix
from ..utils.xml_base import BaseStrType_, encode_str_2_3, showIndent, quote_xml, find_attr_value_, _cast, \
    quote_attrib, GdsCollector_


class ContactType(DataParser):
    """ContactType provides defines the contact information about a party."""
    __hash__ = DataParser.__hash__
    subclass = None
    superclass = None

    def __init__(self, Name=None, Department=None, Role=None, Telephone=None, Fax=None, X400=None, URI=None, Email=None,
                 gds_collector_=None, **kwargs_):
        super(ContactType, self).__init__(gds_collector_, kwargs_)
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.parent_object_ = kwargs_.get('parent_object_')

        if Name is None:
            self._Name = []
        else:
            self._Name = Name

        self._name_nsprefix_ = None

        if Department is None:
            self._department = []
        else:
            self._department = Department

        self._department_nsprefix_ = None

        if Role is None:
            self._role = []
        else:
            self._role = Role

        self._role_nsprefix_ = None

        if Telephone is None:
            self._telephone = []
        else:
            self._telephone = Telephone

        self._telephone_nsprefix_ = None

        if Fax is None:
            self._fax = []
        else:
            self._fax = Fax

        self._fax_nsprefix_ = None

        if X400 is None:
            self._x400 = []
        else:
            self._x400 = X400

        self._x400_nsprefix_ = None

        if URI is None:
            self._uri = []
        else:
            self._uri = URI

        self.URI_nsprefix_ = None

        if Email is None:
            self._email = []
        else:
            self._email = Email

        self._email_nsprefix_ = None
        self._namespacedef = 'xmlns:message="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message"'
        self._namespaceprefix = 'message'
        self._name = 'ContactType'

    def factory(*args_, **kwargs_):
        return ContactType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_Name(self):
        return self._Name

    def set_Name(self, Name):
        self._Name = Name

    def add_Name(self, value):
        self._Name.append(value)

    def insert_Name_at(self, index, value):
        self._Name.insert(index, value)

    def replace_Name_at(self, index, value):
        self._Name[index] = value

    def get_Department(self):
        return self._department

    def set_Department(self, Department):
        self._department = Department

    def add_Department(self, value):
        self._department.append(value)

    def insert_Department_at(self, index, value):
        self._department.insert(index, value)

    def replace_Department_at(self, index, value):
        self._department[index] = value

    def get_Role(self):
        return self._role

    def set_Role(self, Role):
        self._role = Role

    def add_Role(self, value):
        self._role.append(value)

    def insert_Role_at(self, index, value):
        self._role.insert(index, value)

    def replace_Role_at(self, index, value):
        self._role[index] = value

    def get_Telephone(self):
        return self._telephone

    def set_Telephone(self, Telephone):
        self._telephone = Telephone

    def add_Telephone(self, value):
        self._telephone.append(value)

    def insert_Telephone_at(self, index, value):
        self._telephone.insert(index, value)

    def replace_Telephone_at(self, index, value):
        self._telephone[index] = value

    def get_Fax(self):
        return self._fax

    def set_Fax(self, Fax):
        self._fax = Fax

    def add_Fax(self, value):
        self._fax.append(value)

    def insert_Fax_at(self, index, value):
        self._fax.insert(index, value)

    def replace_Fax_at(self, index, value):
        self._fax[index] = value

    def get_X400(self):
        return self._x400

    def set_X400(self, X400):
        self._x400 = X400

    def add_X400(self, value):
        self._x400.append(value)

    def insert_X400_at(self, index, value):
        self._x400.insert(index, value)

    def replace_X400_at(self, index, value):
        self._x400[index] = value

    def get_URI(self):
        return self._uri

    def set_URI(self, URI):
        self._uri = URI

    def add_URI(self, value):
        self._uri.append(value)

    def insert_URI_at(self, index, value):
        self._uri.insert(index, value)

    def replace_URI_at(self, index, value):
        self._uri[index] = value

    def get_Email(self):
        return self._email

    def set_Email(self, Email):
        self._email = Email

    def add_Email(self, value):
        self._email.append(value)

    def insert_Email_at(self, index, value):
        self._email.insert(index, value)

    def replace_Email_at(self, index, value):
        self._email[index] = value

    def has_content_(self):
        if (
                self._Name or
                self._department or
                self._role or
                self._telephone or
                self._fax or
                self._x400 or
                self._uri or
                self._email
        ):
            return True
        else:
            return False

    def export_children(self, outfile, level, pretty_print=True, has_parent=True, **kwargs):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for Name_ in self._Name:
            Name_.export(outfile, level, pretty_print=pretty_print, has_parent=has_parent)

        for Department_ in self._department:
            Department_.export(outfile, level, pretty_print=pretty_print, has_parent=has_parent)

        for Role_ in self._role:
            Role_.export(outfile, level, pretty_print=pretty_print, has_parent=has_parent)

        for Telephone_ in self._telephone:
            namespaceprefix_ = self._telephone_nsprefix_ + ':' if (UseCapturedNS_ and self._telephone_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTelephone>%s</%sTelephone>%s' % (
                namespaceprefix_,
                self.gds_encode(self.gds_format_string(quote_xml(Telephone_), input_name='Telephone')),
                namespaceprefix_, eol_))

        for Fax_ in self._fax:
            namespaceprefix_ = self._fax_nsprefix_ + ':' if (UseCapturedNS_ and self._fax_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sFax>%s</%sFax>%s' % (
                namespaceprefix_, self.gds_encode(self.gds_format_string(quote_xml(Fax_), input_name='Fax')),
                namespaceprefix_, eol_))

        for X400_ in self._x400:
            namespaceprefix_ = self._x400_nsprefix_ + ':' if (UseCapturedNS_ and self._x400_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sX400>%s</%sX400>%s' % (
                namespaceprefix_, self.gds_encode(self.gds_format_string(quote_xml(X400_), input_name='X400')),
                namespaceprefix_, eol_))

        for URI_ in self._uri:
            namespaceprefix_ = self.URI_nsprefix_ + ':' if (UseCapturedNS_ and self.URI_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sURI>%s</%sURI>%s' % (
                namespaceprefix_, self.gds_encode(self.gds_format_string(quote_xml(URI_), input_name='URI')),
                namespaceprefix_, eol_))

        for Email_ in self._email:
            namespaceprefix_ = self._email_nsprefix_ + ':' if (UseCapturedNS_ and self._email_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEmail>%s</%sEmail>%s' % (
                namespaceprefix_, self.gds_encode(self.gds_format_string(quote_xml(Email_), input_name='Email')),
                namespaceprefix_, eol_))

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Name':
            class_obj_ = self.get_class_obj_(child_, TextType)
            obj_ = class_obj_.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._Name.append(obj_)
            obj_.original_tag_name_ = 'Name'

        elif nodeName_ == 'Department':
            class_obj_ = self.get_class_obj_(child_, TextType)
            obj_ = class_obj_.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._department.append(obj_)
            obj_.original_tag_name_ = 'Department'

        elif nodeName_ == 'Role':
            class_obj_ = self.get_class_obj_(child_, TextType)
            obj_ = class_obj_.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._role.append(obj_)
            obj_.original_tag_name_ = 'Role'

        elif nodeName_ == 'Telephone':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Telephone')
            value_ = self.gds_validate_string(value_, node, 'Telephone')
            self._telephone.append(value_)
            self._telephone_nsprefix_ = child_.prefix

        elif nodeName_ == 'Fax':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Fax')
            value_ = self.gds_validate_string(value_, node, 'Fax')
            self._fax.append(value_)
            self._fax_nsprefix_ = child_.prefix

        elif nodeName_ == 'X400':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'X400')
            value_ = self.gds_validate_string(value_, node, 'X400')
            self._x400.append(value_)
            self._x400_nsprefix_ = child_.prefix

        elif nodeName_ == 'URI':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'URI')
            value_ = self.gds_validate_string(value_, node, 'URI')
            self._uri.append(value_)
            self.URI_nsprefix_ = child_.prefix

        elif nodeName_ == 'Email':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Email')
            value_ = self.gds_validate_string(value_, node, 'Email')
            self._email.append(value_)
            self._email_nsprefix_ = child_.prefix


# end class ContactType

class PartyType(DataParser):
    """PartyType defines the information which is sent about various parties
    such as senders and receivers of messages.The id attribute holds the
    identification of the party."""
    __hash__ = DataParser.__hash__
    subclass = None
    superclass = None

    def __init__(self, id_=None, Name=None, Contact=None, extensiontype_=None, gds_collector_=None, **kwargs_):
        super(PartyType, self).__init__(gds_collector_, **kwargs_)
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self._id = _cast(None, id_)
        self._id_nsprefix_ = None

        if Name is None:
            self._Name = []
        else:
            self._Name = Name

        self._name_nsprefix_ = None

        if Contact is None:
            self.Contact = []
        else:
            self.Contact = Contact

        self.Contact_nsprefix_ = None
        self._extensiontype_ = extensiontype_
        self._namespacedef = 'xmlns:message="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message"'
        self._namespaceprefix = 'message'

    def factory(*args_, **kwargs_):
        return PartyType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_Name(self):
        return self._Name

    def set_Name(self, Name):
        self._Name = Name

    def add_Name(self, value):
        self._Name.append(value)

    def insert_Name_at(self, index, value):
        self._Name.insert(index, value)

    def replace_Name_at(self, index, value):
        self._Name[index] = value

    def get_Contact(self):
        return self.Contact

    def set_Contact(self, Contact):
        self.Contact = Contact

    def add_Contact(self, value):
        self.Contact.append(value)

    def insert_Contact_at(self, index, value):
        self.Contact.insert(index, value)

    def replace_Contact_at(self, index, value):
        self.Contact[index] = value

    def get_id(self):
        return self._id

    def set_id(self, id_):
        self._id = id_

    def get_extensiontype_(self):
        return self._extensiontype_

    def set_extensiontype_(self, extensiontype_):
        self._extensiontype_ = extensiontype_

    def has_content_(self):
        if (
                self._Name or
                self.Contact
        ):
            return True
        else:
            return False

    def export_attributes(self, outfile, level, already_processed, namespace_prefix_='', name_='PartyType'):
        if self._id is not None and 'id' not in already_processed:
            already_processed.add('id')
            outfile.write(' id=%s' % (quote_attrib(self._id),))

        if self._extensiontype_ is not None and 'xsi:dim_type' not in already_processed:
            already_processed.add('xsi:dim_type')
            outfile.write(' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
            if ":" not in self._extensiontype_:
                imported_ns_type_prefix_ = ClassToPrefix.get(self._extensiontype_, '')
                outfile.write(' xsi:dim_type="%s%s"' % (imported_ns_type_prefix_, self._extensiontype_))
            else:
                outfile.write(' xsi:dim_type="%s"' % self._extensiontype_)

    def export_attributes_as_dict(self, parent_dict: dict, data: list, valid_fields: list):
        pass

    def export_children(self, outfile, level, pretty_print=True, has_parent=True, **kwargs):
        for Name_ in self._Name:
            Name_.export(outfile, level, pretty_print=pretty_print, has_parent=has_parent)

        for Contact_ in self.Contact:
            Contact_.export(outfile, level, pretty_print=pretty_print, has_parent=has_parent)

    def build_attributes(self, node, attrs, already_processed):
        value = find_attr_value_('id', node)
        if value is not None and 'id' not in already_processed:
            already_processed.add('id')
            self._id = value
            self.validate_id_type(self._id)  # validate dim_type IDType
        value = find_attr_value_('xsi:dim_type', node)
        if value is not None and 'xsi:dim_type' not in already_processed:
            already_processed.add('xsi:dim_type')
            self._extensiontype_ = value

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Name':
            class_obj_ = self.get_class_obj_(child_, TextType)
            obj_ = class_obj_.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._Name.append(obj_)
            obj_.original_tag_name_ = 'Name'
        elif nodeName_ == 'Contact':
            obj_ = ContactType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Contact.append(obj_)
            obj_.original_tag_name_ = 'Contact'


# end class PartyType

class SenderType(PartyType):
    """SenderType extends the basic party structure to add an optional time
    zone declaration."""
    __hash__ = PartyType.__hash__
    subclass = None
    superclass = PartyType

    def __init__(self, id_=None, Name=None, Contact=None, Timezone=None, gds_collector_=None, **kwargs_):
        super(SenderType, self).__init__(id_, Name, Contact, gds_collector_, **kwargs_)
        self.Timezone = Timezone
        self.validate_TimezoneType(self.Timezone)
        self.Timezone_nsprefix_ = None
        self._namespacedef = 'xmlns:message="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message" xmlns:common="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common" '
        self._name = 'SenderType'

    def factory(*args_, **kwargs_):
        return SenderType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_Timezone(self):
        return self.Timezone

    def set_Timezone(self, Timezone):
        self.Timezone = Timezone

    def validate_TimezoneType(self, value):
        result = True
        # Validate dim_type TimezoneType, a restriction on xs:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple dim_type (str)' % {"value": value,
                                                                                                      "lineno": lineno,
                                                                                                      })
                return False
            if not self.gds_validate_simple_patterns(
                    self.validate_TimezoneType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (
                    encode_str_2_3(value), self.validate_TimezoneType_patterns_,))
                result = False
        return result

    validate_TimezoneType_patterns_ = [['^(Z)$', '^((\\+|\\-)(14:00|((0[0-9]|1[0-3]):[0-5][0-9])))$']]

    def has_content_(self):
        if (
                self.Timezone is not None or
                super(SenderType, self).has_content_()
        ):
            return True
        else:
            return False

    def export_attributes(self, outfile, level, already_processed, namespace_prefix_='', name_='SenderType'):
        super(SenderType, self).export_attributes(outfile, level, already_processed, namespace_prefix_,
                                                  name_='SenderType')

    def export_children(self, outfile, level, pretty_print=True, has_parent=True, **kwargs):
        super(SenderType, self).export_children(outfile, level, pretty_print=pretty_print)
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Timezone is not None:
            namespaceprefix_ = self.Timezone_nsprefix_ + ':' if (UseCapturedNS_ and self.Timezone_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTimezone>%s</%sTimezone>%s' % (
                namespaceprefix_,
                self.gds_encode(self.gds_format_string(quote_xml(self.Timezone), input_name='Timezone')),
                namespaceprefix_, eol_))

    def build_attributes(self, node, attrs, already_processed):
        super(SenderType, self).build_attributes(node, attrs, already_processed)

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Timezone':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Timezone')
            value_ = self.gds_validate_string(value_, node, 'Timezone')
            self.Timezone = value_
            self.Timezone_nsprefix_ = child_.prefix
            # validate dim_type TimezoneType
            self.validate_TimezoneType(self.Timezone)
        super(SenderType, self).build_children(child_, node, nodeName_, True)


# end class SenderType

class BaseHeaderType(DataParser):
    """BaseHeaderType in an abstract base dim_type that defines the basis for all
    message headers. Specific message formats will refine this"""
    __hash__ = DataParser.__hash__
    subclass = None
    superclass = None

    def __init__(self, ID=None, Test=False, Prepared=None, Sender=None, Receiver=None, Name=None, Structure=None,
                 DataProvider=None, DataSetAction=None, DataSetID=None, Extracted=None, ReportingBegin=None,
                 ReportingEnd=None, EmbargoDate=None, Source=None, gds_collector_=None, **kwargs_):
        super(BaseHeaderType, self).__init__(gds_collector_, **kwargs_)
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self._ID = ID
        self.validate_id_type(self._ID)
        self._ID_nsprefix_ = "message"
        self._Test = Test
        self._Test_nsprefix_ = "message"
        self._Prepared = Prepared
        self.validate_HeaderTimeType(self._Prepared)
        self._Prepared_nsprefix_ = "message"
        self._Sender = Sender
        self._Sender_nsprefix_ = "message"

        if Receiver is None:
            self._Receiver = []
        else:
            self._Receiver = Receiver

        self._Receiver_nsprefix_ = None

        if Name is None:
            self._Name = []
        else:
            self._Name = Name

        self._name_nsprefix_ = None

        if Structure is None:
            self._structure = []
        else:
            self._structure = Structure

        self._structure_nsprefix_ = None
        self._dataProvider = DataProvider
        self._dataProvider_nsprefix_ = None
        self._DataSetAction = DataSetAction
        self.validate_ActionType(self._DataSetAction)
        self.DataSetAction_nsprefix_ = None

        if DataSetID is None:
            self._DataSetID = []
        else:
            self._DataSetID = DataSetID

        self._DataSetID_nsprefix_ = None

        if isinstance(Extracted, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(Extracted, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = Extracted

        self._Extracted = initvalue_
        self._Extracted_nsprefix_ = None
        self._ReportingBegin = ReportingBegin
        self.validate_ObservationalTimePeriodType(self._ReportingBegin)
        self._ReportingBegin_nsprefix_ = None
        self._ReportingEnd = ReportingEnd
        self.validate_ObservationalTimePeriodType(self._ReportingEnd)
        self._ReportingEnd_nsprefix_ = None

        if isinstance(EmbargoDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(EmbargoDate, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = EmbargoDate

        self._EmbargoDate = initvalue_
        self._EmbargoDate_nsprefix_ = None

        if Source is None:
            self._Source = []
        else:
            self._Source = Source

        self._Source_nsprefix_ = None
        self._namespacedef = 'xmlns:message="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message"'
        self._namespace_prefix = 'message'
        self._name = 'BaseHeaderType'

    def factory(*args_, **kwargs_):
        return BaseHeaderType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_ID(self):
        return self._ID

    def set_ID(self, ID):
        self._ID = ID

    def get_Test(self):
        return self._Test

    def set_Test(self, Test):
        self._Test = Test

    def get_Prepared(self):
        return self._Prepared

    def set_Prepared(self, Prepared):
        self._Prepared = Prepared

    def get_Sender(self):
        return self._Sender

    def set_Sender(self, Sender):
        self._Sender = Sender
        self._Sender._namespace_prefix = 'message'

    def get_Receiver(self):
        return self._Receiver

    def set_Receiver(self, Receiver):
        self._Receiver = Receiver

    def add_Receiver(self, value):
        value._namespace_prefix = 'message'
        self._Receiver.append(value)

    def insert_Receiver_at(self, index, value):
        value._namespace_prefix = 'message'
        self._Receiver.insert(index, value)

    def replace_Receiver_at(self, index, value):
        value._namespace_prefix = 'message'
        self._Receiver[index] = value

    def get_Name(self):
        return self._Name

    def set_Name(self, Name):
        self._Name = Name

    def add_Name(self, value):
        self._Name.append(value)

    def insert_Name_at(self, index, value):
        value._namespace_prefix = 'message'
        self._Name.insert(index, value)

    def replace_Name_at(self, index, value):
        value._namespace_prefix = 'message'
        self._Name[index] = value

    def get_Structure(self):
        return self._structure

    def set_Structure(self, Structure):
        self._structure = Structure

    def add_Structure(self, value):
        value._namespace_prefix = 'message'
        self._structure.append(value)

    def insert_Structure_at(self, index, value):
        value._namespace_prefix = 'message'
        self._structure.insert(index, value)

    def replace_Structure_at(self, index, value):
        self._structure[index] = value

    def get_DataProvider(self):
        return self._dataProvider

    def set_DataProvider(self, DataProvider):
        self._dataProvider = DataProvider

    def get_DataSetAction(self):
        return self._DataSetAction

    def set_DataSetAction(self, DataSetAction):
        self._DataSetAction = DataSetAction

    def get_DataSetID(self):
        return self._DataSetID

    def set_DataSetID(self, DataSetID):
        self._DataSetID = DataSetID

    def add_DataSetID(self, value):
        self._DataSetID.append(value)

    def insert_DataSetID_at(self, index, value):
        self._DataSetID.insert(index, value)

    def replace_DataSetID_at(self, index, value):
        self._DataSetID[index] = value

    def get_Extracted(self):
        return self._Extracted

    def set_Extracted(self, Extracted):
        self._Extracted = Extracted

    def get_ReportingBegin(self):
        return self._ReportingBegin

    def set_ReportingBegin(self, ReportingBegin):
        self._ReportingBegin = ReportingBegin

    def get_ReportingEnd(self):
        return self._ReportingEnd

    def set_ReportingEnd(self, ReportingEnd):
        self._ReportingEnd = ReportingEnd

    def get_EmbargoDate(self):
        return self._EmbargoDate

    def set_EmbargoDate(self, EmbargoDate):
        self._EmbargoDate = EmbargoDate

    def get_Source(self):
        return self._Source

    def set_Source(self, Source):
        self._Source = Source

    def add_Source(self, value):
        self._Source.append(value)

    def insert_Source_at(self, index, value):
        self._Source.insert(index, value)

    def replace_Source_at(self, index, value):
        self._Source[index] = value

    def validate_HeaderTimeType(self, value):
        result = True
        # Validate dim_type HeaderTimeType, a restriction on None.
        pass
        return result

    def validate_ActionType(self, value):
        result = True
        # Validate dim_type ActionType, a restriction on xs:NMTOKEN.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_line_number_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple dim_type (str)' % {"value": value,
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

    def validate_ObservationalTimePeriodType(self, value):
        pass

    def has_content_(self):
        if (
                self._ID is not None or
                self._Test or
                self._Prepared is not None or
                self._Sender is not None or
                self._Receiver or
                self._Name or
                self._structure or
                self._dataProvider is not None or
                self._DataSetAction is not None or
                self._DataSetID or
                self._Extracted is not None or
                self._ReportingBegin is not None or
                self._ReportingEnd is not None or
                self._EmbargoDate is not None or
                self._Source
        ):
            return True
        else:
            return False

    def export_children(self, outfile, level, pretty_print=True, has_parent=True, **kwargs):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self._ID is not None:
            namespaceprefix_ = self._ID_nsprefix_ + ':' if (UseCapturedNS_ and self._ID_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sID>%s</%sID>%s' % (
                namespaceprefix_, self.gds_encode(self.gds_format_string(quote_xml(self._ID), input_name='ID')),
                namespaceprefix_, eol_))
        if self._Test is not None:
            namespaceprefix_ = self._Test_nsprefix_ + ':' if (UseCapturedNS_ and self._Test_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sTest>%s</%sTest>%s' % (
                namespaceprefix_, self.gds_format_boolean(self._Test, input_name='Test'), namespaceprefix_, eol_))
        if self._Prepared is not None:
            namespaceprefix_ = self._Prepared_nsprefix_ + ':' if (UseCapturedNS_ and self._Prepared_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            self._Prepared = self._Prepared.strftime("%Y-%m-%dT%H:%M:%S")
            outfile.write('<%sPrepared>%s</%sPrepared>%s' % (
                namespaceprefix_,
                self.gds_encode(self.gds_format_string(quote_xml(self._Prepared), input_name='Prepared')),
                namespaceprefix_, eol_))
        if self._Sender is not None:
            self._Sender.export(outfile, level, pretty_print=pretty_print, has_parent=has_parent)
        for Receiver_ in self._Receiver:
            Receiver_.export(outfile, level, pretty_print=pretty_print, has_parent=has_parent)
        for Name_ in self._Name:
            Name_.export(outfile, level, pretty_print=pretty_print, has_parent=has_parent)
        for Structure_ in self._structure:
            Structure_.export(outfile, level, pretty_print=pretty_print, has_parent=has_parent)
        if self._dataProvider is not None:
            self._dataProvider.export(outfile, level, pretty_print=pretty_print, has_parent=has_parent)
        if self._DataSetAction is not None:
            namespaceprefix_ = self.DataSetAction_nsprefix_ + ':' if (
                    UseCapturedNS_ and self.DataSetAction_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDataSetAction>%s</%sDataSetAction>%s' % (namespaceprefix_, self.gds_encode(
                self.gds_format_string(quote_xml(self._DataSetAction), input_name='DataSetAction')), namespaceprefix_,
                                                                       eol_))
        for DataSetID_ in self._DataSetID:
            namespaceprefix_ = self._DataSetID_nsprefix_ + ':' if (UseCapturedNS_ and self._DataSetID_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDataSetID>%s</%sDataSetID>%s' % (
                namespaceprefix_,
                self.gds_encode(self.gds_format_string(quote_xml(DataSetID_), input_name='DataSetID')),
                namespaceprefix_, eol_))
        if self._Extracted is not None:
            namespaceprefix_ = self._Extracted_nsprefix_ + ':' if (UseCapturedNS_ and self._Extracted_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sExtracted>%s</%sExtracted>%s' % (
                namespaceprefix_, self.gds_format_datetime(self._Extracted, input_name='Extracted'), namespaceprefix_,
                eol_))
        if self._ReportingBegin is not None:
            namespaceprefix_ = self._ReportingBegin_nsprefix_ + ':' if (
                    UseCapturedNS_ and self._ReportingBegin_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sReportingBegin>%s</%sReportingBegin>%s' % (namespaceprefix_, self.gds_encode(
                self.gds_format_string(quote_xml(self._ReportingBegin), input_name='ReportingBegin')), namespaceprefix_,
                                                                         eol_))
        if self._ReportingEnd is not None:
            namespaceprefix_ = self._ReportingEnd_nsprefix_ + ':' if (
                    UseCapturedNS_ and self._ReportingEnd_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sReportingEnd>%s</%sReportingEnd>%s' % (namespaceprefix_, self.gds_encode(
                self.gds_format_string(quote_xml(self._ReportingEnd), input_name='ReportingEnd')), namespaceprefix_,
                                                                     eol_))
        if self._EmbargoDate is not None:
            namespaceprefix_ = self._EmbargoDate_nsprefix_ + ':' if (
                    UseCapturedNS_ and self._EmbargoDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sEmbargoDate>%s</%sEmbargoDate>%s' % (
                namespaceprefix_, self.gds_format_datetime(self._EmbargoDate, input_name='EmbargoDate'),
                namespaceprefix_,
                eol_))
        for Source_ in self._Source:
            namespaceprefix_ = self._Source_nsprefix_ + ':' if (UseCapturedNS_ and self._Source_nsprefix_) else ''
            Source_.export(outfile, level, pretty_print=pretty_print, has_parent=has_parent)

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'ID':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ID')
            value_ = self.gds_validate_string(value_, node, 'ID')
            self._ID = value_
            self._ID_nsprefix_ = child_.prefix
            # validate dim_type IDType
            self.validate_id_type(self._ID)
        elif nodeName_ == 'Test':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'Test')
            ival_ = self.gds_validate_boolean(ival_, node, 'Test')
            self._Test = ival_
            self._Test_nsprefix_ = child_.prefix
        elif nodeName_ == 'Prepared':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Prepared')
            value_ = self.gds_validate_string(value_, node, 'Prepared')
            self._Prepared = value_
            self._Prepared_nsprefix_ = child_.prefix
            # validate dim_type HeaderTimeType
            self.validate_HeaderTimeType(self._Prepared)
        elif nodeName_ == 'Sender':
            obj_ = SenderType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._Sender = obj_
            obj_.original_tagname_ = 'Sender'
        elif nodeName_ == 'Receiver':
            class_obj_ = self.get_class_obj_(child_, PartyType)
            obj_ = class_obj_.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._Receiver.append(obj_)
            obj_.original_tag_name_ = 'Receiver'
        elif nodeName_ == 'Name':
            class_obj_ = self.get_class_obj_(child_, TextType)
            obj_ = class_obj_.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._Name.append(obj_)
            obj_.original_tag_name_ = 'Name'
        elif nodeName_ == '_structure':
            obj_ = GenericDataStructureType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._structure.append(obj_)
            obj_.original_tag_name_ = '_structure'
        elif nodeName_ == 'Structure':
            obj_ = DataStructureReferenceType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._structure.append(obj_)
            obj_.original_tag_name_ = 'Structure'
        elif nodeName_ == 'DataProvider':
            obj_ = DataProviderReferenceType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._dataProvider = obj_
            obj_.original_tag_name_ = 'DataProvider'
        elif nodeName_ == 'DataSetAction':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DataSetAction')
            value_ = self.gds_validate_string(value_, node, 'DataSetAction')
            self._DataSetAction = value_
            self.DataSetAction_nsprefix_ = child_.prefix
            # validate dim_type ActionType
            self.validate_ActionType(self._DataSetAction)
        elif nodeName_ == 'DataSetID':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DataSetID')
            value_ = self.gds_validate_string(value_, node, 'DataSetID')
            self._DataSetID.append(value_)
            self._DataSetID_nsprefix_ = child_.prefix
            # validate dim_type IDType
            self.validate_id_type(self._DataSetID[-1])
        elif nodeName_ == 'Extracted':
            sval_ = child_.text
            dval_ = self.gds_parse_datetime(sval_)
            self._Extracted = dval_
            self._Extracted_nsprefix_ = child_.prefix
        elif nodeName_ == 'ReportingBegin':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ReportingBegin')
            value_ = self.gds_validate_string(value_, node, 'ReportingBegin')
            self._ReportingBegin = value_
            self._ReportingBegin_nsprefix_ = child_.prefix
            # validate dim_type ObservationalTimePeriodType
            self.validate_ObservationalTimePeriodType(self._ReportingBegin)
        elif nodeName_ == 'ReportingEnd':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ReportingEnd')
            value_ = self.gds_validate_string(value_, node, 'ReportingEnd')
            self._ReportingEnd = value_
            self._ReportingEnd_nsprefix_ = child_.prefix
            # validate dim_type ObservationalTimePeriodType
            self.validate_ObservationalTimePeriodType(self._ReportingEnd)
        elif nodeName_ == 'EmbargoDate':
            sval_ = child_.text
            dval_ = self.gds_parse_datetime(sval_)
            self._EmbargoDate = dval_
            self._EmbargoDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'Source':
            class_obj_ = self.get_class_obj_(child_, TextType)
            obj_ = class_obj_.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self._Source.append(obj_)
            obj_.original_tag_name_ = 'Source'


# end class BaseHeaderType

class GenericDataHeaderType(BaseHeaderType):
    """GenericDataHeaderType defines the header structure for a generic data
    message."""
    __hash__ = DataParser.__hash__
    subclass = None
    superclass = BaseHeaderType

    def __init__(self, ID=None, Test=False, Prepared=None, Sender=None, Receiver=None, Name=None, Structure=None,
                 DataProvider=None, DataSetAction=None, DataSetID=None, Extracted=None, ReportingBegin=None,
                 ReportingEnd=None, EmbargoDate=None, Source=None, gds_collector_=None, **kwargs_):
        super(GenericDataHeaderType, self).__init__(ID, Test, Prepared, Sender, Receiver, Name, Structure, DataProvider,
                                                    DataSetAction, DataSetID, Extracted, ReportingBegin, ReportingEnd,
                                                    EmbargoDate, Source, gds_collector_, **kwargs_)
        self._name = 'GenericDataHeaderType'

    def factory(*args_, **kwargs_):
        return GenericDataHeaderType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def validate_ObservationalTimePeriodType(self, value):
        pass


# end class GenericDataHeaderType

class MessageType(DataParser):
    """MessageType is an abstract dim_type which is used by all of the messages, to
    allow inheritance of common features. Every message consists of a
    mandatory header, followed by optional payload (which may occur
    multiple times), and finally an optional footer section for conveying
    error, warning, and informational messages."""
    __hash__ = DataParser.__hash__
    subclass = None
    superclass = None

    def __init__(self, Header=None, anytypeobjs_=None, Footer=None, gds_collector_=None, **kwargs_):
        super(MessageType, self).__init__(gds_collector_, **kwargs_)
        self._anytypeobjs_ = None
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Header = Header
        self.Header_nsprefix_ = None
        if anytypeobjs_ is None:
            self.anytypeobjs_ = []
        else:
            self.anytypeobjs_ = anytypeobjs_
        self.Footer = Footer
        self.Footer_nsprefix_ = None
        self._namespace_def = 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:message="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message" xmlns:data="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/structurespecific" xmlns:common="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common"'
        self._namespace_prefix = 'message'
        self._name = 'MessageType'

    def factory(*args_, **kwargs_):
        return MessageType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_Header(self):
        return self.Header

    def set_Header(self, Header):
        self.Header = Header

    def get_anytypeobjs_(self):
        return self.anytypeobjs_

    def set_anytypeobjs_(self, anytypeobjs_):
        self.anytypeobjs_ = anytypeobjs_

    def add_anytypeobjs_(self, value):
        self.anytypeobjs_.append(value)

    def insert_anytypeobjs_(self, index, value):
        self._anytypeobjs_[index] = value

    def get_Footer(self):
        return self.Footer

    def set_Footer(self, Footer):
        self.Footer = Footer

    def has_content_(self):
        if (
                self.Header is not None or
                self.anytypeobjs_ or
                self.Footer is not None
        ):
            return True
        else:
            return False

    def export_children(self, outfile, level, pretty_print=True, has_parent=True, **kwargs):
        if self.Header is not None:
            self.Header.export(outfile, level, pretty_print=pretty_print, has_parent=has_parent)
        if self.Footer is not None:
            self.Footer.export(outfile, level, pretty_print=pretty_print, has_parent=has_parent)


# end class MessageType

class GenericDataType(MessageType):
    """GenericDataType defines the contents of a generic data message."""
    __hash__ = DataParser.__hash__
    subclass = None
    superclass = MessageType

    def __init__(self, Header=None, anytypeobjs_=None, Footer=None, DataSet=None, gds_collector_=None, **kwargs_):
        super(GenericDataType, self).__init__(Header, anytypeobjs_, Footer, gds_collector_, **kwargs_)
        self._namespacedef = 'xmlns:message="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message" xmlns:None="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/metadata/structurespecific"  xmlns:data="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic"  xmlns:footer="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message/footer" '
        self._name = 'GenericDataType'

        if DataSet is None:
            self.DataSet = []
        else:
            self.DataSet = DataSet
        self.DataSet_nsprefix_ = None

        if gds_collector_ is not None:
            self.gds_collector_ = gds_collector_
        else:
            self.gds_collector_ = GdsCollector_()

    def factory(*args_, **kwargs_):
        return GenericDataType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_DataSet(self):
        return self.DataSet

    def set_DataSet(self, DataSet):
        self.DataSet = DataSet

    def add_DataSet(self, value):
        self.DataSet.append(value)

    def insert_DataSet_at(self, index, value):
        self.DataSet.insert(index, value)

    def replace_DataSet_at(self, index, value):
        self.DataSet[index] = value

    def has_content_(self):
        if (self.Header is not None or self.DataSet or self.Footer is not None or super(GenericDataType,
                                                                                        self).has_content_()):
            return True
        else:
            return False

    def export_attributes_as_dict(self, valid_fields: list, **kwargs) -> list:
        data = []
        for DataSet_ in self.DataSet:
            parent_dict = {}
            DataSet_.export_attributes_as_dict(parent_dict, )

        return data

    def export_children(self, outfile, level, pretty_print=True, has_parent=True, **kwargs):
        if self.Header is not None:
            self.Header.export(outfile, level, pretty_print=pretty_print, has_parent=has_parent)

        for DataSet_ in self.DataSet:
            DataSet_.export(outfile, level, pretty_print=pretty_print, has_parent=has_parent)

        if self.Footer is not None:
            self.Footer.export(outfile, level, pretty_print=pretty_print, has_parent=has_parent)

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Header':
            obj_ = GenericDataHeaderType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Header = obj_
            obj_.original_tagname_ = 'Header'
        elif nodeName_ == 'DataSet':
            obj_ = GenericDataSet.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DataSet.append(obj_)
            obj_.original_tag_name_ = 'DataSet'
        elif nodeName_ == 'Footer':
            obj_ = FooterType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Footer = obj_
            obj_.original_tag_name_ = 'Footer'


# end class GenericDataType

class StructureSpecificDataHeaderType(BaseHeaderType):
    """StructureSpecificDataHeaderType defines the header structure for a
    structure specific data message."""
    __hash__ = BaseHeaderType.__hash__
    subclass = None
    superclass = BaseHeaderType

    def __init__(self, ID=None, Test=False, Prepared=None, Sender=None, Receiver=None, Name=None, Structure=None,
                 DataProvider=None, DataSetAction=None, DataSetID=None, Extracted=None, ReportingBegin=None,
                 ReportingEnd=None, EmbargoDate=None, Source=None, gds_collector_=None, **kwargs_):
        super(StructureSpecificDataHeaderType, self).__init__(ID, Test, Prepared, Sender, Receiver, Name, Structure,
                                                              DataProvider, DataSetAction, DataSetID, Extracted,
                                                              ReportingBegin, ReportingEnd, EmbargoDate, Source,
                                                              gds_collector_, **kwargs_)
        self._name = 'GenericDataHeaderType'

    def factory(*args_, **kwargs_):
        return StructureSpecificDataHeaderType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def validate_HeaderTimeType(self, value):
        result = True
        return result

    def validate_ObservationalTimePeriodType(self, value):
        result = True
        return result


# end class StructureSpecificDataHeaderType

class StructureSpecificDataType(MessageType):
    """StructureSpecificDataType defines the structure of the structure
    specific data message. Note that the data set payload dim_type is abstract,
    and therefore it will have to be assigned a dim_type in an instance. This
    dim_type must be derived from the base dim_type referenced. This base dim_type
    defines a general structure which can be followed to allow for generic
    processing of the data even if the exact details of the data structure
    specific format are not known."""
    __hash__ = MessageType.__hash__
    subclass = None
    superclass = MessageType

    def __init__(self, Header=None, anytypeobjs_=None, Footer=None, DataSet=None, gds_collector_=None, **kwargs_):
        super(StructureSpecificDataType, self).__init__(Header, anytypeobjs_, Footer, gds_collector_, **kwargs_)

        if DataSet is None:
            self.DataSet = []
        else:
            self.DataSet = DataSet

        self.DataSet_nsprefix_ = None
        self._name = 'StructureSpecificDataType'

        if gds_collector_ is not None:
            self.gds_collector_ = gds_collector_
        else:
            self.gds_collector_ = GdsCollector_()

    def factory(*args_, **kwargs_):
        return StructureSpecificDataType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_DataSet(self):
        return self.DataSet

    def set_DataSet(self, DataSet):
        self.DataSet = DataSet

    def add_DataSet(self, value):
        self.DataSet.append(value)

    def insert_DataSet_at(self, index, value):
        self.DataSet.insert(index, value)

    def replace_DataSet_at(self, index, value):
        self.DataSet[index] = value

    def has_content_(self):
        if (self.Header is not None or self.DataSet or self.Footer is not None or super(MessageType,
                                                                                        self).has_content_()):
            return True
        else:
            return False

    def export_attributes_as_dict(self, valid_fields: list, **kwargs) -> list:
        data = []
        for DataSet_ in self.DataSet:
            parent_dict = {}
            DataSet_.export_attributes_as_dict(parent_dict, )

        return data

    def export_children(self, outfile, level, pretty_print=True, has_parent=True, **kwargs):
        if self.Header is not None:
            self.Header.export(outfile, level, pretty_print=pretty_print, has_parent=has_parent)

        for DataSet_ in self.DataSet:
            DataSet_.export(outfile, level, pretty_print=pretty_print, has_parent=has_parent)

        if self.Footer is not None:
            self.Footer.export(outfile, level, pretty_print=pretty_print, has_parent=has_parent)

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Header':
            obj_ = StructureSpecificDataHeaderType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Header = obj_
            obj_.original_tagname_ = 'Header'
        elif nodeName_ == 'DataSet':
            obj_ = StructureDataSet.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DataSet.append(obj_)
            obj_.original_tag_name_ = 'DataSet'
        elif nodeName_ == 'Footer':
            obj_ = FooterType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Footer = obj_
            obj_.original_tag_name_ = 'Footer'


# end class StructureSpecificDataType


class GenericTimeSeriesDataType(GenericDataType):
    """GenericDataType defines the contents of a generic data message."""
    __hash__ = GenericDataType.__hash__
    subclass = None
    superclass = GenericDataType

    def __init__(self, Header=None, anytypeobjs_=None, Footer=None, DataSet=None, gds_collector_=None, **kwargs_):
        super(GenericTimeSeriesDataType, self).__init__(Header, anytypeobjs_, Footer, gds_collector_, **kwargs_)
        self._namespacedef = 'xmlns:message="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message" xmlns:None="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/metadata/structurespecific"  xmlns:data="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic"  xmlns:footer="http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message/footer" '
        self._name = 'GenericTimeSeriesDataType'

    @staticmethod
    def factory(*args_, **kwargs_):
        return GenericTimeSeriesDataType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_DataSet(self):
        return self.DataSet

    def set_DataSet(self, DataSet):
        self.DataSet = DataSet

    def add_DataSet(self, value):
        self.DataSet.append(value)

    def insert_DataSet_at(self, index, value):
        self.DataSet.insert(index, value)

    def replace_DataSet_at(self, index, value):
        self.DataSet[index] = value

    def has_content_(self):
        if (self.Header is not None or self.DataSet or self.Footer is not None or super(GenericDataType,
                                                                                        self).has_content_()):
            return True
        else:
            return False

    def export_attributes_as_dict(self, valid_fields: list, **kwargs) -> list:
        data = []
        for DataSet_ in self.DataSet:
            parent_dict = {}
            DataSet_.export_attributes_as_dict(parent_dict, )

        return data

    def export_children(self, outfile, level, pretty_print=True, has_parent=True, **kwargs):
        if self.Header is not None:
            self.Header.export(outfile, level, pretty_print=pretty_print, has_parent=has_parent)

        for DataSet_ in self.DataSet:
            DataSet_.export(outfile, level, pretty_print=pretty_print, has_parent=has_parent)

        if self.Footer is not None:
            self.Footer.export(outfile, level, pretty_print=pretty_print, has_parent=has_parent)

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Header':
            obj_ = GenericTimeSeriesDataHeaderType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Header = obj_
            obj_.original_tagname_ = 'Header'
        elif nodeName_ == 'DataSet':
            obj_ = GenericTimeSeriesDataSet.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DataSet.append(obj_)
            obj_.original_tag_name_ = 'DataSet'
        elif nodeName_ == 'Footer':
            obj_ = FooterType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Footer = obj_
            obj_.original_tag_name_ = 'Footer'


class GenericTimeSeriesDataHeaderType(GenericDataHeaderType):
    """GenericTimeSeriesDataHeaderType defines the header structure for a time
    series only generic data message."""
    __hash__ = GenericDataHeaderType.__hash__
    subclass = None
    superclass = GenericDataHeaderType

    def __init__(self, ID=None, Test=False, Prepared=None, Sender=None, Receiver=None, Name=None, Structure=None,
                 DataProvider=None, DataSetAction=None, DataSetID=None, Extracted=None, ReportingBegin=None,
                 ReportingEnd=None, EmbargoDate=None, Source=None, gds_collector_=None, **kwargs_):
        super(GenericTimeSeriesDataHeaderType, self).__init__(ID, Test, Prepared, Sender, Receiver, Name, Structure,
                                                              DataProvider, DataSetAction, DataSetID, Extracted,
                                                              ReportingBegin, ReportingEnd, EmbargoDate, Source,
                                                              gds_collector_, **kwargs_)
        self._name = 'GenericTimeSeriesDataHeaderType'

    def factory(*args_, **kwargs_):
        return GenericTimeSeriesDataHeaderType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def validate_HeaderTimeType(self, value):
        pass

    def validate_ObservationalTimePeriodType(self, value):
        pass


class StructureSpecificTimeSeriesDataType(StructureSpecificDataType):
    """StructureSpecificTimeSeriesDataType defines the structure of the
    structure specific time series data message."""

    __hash__ = StructureSpecificDataType.__hash__
    subclass = None
    superclass = StructureSpecificDataType

    def __init__(self, Header=None, anytypeobjs_=None, Footer=None, DataSet=None, gds_collector_=None, **kwargs_):
        super(StructureSpecificTimeSeriesDataType, self).__init__(Header, anytypeobjs_, Footer, gds_collector_,
                                                                  **kwargs_)

        if DataSet is None:
            self.DataSet = []
        else:
            self.DataSet = DataSet

        self.DataSet_nsprefix_ = None
        self._name = 'StructureSpecificTimeSeriesDataType'

        if gds_collector_ is not None:
            self.gds_collector_ = gds_collector_
        else:
            self.gds_collector_ = GdsCollector_()

    def factory(*args_, **kwargs_):
        return StructureSpecificDataType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_DataSet(self):
        return self.DataSet

    def set_DataSet(self, DataSet):
        self.DataSet = DataSet

    def add_DataSet(self, value):
        self.DataSet.append(value)

    def insert_DataSet_at(self, index, value):
        self.DataSet.insert(index, value)

    def replace_DataSet_at(self, index, value):
        self.DataSet[index] = value

    def has_content_(self):
        if (self.Header is not None or self.DataSet or self.Footer is not None or super(StructureSpecificDataType,
                                                                                        self).has_content_()):
            return True
        else:
            return False

    def export_attributes_as_dict(self, valid_fields: list, **kwargs) -> list:
        data = []
        for DataSet_ in self.DataSet:
            parent_dict = {}
            DataSet_.export_attributes_as_dict(parent_dict, )

        return data

    def export_children(self, outfile, level, pretty_print=True, has_parent=True, **kwargs):
        if self.Header is not None:
            self.Header.export(outfile, level, pretty_print=pretty_print, has_parent=has_parent)

        for DataSet_ in self.DataSet:
            DataSet_.export(outfile, level, pretty_print=pretty_print, has_parent=has_parent)

        if self.Footer is not None:
            self.Footer.export(outfile, level, pretty_print=pretty_print, has_parent=has_parent)

    def build_children(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Header':
            obj_ = StructureSpecificTimeSeriesDataHeaderType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Header = obj_
            obj_.original_tagname_ = 'Header'
        elif nodeName_ == 'DataSet':
            obj_ = StructureTimeSeriesDataSet.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DataSet.append(obj_)
            obj_.original_tag_name_ = 'DataSet'
        elif nodeName_ == 'Footer':
            obj_ = FooterType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Footer = obj_
            obj_.original_tag_name_ = 'Footer'


# end class StructureSpecificDataType


class StructureSpecificTimeSeriesDataHeaderType(StructureSpecificDataHeaderType):
    """StructureSpecificTimeSeriesDataHeaderType defines the header structure
    for a time series only structure specific data message."""
    __hash__ = StructureSpecificDataHeaderType.__hash__
    subclass = None
    superclass = StructureSpecificDataHeaderType

    def __init__(self, ID=None, Test=False, Prepared=None, Sender=None, Receiver=None, Name=None, Structure=None,
                 DataProvider=None, DataSetAction=None, DataSetID=None, Extracted=None, ReportingBegin=None,
                 ReportingEnd=None, EmbargoDate=None, Source=None, gds_collector_=None, **kwargs_):
        super(StructureSpecificTimeSeriesDataHeaderType, self).__init__(ID, Test, Prepared, Sender, Receiver, Name,
                                                                        Structure, DataProvider, DataSetAction,
                                                                        DataSetID,
                                                                        Extracted, ReportingBegin, ReportingEnd,
                                                                        EmbargoDate,
                                                                        Source, gds_collector_, **kwargs_)
        self._name = 'StructureSpecificTimeSeriesDataHeaderType'

    def factory(*args_, **kwargs_):
        return StructureSpecificTimeSeriesDataHeaderType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def validate_HeaderTimeType(self, value):
        result = True
        return result

    def validate_ObservationalTimePeriodType(self, value):
        result = True
        return result
